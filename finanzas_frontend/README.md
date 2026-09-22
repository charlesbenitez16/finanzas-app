# Finanzas — Frontend

React 19 + Vite + TypeScript + Tailwind CSS v4 + shadcn/ui, conectado al
backend Django/DRF de `../finanzas_backend`.

## Stack

- **Vite + React + TypeScript**
- **Tailwind CSS v4** (`@tailwindcss/vite`) + **shadcn/ui** (preset Nova)
- **TanStack Query** para fetching/cache de datos del servidor
- **openapi-fetch** + **openapi-typescript**: cliente HTTP tipado a partir
  del schema OpenAPI del backend (`../finanzas_backend/docs/openapi.json`)
  — no hay tipos escritos a mano para las respuestas de la API
- **React Router** para las rutas
- **react-hook-form + zod** para los formularios
- **zustand** para el estado de sesión (usuario/tokens)

## Requisitos

- Node 20+. El repo trae `.nvmrc` (Node 24); si `nvm` está instalado alcanza
  con `nvm use` parado en esta carpeta.
- pnpm. Si no está activado: `corepack enable && corepack prepare pnpm@latest --activate`.
- Docker + Docker Compose, para levantar el backend (Postgres + Django).

## Puesta en marcha

### 1. Backend

```bash
cd ../finanzas_backend
docker compose up -d
```

Esto levanta Postgres (`:5434`) y Django (`:8000`) — la primera vez aplica
las migraciones de Django y carga los datos sembrados (categorías globales,
niveles de prioridad). Comprobar que responde:

```bash
curl -i http://localhost:8000/api/catalogos/niveles-prioridad/
# 401 es la respuesta correcta acá: existe el endpoint, pero pide login
```

### 2. Frontend

```bash
cd finanzas_frontend
nvm use          # resuelve a Node 24 via .nvmrc
pnpm install
pnpm dev
```

Abrir **http://localhost:5173**. En desarrollo, Vite proxea todo lo que
empieza con `/api` hacia `http://localhost:8000` (ver `vite.config.ts`),
así que **no hace falta configurar CORS en el backend**: desde el punto de
vista del navegador, front y back son el mismo origen.

## Cómo probar todo

Con el backend y el frontend corriendo, este recorrido pasa por los 23
endpoints de la API y deja el estado esperado en cada pantalla. Es el mismo
camino que se usó para verificar la app durante el desarrollo.

1. **Registro** — entrar a `/registro`, crear un usuario (contraseña de al
   menos 8 caracteres y que no sea obvia, ej. no "12345678"). Debe entrar
   directo al Dashboard, con los tres widgets de balance en `0,00`.
2. **Catálogos** — ir a *Catálogos*: deberían aparecer categorías globales
   ya sembradas en la base (Alimentación, Transporte, Vivienda, etc.) y los
   3 niveles de prioridad (Esencial/Importante/Prescindible). Crear una
   categoría propia desde el formulario de arriba — aparece en la tabla
   con badge "Propia".
3. **Servicios fijos** — crear uno (elegir categoría y prioridad de las
   creadas en el paso anterior, un día de vencimiento 1–31, monto
   estimado). Aparece en la tabla; si el día de vencimiento cae dentro de
   la ventana de anticipación, más adelante va a aparecer marcado como
   "Próximo a vencer".
4. **Ingresos** — crear un ingreso. Aparece en la tabla y el card "Total
   del periodo" pasa de `0,00` al monto cargado.
5. **Gastos** — crear un gasto puntual (aparece con tipo "Puntual"). Pagar
   el servicio fijo del paso 3 con "Pagar servicio fijo" (aparece con tipo
   "Servicio fijo"); repetir el mismo pago en el mismo mes/año debe
   devolver error (409 — ya hay un pago de ese servicio en ese periodo).
6. **Dashboard** — volver a *Dashboard*: el balance del periodo ya
   refleja los ingresos y gastos cargados, y si el servicio fijo generó
   una alerta, aparece listada ahí.
7. **Planes financieros** — crear un plan donde los 3 porcentajes sumen
   100 (si no suman 100, el form lo rechaza), activarlo, y ver que la
   sección "Comparativa del periodo" pasa de "No tenés un plan activo" a
   mostrar las metas.
8. **Alertas** — click en "Generar alertas de hoy" (genera algo solo si
   hay un servicio fijo cuyo vencimiento cae dentro de su ventana de
   anticipación); cambiar el estado de una alerta de Pendiente a Enviada.
9. **Sesión** — recargar la página (F5) estando logueado: tiene que seguir
   adentro sin pedir contraseña de nuevo (confirma la renovación
   silenciosa del access token). "Cerrar sesión" desde el sidebar
   redirige a `/login`.

Para cualquier paso, si algo no se ve bien conviene abrir la consola del
navegador (Network + Console) antes que nada: la causa más común es el
backend caído o el token vencido sin refresh (ver sección Autenticación).

## Autenticación

Sigue el flujo documentado en `../finanzas_backend/docs/API_REFERENCE.md`:

- `POST /api/usuarios/login/` y `/registro/` devuelven `{usuario, access, refresh}`.
- `access` se guarda solo en memoria (store de zustand, `src/stores/auth-store.ts`)
  y se manda como `Authorization: Bearer <access>` en cada request
  (`src/api/client.ts`).
- `refresh` se persiste en `localStorage` para sobrevivir a un refresh de
  página. El cliente HTTP decodifica el `exp` del JWT y renueva el `access`
  de forma proactiva antes de que expire (o al arrancar la app, si hay
  `refresh` pero no `access` en memoria todavía).
- Si el refresh también venció, el backend responde 401, se limpia la
  sesión y `ProtectedRoute` redirige a `/login`.

## Estructura

```
src/
  api/
    schema.d.ts   -> tipos generados desde el OpenAPI del backend (no editar a mano)
    client.ts     -> cliente openapi-fetch + interceptor de auth/refresh
  stores/
    auth-store.ts -> sesión (usuario, tokens)
  features/
    auth/         -> login, registro
    dashboard/    -> balance mensual + alertas pendientes
    ingresos/     -> ejemplo de referencia: hooks (api.ts) + página (list + create)
    gastos/       -> gastos puntuales + pago de servicios fijos + balance
    servicios-fijos/
    planes-financieros/
    alertas/
    catalogos/    -> categorías de gasto + niveles de prioridad
  components/
    ui/           -> componentes shadcn/ui (no tocar salvo que sea necesario)
    layout/       -> AppShell (sidebar), ProtectedRoute, PeriodoPicker
  hooks/
    use-periodo.ts -> estado de mes/año compartido por las páginas con filtro de periodo
  router.tsx      -> definición de rutas
```

Cada módulo de `features/` sigue el mismo patrón: un `api.ts` con hooks de
TanStack Query construidos sobre `api` (el cliente tipado) y una o más
páginas. Para agregar algo nuevo, copiá el patrón de `features/ingresos/`.

## Regenerar los tipos de la API

Si el backend cambia su schema (nuevos campos, endpoints, etc.):

```bash
# 1. Regenerar el spec congelado en el backend
cd ../finanzas_backend
docker compose exec backend uv run manage.py spectacular --file docs/openapi.json --format openapi-json

# 2. Regenerar los tipos del frontend a partir de ese spec
cd ../finanzas_frontend
pnpm gen:api
```

## Nota sobre los schemas de escritura (POST)

El backend reutiliza el mismo serializer para leer y escribir en varios
endpoints (p. ej. `CategoriaGasto`, `Ingreso`, `ServicioFijo`), así que el
OpenAPI generado marca campos de solo servidor (`id`, `usuario_id`, `activo`)
como si fueran parte del body de creación. Cada `features/<módulo>/api.ts`
define su propio tipo de input con `Omit<Schema, 'id' | 'usuario_id' | ...>`
para reflejar lo que el body realmente espera, en vez de pelear con el tipo
generado.

## Componentes UI

Instalados con `pnpm dlx shadcn@latest add <componente>`. Ya están:
button, input, label, card, table, dialog, select, dropdown-menu, badge,
tabs, separator, sonner.
