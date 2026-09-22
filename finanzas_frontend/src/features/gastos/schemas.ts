import { z } from 'zod'

export const gastoSchema = z.object({
  categoria_id: z.coerce.number().min(1, 'Elegí una categoría'),
  prioridad_id: z.coerce.number().min(1, 'Elegí una prioridad'),
  monto: z.coerce.number().positive('El monto debe ser mayor a 0'),
  fecha_gasto: z.string().min(1, 'La fecha es requerida'),
  periodo_mes: z.coerce.number().min(1).max(12),
  periodo_anio: z.coerce.number().min(2000),
  descripcion: z.string().optional(),
})

export type GastoFormInput = z.input<typeof gastoSchema>
export type GastoFormValues = z.output<typeof gastoSchema>

export const pagoServicioSchema = z.object({
  servicio_fijo_id: z.coerce.number().min(1, 'Elegí un servicio'),
  monto: z.coerce.number().positive('El monto debe ser mayor a 0'),
  fecha_gasto: z.string().min(1, 'La fecha es requerida'),
  periodo_mes: z.coerce.number().min(1).max(12),
  periodo_anio: z.coerce.number().min(2000),
  descripcion: z.string().optional(),
})

export type PagoServicioFormInput = z.input<typeof pagoServicioSchema>
export type PagoServicioFormValues = z.output<typeof pagoServicioSchema>
