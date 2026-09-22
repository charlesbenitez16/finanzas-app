import { z } from 'zod'

export const planFinancieroSchema = z
  .object({
    nombre: z.string().min(1, 'El nombre es requerido'),
    porcentaje_gasto_fijo: z.coerce.number().min(0).max(100),
    porcentaje_ahorro: z.coerce.number().min(0).max(100),
    porcentaje_gasto_libre: z.coerce.number().min(0).max(100),
  })
  .refine(
    (v) => v.porcentaje_gasto_fijo + v.porcentaje_ahorro + v.porcentaje_gasto_libre === 100,
    { message: 'Los tres porcentajes deben sumar 100', path: ['porcentaje_gasto_libre'] },
  )

export type PlanFinancieroFormInput = z.input<typeof planFinancieroSchema>
export type PlanFinancieroFormValues = z.output<typeof planFinancieroSchema>
