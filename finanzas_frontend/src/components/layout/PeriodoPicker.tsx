import { MESES } from '@/lib/format'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Input } from '@/components/ui/input'

interface PeriodoPickerProps {
  mes: number
  anio: number
  onMesChange: (mes: number) => void
  onAnioChange: (anio: number) => void
}

export function PeriodoPicker({ mes, anio, onMesChange, onAnioChange }: PeriodoPickerProps) {
  return (
    <div className="flex items-center gap-2">
      <Select value={String(mes)} onValueChange={(v) => onMesChange(Number(v))}>
        <SelectTrigger className="w-40">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {MESES.map((nombre, i) => (
            <SelectItem key={nombre} value={String(i + 1)}>
              {nombre}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <Input
        type="number"
        className="w-24"
        value={anio}
        onChange={(e) => onAnioChange(Number(e.target.value))}
      />
    </div>
  )
}
