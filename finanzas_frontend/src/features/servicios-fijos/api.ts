import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type ServicioFijo = components['schemas']['ServicioFijo']
export type ServicioFijoInput = Omit<ServicioFijo, 'id' | 'usuario_id' | 'activo'>

export function useServiciosFijos() {
  return useQuery({
    queryKey: ['servicios-fijos'],
    queryFn: () => unwrap(api.GET('/api/servicios-fijos/')),
  })
}

export function useCrearServicioFijo() {
  const queryClient = useQueryClient()
  return useMutation({
    // Ver nota en features/catalogos/api.ts sobre el cast.
    mutationFn: (body: ServicioFijoInput) =>
      unwrap(api.POST('/api/servicios-fijos/', { body: body as ServicioFijo })),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['servicios-fijos'] })
    },
  })
}

export function useProximosAVencer(fecha?: string) {
  return useQuery({
    queryKey: ['servicios-fijos', 'proximos-a-vencer', fecha],
    queryFn: () =>
      unwrap(
        api.GET('/api/servicios-fijos/proximos-a-vencer/', {
          params: { query: fecha ? { fecha } : {} },
        }),
      ),
  })
}
