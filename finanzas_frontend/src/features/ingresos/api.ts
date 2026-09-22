import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type Ingreso = components['schemas']['Ingreso']
export type IngresoInput = Omit<Ingreso, 'id' | 'usuario_id'>

export function useIngresos(mes: number, anio: number) {
  return useQuery({
    queryKey: ['ingresos', mes, anio],
    queryFn: () => unwrap(api.GET('/api/ingresos/', { params: { query: { mes, anio } } })),
  })
}

export function useCrearIngreso() {
  const queryClient = useQueryClient()
  return useMutation({
    // Ver nota en features/catalogos/api.ts sobre el cast: el schema de
    // escritura reutiliza el de lectura y exige campos de solo servidor.
    mutationFn: (body: IngresoInput) =>
      unwrap(api.POST('/api/ingresos/', { body: body as Ingreso })),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ingresos'] })
      queryClient.invalidateQueries({ queryKey: ['gastos', 'balance-mensual'] })
    },
  })
}

export function useTotalIngresosPeriodo(mes: number, anio: number) {
  return useQuery({
    queryKey: ['ingresos', 'total-periodo', mes, anio],
    queryFn: () =>
      unwrap(api.GET('/api/ingresos/total-periodo/', { params: { query: { mes, anio } } })),
  })
}
