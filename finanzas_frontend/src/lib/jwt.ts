function getTokenExpiryMs(token: string): number | null {
  try {
    const payload = token.split('.')[1]
    const json = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
    const { exp } = JSON.parse(json) as { exp?: number }
    return typeof exp === 'number' ? exp * 1000 : null
  } catch {
    return null
  }
}

export function isTokenExpiringSoon(token: string, thresholdMs = 10_000): boolean {
  const expiry = getTokenExpiryMs(token)
  if (expiry === null) return false
  return Date.now() + thresholdMs >= expiry
}
