from django.contrib import messages
from django.db.models import Count, F, Q
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
from .forms import (
    SucursalForm,
    EmpleadoForm,
    VeterinarioForm,
    EstudianteForm,
    RazaForm,
    DuenioForm,
    PacienteForm,
    ConsultaForm,
    VacunacionForm,
    MedicamentoForm,
    StockForm,
)


class FormularioVistaMixin:
    titulo = ''
    volver_url = None
    mensaje_exito = 'Los datos se guardaron correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['volver_url'] = self.volver_url
        return context

    def form_valid(self, form):
        messages.success(self.request, self.mensaje_exito)
        return super().form_valid(form)


class EliminarVistaMixin:
    titulo = 'Eliminar registro'
    volver_url = None
    mensaje_exito = 'El registro se eliminó correctamente.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = self.titulo
        context['volver_url'] = self.volver_url
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.mensaje_exito)
        return super().delete(request, *args, **kwargs)


# ------------------------------------------------------------ HOME

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        context['total_sucursales'] = Sucursal.objects.count()
        context['total_empleados'] = Empleado.objects.count()
        context['total_pacientes'] = Perro.objects.count()
        context['consultas_hoy'] = Consulta.objects.filter(fechaEntrada=hoy).count()
        context['internados'] = Consulta.objects.filter(
            internado=True,
            fechaSalida__isnull=True,
        ).select_related('perro_id')

        context['sucursales'] = Sucursal.objects.annotate(total=Count('perro'))

        context['ultimas_consultas'] = (
            Consulta.objects.select_related('perro_id', 'empleado_id')
            .order_by('-fechaEntrada')[:5]
        )

        context['vacunas_proximas'] = (
            CalendarioVacuna.objects.filter(
                fechaAplicacion__isnull=True,
                fechaProgramada__gte=hoy,
            )
            .select_related('perro_id', 'vacuna_id')
            .order_by('fechaProgramada')[:5]
        )
        context['total_vacunas_proximas'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=True,
            fechaProgramada__gte=hoy,
        ).count()

        context['vacunas_atrasadas'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=True,
            fechaProgramada__lt=hoy,
        ).select_related('perro_id', 'vacuna_id')

        context['stock_bajo'] = StockMedicamento.objects.filter(
            cantidadExistente__lt=F('cantidadMinima')
        ).select_related('medicamento_id')

        return context


# ------------------------------------------------------------ SUCURSAL

class SucursalesView(ListView):
    model = Sucursal
    template_name = 'sucursales.html'
    queryset = Sucursal.objects.select_related('supervisor', 'supervisor_suplente')


class SucursalView(DetailView):
    model = Sucursal
    template_name = 'sucursal.html'
    context_object_name = 'sucursal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleados'] = self.object.empleado_set.all()
        context['pacientes'] = self.object.perro_set.select_related('raza', 'duenio')
        return context


class SucursalCreateView(FormularioVistaMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    titulo = 'Nueva sucursal'
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalUpdateView(FormularioVistaMixin, UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    titulo = 'Editar sucursal'
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalDeleteView(EliminarVistaMixin, DeleteView):
    model = Sucursal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


# ------------------------------------------------------------ EMPLEADO

class EmpleadosView(ListView):
    model = Empleado
    template_name = 'empleados.html'
    queryset = Empleado.objects.select_related('sucursal')


class EmpleadoView(DetailView):
    model = Empleado
    template_name = 'empleado.html'
    context_object_name = 'empleado'


class EmpleadoCreateView(FormularioVistaMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Nuevo empleado'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoUpdateView(FormularioVistaMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Editar empleado'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoDeleteView(EliminarVistaMixin, DeleteView):
    model = Empleado
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class VeterinarioCreateView(FormularioVistaMixin, CreateView):
    model = Veterinario
    form_class = VeterinarioForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Nuevo veterinario'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class EstudianteCreateView(FormularioVistaMixin, CreateView):
    model = Estudiantes
    form_class = EstudianteForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Nuevo estudiante'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


# ------------------------------------------------------------ RAZA

class RazasView(ListView):
    model = Raza
    template_name = 'razas.html'


class RazaView(DetailView):
    model = Raza
    template_name = 'raza.html'
    context_object_name = 'raza'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.object.perro_set.select_related('duenio', 'sucursal')
        return context


class RazaCreateView(FormularioVistaMixin, CreateView):
    model = Raza
    form_class = RazaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    titulo = 'Nueva raza'
    volver_url = reverse_lazy('sabueso_feliz:razas')


class RazaUpdateView(FormularioVistaMixin, UpdateView):
    model = Raza
    form_class = RazaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    titulo = 'Editar raza'
    volver_url = reverse_lazy('sabueso_feliz:razas')


class RazaDeleteView(EliminarVistaMixin, DeleteView):
    model = Raza
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    volver_url = reverse_lazy('sabueso_feliz:razas')


# ------------------------------------------------------------ DUEÑO

class DueniosView(ListView):
    model = Duenio
    template_name = 'duenios.html'


class DuenioView(DetailView):
    model = Duenio
    template_name = 'duenio.html'
    context_object_name = 'duenio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.object.perro_set.select_related('raza', 'sucursal')
        return context


class DuenioCreateView(FormularioVistaMixin, CreateView):
    model = Duenio
    form_class = DuenioForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    titulo = 'Nuevo propietario'
    volver_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioUpdateView(FormularioVistaMixin, UpdateView):
    model = Duenio
    form_class = DuenioForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    titulo = 'Editar propietario'
    volver_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioDeleteView(EliminarVistaMixin, DeleteView):
    model = Duenio
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    volver_url = reverse_lazy('sabueso_feliz:duenios')


# ------------------------------------------------------------ PACIENTE

class PacientesView(ListView):
    model = Perro
    template_name = 'pacientes.html'

    def get_queryset(self):
        qs = Perro.objects.select_related('raza', 'duenio', 'sucursal')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(nroHistoriaClinica__icontains=q)
                | Q(duenio__nombre__icontains=q)
                | Q(duenio__apellido__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class PacienteView(DetailView):
    model = Perro
    template_name = 'paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultas'] = self.object.consulta_set.select_related('empleado_id')
        context['vacunaciones'] = self.object.calendariovacuna_set.select_related(
            'vacuna_id', 'empleado_id'
        )
        return context


class PacienteCreateView(FormularioVistaMixin, CreateView):
    model = Perro
    form_class = PacienteForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    titulo = 'Registrar perro'
    volver_url = reverse_lazy('sabueso_feliz:pacientes')


class PacienteUpdateView(FormularioVistaMixin, UpdateView):
    model = Perro
    form_class = PacienteForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    titulo = 'Editar paciente'
    volver_url = reverse_lazy('sabueso_feliz:pacientes')


class PacienteDeleteView(EliminarVistaMixin, DeleteView):
    model = Perro
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    volver_url = reverse_lazy('sabueso_feliz:pacientes')


# ------------------------------------------------------------ CONSULTA

class ConsultasView(ListView):
    model = Consulta
    template_name = 'consultas.html'

    def get_queryset(self):
        qs = Consulta.objects.select_related('perro_id', 'empleado_id').order_by('-fechaEntrada')
        if self.request.GET.get('internados'):
            qs = qs.filter(internado=True, fechaSalida__isnull=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solo_internados'] = bool(self.request.GET.get('internados'))
        return context


class ConsultaView(DetailView):
    model = Consulta
    template_name = 'consulta.html'
    context_object_name = 'consulta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sintomas'] = self.object.consultasintoma_set.select_related('sintoma_id')
        context['recetas'] = self.object.recetamedicamento_set.select_related('medicamento_id')
        return context


class ConsultaCreateView(FormularioVistaMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    titulo = 'Nueva consulta'
    volver_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaUpdateView(FormularioVistaMixin, UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    titulo = 'Editar consulta'
    volver_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaDeleteView(EliminarVistaMixin, DeleteView):
    model = Consulta
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    volver_url = reverse_lazy('sabueso_feliz:consultas')


# ------------------------------------------------------------ VACUNACIÓN

class VacunacionesView(ListView):
    model = CalendarioVacuna
    template_name = 'vacunaciones.html'

    def get_queryset(self):
        return (
            CalendarioVacuna.objects
            .select_related('perro_id', 'vacuna_id', 'empleado_id')
            .order_by('fechaProgramada')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hoy'] = timezone.localdate()
        return context


class VacunacionView(DetailView):
    model = CalendarioVacuna
    template_name = 'vacunacion.html'
    context_object_name = 'vacunacion'


class VacunacionCreateView(FormularioVistaMixin, CreateView):
    model = CalendarioVacuna
    form_class = VacunacionForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    titulo = 'Nueva vacunación'
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionUpdateView(FormularioVistaMixin, UpdateView):
    model = CalendarioVacuna
    form_class = VacunacionForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    titulo = 'Editar vacunación'
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionDeleteView(EliminarVistaMixin, DeleteView):
    model = CalendarioVacuna
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


# ------------------------------------------------------------ MEDICAMENTO

class MedicamentosView(ListView):
    model = Medicamento
    template_name = 'medicamentos.html'


class MedicamentoCreateView(FormularioVistaMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    titulo = 'Nuevo medicamento'
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoUpdateView(FormularioVistaMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    titulo = 'Editar medicamento'
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoDeleteView(EliminarVistaMixin, DeleteView):
    model = Medicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


# ------------------------------------------------------------ COMPRAS (STOCK)

class ComprasView(ListView):
    model = StockMedicamento
    template_name = 'compras.html'

    def get_queryset(self):
        qs = StockMedicamento.objects.select_related('medicamento_id')
        if self.request.GET.get('alerta'):
            qs = qs.filter(cantidadExistente__lt=F('cantidadMinima'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solo_alertas'] = bool(self.request.GET.get('alerta'))
        return context


class CompraCreateView(FormularioVistaMixin, CreateView):
    model = StockMedicamento
    form_class = StockForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    titulo = 'Nueva compra / stock'
    volver_url = reverse_lazy('sabueso_feliz:compras')


class CompraUpdateView(FormularioVistaMixin, UpdateView):
    model = StockMedicamento
    form_class = StockForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    titulo = 'Editar stock'
    volver_url = reverse_lazy('sabueso_feliz:compras')


class CompraDeleteView(EliminarVistaMixin, DeleteView):
    model = StockMedicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    volver_url = reverse_lazy('sabueso_feliz:compras')
