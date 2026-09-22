import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useCrearIngreso } from './api'
import { ingresoSchema, type IngresoFormInput, type IngresoFormValues } from './schemas'

interface IngresoFormDialogProps {
  mes: number
  anio: number
}

export function IngresoFormDialog({ mes, anio }: IngresoFormDialogProps) {
  const [open, setOpen] = useState(false)
  const crearIngreso = useCrearIngreso()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<IngresoFormInput, unknown, IngresoFormValues>({
    resolver: zodResolver(ingresoSchema),
    defaultValues: {
      fecha: new Date().toISOString().slice(0, 10),
      periodo_mes: mes,
      periodo_anio: anio,
    },
  })

  const onSubmit = (values: IngresoFormValues) => {
    crearIngreso.mutate(
      { ...values, monto: String(values.monto) },
      {
        onSuccess: () => {
          toast.success('Ingreso registrado')
          reset()
          setOpen(false)
        },
        onError: () => toast.error('No se pudo registrar el ingreso'),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Nuevo ingreso</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nuevo ingreso</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="monto">Monto</Label>
              <Input id="monto" type="number" step="0.01" {...register('monto')} />
              {errors.monto && <p className="text-xs text-destructive">{errors.monto.message}</p>}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="fecha">Fecha</Label>
              <Input id="fecha" type="date" {...register('fecha')} />
              {errors.fecha && <p className="text-xs text-destructive">{errors.fecha.message}</p>}
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="periodo_mes">Mes del periodo</Label>
              <Input id="periodo_mes" type="number" min={1} max={12} {...register('periodo_mes')} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="periodo_anio">Año del periodo</Label>
              <Input id="periodo_anio" type="number" {...register('periodo_anio')} />
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="fuente">Fuente (opcional)</Label>
            <Input id="fuente" {...register('fuente')} />
          </div>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="descripcion">Descripción (opcional)</Label>
            <Input id="descripcion" {...register('descripcion')} />
          </div>
          <DialogFooter>
            <Button type="submit" disabled={crearIngreso.isPending}>
              {crearIngreso.isPending ? 'Guardando…' : 'Guardar'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
