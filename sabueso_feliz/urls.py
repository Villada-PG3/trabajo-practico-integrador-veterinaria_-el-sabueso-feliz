from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = 'sabueso_feliz'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('login/', LoginView.as_view(
        template_name='login.html'
    ), name='login'),

    path('sucursales/', views.SucursalesView.as_view(), name='sucursales'),
    path('sucursales/<int:pk>/', views.SucursalView.as_view(), name='sucursal'),

    path('empleados/', views.EmpleadosView.as_view(), name='empleados'),

    path('razas/', views.RazasView.as_view(), name='razas'),
    path('razas/<int:pk>/', views.RazaView.as_view(), name='raza'),

    path('pacientes/', views.PacientesView.as_view(), name='pacientes'),
    path('pacientes/<int:pk>/', views.PacienteView.as_view(), name='paciente'),

    path('consultas/', views.ConsultasView.as_view(), name='consultas'),
    path('consultas/<int:pk>/', views.ConsultaView.as_view(), name='consulta'),

    path('vacunaciones/', views.VacunacionesView.as_view(), name='vacunaciones'),
    path('vacunaciones/<int:pk>/', views.VacunacionView.as_view(), name='vacunacion'),

    path('medicamentos/', views.MedicamentosView.as_view(), name='medicamentos'),

    path('compras/', views.ComprasView.as_view(), name='compras'),
]