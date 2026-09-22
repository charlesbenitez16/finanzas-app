import { z } from 'zod'

export const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'La contraseña es requerida'),
})

export type LoginInput = z.infer<typeof loginSchema>

export const registroSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido').max(150),
  email: z.string().email('Email inválido').max(150),
  password: z.string().min(8, 'Mínimo 8 caracteres'),
})

export type RegistroInput = z.infer<typeof registroSchema>
