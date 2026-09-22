import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { UserPlus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useRegistro } from './api'
import { registroSchema, type RegistroInput } from './schemas'

export function RegisterPage() {
  const navigate = useNavigate()
  const registro = useRegistro()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegistroInput>({ resolver: zodResolver(registroSchema) })

  const onSubmit = (values: RegistroInput) => {
    registro.mutate(values, {
      onSuccess: () => navigate('/', { replace: true }),
      onError: () => toast.error('No se pudo registrar. ¿El email ya está en uso?'),
    })
  }

  return (
    <div className="flex min-h-svh items-center justify-center bg-[linear-gradient(135deg,#667eea_0%,#764ba2_100%)] p-4">
      <Card className="w-full max-w-md border-0 shadow-xl [--card-spacing:--spacing(8)]">
        <CardHeader>
          <div className="flex flex-col items-center gap-3 pb-2 text-center">
            <span className="flex size-14 items-center justify-center rounded-2xl bg-primary text-primary-foreground shadow-sm">
              <UserPlus className="size-7" />
            </span>
            <div className="flex flex-col gap-1.5">
              <CardTitle className="text-2xl font-bold">Crear cuenta</CardTitle>
              <CardDescription>Registrate para empezar a usar Finanzas</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="nombre">Nombre</Label>
              <Input id="nombre" autoComplete="name" {...register('nombre')} />
              {errors.nombre && (
                <p className="text-xs text-destructive">{errors.nombre.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" autoComplete="email" {...register('email')} />
              {errors.email && (
                <p className="text-xs text-destructive">{errors.email.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="password">Contraseña</Label>
              <Input
                id="password"
                type="password"
                autoComplete="new-password"
                {...register('password')}
              />
              {errors.password && (
                <p className="text-xs text-destructive">{errors.password.message}</p>
              )}
            </div>
            <Button type="submit" disabled={registro.isPending} className="mt-2 w-full">
              {registro.isPending ? 'Creando cuenta…' : 'Crear cuenta'}
            </Button>
          </form>
          <p className="mt-6 text-center text-sm text-muted-foreground">
            ¿Ya tenés cuenta?{' '}
            <Link to="/login" className="font-semibold text-primary underline-offset-4 hover:underline">
              Iniciá sesión
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
