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
import { useCrearPlan } from './api'
import {
  planFinancieroSchema,
  type PlanFinancieroFormInput,
  type PlanFinancieroFormValues,
} from './schemas'

export function PlanFormDialog() {
  const [open, setOpen] = useState(false)
  const crearPlan = useCrearPlan()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<PlanFinancieroFormInput, unknown, PlanFinancieroFormValues>({
    resolver: zodResolver(planFinancieroSchema),
  })

  const onSubmit = (values: PlanFinancieroFormValues) => {
    crearPlan.mutate(
      {
        ...values,
        porcentaje_gasto_fijo: String(values.porcentaje_gasto_fijo),
        porcentaje_ahorro: String(values.porcentaje_ahorro),
        porcentaje_gasto_libre: String(values.porcentaje_gasto_libre),
      },
      {
        onSuccess: () => {
          toast.success('Plan creado (recordá activarlo)')
          reset()
          setOpen(false)
        },
        onError: () => toast.error('Los porcentajes deben sumar 100'),
      },
    )
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>Nuevo plan</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nuevo plan financiero</DialogTitle>
        </DialogHeader>
        <form className="flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="nombre">Nombre</Label>
            <Input id="nombre" {...register('nombre')} />
            {errors.nombre && <p className="text-xs text-destructive">{errors.nombre.message}</p>}
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="porcentaje_gasto_fijo">% gasto fijo</Label>
              <Input id="porcentaje_gasto_fijo" type="number" {...register('porcentaje_gasto_fijo')} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="porcentaje_ahorro">% ahorro</Label>
              <Input id="porcentaje_ahorro" type="number" {...register('porcentaje_ahorro')} />
            </div>
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="porcentaje_gasto_libre">% gasto libre</Label>
              <Input id="porcentaje_gasto_libre" type="number" {...register('porcentaje_gasto_libre')} />
            </div>
          </div>
          {errors.porcentaje_gasto_libre && (
            <p className="text-xs text-destructive">{errors.porcentaje_gasto_libre.message}</p>
          )}
          <DialogFooter>
            <Button type="submit" disabled={crearPlan.isPending}>
              {crearPlan.isPending ? 'Guardando…' : 'Guardar'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
