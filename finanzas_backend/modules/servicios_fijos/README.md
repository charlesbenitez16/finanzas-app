# Módulo `servicios_fijos` — esqueleto (kata)

Entidad `SERVICIOS_FIJOS` del `.mermaid` / tabla `servicios_fijos` de
`01_schema.sql`. Es la "plantilla" de un gasto recurrente; cada mes
genera un pago real que se registra como `Gasto` en `modules/gastos`.
Módulo propio (decisión de arquitectura: aggregate root con ciclo de
vida independiente). Estructura calcada de `modules/catalogos/`.

## Qué implementar y en qué orden

1. **`domain/entities.py` → `ServicioFijo`**: `esta_activo()`,
   `esta_vigente(fecha)`, `fecha_vencimiento_en(mes, anio)`,
   `dias_para_vencimiento(fecha_ref)`, `debe_generar_alerta(fecha_ref)`.
2. **`domain/ports/repositories.py` → `ServicioFijoRepository`**:
   incluye `listar_proximos_a_vencer(fecha_referencia)` — la query
   comentada al final de `01_schema.sql` (insumo del generador de alertas).
3. **`infrastructure/models.py`**: `ServicioFijoModel` (`managed = False`).
   Decisión: FK reales a `catalogos.*` vs `IntegerField` desacoplado
   (documentado en el docstring).
4. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del puerto.
5. **`application/use_cases/`**: `crear_servicio_fijo` (valida CHECKs),
   `listar_servicios_activos`, `listar_servicios_proximos_a_vencer`,
   `desactivar_servicio_fijo`.
6. **`interfaces/api/`**: `ServiciosFijosView` (GET/POST),
   `ServiciosProximosAVencerView`.

## Consultas SQL mapeadas (regla 4)

| SQL | Puerto | Caso de uso |
|---|---|---|
| Query comentada final de `01_schema.sql` (servicios próximos a vencer, sin el `NOT EXISTS`) | `ServicioFijoRepository.listar_proximos_a_vencer` | `ListarServiciosProximosAVencerUseCase` → lo consume `GenerarAlertasDeVencimientoUseCase` en `modules/alertas` |
| `idx_servicios_usuario` | `ServicioFijoRepository.listar_por_usuario` | `ListarServiciosActivosUseCase` |

## Probar

```bash
uv run python -m unittest modules.servicios_fijos.tests.domain.test_entities \
    modules.servicios_fijos.tests.application.test_use_cases -v
```
