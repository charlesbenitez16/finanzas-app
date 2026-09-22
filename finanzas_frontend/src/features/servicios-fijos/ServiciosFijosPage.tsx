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
import { formatMonto } from '@/lib/format'
import { useProximosAVencer, useServiciosFijos } from './api'
import { ServicioFijoFormDialog } from './ServicioFijoFormDialog'

export function ServiciosFijosPage() {
  const servicios = useServiciosFijos()
  const proximos = useProximosAVencer()
  const proximosIds = new Set(proximos.data?.map((s) => s.id))

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Servicios fijos</h1>
        <ServicioFijoFormDialog />
      </div>

      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nombre</TableHead>
                <TableHead>Día de vencimiento</TableHead>
                <TableHead className="text-right">Monto estimado</TableHead>
                <TableHead>Estado</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {servicios.data?.map((servicio) => (
                <TableRow key={servicio.id}>
                  <TableCell>{servicio.nombre}</TableCell>
                  <TableCell>{servicio.dia_vencimiento}</TableCell>
                  <TableCell className="text-right">
                    {servicio.monto_estimado ? formatMonto(servicio.monto_estimado) : '—'}
                  </TableCell>
                  <TableCell>
                    {proximosIds.has(servicio.id) && (
                      <Badge variant="destructive">Próximo a vencer</Badge>
                    )}
                  </TableCell>
                </TableRow>
              ))}
              {servicios.data?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} className="text-center text-muted-foreground">
                    No tenés servicios fijos activos.
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
