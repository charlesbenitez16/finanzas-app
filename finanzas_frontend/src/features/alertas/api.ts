import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type EstadoAlerta = components['schemas']['AlertaPagoEstadoEnum']
type CambiarEstado = components['schemas']['CambiarEstadoAlertaEstadoEnum']

export function useAlertas(estado?: EstadoAlerta) {
  return useQuery({
    queryKey: ['alertas', estado],
    queryFn: () => unwrap(api.GET('/api/alertas/', { params: { query: estado ? { estado } : {} } })),
  })
}

export function useGenerarAlertas() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (fecha?: string) =>
      unwrap(api.POST('/api/alertas/generar/', { params: { query: fecha ? { fecha } : {} } })),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alertas'] })
    },
  })
}

export function useCambiarEstadoAlerta() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ alertaId, estado }: { alertaId: number; estado: CambiarEstado }) =>
      unwrap(
        api.PATCH('/api/alertas/{alerta_id}/', {
          params: { path: { alerta_id: alertaId } },
          body: { estado },
        }),
      ),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alertas'] })
    },
  })
}
