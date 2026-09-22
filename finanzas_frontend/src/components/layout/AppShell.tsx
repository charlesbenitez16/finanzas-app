import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Wallet, LogOut } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/stores/auth-store'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/ingresos', label: 'Ingresos' },
  { to: '/gastos', label: 'Gastos' },
  { to: '/servicios-fijos', label: 'Servicios fijos' },
  { to: '/planes-financieros', label: 'Planes financieros' },
  { to: '/alertas', label: 'Alertas' },
  { to: '/catalogos', label: 'Catálogos' },
]

export function AppShell() {
  const usuario = useAuthStore((s) => s.usuario)
  const clearSession = useAuthStore((s) => s.clearSession)
  const navigate = useNavigate()

  const handleLogout = () => {
    clearSession()
    navigate('/login', { replace: true })
  }

  return (
    <div className="flex min-h-svh bg-muted/30">
      <aside className="flex w-64 shrink-0 flex-col gap-1 border-r border-border bg-card p-4 shadow-sm">
        <div className="flex items-center gap-2.5 px-2 pt-1 pb-5">
          <span className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
            <Wallet className="size-5" />
          </span>
          <p className="font-heading text-lg font-bold text-foreground">Finanzas</p>
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  'rounded-lg px-3 py-2.5 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground',
                  isActive && 'bg-primary/10 font-semibold text-primary hover:bg-primary/10 hover:text-primary',
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-border pt-3">
          <p className="truncate px-2 text-xs text-muted-foreground">{usuario?.email}</p>
          <Button
            variant="ghost"
            size="sm"
            className="mt-1 w-full justify-start gap-2 text-muted-foreground hover:text-destructive"
            onClick={handleLogout}
          >
            <LogOut className="size-4" />
            Cerrar sesión
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto p-8">
        <div className="mx-auto max-w-6xl">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
