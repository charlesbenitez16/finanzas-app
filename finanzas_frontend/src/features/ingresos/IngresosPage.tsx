import { PeriodoPicker } from '@/components/layout/PeriodoPicker'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { usePeriodo } from '@/hooks/use-periodo'
import { formatDate, formatMonto } from '@/lib/format'
import { useIngresos, useTotalIngresosPeriodo } from './api'
import { IngresoFormDialog } from './IngresoFormDialog'

export function IngresosPage() {
  const { mes, anio, setMes, setAnio } = usePeriodo()
  const ingresos = useIngresos(mes, anio)
  const total = useTotalIngresosPeriodo(mes, anio)

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Ingresos</h1>
        <div className="flex items-center gap-3">
          <PeriodoPicker mes={mes} anio={anio} onMesChange={setMes} onAnioChange={setAnio} />
          <IngresoFormDialog mes={mes} anio={anio} />
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardDescription>Total del periodo</CardDescription>
          <CardTitle className="text-2xl">
            {total.data ? formatMonto(total.data.total_ingresos) : '—'}
          </CardTitle>
        </CardHeader>
      </Card>

      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Fecha</TableHead>
                <TableHead>Fuente</TableHead>
                <TableHead>Descripción</TableHead>
                <TableHead className="text-right">Monto</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ingresos.data?.map((ingreso) => (
                <TableRow key={ingreso.id}>
                  <TableCell>{formatDate(ingreso.fecha)}</TableCell>
                  <TableCell>{ingreso.fuente ?? '—'}</TableCell>
                  <TableCell>{ingreso.descripcion ?? '—'}</TableCell>
                  <TableCell className="text-right">{formatMonto(ingreso.monto)}</TableCell>
                </TableRow>
              ))}
              {ingresos.data?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-muted-foreground">
                    Sin ingresos en este periodo.
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
