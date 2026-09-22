import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import type { components } from '@/api/schema'

type CategoriaGasto = components['schemas']['CategoriaGasto']
export type CategoriaGastoInput = Omit<CategoriaGasto, 'id' | 'usuario_id'>

export function useCategorias() {
  return useQuery({
    queryKey: ['catalogos', 'categorias'],
    queryFn: () => unwrap(api.GET('/api/catalogos/categorias/')),
  })
}

export function useCrearCategoria() {
  const queryClient = useQueryClient()
  return useMutation({
    // El backend reutiliza el mismo serializer de lectura/escritura, así que
    // el schema generado exige `id`/`usuario_id` (de solo servidor) en el
    // body. El cast documenta que efectivamente no los mandamos.
    mutationFn: (body: CategoriaGastoInput) =>
      unwrap(api.POST('/api/catalogos/categorias/', { body: body as CategoriaGasto })),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['catalogos', 'categorias'] })
    },
  })
}

export function useNivelesPrioridad() {
  return useQuery({
    queryKey: ['catalogos', 'niveles-prioridad'],
    queryFn: () => unwrap(api.GET('/api/catalogos/niveles-prioridad/')),
  })
}
