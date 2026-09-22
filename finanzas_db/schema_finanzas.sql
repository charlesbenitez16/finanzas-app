-- =========================================================================
-- MODELO DE BASE DE DATOS: SISTEMA DE FINANZAS PERSONALES
-- Motor objetivo: PostgreSQL 14+
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. USUARIOS
-- -------------------------------------------------------------------------
CREATE TABLE usuarios (
    id              BIGSERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    fecha_registro  TIMESTAMP NOT NULL DEFAULT NOW(),
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    -- Vinculo con auth_user (la tabla que Django usa de verdad para
    -- autenticar: sesion, Basic Auth, JWT). SIN "REFERENCES auth_user(id)"
    -- a proposito: auth_user todavia no existe cuando este script corre
    -- (lo crea "manage.py migrate", DESPUES de que Postgres ya cargo este
    -- schema al arrancar el contenedor). La integridad referencial la
    -- garantiza la app (modules/usuarios/infrastructure/repositories.py
    -- crea ambas filas en una misma transaccion), no la base.
    auth_user_id    BIGINT UNIQUE
);

-- IMPORTANTE sobre los `usuario_id BIGINT ... REFERENCES usuarios(id)` de
-- las tablas de abajo (categorias_gasto, ingresos, servicios_fijos,
-- gastos, plan_financiero, alertas_pago): quedan escritos asi por ser
-- fieles al modelo original, pero en los hechos el codigo Django SIEMPRE
-- usa el id de `auth_user` (request.user.id) como usuario_id, nunca el
-- id de esta tabla `usuarios`. Por eso, apenas migran las apps de Django,
-- una migracion en infrastructure/migrations/0002_fix_usuario_id_fk.py de
-- cada modulo DROPea esa constraint y la vuelve a crear apuntando a
-- auth_user(id) (no se puede escribir asi directamente aca porque
-- auth_user todavia no existe cuando este script corre). Si consultas
-- estas tablas con SQL crudo despues de "manage.py migrate", el
-- usuario_id real que vas a encontrar ahi es un id de auth_user, no de
-- `usuarios`.

-- -------------------------------------------------------------------------
-- 2. NIVELES DE PRIORIDAD (catálogo para el modo "emergencia")
-- -------------------------------------------------------------------------
CREATE TABLE niveles_prioridad (
    id          SMALLSERIAL PRIMARY KEY,
    nombre      VARCHAR(50) NOT NULL UNIQUE,     -- Esencial, Importante, Prescindible
    nivel_orden SMALLINT NOT NULL UNIQUE,        -- 1 = mas critico, 3 = mas prescindible
    descripcion TEXT,
    color       VARCHAR(20)
);

-- -------------------------------------------------------------------------
-- 3. CATEGORIAS DE GASTO
--    usuario_id NULL -> categoria global del sistema (visible para todos)
--    usuario_id X    -> categoria personalizada creada por ese usuario
-- -------------------------------------------------------------------------
CREATE TABLE categorias_gasto (
    id          SERIAL PRIMARY KEY,
    usuario_id  BIGINT REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre      VARCHAR(100) NOT NULL,
    icono       VARCHAR(50),
    UNIQUE (usuario_id, nombre)
);

-- -------------------------------------------------------------------------
-- 4. INGRESOS (variables mes a mes)
-- -------------------------------------------------------------------------
CREATE TABLE ingresos (
    id              BIGSERIAL PRIMARY KEY,
    usuario_id      BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    monto           NUMERIC(12,2) NOT NULL CHECK (monto > 0),
    fecha           DATE NOT NULL,
    periodo_mes     SMALLINT NOT NULL CHECK (periodo_mes BETWEEN 1 AND 12),
    periodo_anio    SMALLINT NOT NULL,
    fuente          VARCHAR(100),               -- Salario, Freelance, Bono, Renta, etc.
    descripcion     TEXT,
    fecha_registro  TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_ingresos_usuario_periodo ON ingresos(usuario_id, periodo_anio, periodo_mes);

-- -------------------------------------------------------------------------
-- 5. SERVICIOS FIJOS / GASTOS RECURRENTES (la "plantilla" del gasto)
--    Ej: Internet, Agua, Luz, Gimnasio, Streaming...
-- -------------------------------------------------------------------------
CREATE TABLE servicios_fijos (
    id                          BIGSERIAL PRIMARY KEY,
    usuario_id                  BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    categoria_id                INT NOT NULL REFERENCES categorias_gasto(id),
    prioridad_id                SMALLINT NOT NULL REFERENCES niveles_prioridad(id),
    nombre                      VARCHAR(150) NOT NULL,       -- "Internet Movistar", "Agua"
    dia_vencimiento              SMALLINT NOT NULL CHECK (dia_vencimiento BETWEEN 1 AND 31),
    monto_estimado              NUMERIC(12,2) CHECK (monto_estimado >= 0),
    es_monto_variable           BOOLEAN NOT NULL DEFAULT FALSE,  -- true: agua/luz (cambia cada mes)
    dias_anticipacion_alerta    SMALLINT NOT NULL DEFAULT 3,
    activo                      BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_inicio                DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin                   DATE,
    notas                       TEXT
);
CREATE INDEX idx_servicios_usuario ON servicios_fijos(usuario_id);

-- -------------------------------------------------------------------------
-- 6. GASTOS (toda transaccion real: pagos de servicios fijos + gastos
--    puntuales como mercado, salidas, compras varias)
-- -------------------------------------------------------------------------
CREATE TABLE gastos (
    id                  BIGSERIAL PRIMARY KEY,
    usuario_id          BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    categoria_id        INT NOT NULL REFERENCES categorias_gasto(id),
    servicio_fijo_id    BIGINT REFERENCES servicios_fijos(id) ON DELETE SET NULL, -- NULL = gasto no recurrente
    prioridad_id        SMALLINT NOT NULL REFERENCES niveles_prioridad(id),
    monto               NUMERIC(12,2) NOT NULL CHECK (monto > 0),
    fecha_gasto         DATE NOT NULL,
    periodo_mes         SMALLINT NOT NULL CHECK (periodo_mes BETWEEN 1 AND 12),
    periodo_anio        SMALLINT NOT NULL,
    estado              VARCHAR(20) NOT NULL DEFAULT 'Pagado'
                         CHECK (estado IN ('Pagado','Pendiente','Vencido')),
    descripcion         TEXT,
    fecha_registro      TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_gastos_usuario_periodo ON gastos(usuario_id, periodo_anio, periodo_mes);
CREATE INDEX idx_gastos_servicio ON gastos(servicio_fijo_id);

-- Evita registrar dos veces el mismo servicio fijo en el mismo periodo
CREATE UNIQUE INDEX uq_gasto_servicio_periodo
    ON gastos(servicio_fijo_id, periodo_anio, periodo_mes)
    WHERE servicio_fijo_id IS NOT NULL;

-- -------------------------------------------------------------------------
-- 7. PLAN FINANCIERO (ej. estilo 50/30/20 pero personalizable)
-- -------------------------------------------------------------------------
CREATE TABLE plan_financiero (
    id                      BIGSERIAL PRIMARY KEY,
    usuario_id              BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nombre                  VARCHAR(100) NOT NULL DEFAULT 'Mi plan',
    porcentaje_gasto_fijo   NUMERIC(5,2) NOT NULL CHECK (porcentaje_gasto_fijo >= 0),
    porcentaje_ahorro       NUMERIC(5,2) NOT NULL CHECK (porcentaje_ahorro >= 0),
    porcentaje_gasto_libre  NUMERIC(5,2) NOT NULL CHECK (porcentaje_gasto_libre >= 0),
    fecha_inicio            DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin               DATE,
    activo                  BOOLEAN NOT NULL DEFAULT TRUE,
    CHECK (porcentaje_gasto_fijo + porcentaje_ahorro + porcentaje_gasto_libre = 100)
);
-- Solo un plan activo por usuario a la vez
CREATE UNIQUE INDEX uq_plan_activo_usuario ON plan_financiero(usuario_id) WHERE activo = TRUE;

-- -------------------------------------------------------------------------
-- 8. ALERTAS DE VENCIMIENTO DE PAGO
-- -------------------------------------------------------------------------
CREATE TABLE alertas_pago (
    id                  BIGSERIAL PRIMARY KEY,
    usuario_id          BIGINT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    servicio_fijo_id    BIGINT NOT NULL REFERENCES servicios_fijos(id) ON DELETE CASCADE,
    gasto_id            BIGINT REFERENCES gastos(id) ON DELETE SET NULL, -- se llena al registrar el pago
    periodo_mes         SMALLINT NOT NULL CHECK (periodo_mes BETWEEN 1 AND 12),
    periodo_anio        SMALLINT NOT NULL,
    fecha_alerta        DATE NOT NULL,
    estado              VARCHAR(20) NOT NULL DEFAULT 'Pendiente'
                         CHECK (estado IN ('Pendiente','Enviada','Leida','Resuelta')),
    mensaje             TEXT,
    fecha_creacion      TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_alertas_usuario_estado ON alertas_pago(usuario_id, estado);
CREATE UNIQUE INDEX uq_alerta_servicio_periodo
    ON alertas_pago(servicio_fijo_id, periodo_anio, periodo_mes);

-- =========================================================================
-- DATOS SEMILLA
-- =========================================================================
INSERT INTO niveles_prioridad (nombre, nivel_orden, descripcion, color) VALUES
('Esencial',     1, 'Indispensable para vivir: vivienda, alimentacion basica, salud', '#e74c3c'),
('Importante',   2, 'Necesario pero con margen de reduccion: internet, transporte, educacion', '#f39c12'),
('Prescindible', 3, 'Se puede suspender en una emergencia: gimnasio, streaming, ocio', '#2ecc71');

INSERT INTO categorias_gasto (usuario_id, nombre, icono) VALUES
(NULL, 'Vivienda', 'home'),
(NULL, 'Servicios Basicos', 'bolt'),
(NULL, 'Alimentacion', 'shopping-cart'),
(NULL, 'Transporte', 'car'),
(NULL, 'Salud', 'heart'),
(NULL, 'Educacion', 'book'),
(NULL, 'Entretenimiento', 'film'),
(NULL, 'Gimnasio / Deporte', 'dumbbell'),
(NULL, 'Otros', 'more-horizontal');

-- =========================================================================
-- VISTAS PARA LAS FUNCIONALIDADES CLAVE
-- =========================================================================

-- -------------------------------------------------------------------------
-- A) Balance mensual (ingresos - gastos) por usuario y periodo
-- -------------------------------------------------------------------------
CREATE VIEW vista_balance_mensual AS
WITH periodos AS (
    SELECT usuario_id, periodo_anio AS anio, periodo_mes AS mes FROM ingresos
    UNION
    SELECT usuario_id, periodo_anio, periodo_mes FROM gastos
),
ing AS (
    SELECT usuario_id, periodo_anio AS anio, periodo_mes AS mes, SUM(monto) AS total_ingresos
    FROM ingresos GROUP BY usuario_id, periodo_anio, periodo_mes
),
gas AS (
    SELECT usuario_id, periodo_anio AS anio, periodo_mes AS mes, SUM(monto) AS total_gastos
    FROM gastos GROUP BY usuario_id, periodo_anio, periodo_mes
)
SELECT DISTINCT
    p.usuario_id, p.anio, p.mes,
    COALESCE(i.total_ingresos, 0) AS total_ingresos,
    COALESCE(g.total_gastos, 0)   AS total_gastos,
    COALESCE(i.total_ingresos, 0) - COALESCE(g.total_gastos, 0) AS balance
FROM periodos p
LEFT JOIN ing i ON i.usuario_id = p.usuario_id AND i.anio = p.anio AND i.mes = p.mes
LEFT JOIN gas g ON g.usuario_id = p.usuario_id AND g.anio = p.anio AND g.mes = p.mes;

-- -------------------------------------------------------------------------
-- B) % de variacion de cada servicio fijo respecto al mes anterior
--    (ej. Agua: 5000 -> 5500 = +10%)
-- -------------------------------------------------------------------------
CREATE VIEW vista_variacion_servicios AS
SELECT
    g.usuario_id,
    g.servicio_fijo_id,
    sf.nombre AS servicio,
    g.periodo_anio,
    g.periodo_mes,
    g.monto AS monto_actual,
    LAG(g.monto) OVER w AS monto_anterior,
    ROUND(
        (g.monto - LAG(g.monto) OVER w) / NULLIF(LAG(g.monto) OVER w, 0) * 100
    , 2) AS porcentaje_variacion
FROM gastos g
JOIN servicios_fijos sf ON sf.id = g.servicio_fijo_id
WHERE g.servicio_fijo_id IS NOT NULL
WINDOW w AS (PARTITION BY g.servicio_fijo_id ORDER BY g.periodo_anio, g.periodo_mes);

-- -------------------------------------------------------------------------
-- C) Ahorro potencial por nivel de prioridad (simulacion "modo emergencia")
-- -------------------------------------------------------------------------
CREATE VIEW vista_ahorro_potencial_por_prioridad AS
SELECT
    g.usuario_id,
    g.periodo_anio,
    g.periodo_mes,
    np.nombre AS prioridad,
    np.nivel_orden,
    SUM(g.monto) AS total_por_prioridad
FROM gastos g
JOIN niveles_prioridad np ON np.id = g.prioridad_id
GROUP BY g.usuario_id, g.periodo_anio, g.periodo_mes, np.nombre, np.nivel_orden
ORDER BY g.usuario_id, g.periodo_anio, g.periodo_mes, np.nivel_orden;

-- -------------------------------------------------------------------------
-- D) Comparacion plan financiero vs. ejecucion real de un mes
-- -------------------------------------------------------------------------
CREATE VIEW vista_plan_vs_real AS
SELECT
    pf.usuario_id,
    b.anio, b.mes,
    b.total_ingresos,
    ROUND(b.total_ingresos * pf.porcentaje_gasto_fijo / 100, 2)  AS meta_gasto_fijo,
    ROUND(b.total_ingresos * pf.porcentaje_ahorro / 100, 2)      AS meta_ahorro,
    ROUND(b.total_ingresos * pf.porcentaje_gasto_libre / 100, 2) AS meta_gasto_libre,
    b.total_gastos AS gasto_real,
    b.balance AS balance_real
FROM plan_financiero pf
JOIN vista_balance_mensual b ON b.usuario_id = pf.usuario_id
WHERE pf.activo = TRUE;

-- -------------------------------------------------------------------------
-- E) Servicios proximos a vencer (para el generador de alertas)
--    Ejemplo: correr esto diario desde un job / cron
-- -------------------------------------------------------------------------
-- SELECT sf.*
-- FROM servicios_fijos sf
-- WHERE sf.activo = TRUE
--   AND (sf.dia_vencimiento - EXTRACT(DAY FROM CURRENT_DATE)::int) = sf.dias_anticipacion_alerta
--   AND NOT EXISTS (
--       SELECT 1 FROM gastos g
--       WHERE g.servicio_fijo_id = sf.id
--         AND g.periodo_mes = EXTRACT(MONTH FROM CURRENT_DATE)
--         AND g.periodo_anio = EXTRACT(YEAR FROM CURRENT_DATE)
--   );
