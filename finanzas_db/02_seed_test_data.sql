-- =========================================================================
-- DATOS DE PRUEBA / SEED HISTORICO
-- Para validar variacion de precios, balance mensual y plan financiero
-- Ejecutar DESPUES de schema_finanzas.sql (01_schema.sql)
-- =========================================================================

-- -------------------------------------------------------------------------
-- 1. Usuario de prueba
-- -------------------------------------------------------------------------
INSERT INTO usuarios (nombre, email, password_hash) VALUES
('Charles Prueba', 'charles.prueba@example.com', 'hash_ficticio_para_pruebas');

-- -------------------------------------------------------------------------
-- 2. Servicios fijos del usuario de prueba
-- -------------------------------------------------------------------------
INSERT INTO servicios_fijos (usuario_id, categoria_id, prioridad_id, nombre, dia_vencimiento, monto_estimado, es_monto_variable, dias_anticipacion_alerta)
SELECT u.id,
       (SELECT id FROM categorias_gasto WHERE nombre = 'Servicios Basicos' AND usuario_id IS NULL),
       (SELECT id FROM niveles_prioridad WHERE nombre = 'Importante'),
       'Internet Movistar', 10, 25000, FALSE, 3
FROM usuarios u WHERE u.email = 'charles.prueba@example.com';

INSERT INTO servicios_fijos (usuario_id, categoria_id, prioridad_id, nombre, dia_vencimiento, monto_estimado, es_monto_variable, dias_anticipacion_alerta)
SELECT u.id,
       (SELECT id FROM categorias_gasto WHERE nombre = 'Servicios Basicos' AND usuario_id IS NULL),
       (SELECT id FROM niveles_prioridad WHERE nombre = 'Esencial'),
       'Agua', 15, 5000, TRUE, 3
FROM usuarios u WHERE u.email = 'charles.prueba@example.com';

INSERT INTO servicios_fijos (usuario_id, categoria_id, prioridad_id, nombre, dia_vencimiento, monto_estimado, es_monto_variable, dias_anticipacion_alerta)
SELECT u.id,
       (SELECT id FROM categorias_gasto WHERE nombre = 'Servicios Basicos' AND usuario_id IS NULL),
       (SELECT id FROM niveles_prioridad WHERE nombre = 'Esencial'),
       'Luz', 20, 30000, TRUE, 5
FROM usuarios u WHERE u.email = 'charles.prueba@example.com';

INSERT INTO servicios_fijos (usuario_id, categoria_id, prioridad_id, nombre, dia_vencimiento, monto_estimado, es_monto_variable, dias_anticipacion_alerta)
SELECT u.id,
       (SELECT id FROM categorias_gasto WHERE nombre = 'Gimnasio / Deporte' AND usuario_id IS NULL),
       (SELECT id FROM niveles_prioridad WHERE nombre = 'Prescindible'),
       'Gimnasio Smart Fit', 5, 15000, FALSE, 2
FROM usuarios u WHERE u.email = 'charles.prueba@example.com';

-- -------------------------------------------------------------------------
-- 3. Ingresos (6 meses, con montos variables y un ingreso extra en marzo)
-- -------------------------------------------------------------------------
INSERT INTO ingresos (usuario_id, monto, fecha, periodo_mes, periodo_anio, fuente, descripcion)
SELECT u.id, v.monto, v.fecha, v.mes, v.anio, v.fuente, v.descripcion
FROM usuarios u,
(VALUES
    (800000, DATE '2026-01-30', 1, 2026, 'Salario', 'Sueldo enero'),
    (750000, DATE '2026-02-27', 2, 2026, 'Salario', 'Sueldo febrero'),
    (900000, DATE '2026-03-30', 3, 2026, 'Salario', 'Sueldo marzo'),
    (120000, DATE '2026-03-15', 3, 2026, 'Freelance', 'Proyecto extra marzo'),
    (820000, DATE '2026-04-30', 4, 2026, 'Salario', 'Sueldo abril'),
    (780000, DATE '2026-05-29', 5, 2026, 'Salario', 'Sueldo mayo'),
    (950000, DATE '2026-06-30', 6, 2026, 'Salario', 'Sueldo junio')
) AS v(monto, fecha, mes, anio, fuente, descripcion)
WHERE u.email = 'charles.prueba@example.com';

-- -------------------------------------------------------------------------
-- 4. Pagos de servicios fijos (con variacion real de precio en Agua y Luz)
-- -------------------------------------------------------------------------
INSERT INTO gastos (usuario_id, categoria_id, servicio_fijo_id, prioridad_id, monto, fecha_gasto, periodo_mes, periodo_anio, estado, descripcion)
SELECT u.id, sf.categoria_id, sf.id, sf.prioridad_id, v.monto, v.fecha, v.mes, v.anio, 'Pagado', v.servicio || ' - pago mensual'
FROM usuarios u
JOIN servicios_fijos sf ON sf.usuario_id = u.id
JOIN (VALUES
    ('Internet Movistar', 25000, DATE '2026-01-10', 1, 2026),
    ('Internet Movistar', 25000, DATE '2026-02-10', 2, 2026),
    ('Internet Movistar', 25000, DATE '2026-03-10', 3, 2026),
    ('Internet Movistar', 27000, DATE '2026-04-10', 4, 2026),
    ('Internet Movistar', 27000, DATE '2026-05-10', 5, 2026),
    ('Internet Movistar', 27000, DATE '2026-06-10', 6, 2026),
    ('Agua', 5000, DATE '2026-01-15', 1, 2026),
    ('Agua', 5200, DATE '2026-02-15', 2, 2026),
    ('Agua', 5500, DATE '2026-03-15', 3, 2026),
    ('Agua', 5300, DATE '2026-04-15', 4, 2026),
    ('Agua', 6000, DATE '2026-05-15', 5, 2026),
    ('Agua', 6100, DATE '2026-06-15', 6, 2026),
    ('Luz', 28000, DATE '2026-01-20', 1, 2026),
    ('Luz', 30000, DATE '2026-02-20', 2, 2026),
    ('Luz', 34000, DATE '2026-03-20', 3, 2026),
    ('Luz', 31000, DATE '2026-04-20', 4, 2026),
    ('Luz', 29000, DATE '2026-05-20', 5, 2026),
    ('Luz', 33000, DATE '2026-06-20', 6, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-01-05', 1, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-02-05', 2, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-03-05', 3, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-04-05', 4, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-05-05', 5, 2026),
    ('Gimnasio Smart Fit', 15000, DATE '2026-06-05', 6, 2026)
) AS v(servicio, monto, fecha, mes, anio) ON v.servicio = sf.nombre
WHERE u.email = 'charles.prueba@example.com';

-- -------------------------------------------------------------------------
-- 5. Gastos puntuales, no ligados a un servicio fijo (mercado, ocio)
-- -------------------------------------------------------------------------
INSERT INTO gastos (usuario_id, categoria_id, servicio_fijo_id, prioridad_id, monto, fecha_gasto, periodo_mes, periodo_anio, estado, descripcion)
SELECT
    u.id,
    (SELECT id FROM categorias_gasto WHERE nombre = v.categoria AND usuario_id IS NULL),
    NULL,
    (SELECT id FROM niveles_prioridad WHERE nombre = v.prioridad),
    v.monto, v.fecha, v.mes, v.anio, 'Pagado', v.descripcion
FROM usuarios u,
(VALUES
    ('Alimentacion', 'Esencial', 180000, DATE '2026-01-08', 1, 2026, 'Mercado del mes'),
    ('Alimentacion', 'Esencial', 190000, DATE '2026-02-08', 2, 2026, 'Mercado del mes'),
    ('Alimentacion', 'Esencial', 175000, DATE '2026-03-08', 3, 2026, 'Mercado del mes'),
    ('Alimentacion', 'Esencial', 200000, DATE '2026-04-08', 4, 2026, 'Mercado del mes'),
    ('Alimentacion', 'Esencial', 195000, DATE '2026-05-08', 5, 2026, 'Mercado del mes'),
    ('Alimentacion', 'Esencial', 210000, DATE '2026-06-08', 6, 2026, 'Mercado del mes'),
    ('Entretenimiento', 'Prescindible', 40000, DATE '2026-01-20', 1, 2026, 'Cine y salidas'),
    ('Entretenimiento', 'Prescindible', 35000, DATE '2026-02-18', 2, 2026, 'Cine y salidas'),
    ('Entretenimiento', 'Prescindible', 50000, DATE '2026-03-22', 3, 2026, 'Cine y salidas'),
    ('Entretenimiento', 'Prescindible', 30000, DATE '2026-04-19', 4, 2026, 'Cine y salidas'),
    ('Entretenimiento', 'Prescindible', 45000, DATE '2026-05-21', 5, 2026, 'Cine y salidas'),
    ('Entretenimiento', 'Prescindible', 60000, DATE '2026-06-20', 6, 2026, 'Cine y salidas')
) AS v(categoria, prioridad, monto, fecha, mes, anio, descripcion)
WHERE u.email = 'charles.prueba@example.com';

-- -------------------------------------------------------------------------
-- 6. Plan financiero activo
-- -------------------------------------------------------------------------
INSERT INTO plan_financiero (usuario_id, nombre, porcentaje_gasto_fijo, porcentaje_ahorro, porcentaje_gasto_libre, fecha_inicio)
SELECT u.id, 'Plan 2026', 50, 20, 30, DATE '2026-01-01'
FROM usuarios u WHERE u.email = 'charles.prueba@example.com';
