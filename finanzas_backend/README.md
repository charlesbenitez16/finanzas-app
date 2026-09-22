# Finanzas backend

Monolito modular + arquitectura hexagonal, Django + DRF, gestionado con `uv`.

## Requisitos

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) instalado
- El contenedor de PostgreSQL del proyecto corriendo (`docker-compose.yml` en el repo de la base de datos)

## Instalación

```bash
uv sync
```

Esto crea el entorno virtual (`.venv/`) e instala exactamente las versiones fijadas en `uv.lock` (Django 6.1, DRF, psycopg).

## Configuración de base de datos

Por defecto, `config/settings/base.py` usa las mismas credenciales que ya definimos en `docker-compose.yml`:

| Variable | Valor por defecto |
|---|---|
| `POSTGRES_DB` | `finanzas_db` |
| `POSTGRES_USER` | `finanzas_user` |
| `POSTGRES_PASSWORD` | `finanzas_pass` |
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5432` |

Si tu contenedor corre con otro puerto/host, exporta esas variables de entorno antes de correr cualquier comando (o creá un `.env` y cargalo vos mismo, no agregué esa dependencia para no sumar complejidad extra).

## Correr el proyecto

```bash
# Aplica las migraciones propias de Django (auth, sessions, admin).
# OJO: los modelos de catalogos tienen managed = False, asi que esto
# NO va a tocar categorias_gasto ni niveles_prioridad (esas ya existen
# gracias a 01_schema.sql). Ver la nota en infrastructure/models.py.
uv run manage.py migrate

# Crear un usuario admin para poder entrar a /admin/
uv run manage.py createsuperuser

# Levantar el servidor de desarrollo
uv run manage.py runserver
```

Con el servidor corriendo:
- Admin: http://localhost:8000/admin/
- API de catalogos (una vez que completes las vistas): http://localhost:8000/api/catalogos/categorias/ y http://localhost:8000/api/catalogos/niveles-prioridad/

## Tests

```bash
uv run manage.py test
```

## Estructura del proyecto

Ver `arquitectura_backend.md` (entregado antes) para la explicación completa de la arquitectura. Resumen rápido:

```
config/       -> configuracion Django (settings, urls raiz)
shared/       -> kernel compartido entre modulos (Entity base, eventos, etc.)
modules/      -> un paquete por modulo/bounded context
  catalogos/  -> primer modulo implementado (ver su propio README)
```

## Estado del proyecto

`catalogos` está completo (las 4 capas + tests) y sirve como módulo de
referencia. Ver `modules/catalogos/README.md` para el detalle de qué se
implementó en cada capa y la guía para replicar el patrón.

## Próximos pasos

Replicar el mismo patrón de `catalogos/` para `ingresos`, `gastos`,
`planes_financieros`, `alertas` y `usuarios`. El orden sugerido es ese:
`usuarios` al final porque varios de los otros módulos (como `gastos`)
lo necesitan solo como una FK, mientras que `ingresos` es el más simple
para practicar el patrón una vez más antes de entrar a `gastos`, que es
el módulo con más lógica de negocio (variación de precios, modo
emergencia).
