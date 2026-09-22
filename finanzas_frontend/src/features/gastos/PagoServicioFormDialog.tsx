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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useServiciosFijos } from '@/features/servicios-fijos/api'
import { usePagarServicio } from './api'
import {
  pagoServicioSchema,
  type PagoServicioFormInput,
  type PagoServicioFormValues,
} from './schemas'

interface PagoServicioFormDialogProps {
  mes: number
  anio: number
}

export function PagoServicioFormDialog({ mes, anio }: PagoServicioFormDialogProps) {
  const [open, setOpen] = useState(false)
  const servicios = useServiciosFijos()
  const pagarServicio = usePagarServicio()
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<PagoServicioFormInput, unknown, PagoServicioFormValues>({
    resolver: zodResolver(pagoServicioSchema),
    defaultValues: {
      fecha_gasto: new Date().toISOString().slice(0, 10),
      periodo_mes: mes,
      periodo_anio: anio,
    },
  })

  const onSubmit = (values: PagoServicioFormValues) => {
    pagarServicio.mutate(
      { ...values, monto: String(values.monto) },
      {
        onSuccess: () => {
          toast.success('Pago registrado')
          reset()
          setOpen(false)
        },
        onError: (error) => {
          const message =
            typeof error === 'object' && error && 'detail' in error
              ? String((error as { detail: unknown }).detail)
              : 'No se pudo registrar el pago (¿ya existe un pago de este servicio en el periodo?)'
          toast.error(message)
        },
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">Pagar servicio fijo</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Registrar pago de servicio fijo</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-col gap-1.5">
            <Label>Servicio fijo</Label>
            <Select
              value={String(watch('servicio_fijo_id') ?? '')}
              onValueChange={(v) => setValue('servicio_fijo_id', Number(v))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Elegí un servicio" />
              </SelectTrigger>
              <SelectContent>
                {servicios.data?.map((s) => (
                  <SelectItem key={s.id} value={String(s.id)}>
                    {s.nombre}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {errors.servicio_fijo_id && (
              <p className="text-xs text-destructive">{errors.servicio_fijo_id.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="monto">Monto</Label>
              <Input id="monto" type="number" step="0.01" {...register('monto')} />
              {errors.monto && <p className="text-xs text-destructive">{errors.monto.message}</p>}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="fecha_gasto">Fecha</Label>
              <Input id="fecha_gasto" type="date" {...register('fecha_gasto')} />
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
            <Label htmlFor="descripcion">Descripción (opcional)</Label>
            <Input id="descripcion" {...register('descripcion')} />
          </div>

          <DialogFooter>
            <Button type="submit" disabled={pagarServicio.isPending}>
              {pagarServicio.isPending ? 'Guardando…' : 'Guardar'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
