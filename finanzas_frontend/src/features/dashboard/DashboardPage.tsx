import { TrendingUp, TrendingDown, Scale, BellRing } from 'lucide-react'
import { PeriodoPicker } from '@/components/layout/PeriodoPicker'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useBalanceMensual } from '@/features/gastos/api'
import { useAlertas } from '@/features/alertas/api'
import { usePeriodo } from '@/hooks/use-periodo'
import { formatMonto } from '@/lib/format'

export function DashboardPage() {
  const { mes, anio, setMes, setAnio } = usePeriodo()
  const balance = useBalanceMensual(mes, anio)
  const alertas = useAlertas('Pendiente')

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Dashboard</h1>
        <PeriodoPicker mes={mes} anio={anio} onMesChange={setMes} onAnioChange={setAnio} />
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <Card>
          <CardHeader className="flex-row items-center gap-4">
            <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-success text-success-foreground">
              <TrendingUp className="size-5" />
            </span>
            <div className="flex flex-col gap-1">
              <CardDescription>Ingresos del periodo</CardDescription>
              <CardTitle className="text-2xl">
                {balance.data ? formatMonto(balance.data.total_ingresos) : '—'}
              </CardTitle>
            </div>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="flex-row items-center gap-4">
            <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-warning text-warning-foreground">
              <TrendingDown className="size-5" />
            </span>
            <div className="flex flex-col gap-1">
              <CardDescription>Gastos del periodo</CardDescription>
              <CardTitle className="text-2xl">
                {balance.data ? formatMonto(balance.data.total_gastos) : '—'}
              </CardTitle>
            </div>
          </CardHeader>
        </Card>
        <Card>
          <CardHeader className="flex-row items-center gap-4">
            <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground">
              <Scale className="size-5" />
            </span>
            <div className="flex flex-col gap-1">
              <CardDescription>Balance</CardDescription>
              <CardTitle className="text-2xl">
                {balance.data ? formatMonto(balance.data.balance) : '—'}
              </CardTitle>
            </div>
          </CardHeader>
        </Card>
      </div>

      <Card>
        <CardHeader className="flex-row items-center gap-4">
          <span className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-destructive text-white">
            <BellRing className="size-5" />
          </span>
          <div className="flex flex-col gap-1">
            <CardTitle>Alertas pendientes</CardTitle>
            <CardDescription>
              {alertas.data?.length ?? 0} alerta(s) pendiente(s) de servicios próximos a vencer
            </CardDescription>
          </div>
        </CardHeader>
        {!!alertas.data?.length && (
          <CardContent>
            <ul className="flex flex-col gap-2 text-sm">
              {alertas.data.map((alerta) => (
                <li key={alerta.id} className="flex justify-between border-b border-border pb-2 last:border-0">
                  <span>{alerta.mensaje ?? `Servicio #${alerta.servicio_fijo_id}`}</span>
                  <span className="text-muted-foreground">{alerta.fecha_alerta}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        )}
      </Card>
    </div>
  )
}
