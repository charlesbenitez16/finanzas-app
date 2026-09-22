import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/stores/auth-store'

export function ProtectedRoute() {
  const usuario = useAuthStore((s) => s.usuario)

  if (!usuario) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}
