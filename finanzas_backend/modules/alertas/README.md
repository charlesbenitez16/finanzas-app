# Módulo `alertas` — esqueleto (kata)

Entidad `ALERTAS_PAGO` del `.mermaid` / tabla `alertas_pago` de
`01_schema.sql`. Recordatorios de vencimiento de servicios fijos, con
máquina de estados `Pendiente → Enviada → Leida → Resuelta`. Estructura
calcada de `modules/catalogos/`.

## Qué implementar y en qué orden

1. **`domain/entities.py` → `AlertaPago`**: `esta_pendiente()`,
   `esta_resuelta()`, `marcar_enviada()`, `marcar_leida()`,
   `resolver(gasto_id)`, `es_estado_valido()`. La entidad **sí** valida
   su propia máquina de estados (solo mira `self.estado`).
2. **`domain/ports/repositories.py` → `AlertaPagoRepository`**:
   `listar_por_usuario_y_estado` (idx), `existe_alerta_para_servicio_en_periodo`
   y `obtener_por_servicio_y_periodo` (uq_alerta_servicio_periodo).
3. **`infrastructure/models.py`**: `AlertaPagoModel` (`managed = False`),
   índice `idx_alertas_usuario_estado`, `UniqueConstraint`
   `uq_alerta_servicio_periodo`.
4. **`infrastructure/repositories.py`**: `_a_entidad()` + métodos del puerto.
5. **`application/use_cases/`**:
   - `generar_alertas_de_vencimiento` (job/cron — cruza con
     `servicios_fijos`; traduce la query comentada de `01_schema.sql`)
   - `listar_alertas_pendientes`
   - `marcar_alerta` (`MarcarAlertaComoEnviadaUseCase` /
     `MarcarAlertaComoLeidaUseCase`)
   - `resolver_alerta_al_pagar` → **handler del evento `GastoRegistrado`**
     (publicado por `modules/gastos`). El wiring va en `apps.py::ready()`.
6. **`interfaces/api/`**: `AlertasView` (GET `?estado=`),
   `GenerarAlertasView` (POST `/generar/`), `AlertaDetailView` (PATCH).

## Consultas SQL / eventos mapeados (regla 4)

| Origen | Puerto / mecanismo | Caso de uso |
|---|---|---|
| Query comentada final de `01_schema.sql` (generador de alertas) | `ServicioFijoRepository.listar_proximos_a_vencer` + `AlertaPagoRepository.existe_alerta_para_servicio_en_periodo` | `GenerarAlertasDeVencimientoUseCase` |
| `idx_alertas_usuario_estado` | `AlertaPagoRepository.listar_por_usuario_y_estado` | `ListarAlertasPendientesUseCase` |
| `uq_alerta_servicio_periodo` | `AlertaPagoRepository.existe_alerta_para_servicio_en_periodo` / `obtener_por_servicio_y_periodo` | `GenerarAlertasDeVencimientoUseCase` / `ResolverAlertaAlPagarUseCase` |
| Relación `GASTOS |o--o| ALERTAS_PAGO : resuelve` del `.mermaid` | evento `GastoRegistrado` (bus en `shared/domain/events.py`) | `ResolverAlertaAlPagarUseCase` |

## Probar

```bash
uv run python -m unittest modules.alertas.tests.domain.test_entities \
    modules.alertas.tests.application.test_use_cases -v
```
