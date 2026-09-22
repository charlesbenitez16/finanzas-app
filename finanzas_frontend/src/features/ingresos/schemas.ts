import { z } from 'zod'

export const ingresoSchema = z.object({
  monto: z.coerce.number().positive('El monto debe ser mayor a 0'),
  fecha: z.string().min(1, 'La fecha es requerida'),
  periodo_mes: z.coerce.number().min(1).max(12),
  periodo_anio: z.coerce.number().min(2000),
  fuente: z.string().optional(),
  descripcion: z.string().optional(),
})

export type IngresoFormInput = z.input<typeof ingresoSchema>
export type IngresoFormValues = z.output<typeof ingresoSchema>
