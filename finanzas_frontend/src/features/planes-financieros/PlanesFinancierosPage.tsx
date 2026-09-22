import { PeriodoPicker } from '@/components/layout/PeriodoPicker'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
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
import { formatMonto } from '@/lib/format'
import { useActivarPlan, useComparativa, usePlanesFinancieros } from './api'
import { PlanFormDialog } from './PlanFormDialog'

export function PlanesFinancierosPage() {
  const { mes, anio, setMes, setAnio } = usePeriodo()
  const planes = usePlanesFinancieros()
  const comparativa = useComparativa(mes, anio)
  const activarPlan = useActivarPlan()

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Planes financieros</h1>
        <PlanFormDialog />
      </div>

      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nombre</TableHead>
                <TableHead className="text-right">% gasto fijo</TableHead>
                <TableHead className="text-right">% ahorro</TableHead>
                <TableHead className="text-right">% gasto libre</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead />
              </TableRow>
            </TableHeader>
            <TableBody>
              {planes.data?.map((plan) => (
                <TableRow key={plan.id}>
                  <TableCell>{plan.nombre}</TableCell>
                  <TableCell className="text-right">{plan.porcentaje_gasto_fijo}%</TableCell>
                  <TableCell className="text-right">{plan.porcentaje_ahorro}%</TableCell>
                  <TableCell className="text-right">{plan.porcentaje_gasto_libre}%</TableCell>
                  <TableCell>
                    {plan.activo && <Badge variant="success">Activo</Badge>}
                  </TableCell>
                  <TableCell>
                    {!plan.activo && (
                      <Button
                        size="sm"
                        variant="outline"
                        disabled={activarPlan.isPending}
                        onClick={() => activarPlan.mutate(plan.id)}
                      >
                        Activar
                      </Button>
                    )}
                  </TableCell>
                </TableRow>
              ))}
              {planes.data?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} className="text-center text-muted-foreground">
                    Todavía no creaste ningún plan.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <div className="flex items-center justify-between">
        <h2 className="font-heading text-lg font-semibold">Comparativa del periodo</h2>
        <PeriodoPicker mes={mes} anio={anio} onMesChange={setMes} onAnioChange={setAnio} />
      </div>

      {comparativa.isError && (
        <Card>
          <CardHeader>
            <CardDescription>No tenés un plan activo para este periodo.</CardDescription>
          </CardHeader>
        </Card>
      )}

      {comparativa.data && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Card>
            <CardHeader>
              <CardDescription>Meta gasto fijo</CardDescription>
              <CardTitle className="text-xl">{formatMonto(comparativa.data.meta_gasto_fijo)}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Meta ahorro</CardDescription>
              <CardTitle className="text-xl">{formatMonto(comparativa.data.meta_ahorro)}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Meta gasto libre</CardDescription>
              <CardTitle className="text-xl">{formatMonto(comparativa.data.meta_gasto_libre)}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Gasto real</CardDescription>
              <CardTitle className="text-xl">{formatMonto(comparativa.data.gasto_real)}</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader>
              <CardDescription>Balance real</CardDescription>
              <CardTitle className="text-xl">{formatMonto(comparativa.data.balance_real)}</CardTitle>
            </CardHeader>
          </Card>
        </div>
      )}
    </div>
  )
}
