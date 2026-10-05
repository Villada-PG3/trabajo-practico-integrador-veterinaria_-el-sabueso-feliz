from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class SucursalesView(TemplateView):
    template_name = 'sucursales.html'

class SucursalView(TemplateView):
    template_name = 'sucursal.html'

class EmpleadosView(TemplateView):
    template_name = 'empleados.html'

class RazasView(TemplateView):
    template_name = 'razas.html'

class RazaView(TemplateView):
    template_name = 'raza.html'

class PacientesView(TemplateView):
    template_name = 'pacientes.html'

class PacienteView(TemplateView):
    template_name = 'paciente.html'

class ConsultasView(TemplateView):
    template_name = 'consultas.html'

class ConsultaView(TemplateView):
    template_name = 'consulta.html'

class VacunacionesView(TemplateView):
    template_name = 'vacunaciones.html'

class VacunacionView(TemplateView):
    template_name = 'vacunacion.html'

class MedicamentosView(TemplateView):
    template_name = 'medicamentos.html'

class ComprasView(TemplateView):
    template_name = 'compras.html'