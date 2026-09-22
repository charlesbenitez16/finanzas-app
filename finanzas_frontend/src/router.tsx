import { createBrowserRouter } from 'react-router-dom'
import { AppShell } from '@/components/layout/AppShell'
import { ProtectedRoute } from '@/components/layout/ProtectedRoute'
import { LoginPage } from '@/features/auth/LoginPage'
import { RegisterPage } from '@/features/auth/RegisterPage'
import { AlertasPage } from '@/features/alertas/AlertasPage'
import { CatalogosPage } from '@/features/catalogos/CatalogosPage'
import { DashboardPage } from '@/features/dashboard/DashboardPage'
import { GastosPage } from '@/features/gastos/GastosPage'
import { IngresosPage } from '@/features/ingresos/IngresosPage'
import { PlanesFinancierosPage } from '@/features/planes-financieros/PlanesFinancierosPage'
import { ServiciosFijosPage } from '@/features/servicios-fijos/ServiciosFijosPage'

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  { path: '/registro', element: <RegisterPage /> },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppShell />,
        children: [
          { path: '/', element: <DashboardPage /> },
          { path: '/ingresos', element: <IngresosPage /> },
          { path: '/gastos', element: <GastosPage /> },
          { path: '/servicios-fijos', element: <ServiciosFijosPage /> },
          { path: '/planes-financieros', element: <PlanesFinancierosPage /> },
          { path: '/alertas', element: <AlertasPage /> },
          { path: '/catalogos', element: <CatalogosPage /> },
        ],
      },
    ],
  },
])
