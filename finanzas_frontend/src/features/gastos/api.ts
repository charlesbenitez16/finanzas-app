import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type Gasto = components['schemas']['Gasto']
export type GastoInput = Omit<Gasto, 'id' | 'usuario_id' | 'servicio_fijo_id'>
export type PagoServicioInput = components['schemas']['RegistrarPagoServicioFijo']

export function useGastos(mes: number, anio: number) {
  return useQuery({
    queryKey: ['gastos', mes, anio],
    queryFn: () => unwrap(api.GET('/api/gastos/', { params: { query: { mes, anio } } })),
  })
}

function invalidateGastos(queryClient: ReturnType<typeof useQueryClient>) {
  queryClient.invalidateQueries({ queryKey: ['gastos'] })
  queryClient.invalidateQueries({ queryKey: ['alertas'] })
}

export function useCrearGasto() {
  const queryClient = useQueryClient()
  return useMutation({
    // Ver nota en features/catalogos/api.ts sobre el cast.
    mutationFn: (body: GastoInput) => unwrap(api.POST('/api/gastos/', { body: body as Gasto })),
    onSuccess: () => invalidateGastos(queryClient),
  })
}

export function usePagarServicio() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (body: PagoServicioInput) =>
      unwrap(api.POST('/api/gastos/pagos-servicio/', { body })),
    onSuccess: () => invalidateGastos(queryClient),
  })
}

export function useBalanceMensual(mes: number, anio: number) {
  return useQuery({
    queryKey: ['gastos', 'balance-mensual', mes, anio],
    queryFn: () =>
      unwrap(api.GET('/api/gastos/balance-mensual/', { params: { query: { mes, anio } } })),
  })
}

export function useVariacionServicio(servicioFijoId: number | null) {
  return useQuery({
    queryKey: ['gastos', 'variacion-servicios', servicioFijoId],
    enabled: servicioFijoId !== null,
    queryFn: () =>
      unwrap(
        api.GET('/api/gastos/variacion-servicios/', {
          params: { query: { servicio_fijo_id: servicioFijoId! } },
        }),
      ),
  })
}

export function useModoEmergencia(mes: number, anio: number) {
  return useQuery({
    queryKey: ['gastos', 'modo-emergencia', mes, anio],
    queryFn: () =>
      unwrap(api.GET('/api/gastos/modo-emergencia/', { params: { query: { mes, anio } } })),
  })
}
