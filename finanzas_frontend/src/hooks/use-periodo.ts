import { useState } from 'react'

export function usePeriodo() {
  const now = new Date()
  const [mes, setMes] = useState(now.getMonth() + 1)
  const [anio, setAnio] = useState(now.getFullYear())
  return { mes, anio, setMes, setAnio }
}
