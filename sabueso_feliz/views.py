from django.db.models import Count, F
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import (
    Sucursal,
    Empleado,
    Veterinario,
    Estudiantes,
    Raza,
    Duenio,
    Perro,
    Consulta,
    CalendarioVacuna,
    Medicamento,
    StockMedicamento,
)
from .forms import SucursalForm


# ------------------------------------------------------------ HOME

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        context['total_sucursales'] = Sucursal.objects.count()
        context['total_empleados'] = Empleado.objects.count()
        context['total_pacientes'] = Perro.objects.count()
        context['total_consultas'] = Consulta.objects.count()

        # Pacientes por sucursal
        context['sucursales'] = Sucursal.objects.annotate(
            total=Count('perro')
        )

        # Perros internados actualmente
        context['internados'] = Consulta.objects.filter(
            internado=True,
            fechaSalida__isnull=True,
        )

        # Últimas 5 consultas
        context['ultimas_consultas'] = (
            Consulta.objects.order_by('-fechaEntrada')[:5]
        )

        # Vacunas pendientes
        context['vacunas_proximas'] = (
            CalendarioVacuna.objects.filter(
                fechaAplicacion__isnull=True,
                fechaProgramada__gte=hoy,
            )
            .order_by('fechaProgramada')[:5]
        )

        context['vacunas_atrasadas'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=True,
            fechaProgramada__lt=hoy,
        )

        # Medicamentos con stock por debajo del mínimo
        context['stock_bajo'] = StockMedicamento.objects.filter(
            cantidadExistente__lt=F('cantidadMinima')
        )

        return context


class SucursalCreateView(CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalUpdateView(UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


# ------------------------------------------------------------ SUCURSAL

class SucursalesView(ListView):
    model = Sucursal
    template_name = 'sucursales.html'


class SucursalView(DetailView):
    model = Sucursal
    template_name = 'sucursal.html'


class SucursalCreateView(CreateView):
    model = Sucursal
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalUpdateView(UpdateView):
    model = Sucursal
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalDeleteView(DeleteView):
    model = Sucursal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


# ------------------------------------------------------------ EMPLEADO

class EmpleadosView(ListView):
    model = Empleado
    template_name = 'empleados.html'


class EmpleadoView(DetailView):
    model = Empleado
    template_name = 'empleado.html'


class EmpleadoCreateView(CreateView):
    model = Empleado
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


# Alta de veterinarios y estudiantes con sus campos adicionales

class VeterinarioCreateView(CreateView):
    model = Veterinario
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


class EstudianteCreateView(CreateView):
    model = Estudiantes
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


# ------------------------------------------------------------ RAZA

class RazasView(ListView):
    model = Raza
    template_name = 'razas.html'


class RazaView(DetailView):
    model = Raza
    template_name = 'raza.html'


class RazaCreateView(CreateView):
    model = Raza
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')


class RazaUpdateView(UpdateView):
    model = Raza
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')


class RazaDeleteView(DeleteView):
    model = Raza
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:razas')


# ------------------------------------------------------------ DUEÑO

class DueniosView(ListView):
    model = Duenio
    template_name = 'duenios.html'


class DuenioView(DetailView):
    model = Duenio
    template_name = 'duenio.html'


class DuenioCreateView(CreateView):
    model = Duenio
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioUpdateView(UpdateView):
    model = Duenio
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioDeleteView(DeleteView):
    model = Duenio
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')


# ------------------------------------------------------------ PACIENTE

class PacientesView(ListView):
    model = Perro
    template_name = 'pacientes.html'


class PacienteView(DetailView):
    model = Perro
    template_name = 'paciente.html'


class PacienteCreateView(CreateView):
    model = Perro
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')


class PacienteUpdateView(UpdateView):
    model = Perro
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')


class PacienteDeleteView(DeleteView):
    model = Perro
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')


# ------------------------------------------------------------ CONSULTA

class ConsultasView(ListView):
    model = Consulta
    template_name = 'consultas.html'


class ConsultaView(DetailView):
    model = Consulta
    template_name = 'consulta.html'


class ConsultaCreateView(CreateView):
    model = Consulta
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaUpdateView(UpdateView):
    model = Consulta
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')


# ------------------------------------------------------------ VACUNACIÓN

class VacunacionesView(ListView):
    model = CalendarioVacuna
    template_name = 'vacunaciones.html'


class VacunacionView(DetailView):
    model = CalendarioVacuna
    template_name = 'vacunacion.html'


class VacunacionCreateView(CreateView):
    model = CalendarioVacuna
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionUpdateView(UpdateView):
    model = CalendarioVacuna
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionDeleteView(DeleteView):
    model = CalendarioVacuna
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')


# ------------------------------------------------------------ MEDICAMENTO

class MedicamentosView(ListView):
    model = Medicamento
    template_name = 'medicamentos.html'


class MedicamentoCreateView(CreateView):
    model = Medicamento
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')


# ------------------------------------------------------------ COMPRAS (STOCK)

class ComprasView(ListView):
    model = StockMedicamento
    template_name = 'compras.html'


class CompraCreateView(CreateView):
    model = StockMedicamento
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')


class CompraUpdateView(UpdateView):
    model = StockMedicamento
    fields = '__all__'
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')


class CompraDeleteView(DeleteView):
    model = StockMedicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:compras')