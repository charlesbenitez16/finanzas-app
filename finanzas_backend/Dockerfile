# Imagen de desarrollo para finanzas_backend (Django + DRF, gestionado con uv).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.dev

# psycopg[binary] ya trae su propio libpq, no hace falta libpq-dev/gcc.
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copiar solo los manifiestos primero: si el codigo cambia pero las
# dependencias no, esta capa se reusa de la cache de Docker.
COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
