import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type PlanFinanciero = components['schemas']['PlanFinanciero']
export type PlanFinancieroInput = Omit<PlanFinanciero, 'id' | 'usuario_id' | 'activo'>

export function usePlanesFinancieros() {
  return useQuery({
    queryKey: ['planes-financieros'],
    queryFn: () => unwrap(api.GET('/api/planes-financieros/')),
  })
}

export function useCrearPlan() {
  const queryClient = useQueryClient()
  return useMutation({
    // Ver nota en features/catalogos/api.ts sobre el cast.
    mutationFn: (body: PlanFinancieroInput) =>
      unwrap(api.POST('/api/planes-financieros/', { body: body as PlanFinanciero })),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['planes-financieros'] })
    },
  })
}

export function useActivarPlan() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (planId: number) =>
      unwrap(
        api.POST('/api/planes-financieros/{plan_id}/activar/', {
          params: { path: { plan_id: planId } },
        }),
      ),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['planes-financieros'] })
      queryClient.invalidateQueries({ queryKey: ['planes-financieros', 'comparativa'] })
    },
  })
}

export function useComparativa(mes: number, anio: number) {
  return useQuery({
    queryKey: ['planes-financieros', 'comparativa', mes, anio],
    queryFn: () =>
      unwrap(
        api.GET('/api/planes-financieros/comparativa/', { params: { query: { mes, anio } } }),
      ),
    retry: false,
  })
}
