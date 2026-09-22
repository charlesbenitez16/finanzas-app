# Módulo `ingresos` — esqueleto (kata)

Entidad `INGRESOS` del `.mermaid` / tabla `ingresos` de `01_schema.sql`.
Estructura calcada de `modules/catalogos/`. Cuerpos vacíos con la
consigna en cada docstring y un `# TODO:` por pieza.

## Qué implementar y en qué orden

1. **`domain/entities.py` → `Ingreso`**: `pertenece_al_periodo(mes, anio)`,
   `es_monto_valido()` (CHECK `monto > 0`).
2. **`domain/ports/repositories.py` → `IngresoRepository`**:
   `obtener_por_id`, `crear`, `listar_por_usuario_y_periodo`,
   `sumar_montos_por_periodo` (lado *ingresos* de `vista_balance_mensual`).
3. **`infrastructure/models.py`**: `IngresoModel` (`managed = False`,
   `idx_ingresos_usuario_periodo`).
4. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del puerto.
5. **`application/use_cases/`**: `registrar_ingreso`,
   `listar_ingresos_del_periodo`, `calcular_total_ingresos_periodo`.
6. **`interfaces/api/`**: `IngresosView` (GET/POST), `TotalIngresosPeriodoView`.

## Consultas SQL mapeadas (regla 4)

| SQL | Puerto | Caso de uso |
|---|---|---|
| `vista_balance_mensual` (lado ingresos): `SELECT SUM(monto) ... GROUP BY periodo` | `IngresoRepository.sumar_montos_por_periodo` | `CalcularTotalIngresosPeriodoUseCase` — lo consume `CalcularBalanceMensualUseCase` en `modules/gastos` |
| `idx_ingresos_usuario_periodo` | `IngresoRepository.listar_por_usuario_y_periodo` | `ListarIngresosDelPeriodoUseCase` |

## Probar

```bash
uv run python -m unittest modules.ingresos.tests.domain.test_entities \
    modules.ingresos.tests.application.test_use_cases -v
```
