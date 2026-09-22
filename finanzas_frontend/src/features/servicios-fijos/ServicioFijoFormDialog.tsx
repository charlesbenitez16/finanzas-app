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
import { useCategorias, useNivelesPrioridad } from '@/features/catalogos/api'
import { useCrearServicioFijo } from './api'
import {
  servicioFijoSchema,
  type ServicioFijoFormInput,
  type ServicioFijoFormValues,
} from './schemas'

export function ServicioFijoFormDialog() {
  const [open, setOpen] = useState(false)
  const categorias = useCategorias()
  const niveles = useNivelesPrioridad()
  const crearServicio = useCrearServicioFijo()
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<ServicioFijoFormInput, unknown, ServicioFijoFormValues>({
    resolver: zodResolver(servicioFijoSchema),
  })

  const onSubmit = (values: ServicioFijoFormValues) => {
    crearServicio.mutate(
      {
        ...values,
        monto_estimado: values.monto_estimado ? String(values.monto_estimado) : undefined,
        dias_anticipacion_alerta: values.dias_anticipacion_alerta ?? 3,
        es_monto_variable: false,
      },
      {
        onSuccess: () => {
          toast.success('Servicio fijo creado')
          reset()
          setOpen(false)
        },
        onError: () => toast.error('No se pudo crear el servicio fijo'),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Nuevo servicio fijo</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nuevo servicio fijo</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="nombre">Nombre</Label>
            <Input id="nombre" {...register('nombre')} />
            {errors.nombre && <p className="text-xs text-destructive">{errors.nombre.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label>Categoría</Label>
              <Select value={String(watch('categoria_id') ?? '')} onValueChange={(v) => setValue('categoria_id', Number(v))}>
                <SelectTrigger>
                  <SelectValue placeholder="Elegí una categoría" />
                </SelectTrigger>
                <SelectContent>
                  {categorias.data?.map((c) => (
                    <SelectItem key={c.id} value={String(c.id)}>
                      {c.nombre}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.categoria_id && (
                <p className="text-xs text-destructive">{errors.categoria_id.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label>Prioridad</Label>
              <Select value={String(watch('prioridad_id') ?? '')} onValueChange={(v) => setValue('prioridad_id', Number(v))}>
                <SelectTrigger>
                  <SelectValue placeholder="Elegí una prioridad" />
                </SelectTrigger>
                <SelectContent>
                  {niveles.data?.map((n) => (
                    <SelectItem key={n.id} value={String(n.id)}>
                      {n.nombre}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {errors.prioridad_id && (
                <p className="text-xs text-destructive">{errors.prioridad_id.message}</p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="dia_vencimiento">Día de vencimiento</Label>
              <Input id="dia_vencimiento" type="number" min={1} max={31} {...register('dia_vencimiento')} />
              {errors.dia_vencimiento && (
                <p className="text-xs text-destructive">{errors.dia_vencimiento.message}</p>
              )}
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="monto_estimado">Monto estimado</Label>
              <Input id="monto_estimado" type="number" step="0.01" {...register('monto_estimado')} />
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="dias_anticipacion_alerta">Días de anticipación de alerta</Label>
            <Input
              id="dias_anticipacion_alerta"
              type="number"
              placeholder="3"
              {...register('dias_anticipacion_alerta')}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="notas">Notas (opcional)</Label>
            <Input id="notas" {...register('notas')} />
          </div>

          <DialogFooter>
            <Button type="submit" disabled={crearServicio.isPending}>
              {crearServicio.isPending ? 'Guardando…' : 'Guardar'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
