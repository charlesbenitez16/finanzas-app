import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { PeriodoPicker } from '@/components/layout/PeriodoPicker'
import { usePeriodo } from '@/hooks/use-periodo'
import { formatDate, formatMonto } from '@/lib/format'
import { useGastos } from './api'
import { GastoFormDialog } from './GastoFormDialog'
import { PagoServicioFormDialog } from './PagoServicioFormDialog'

const ESTADO_VARIANT = {
  Pagado: 'success',
  Pendiente: 'warning',
  Vencido: 'destructive',
} as const

export function GastosPage() {
  const { mes, anio, setMes, setAnio } = usePeriodo()
  const gastos = useGastos(mes, anio)

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Gastos</h1>
        <div className="flex items-center gap-3">
          <PeriodoPicker mes={mes} anio={anio} onMesChange={setMes} onAnioChange={setAnio} />
          <PagoServicioFormDialog mes={mes} anio={anio} />
          <GastoFormDialog mes={mes} anio={anio} />
        </div>
      </div>

      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Fecha</TableHead>
                <TableHead>Descripción</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead className="text-right">Monto</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {gastos.data?.map((gasto) => (
                <TableRow key={gasto.id}>
                  <TableCell>{formatDate(gasto.fecha_gasto)}</TableCell>
                  <TableCell>{gasto.descripcion ?? '—'}</TableCell>
                  <TableCell>
                    <Badge variant={ESTADO_VARIANT[gasto.estado]}>{gasto.estado}</Badge>
                  </TableCell>
                  <TableCell>
                    {gasto.servicio_fijo_id ? 'Servicio fijo' : 'Puntual'}
                  </TableCell>
                  <TableCell className="text-right">{formatMonto(gasto.monto)}</TableCell>
                </TableRow>
              ))}
              {gastos.data?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground">
                    Sin gastos en este periodo.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
