from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
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
    FormView,
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
    ContactoForm,
    RegistroUsuarioForm,
)


# ------------------------------------------------------------
# MIXINS REUTILIZABLES
# ------------------------------------------------------------

class FormularioVistaMixin:
    """Mixin para enriquecer vistas de formularios (Clase 14)."""
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
    """Mixin para vistas de confirmación de eliminación (Clase 15)."""
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


# ------------------------------------------------------------
# HOME, ACERCA DE, CONTACTO, REGISTRO
# ------------------------------------------------------------

class HomeView(TemplateView):
    """Vista principal con métricas e información del día (Clase 9)."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        context['total_sucursales'] = Sucursal.objects.count()
        context['total_empleados'] = Empleado.objects.count()
        context['total_veterinarios'] = Empleado.objects.veterinarios().count()
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


class AcercaDeView(TemplateView):
    """Vista institucional y del equipo de desarrollo (Clase 2 & 18)."""
    template_name = 'acerca_de.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre_proyecto'] = 'Veterinaria El Sabueso Feliz'
        context['materia'] = 'Programación 3'
        return context


class ContactoView(FormView):
    """Vista de formulario de contacto con forms.Form genérico (Clase 12)."""
    template_name = 'contacto.html'
    form_class = ContactoForm
    success_url = reverse_lazy('sabueso_feliz:contacto')

    def form_valid(self, form):
        nombre = form.cleaned_data.get('nombre')
        messages.success(
            self.request,
            f"¡Muchas gracias {nombre}! Tu consulta ha sido recibida y será atendida a la brevedad."
        )
        return super().form_valid(form)


class RegistroView(FormView):
    """Registro de nuevos usuarios con login automático posterior (Clase 17)."""
    template_name = 'registration/registro.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('sabueso_feliz:home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f"¡Bienvenido/a, {user.username}! Tu cuenta ha sido creada exitosamente."
        )
        return super().form_valid(form)


# ------------------------------------------------------------
# SUCURSAL
# ------------------------------------------------------------

class SucursalesView(ListView):
    model = Sucursal
    template_name = 'sucursales.html'
    paginate_by = 6
    queryset = Sucursal.objects.select_related('supervisor', 'supervisor_suplente')


class SucursalView(DetailView):
    model = Sucursal
    template_name = 'sucursal.html'
    context_object_name = 'sucursal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empleados'] = self.object.empleados.select_related('veterinario', 'estudiantes')
        context['pacientes'] = self.object.perro_set.select_related('raza', 'duenio')
        return context


class SucursalCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    titulo = 'Nueva sucursal'
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    titulo = 'Editar sucursal'
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


class SucursalDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Sucursal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')
    volver_url = reverse_lazy('sabueso_feliz:sucursales')


# ------------------------------------------------------------
# EMPLEADO (Con filtrado por Rol: Veterinario / Estudiante / General)
# ------------------------------------------------------------

class EmpleadosView(ListView):
    """
    Listado de empleados con filtro por tipo (Veterinario / Estudiante / General),
    sucursal, buscador y paginación (Clases 10 y 11).
    """
    model = Empleado
    template_name = 'empleados.html'
    paginate_by = 6
    context_object_name = 'empleados'

    def get_queryset(self):
        qs = Empleado.objects.select_related('sucursal', 'veterinario', 'estudiantes').order_by('apellido', 'nombre')

        tipo = self.request.GET.get('tipo', '').strip().lower()
        if tipo == 'veterinario':
            qs = qs.veterinarios()
        elif tipo == 'estudiante':
            qs = qs.estudiantes()
        elif tipo == 'general':
            qs = qs.generales()

        sucursal_id = self.request.GET.get('sucursal')
        if sucursal_id:
            qs = qs.filter(sucursal_id=sucursal_id)

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(apellido__icontains=q)
                | Q(nroDocumento__icontains=q)
                | Q(sucursal__nombre__icontains=q)
                | Q(veterinario__matriculaHabilitante__icontains=q)
                | Q(estudiantes__legajo__icontains=q)
            ).distinct()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_actual'] = self.request.GET.get('tipo', '')
        context['sucursal_actual'] = self.request.GET.get('sucursal', '')
        context['q'] = self.request.GET.get('q', '')
        context['total_general'] = Empleado.objects.count()
        context['total_veterinarios'] = Empleado.objects.veterinarios().count()
        context['total_estudiantes'] = Empleado.objects.estudiantes().count()
        context['total_otros'] = Empleado.objects.generales().count()
        return context


class EmpleadoView(DetailView):
    model = Empleado
    template_name = 'empleado.html'
    context_object_name = 'empleado'


class EmpleadoCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Nuevo empleado'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    titulo = 'Editar empleado'
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Empleado
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')
    volver_url = reverse_lazy('sabueso_feliz:empleados')


class VeterinarioCreateView(EmpleadoCreateView):
    titulo = 'Nuevo veterinario'
    initial = {'tipo_empleado': 'veterinario'}


class EstudianteCreateView(EmpleadoCreateView):
    titulo = 'Nuevo estudiante'
    initial = {'tipo_empleado': 'estudiante'}


# ------------------------------------------------------------
# RAZA
# ------------------------------------------------------------

class RazasView(ListView):
    model = Raza
    template_name = 'razas.html'
    paginate_by = 6


class RazaView(DetailView):
    model = Raza
    template_name = 'raza.html'
    context_object_name = 'raza'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.object.perro_set.select_related('duenio', 'sucursal')
        return context


class RazaCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Raza
    form_class = RazaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    titulo = 'Nueva raza'
    volver_url = reverse_lazy('sabueso_feliz:razas')


class RazaUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Raza
    form_class = RazaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    titulo = 'Editar raza'
    volver_url = reverse_lazy('sabueso_feliz:razas')


class RazaDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Raza
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:razas')
    volver_url = reverse_lazy('sabueso_feliz:razas')


# ------------------------------------------------------------
# DUEÑO
# ------------------------------------------------------------

class DueniosView(ListView):
    model = Duenio
    template_name = 'duenios.html'
    paginate_by = 6


class DuenioView(DetailView):
    model = Duenio
    template_name = 'duenio.html'
    context_object_name = 'duenio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pacientes'] = self.object.perro_set.select_related('raza', 'sucursal')
        return context


class DuenioCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Duenio
    form_class = DuenioForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    titulo = 'Nuevo propietario'
    volver_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Duenio
    form_class = DuenioForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    titulo = 'Editar propietario'
    volver_url = reverse_lazy('sabueso_feliz:duenios')


class DuenioDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Duenio
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:duenios')
    volver_url = reverse_lazy('sabueso_feliz:duenios')


# ------------------------------------------------------------
# PACIENTE (Perro)
# ------------------------------------------------------------

class PacientesView(ListView):
    model = Perro
    template_name = 'pacientes.html'
    paginate_by = 6

    def get_queryset(self):
        qs = Perro.objects.select_related('raza', 'duenio', 'sucursal', 'creado_por')

        raza_id = self.request.GET.get('raza')
        if raza_id:
            qs = qs.filter(raza_id=raza_id)

        sucursal_id = self.request.GET.get('sucursal')
        if sucursal_id:
            qs = qs.filter(sucursal_id=sucursal_id)

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(nroHistoriaClinica__icontains=q)
                | Q(duenio__nombre__icontains=q)
                | Q(duenio__apellido__icontains=q)
                | Q(raza__denominacion__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['raza_actual'] = self.request.GET.get('raza', '')
        context['sucursal_actual'] = self.request.GET.get('sucursal', '')
        return context


class PacienteView(DetailView):
    model = Perro
    template_name = 'paciente.html'
    context_object_name = 'paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consultas'] = self.object.consultas.select_related('empleado_id')
        context['vacunaciones'] = self.object.vacunaciones.select_related(
            'vacuna_id', 'empleado_id'
        )
        return context


class PacienteCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Perro
    form_class = PacienteForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    titulo = 'Registrar perro'
    volver_url = reverse_lazy('sabueso_feliz:pacientes')

    def form_valid(self, form):
        # Clase 17: Asignar usuario creador automáticamente
        if self.request.user.is_authenticated:
            form.instance.creado_por = self.request.user
        return super().form_valid(form)


class PacienteUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Perro
    form_class = PacienteForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    titulo = 'Editar paciente'
    volver_url = reverse_lazy('sabueso_feliz:pacientes')


class PacienteDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Perro
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:pacientes')
    volver_url = reverse_lazy('sabueso_feliz:pacientes')


# ------------------------------------------------------------
# CONSULTA
# ------------------------------------------------------------

class ConsultasView(ListView):
    model = Consulta
    template_name = 'consultas.html'
    paginate_by = 6

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
        context['sintomas'] = self.object.sintomas.select_related('sintoma_id')
        context['recetas'] = self.object.recetas.select_related('medicamento_id')
        return context


class ConsultaCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    titulo = 'Nueva consulta'
    volver_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    titulo = 'Editar consulta'
    volver_url = reverse_lazy('sabueso_feliz:consultas')


class ConsultaDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Consulta
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:consultas')
    volver_url = reverse_lazy('sabueso_feliz:consultas')


# ------------------------------------------------------------
# VACUNACIÓN
# ------------------------------------------------------------

class VacunacionesView(ListView):
    model = CalendarioVacuna
    template_name = 'vacunaciones.html'
    paginate_by = 6

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


class VacunacionCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = CalendarioVacuna
    form_class = VacunacionForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    titulo = 'Nueva vacunación'
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = CalendarioVacuna
    form_class = VacunacionForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    titulo = 'Editar vacunación'
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


class VacunacionDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = CalendarioVacuna
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:vacunaciones')
    volver_url = reverse_lazy('sabueso_feliz:vacunaciones')


# ------------------------------------------------------------
# MEDICAMENTO
# ------------------------------------------------------------

class MedicamentosView(ListView):
    model = Medicamento
    template_name = 'medicamentos.html'
    paginate_by = 8


class MedicamentoCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    titulo = 'Nuevo medicamento'
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    titulo = 'Editar medicamento'
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


class MedicamentoDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = Medicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:medicamentos')
    volver_url = reverse_lazy('sabueso_feliz:medicamentos')


# ------------------------------------------------------------
# COMPRAS (STOCK)
# ------------------------------------------------------------

class ComprasView(ListView):
    model = StockMedicamento
    template_name = 'compras.html'
    paginate_by = 8

    def get_queryset(self):
        qs = StockMedicamento.objects.select_related('medicamento_id')
        if self.request.GET.get('alerta'):
            qs = qs.filter(cantidadExistente__lt=F('cantidadMinima'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['solo_alertas'] = bool(self.request.GET.get('alerta'))
        return context


class CompraCreateView(LoginRequiredMixin, FormularioVistaMixin, CreateView):
    model = StockMedicamento
    form_class = StockForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    titulo = 'Nueva compra / stock'
    volver_url = reverse_lazy('sabueso_feliz:compras')


class CompraUpdateView(LoginRequiredMixin, FormularioVistaMixin, UpdateView):
    model = StockMedicamento
    form_class = StockForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    titulo = 'Editar stock'
    volver_url = reverse_lazy('sabueso_feliz:compras')


class CompraDeleteView(LoginRequiredMixin, EliminarVistaMixin, DeleteView):
    model = StockMedicamento
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:compras')
    volver_url = reverse_lazy('sabueso_feliz:compras')
