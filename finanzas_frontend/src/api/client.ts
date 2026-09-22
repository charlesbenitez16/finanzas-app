import createClient, { type Middleware } from 'openapi-fetch'
import { isTokenExpiringSoon } from '@/lib/jwt'
import { useAuthStore } from '@/stores/auth-store'
import type { paths } from './schema'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

let refreshPromise: Promise<string | null> | null = null

async function refreshAccessToken(): Promise<string | null> {
  const { refreshToken } = useAuthStore.getState()
  if (!refreshToken) return null

  if (!refreshPromise) {
    refreshPromise = fetch(`${BASE_URL}/api/usuarios/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    })
      .then(async (res) => {
        if (!res.ok) return null
        const data = (await res.json()) as { access: string }
        useAuthStore.getState().setAccessToken(data.access)
        return data.access
      })
      .catch(() => null)
      .finally(() => {
        refreshPromise = null
      })
  }

  return refreshPromise
}

const authMiddleware: Middleware = {
  async onRequest({ request }) {
    const isAuthEndpoint = request.url.includes('/api/usuarios/')
    if (!isAuthEndpoint) {
      let { accessToken } = useAuthStore.getState()
      const { refreshToken } = useAuthStore.getState()
      if (refreshToken && (!accessToken || isTokenExpiringSoon(accessToken))) {
        accessToken = await refreshAccessToken()
      }
      if (accessToken) {
        request.headers.set('Authorization', `Bearer ${accessToken}`)
      }
    }
    return request
  },
  async onResponse({ request, response }) {
    const isAuthEndpoint = request.url.includes('/api/usuarios/')
    if (response.status === 401 && !isAuthEndpoint) {
      useAuthStore.getState().clearSession()
    }
    return response
  },
}

export const api = createClient<paths>({ baseUrl: BASE_URL })
api.use(authMiddleware)

/**
 * openapi-fetch responde `{ data, error }`; para los endpoints cuyo schema
 * no describe el body de error (ver README, "schemas de escritura") el tipo
 * de `error` no siempre permite que TS descarte `data: undefined` con un
 * simple `if`. Este helper centraliza ese chequeo para todos los hooks.
 */
export async function unwrap<T>(
  request: Promise<{ data?: T; error?: unknown }>,
): Promise<T> {
  const { data, error } = await request
  if (error !== undefined) throw error
  if (data === undefined) throw new Error('Respuesta vacía de la API')
  return data
}
