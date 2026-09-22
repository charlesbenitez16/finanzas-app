# Módulo `planes_financieros` — esqueleto (kata)

Entidad `PLAN_FINANCIERO` del `.mermaid` / tabla `plan_financiero` de
`01_schema.sql`. Reparto del ingreso estilo 50/30/20 personalizable.
Estructura calcada de `modules/catalogos/`.

## Qué implementar y en qué orden

1. **`domain/entities.py`**:
   - `PlanFinanciero` → `porcentajes_suman_100()` (la entidad **sí**
     puede validar su propia invariante, a diferencia de `NivelPrioridad`),
     `esta_activo()`, `esta_vigente(fecha)`, `meta_gasto_fijo(ingreso)`,
     `meta_ahorro(ingreso)`, `meta_gasto_libre(ingreso)`.
   - `ComparativaPlanVsReal` → objeto de lectura (fila de `vista_plan_vs_real`).
2. **`domain/ports/repositories.py` → `PlanFinancieroRepository`**:
   `obtener_plan_activo` es la traducción de `uq_plan_activo_usuario` y
   el insumo de `vista_plan_vs_real`.
3. **`infrastructure/models.py`**: `PlanFinancieroModel` (`managed = False`),
   con `UniqueConstraint` parcial `uq_plan_activo_usuario`.
4. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del puerto.
5. **`application/use_cases/`**: `crear_plan_financiero` (valida suma 100),
   `activar_plan_financiero` (desactiva el anterior),
   `obtener_plan_activo`, `comparar_plan_vs_real` (reusa
   `CalcularBalanceMensualUseCase` de `modules/gastos`).
6. **`interfaces/api/`**: `PlanesFinancierosView`, `ActivarPlanView`
   (`/<id>/activar/`), `ComparativaView`.

## Consultas SQL mapeadas (regla 4)

| Vista / constraint SQL | Puerto | Caso de uso |
|---|---|---|
| `vista_plan_vs_real` | `PlanFinancieroRepository.obtener_plan_activo` (+ `CalcularBalanceMensualUseCase`) | `CompararPlanVsRealUseCase` |
| `uq_plan_activo_usuario` (`WHERE activo = TRUE`) | `PlanFinancieroRepository.obtener_plan_activo` | `ActivarPlanFinancieroUseCase` |
| `CHECK (suma de porcentajes = 100)` | — (regla de entidad) | `PlanFinanciero.porcentajes_suman_100()` |

## Probar

```bash
uv run python -m unittest modules.planes_financieros.tests.domain.test_entities \
    modules.planes_financieros.tests.application.test_use_cases -v
```
