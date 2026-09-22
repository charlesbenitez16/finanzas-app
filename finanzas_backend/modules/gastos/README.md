# Módulo `gastos` — esqueleto (kata)

Entidad `GASTOS` del `.mermaid` / tabla `gastos` de `01_schema.sql`. Es
el módulo con **más lógica de negocio**: balance mensual, variación de
precios y modo emergencia. Estructura calcada de `modules/catalogos/`.

## Qué implementar y en qué orden

1. **`domain/entities.py`**:
   - `Gasto` → `es_pago_de_servicio_fijo()`, `esta_pagado()`,
     `pertenece_al_periodo()`, `es_estado_valido()`.
   - `BalanceMensual`, `VariacionServicio`, `AhorroPorPrioridad` →
     objetos de **lectura** (no entidades, sin id).
2. **`domain/events.py` → `GastoRegistrado`**: evento que publica este
   módulo; `modules/alertas` se suscribe (bus en `shared/domain/events.py`).
3. **`domain/ports/repositories.py` → `GastoRepository`**: contiene las
   traducciones de las vistas A, B, C y la constraint
   `uq_gasto_servicio_periodo`.
4. **`infrastructure/models.py`**: `GastoModel` (`managed = False`), con
   `UniqueConstraint` parcial `uq_gasto_servicio_periodo`.
5. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del
   puerto (aquí van los `Sum`/`annotate`/`values` del ORM).
6. **`application/use_cases/`**:
   - `registrar_gasto` (puntual) · `registrar_pago_servicio_fijo`
     (chequea duplicado + publica evento)
   - `listar_gastos_del_periodo`
   - `calcular_balance_mensual` (inyecta `IngresoRepository` + `GastoRepository`)
   - `calcular_variacion_servicios` (LAG en Python)
   - `simular_modo_emergencia` (inyecta `NivelPrioridadRepository` de
     `catalogos` + `GastoRepository` — el caso que `catalogos` anticipó)
7. **`interfaces/api/`**: `GastosView`, `PagosServicioFijoView`,
   `BalanceMensualView`, `VariacionServiciosView`, `ModoEmergenciaView`.

## Consultas SQL mapeadas (regla 4)

| Vista / constraint SQL | Puerto | Caso de uso |
|---|---|---|
| `vista_balance_mensual` (lado gastos) | `GastoRepository.sumar_montos_por_periodo` | `CalcularBalanceMensualUseCase` |
| `vista_variacion_servicios` (`LAG`) | `GastoRepository.listar_pagos_de_servicio_fijo` | `CalcularVariacionServiciosUseCase` |
| `vista_ahorro_potencial_por_prioridad` | `GastoRepository.total_por_prioridad` | `SimularModoEmergenciaUseCase` |
| `uq_gasto_servicio_periodo` | `GastoRepository.existe_pago_de_servicio_en_periodo` | `RegistrarPagoDeServicioFijoUseCase` |
| `idx_gastos_usuario_periodo` | `GastoRepository.listar_por_usuario_y_periodo` | `ListarGastosDelPeriodoUseCase` |

## Probar

```bash
uv run python -m unittest modules.gastos.tests.domain.test_entities \
    modules.gastos.tests.application.test_use_cases -v
```
