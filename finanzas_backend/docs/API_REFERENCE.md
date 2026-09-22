# API Reference — Finanzas Backend

Referencia de los 23 endpoints de la API, para armar el frontend sin tener
que levantar Swagger cada vez. Generada a partir del código real
(`manage.py spectacular`) el 2026-09-14.

**Si el backend cambia, esto puede quedar desactualizado.** La fuente de
verdad siempre es Swagger UI / el schema en vivo (ver abajo). Este archivo
es un snapshot legible para tenerlo a mano mientras programás el front.

## Dónde está todo

| Qué | Dónde |
|---|---|
| Swagger UI (probar endpoints desde el navegador) | `http://localhost:8000/api/docs/` |
| ReDoc (lectura, más prolijo para consulta) | `http://localhost:8000/api/redoc/` |
| Spec OpenAPI en vivo (siempre actualizado) | `http://localhost:8000/api/schema/` |
| Spec OpenAPI congelado en el repo | `docs/openapi.yaml` / `docs/openapi.json` |

Para regenerar el spec congelado después de tocar algo:
```bash
docker compose exec backend uv run manage.py spectacular --file docs/openapi.yaml --format openapi
docker compose exec backend uv run manage.py spectacular --file docs/openapi.json --format openapi-json
```

### Usar el spec para el frontend (además de leer esta tabla)

- **Postman / Insomnia**: `Import` → pegar `http://localhost:8000/api/schema/`
  (o importar el archivo `docs/openapi.json`) → te arma la colección completa
  con todos los endpoints, ya tipados.
- **Generar un cliente TypeScript tipado** (recomendado si el front es
  React/Vue/etc.), por ejemplo con `openapi-typescript`:
  ```bash
  npx openapi-typescript docs/openapi.json -o src/api/schema.d.ts
  ```
  o con `orval` / `openapi-typescript-codegen` si querés además los hooks
  de fetch generados. Cualquiera de estas herramientas lee `docs/openapi.json`
  y te da tipos + funciones, así no transcribís esta tabla a mano.


## Autenticación (JWT) — cómo la usa el front

`registro` y `login` crean/validan contra la tabla `usuarios`, que ahora
está vinculada 1 a 1 con un `auth.User` real de Django (`usuarios.auth_user_id`).
Ambos endpoints devuelven, junto con los datos del usuario, un par de
tokens JWT — **ya autenticado, no hace falta ningún paso extra**.

**Flujo para el front:**
1. `POST /api/usuarios/registro/` (una sola vez) o `POST /api/usuarios/login/`
   (las siguientes veces) → responden `{usuario, access, refresh}`.
2. Guardá `access` y `refresh` (ej. en memoria + `localStorage`/`secure storage`).
3. En **todos** los demás endpoints, mandá el header:
   ```
   Authorization: Bearer <access>
   ```
4. `access` expira a la hora (`SIMPLE_JWT.ACCESS_TOKEN_LIFETIME`). Cuando el
   backend responda 401 por token vencido, pedí uno nuevo con:
   ```
   POST /api/usuarios/token/refresh/   Body: {"refresh": "<refresh>"}
   →  {"access": "<access nuevo>"}
   ```
   `refresh` dura 7 días (`SIMPLE_JWT.REFRESH_TOKEN_LIFETIME`); cuando
   también vence, no hay forma de renovar: hay que loguearse de nuevo.

**Nota:** los usuarios creados a mano con `createsuperuser` (ej. `admin`,
para probar por Basic Auth en Swagger/curl) **no** tienen fila en
`usuarios` ni token vía este flujo — son solo para pruebas manuales por
Basic Auth/sesión. El flujo de arriba es el que usa el front de verdad.


## Índice

| Módulo | Endpoints |
|---|---|
| [Usuarios](#usuarios) | registro, login, refresh de token |
| [Catálogos](#catálogos) | categorías de gasto, niveles de prioridad |
| [Ingresos](#ingresos) | listar/crear, total del periodo |
| [Servicios Fijos](#servicios-fijos) | listar/crear, próximos a vencer |
| [Gastos](#gastos) | listar/crear, pago de servicio, balance, variación, modo emergencia |
| [Planes Financieros](#planes-financieros) | listar/crear, activar, comparativa |
| [Alertas](#alertas) | listar, generar, cambiar estado |

**Auth**: salvo que diga "🔓 pública", todo endpoint requiere el header
`Authorization: Bearer <access>` (ver arriba). Todas las fechas son
`YYYY-MM-DD`, todos los montos son strings decimales (`"12345.67"`, no
number, por precisión).


---
## Usuarios

### 🔓 `POST /api/usuarios/registro/`
Alta de usuario. Crea el perfil (`usuarios`) + su `auth.User` vinculado.
Devuelve el usuario **ya autenticado**.

**Body:**
| Campo | Tipo | Requerido |
|---|---|---|
| nombre | string (≤150) | sí |
| email | string (email, ≤150) | sí |
| password | string (≥8, write-only) | sí |

**201** → `{usuario: {id, nombre, email, fecha_registro, activo}, access, refresh}`
**400** → email ya registrado.

### 🔓 `POST /api/usuarios/login/`
**Body:** `{email, password}`
**200** → `{usuario, access, refresh}` (mismo shape que registro).
**401** → credenciales inválidas o usuario inactivo.

### 🔓 `POST /api/usuarios/token/refresh/`
Renueva el `access` cuando expira, sin pedir contraseña de nuevo.

**Body:** `{refresh}`
**200** → `{access}`
**401** → refresh inválido o vencido (hay que loguearse de nuevo).


---
## Catálogos

### `GET /api/catalogos/categorias/`
Categorías globales (`usuario_id: null`) + las personalizadas del usuario logueado.
**200** → `CategoriaGasto[]`: `{id, usuario_id, nombre, icono}`

### `POST /api/catalogos/categorias/`
Crea una categoría propia del usuario.
**Body:** `{nombre, icono?}`
**201** → `CategoriaGasto` · **400** → nombre duplicado para este usuario.

### `GET /api/catalogos/niveles-prioridad/`
Catálogo fijo de solo lectura, ordenado por `nivel_orden`.
**200** → `NivelPrioridad[]`: `{id, nombre, nivel_orden, descripcion, color}`


---
## Ingresos

### `GET /api/ingresos/?mes=&anio=`
Ingresos del usuario en el periodo, ordenados por fecha.
**Query:** `mes` (1-12, requerido), `anio` (requerido)
**200** → `Ingreso[]`: `{id, usuario_id, monto, fecha, periodo_mes, periodo_anio, fuente, descripcion}`

### `POST /api/ingresos/`
**Body:** `{monto, fecha, periodo_mes, periodo_anio, fuente?, descripcion?}`
**201** → `Ingreso` · **400** → monto ≤ 0 o periodo inválido.

### `GET /api/ingresos/total-periodo/?mes=&anio=`
Suma de ingresos del periodo.
**200** → `{periodo_mes, periodo_anio, total_ingresos}`


---
## Servicios Fijos

### `GET /api/servicios-fijos/`
Servicios fijos **activos** del usuario, ordenados por nombre.
**200** → `ServicioFijo[]`: `{id, usuario_id, categoria_id, prioridad_id, nombre, dia_vencimiento, monto_estimado, es_monto_variable, dias_anticipacion_alerta, activo, fecha_inicio, fecha_fin, notas}`

### `POST /api/servicios-fijos/`
**Body:** `{categoria_id, prioridad_id, nombre, dia_vencimiento (1-31), monto_estimado?, es_monto_variable?, dias_anticipacion_alerta?, fecha_inicio?, fecha_fin?, notas?}`
**201** → `ServicioFijo` · **400** → dia_vencimiento/monto_estimado/rango de fechas inválido.

### `GET /api/servicios-fijos/proximos-a-vencer/?fecha=`
Servicios activos cuyo vencimiento cae dentro de su ventana de anticipación.
**Query:** `fecha` (opcional, YYYY-MM-DD, default hoy)
**200** → `ServicioFijo[]`


---
## Gastos

### `GET /api/gastos/?mes=&anio=`
Gastos del usuario en el periodo (puntuales + pagos de servicio fijo).
**200** → `Gasto[]`: `{id, usuario_id, categoria_id, servicio_fijo_id, prioridad_id, monto, fecha_gasto, periodo_mes, periodo_anio, estado, descripcion}`
(`servicio_fijo_id` es `null` en un gasto puntual; `estado` ∈ `Pagado|Pendiente|Vencido`)

### `POST /api/gastos/`
Gasto puntual (NO ligado a un servicio fijo — mercado, salidas, etc.).
**Body:** `{categoria_id, prioridad_id, monto, fecha_gasto, periodo_mes, periodo_anio, estado?, descripcion?}`
**201** → `Gasto` · **400** → monto o estado inválido.

### `POST /api/gastos/pagos-servicio/`
Pago de un servicio fijo. `categoria_id`/`prioridad_id` NO van en el body: se
deducen del servicio.
**Body:** `{servicio_fijo_id, monto, fecha_gasto, periodo_mes, periodo_anio, descripcion?}`
**201** → `Gasto` · **400** → monto inválido · **404** → servicio_fijo_id inexistente · **409** → ya hay un pago de ese servicio en ese periodo.

### `GET /api/gastos/balance-mensual/?mes=&anio=`
**200** → `{usuario_id, periodo_mes, periodo_anio, total_ingresos, total_gastos, balance}`

### `GET /api/gastos/variacion-servicios/?servicio_fijo_id=`
% de variación de un servicio fijo mes a mes.
**Query:** `servicio_fijo_id` (requerido)
**200** → `VariacionServicio[]`: `{servicio_fijo_id, servicio, periodo_mes, periodo_anio, monto_actual, monto_anterior, porcentaje_variacion}`
(`monto_anterior`/`porcentaje_variacion` son `null` en el primer periodo)

### `GET /api/gastos/modo-emergencia/?mes=&anio=`
Simulación: gasto por prioridad + ahorro acumulado si se suspende desde lo más prescindible.
**200** → `AhorroEmergencia[]`: `{prioridad, nivel_orden, total_periodo, ahorro_acumulado_si_suspende}`


---
## Planes Financieros

### `GET /api/planes-financieros/`
Todos los planes del usuario (activos e inactivos), más nuevo primero.
**200** → `PlanFinanciero[]`: `{id, usuario_id, nombre, porcentaje_gasto_fijo, porcentaje_ahorro, porcentaje_gasto_libre, fecha_inicio, fecha_fin, activo}`

### `POST /api/planes-financieros/`
Crea un plan. **Nace inactivo** — hay que activarlo aparte. Los 3 porcentajes deben sumar 100.
**Body:** `{porcentaje_gasto_fijo, porcentaje_ahorro, porcentaje_gasto_libre, nombre?, fecha_inicio?, fecha_fin?}`
**201** → `PlanFinanciero` · **400** → porcentajes no suman 100.

### `POST /api/planes-financieros/{plan_id}/activar/`
Activa ese plan y desactiva el que estaba activo (si había). Sin body.
**200** → `PlanFinanciero` · **404** → no existe el plan.

### `GET /api/planes-financieros/comparativa/?mes=&anio=`
Metas del plan activo vs. ejecución real del periodo.
**200** → `{usuario_id, periodo_mes, periodo_anio, total_ingresos, meta_gasto_fijo, meta_ahorro, meta_gasto_libre, gasto_real, balance_real}`
**404** → el usuario no tiene plan activo.


---
## Alertas

### `GET /api/alertas/?estado=`
**Query:** `estado` (opcional: `Pendiente` (default) `|Enviada|Leida|Resuelta`)
**200** → `AlertaPago[]`: `{id, usuario_id, servicio_fijo_id, gasto_id, periodo_mes, periodo_anio, fecha_alerta, estado, mensaje}`
(`gasto_id` es `null` hasta que se paga el servicio)

### `POST /api/alertas/generar/?fecha=`
Genera alertas `Pendiente` para servicios próximos a vencer. Idempotente
(no duplica). Pensado para correrse como job/cron diario.
**Query o body:** `fecha` (opcional, default hoy)
**201** → `AlertaPago[]` (solo las nuevas creadas en esta corrida)

### `PATCH /api/alertas/{alerta_id}/`
Transición manual de estado: `Pendiente→Enviada` o `Enviada→Leida`.
`Resuelta` **no se setea acá**: pasa sola cuando se paga el servicio fijo
correspondiente (evento `GastoRegistrado` → se resuelve la alerta del
mismo servicio_fijo_id + periodo).
**Body:** `{estado: "Enviada" | "Leida"}`
**200** → `AlertaPago` · **404** → no existe la alerta · **409** → transición no permitida.


---
## Códigos de error comunes

| Código | Cuándo |
|---|---|
| 400 | Body inválido (falta un campo requerido, tipo incorrecto) o regla de negocio violada (ver cada endpoint) |
| 401 | Credenciales inválidas (`/usuarios/login/`) |
| 403 | No autenticado / sin permiso (endpoints protegidos, sin sesión ni Basic Auth) |
| 404 | El recurso referenciado no existe |
| 409 | Conflicto: duplicado (pago de servicio en el mismo periodo) o transición de estado no permitida |
