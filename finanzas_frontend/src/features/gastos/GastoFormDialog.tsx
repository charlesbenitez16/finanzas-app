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
import { useCrearGasto } from './api'
import { gastoSchema, type GastoFormInput, type GastoFormValues } from './schemas'

interface GastoFormDialogProps {
  mes: number
  anio: number
}

export function GastoFormDialog({ mes, anio }: GastoFormDialogProps) {
  const [open, setOpen] = useState(false)
  const categorias = useCategorias()
  const niveles = useNivelesPrioridad()
  const crearGasto = useCrearGasto()
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    watch,
    formState: { errors },
  } = useForm<GastoFormInput, unknown, GastoFormValues>({
    resolver: zodResolver(gastoSchema),
    defaultValues: {
      fecha_gasto: new Date().toISOString().slice(0, 10),
      periodo_mes: mes,
      periodo_anio: anio,
    },
  })

  const onSubmit = (values: GastoFormValues) => {
    crearGasto.mutate(
      { ...values, monto: String(values.monto), estado: 'Pagado' },
      {
        onSuccess: () => {
          toast.success('Gasto registrado')
          reset()
          setOpen(false)
        },
        onError: () => toast.error('No se pudo registrar el gasto'),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Nuevo gasto</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nuevo gasto puntual</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
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
            <Button type="submit" disabled={crearGasto.isPending}>
              {crearGasto.isPending ? 'Guardando…' : 'Guardar'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
