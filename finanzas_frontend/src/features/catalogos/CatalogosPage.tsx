import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { toast } from 'sonner'
import { z } from 'zod'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { useCategorias, useCrearCategoria, useNivelesPrioridad } from './api'

const categoriaSchema = z.object({
  nombre: z.string().min(1, 'El nombre es requerido'),
  icono: z.string().optional(),
})
type CategoriaFormValues = z.infer<typeof categoriaSchema>

export function CatalogosPage() {
  const categorias = useCategorias()
  const niveles = useNivelesPrioridad()
  const crearCategoria = useCrearCategoria()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CategoriaFormValues>({ resolver: zodResolver(categoriaSchema) })

  const onSubmit = (values: CategoriaFormValues) => {
    crearCategoria.mutate(values, {
      onSuccess: () => {
        toast.success('Categoría creada')
        reset()
      },
      onError: () => toast.error('Ya existe una categoría con ese nombre'),
    })
  }

  return (
    <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Categorías de gasto</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <form className="flex items-start gap-2" onSubmit={handleSubmit(onSubmit)}>
            <div className="flex-1">
              <Input placeholder="Nombre de la categoría" {...register('nombre')} />
              {errors.nombre && (
                <p className="mt-1 text-xs text-destructive">{errors.nombre.message}</p>
              )}
            </div>
            <Input className="w-20" placeholder="Ícono" {...register('icono')} />
            <Button type="submit" disabled={crearCategoria.isPending}>
              Agregar
            </Button>
          </form>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nombre</TableHead>
                <TableHead>Ícono</TableHead>
                <TableHead>Origen</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {categorias.data?.map((c) => (
                <TableRow key={c.id}>
                  <TableCell>{c.nombre}</TableCell>
                  <TableCell>{c.icono ?? '—'}</TableCell>
                  <TableCell>
                    <Badge variant={c.usuario_id ? 'secondary' : 'outline'}>
                      {c.usuario_id ? 'Propia' : 'Global'}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Niveles de prioridad</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Orden</TableHead>
                <TableHead>Nombre</TableHead>
                <TableHead>Descripción</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {niveles.data?.map((n) => (
                <TableRow key={n.id}>
                  <TableCell>{n.nivel_orden}</TableCell>
                  <TableCell>
                    <span className="inline-flex items-center gap-2">
                      {n.color && (
                        <span
                          className="size-2.5 rounded-full"
                          style={{ backgroundColor: n.color }}
                        />
                      )}
                      {n.nombre}
                    </span>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{n.descripcion ?? '—'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
