import { create } from 'zustand'
import type { components } from '@/api/schema'

type Usuario = components['schemas']['Usuario']

const REFRESH_KEY = 'finanzas.refreshToken'
const USUARIO_KEY = 'finanzas.usuario'

function readUsuario(): Usuario | null {
  try {
    const raw = localStorage.getItem(USUARIO_KEY)
    return raw ? (JSON.parse(raw) as Usuario) : null
  } catch {
    return null
  }
}

interface AuthState {
  usuario: Usuario | null
  accessToken: string | null
  refreshToken: string | null
  setSession: (data: { usuario: Usuario; access: string; refresh: string }) => void
  setAccessToken: (access: string) => void
  clearSession: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  usuario: readUsuario(),
  accessToken: null,
  refreshToken: localStorage.getItem(REFRESH_KEY),
  setSession: ({ usuario, access, refresh }) => {
    localStorage.setItem(REFRESH_KEY, refresh)
    localStorage.setItem(USUARIO_KEY, JSON.stringify(usuario))
    set({ usuario, accessToken: access, refreshToken: refresh })
  },
  setAccessToken: (access) => set({ accessToken: access }),
  clearSession: () => {
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USUARIO_KEY)
    set({ usuario: null, accessToken: null, refreshToken: null })
  },
}))
