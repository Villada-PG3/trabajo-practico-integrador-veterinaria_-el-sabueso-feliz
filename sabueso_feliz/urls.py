from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'sabueso_feliz'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    path('sucursales/', views.SucursalesView.as_view(), name='sucursales'),
    path('sucursales/nueva/', views.SucursalCreateView.as_view(), name='sucursal_crear'),
    path('sucursales/<int:pk>/', views.SucursalView.as_view(), name='sucursal'),
    path('sucursales/<int:pk>/editar/', views.SucursalUpdateView.as_view(), name='sucursal_editar'),
    path('sucursales/<int:pk>/eliminar/', views.SucursalDeleteView.as_view(), name='sucursal_eliminar'),

    # Empleados
    path('empleados/', views.EmpleadosView.as_view(), name='empleados'),
    path('empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_crear'),
    path('empleados/nuevo-veterinario/', views.VeterinarioCreateView.as_view(), name='veterinario_crear'),
    path('empleados/nuevo-estudiante/', views.EstudianteCreateView.as_view(), name='estudiante_crear'),
    path('empleados/<int:pk>/', views.EmpleadoView.as_view(), name='empleado'),
    path('empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_editar'),
    path('empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado_eliminar'),

    # Razas
    path('razas/', views.RazasView.as_view(), name='razas'),
    path('razas/nueva/', views.RazaCreateView.as_view(), name='raza_crear'),
    path('razas/<int:pk>/', views.RazaView.as_view(), name='raza'),
    path('razas/<int:pk>/editar/', views.RazaUpdateView.as_view(), name='raza_editar'),
    path('razas/<int:pk>/eliminar/', views.RazaDeleteView.as_view(), name='raza_eliminar'),

    # Dueños
    path('duenios/', views.DueniosView.as_view(), name='duenios'),
    path('duenios/nuevo/', views.DuenioCreateView.as_view(), name='duenio_crear'),
    path('duenios/<int:pk>/', views.DuenioView.as_view(), name='duenio'),
    path('duenios/<int:pk>/editar/', views.DuenioUpdateView.as_view(), name='duenio_editar'),
    path('duenios/<int:pk>/eliminar/', views.DuenioDeleteView.as_view(), name='duenio_eliminar'),

    # Pacientes
    path('pacientes/', views.PacientesView.as_view(), name='pacientes'),
    path('pacientes/nuevo/', views.PacienteCreateView.as_view(), name='paciente_crear'),
    path('pacientes/<int:pk>/', views.PacienteView.as_view(), name='paciente'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_editar'),
    path('pacientes/<int:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='paciente_eliminar'),

    # Consultas
    path('consultas/', views.ConsultasView.as_view(), name='consultas'),
    path('consultas/nueva/', views.ConsultaCreateView.as_view(), name='consulta_crear'),
    path('consultas/<int:pk>/', views.ConsultaView.as_view(), name='consulta'),
    path('consultas/<int:pk>/editar/', views.ConsultaUpdateView.as_view(), name='consulta_editar'),
    path('consultas/<int:pk>/eliminar/', views.ConsultaDeleteView.as_view(), name='consulta_eliminar'),

    # Vacunaciones
    path('vacunaciones/', views.VacunacionesView.as_view(), name='vacunaciones'),
    path('vacunaciones/nueva/', views.VacunacionCreateView.as_view(), name='vacunacion_crear'),
    path('vacunaciones/<int:pk>/', views.VacunacionView.as_view(), name='vacunacion'),
    path('vacunaciones/<int:pk>/editar/', views.VacunacionUpdateView.as_view(), name='vacunacion_editar'),
    path('vacunaciones/<int:pk>/eliminar/', views.VacunacionDeleteView.as_view(), name='vacunacion_eliminar'),

    # Medicamentos
    path('medicamentos/', views.MedicamentosView.as_view(), name='medicamentos'),
    path('medicamentos/nuevo/', views.MedicamentoCreateView.as_view(), name='medicamento_crear'),
    path('medicamentos/<int:pk>/editar/', views.MedicamentoUpdateView.as_view(), name='medicamento_editar'),
    path('medicamentos/<int:pk>/eliminar/', views.MedicamentoDeleteView.as_view(), name='medicamento_eliminar'),

    # Compras (stock)
    path('compras/', views.ComprasView.as_view(), name='compras'),
    path('compras/nueva/', views.CompraCreateView.as_view(), name='compra_crear'),
    path('compras/<int:pk>/editar/', views.CompraUpdateView.as_view(), name='compra_editar'),
    path('compras/<int:pk>/eliminar/', views.CompraDeleteView.as_view(), name='compra_eliminar'),
]