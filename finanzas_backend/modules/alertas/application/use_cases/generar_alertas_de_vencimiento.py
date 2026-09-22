"""Caso de uso: generar alertas para los servicios fijos proximos a vencer (job/cron)."""

from dataclasses import dataclass
from datetime import date

from modules.alertas.domain.entities import AlertaPago
from modules.alertas.domain.ports.repositories import AlertaPagoRepository
from modules.servicios_fijos.domain.ports.repositories import ServicioFijoRepository
from shared.domain.events import event_bus
from modules.alertas.domain.events import AlertaGenerada

@dataclass
class GenerarAlertasDeVencimientoUseCase:
    """
    CONSIGNA
    --------
    Es la traduccion completa de la query comentada al final de
    01_schema.sql ("Servicios proximos a vencer... correr esto diario
    desde un job / cron"). CRUZA dos modulos: servicios_fijos y alertas.

      1. servicios = self.servicio_fijo_repositorio.listar_proximos_a_vencer(
             fecha_referencia)   # ya filtra activos + ventana de anticipacion
      2. por cada servicio:
           - determinar el periodo (mes, anio) del vencimiento
           - si NOT self.alerta_repositorio.existe_alerta_para_servicio_en_periodo(
                 servicio.id, mes, anio):        # uq_alerta_servicio_periodo
               crear una AlertaPago(estado='Pendiente', fecha_alerta=...,
               mensaje=...) y persistirla
      3. devolver la lista de alertas creadas (las nuevas, no las que ya existian)

    El "AND NOT EXISTS (pago de este mes)" de la query SQL: decidi si lo
    chequeas aca (necesitarias el GastoRepository) o si confias en que un
    servicio ya pagado no aparece como "proximo a vencer". Deja tu
    decision como TODO.

    Params de ejecutar(): fecha_referencia: date | None (default: hoy)
    Retorno: list[AlertaPago] (las creadas en esta corrida)
    """

    servicio_fijo_repositorio: ServicioFijoRepository
    alerta_repositorio: AlertaPagoRepository

    def ejecutar(self, fecha_referencia: date | None = None) -> list[AlertaPago]:
        fecha_referencia = fecha_referencia or date.today()
        servicios = self.servicio_fijo_repositorio.listar_proximos_a_vencer(fecha_referencia)
        creadas = []
        for s in servicios:
            venc = s.fecha_vencimiento_en(fecha_referencia.month, fecha_referencia.year)
            mes, anio = venc.month, venc.year
            if self.alerta_repositorio.existe_alerta_para_servicio_en_periodo(s.id, mes, anio):
                continue
            alerta = AlertaPago(
                usuario_id=s.usuario_id, servicio_fijo_id=s.id, gasto_id=None,
                periodo_mes=mes, periodo_anio=anio, fecha_alerta=fecha_referencia,
                estado="Pendiente",
                mensaje=f"Tu servicio '{s.nombre}' vence el {venc.isoformat()}.",
            )
            alerta_creada = self.alerta_repositorio.crear(alerta)
            event_bus.publicar(AlertaGenerada(
                alerta_id=alerta_creada.id,
                usuario_id=alerta_creada.usuario_id,
                servicio_fijo_id=alerta_creada.servicio_fijo_id,
                mensaje=alerta_creada.mensaje,
            ))
            creadas.append(alerta_creada)
        return creadas
