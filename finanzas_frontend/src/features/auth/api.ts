import { useMutation } from '@tanstack/react-query'
import { api, unwrap } from '@/api/client'
import { useAuthStore } from '@/stores/auth-store'

export function useLogin() {
  const setSession = useAuthStore((s) => s.setSession)
  return useMutation({
    mutationFn: (body: { email: string; password: string }) =>
      unwrap(api.POST('/api/usuarios/login/', { body })),
    onSuccess: (data) => setSession(data),
  })
}

export function useRegistro() {
  const setSession = useAuthStore((s) => s.setSession)
  return useMutation({
    mutationFn: (body: { nombre: string; email: string; password: string }) =>
      unwrap(api.POST('/api/usuarios/registro/', { body })),
    onSuccess: (data) => setSession(data),
  })
}
