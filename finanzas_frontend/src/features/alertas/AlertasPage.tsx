import { useState } from 'react'
import { toast } from 'sonner'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import type { components } from '@/api/schema'
import { useAlertas, useCambiarEstadoAlerta, useGenerarAlertas } from './api'

type EstadoAlerta = components['schemas']['AlertaPagoEstadoEnum']

const ESTADOS: EstadoAlerta[] = ['Pendiente', 'Enviada', 'Leida', 'Resuelta']

const SIGUIENTE_ESTADO: Partial<Record<EstadoAlerta, 'Enviada' | 'Leida'>> = {
  Pendiente: 'Enviada',
  Enviada: 'Leida',
}

export function AlertasPage() {
  const [estado, setEstado] = useState<EstadoAlerta>('Pendiente')
  const alertas = useAlertas(estado)
  const generarAlertas = useGenerarAlertas()
  const cambiarEstado = useCambiarEstadoAlerta()

  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between">
        <h1 className="font-heading text-2xl font-bold">Alertas</h1>
        <Button
          variant="outline"
          disabled={generarAlertas.isPending}
          onClick={() =>
            generarAlertas.mutate(undefined, {
              onSuccess: (data) => toast.success(`${data?.length ?? 0} alerta(s) nueva(s) generada(s)`),
            })
          }
        >
          Generar alertas de hoy
        </Button>
      </div>

      <Tabs value={estado} onValueChange={(v) => setEstado(v as EstadoAlerta)}>
        <TabsList>
          {ESTADOS.map((e) => (
            <TabsTrigger key={e} value={e}>
              {e}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>

      <Card>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Fecha</TableHead>
                <TableHead>Mensaje</TableHead>
                <TableHead>Periodo</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead />
              </TableRow>
            </TableHeader>
            <TableBody>
              {alertas.data?.map((alerta) => {
                const siguiente = SIGUIENTE_ESTADO[alerta.estado]
                return (
                  <TableRow key={alerta.id}>
                    <TableCell>{alerta.fecha_alerta}</TableCell>
                    <TableCell>{alerta.mensaje ?? '—'}</TableCell>
                    <TableCell>{alerta.periodo_mes}/{alerta.periodo_anio}</TableCell>
                    <TableCell>
                      <Badge
                        variant={
                          alerta.estado === 'Resuelta'
                            ? 'success'
                            : alerta.estado === 'Pendiente'
                              ? 'warning'
                              : 'info'
                        }
                      >
                        {alerta.estado}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {siguiente && (
                        <Button
                          size="sm"
                          variant="outline"
                          disabled={cambiarEstado.isPending}
                          onClick={() =>
                            cambiarEstado.mutate({ alertaId: alerta.id, estado: siguiente })
                          }
                        >
                          Marcar {siguiente}
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                )
              })}
              {alertas.data?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground">
                    Sin alertas en este estado.
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
