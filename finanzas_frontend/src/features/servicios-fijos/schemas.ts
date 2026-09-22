import { z } from 'zod'

export const servicioFijoSchema = z.object({
  categoria_id: z.coerce.number().min(1, 'Elegí una categoría'),
  prioridad_id: z.coerce.number().min(1, 'Elegí una prioridad'),
  nombre: z.string().min(1, 'El nombre es requerido'),
  dia_vencimiento: z.coerce.number().min(1).max(31),
  monto_estimado: z.coerce.number().optional(),
  dias_anticipacion_alerta: z.coerce.number().optional(),
  notas: z.string().optional(),
})

export type ServicioFijoFormInput = z.input<typeof servicioFijoSchema>
export type ServicioFijoFormValues = z.output<typeof servicioFijoSchema>
