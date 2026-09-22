"""Caso de uso: registrar el pago mensual de un servicio fijo como un Gasto."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from modules.gastos.domain.entities import Gasto
from modules.gastos.domain.exceptions import MontoInvalido, PagoDeServicioDuplicado
from modules.gastos.domain.ports.repositories import GastoRepository

from shared.domain.events import event_bus
from modules.gastos.domain.events import GastoRegistrado


@dataclass
class RegistrarPagoDeServicioFijoUseCase:
    """
    CONSIGNA
    --------
    Registra el pago de un servicio fijo (Internet, Agua, Luz...) para un
    periodo. Es un Gasto con servicio_fijo_id seteado.
      1. monto > 0 -> si no, MontoInvalido
      2. NO puede existir ya un pago de ese servicio en ese periodo
         (constraint uq_gasto_servicio_periodo):
         si self.repositorio.existe_pago_de_servicio_en_periodo(...) ->
         raise PagoDeServicioDuplicado
      3. construir el Gasto y persistir.
      4. publicar GastoRegistrado(gasto_id, usuario_id, servicio_fijo_id,
         periodo_mes, periodo_anio) para que el modulo `alertas` marque la
         alerta de ese servicio/periodo como 'Resuelta'.

    Nota: categoria_id y prioridad_id normalmente se heredan del propio
    servicio fijo. Decidi si los recibe la vista o si este caso de uso
    consulta el ServicioFijoRepository (dependeria de otro modulo). Deja
    tu decision como TODO.

    Params de ejecutar(): usuario_id, servicio_fijo_id, categoria_id,
        prioridad_id, monto, fecha_gasto, periodo_mes, periodo_anio, descripcion
    Retorno: Gasto (con id)
    """

    repositorio: GastoRepository

    def ejecutar(
        self,
        usuario_id: int,
        servicio_fijo_id: int,
        categoria_id: int,
        prioridad_id: int,
        monto: Decimal,
        fecha_gasto: date,
        periodo_mes: int,
        periodo_anio: int,
        descripcion: Optional[str] = None,
    ) -> Gasto:
        if monto is None or monto <= 0:
            raise MontoInvalido("El monto debe ser mayor a 0")
        if self.repositorio.existe_pago_de_servicio_en_periodo(
            servicio_fijo_id, periodo_mes, periodo_anio
        ):
            raise PagoDeServicioDuplicado(
                f"El servicio {servicio_fijo_id} ya tiene un pago en "
                f"{periodo_mes}/{periodo_anio}"
            )
        gasto = Gasto(
            usuario_id=usuario_id, categoria_id=categoria_id,
            servicio_fijo_id=servicio_fijo_id, prioridad_id=prioridad_id,
            monto=monto, fecha_gasto=fecha_gasto, periodo_mes=periodo_mes,
            periodo_anio=periodo_anio, estado="Pagado", descripcion=descripcion,
        )
        gasto = self.repositorio.crear(gasto)
        event_bus.publicar(GastoRegistrado(
            gasto_id=gasto.id, usuario_id=usuario_id,
            servicio_fijo_id=servicio_fijo_id,
            periodo_mes=periodo_mes, periodo_anio=periodo_anio,
        ))
        return gasto
