from datetime import timedelta
from django.db.models import Count, F, Q
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import EmpleadoForm, SucursalForm
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

        # Actividad de hoy
        context['consultas_hoy'] = (
            Consulta.objects.filter(fechaEntrada=hoy)
            .select_related('perro_id', 'empleado_id')
        )
        context['vacunas_hoy'] = (
            CalendarioVacuna.objects
            .filter(fechaProgramada=hoy, fechaAplicacion__isnull=True)
            .select_related('perro_id', 'vacuna_id')
        )

        # Indicadores
        context['internados_count'] = Consulta.objects.filter(
            internado=True, fechaSalida__isnull=True
        ).count()
        context['vacunas_semana'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=True,
            fechaProgramada__range=(hoy, hoy + timedelta(days=7)),
        ).count()
        context['vacunas_atrasadas_count'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=True, fechaProgramada__lt=hoy
        ).count()
        context['stock_bajo'] = (
            StockMedicamento.objects
            .filter(cantidadExistente__lt=F('cantidadMinima'))
            .select_related('medicamento_id')
        )
        return context


# ------------------------------------------------------------ SUCURSAL

class SucursalesView(ListView):
    model = Sucursal
    template_name = 'sucursales.html'

    def get_queryset(self):
        return (
            Sucursal.objects
            .select_related('supervisor', 'supervisor_suplente')
            .annotate(
                total_empleados=Count('empleado', distinct=True),
                total_pacientes=Count('perro', distinct=True),
            )
        )


class SucursalView(DetailView):
    model = Sucursal
    template_name = 'sucursal.html'


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


class SucursalDeleteView(DeleteView):
    model = Sucursal
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('sabueso_feliz:sucursales')


# ------------------------------------------------------------ EMPLEADO

class EmpleadosView(ListView):
    model = Empleado
    template_name = 'empleados.html'

    def get_queryset(self):
        qs = Empleado.objects.select_related('sucursal')
        tipo = self.request.GET.get('tipo')
        if tipo == 'veterinarios':
            qs = qs.filter(veterinario__isnull=False)
        elif tipo == 'estudiantes':
            qs = qs.filter(estudiantes__isnull=False)
        return qs


class EmpleadoView(DetailView):
    model = Empleado
    template_name = 'empleado.html'


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'form.html'
    success_url = reverse_lazy('sabueso_feliz:empleados')


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
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

    def get_queryset(self):
        qs = Raza.objects.order_by('denominacion')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(denominacion__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


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

    def get_queryset(self):
        qs = Perro.objects.select_related('raza', 'duenio', 'sucursal').order_by('nombre')

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(nroHistoriaClinica__icontains=q)
                | Q(duenio__nombre__icontains=q)
                | Q(duenio__apellido__icontains=q)
            )

        sucursal = self.request.GET.get('sucursal')
        if sucursal:
            qs = qs.filter(sucursal_id=sucursal)

        raza = self.request.GET.get('raza')
        if raza:
            qs = qs.filter(raza_id=raza)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sucursales'] = Sucursal.objects.all()
        context['razas'] = Raza.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['sucursal_sel'] = self.request.GET.get('sucursal', '')
        context['raza_sel'] = self.request.GET.get('raza', '')
        return context


class PacienteView(DetailView):
    model = Perro
    template_name = 'paciente.html'
    context_object_name = 'perro'

    def get_queryset(self):
        return Perro.objects.select_related('raza', 'duenio', 'sucursal')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perro = self.object
        hoy = timezone.localdate()
        ver = self.request.GET.get('ver', '')

        consultas = (
            Consulta.objects.filter(perro_id=perro)
            .select_related('empleado_id')
            .prefetch_related(
                'consultasintoma_set__sintoma_id',
                'consultadiagnostico_set__diagnostico_id',
                'recetamedicamento_set__medicamento_id',
            )
            .order_by('-fechaEntrada')
        )
        vacunas = (
            CalendarioVacuna.objects.filter(perro_id=perro)
            .select_related('vacuna_id', 'empleado_id')
        )

        eventos = []
        if ver != 'vacunas':
            eventos += [{'tipo': 'consulta', 'fecha': c.fechaEntrada, 'obj': c}
                        for c in consultas]
        if ver != 'consultas':
            eventos += [{'tipo': 'vacuna',
                         'fecha': v.fechaAplicacion or v.fechaProgramada, 'obj': v}
                        for v in vacunas]
        eventos.sort(key=lambda e: e['fecha'], reverse=True)

        context['eventos'] = eventos
        context['ver'] = ver
        context['hoy'] = hoy
        context['ultima_consulta'] = consultas.first()
        context['proxima_vacuna'] = (
            vacunas.filter(fechaAplicacion__isnull=True)
            .order_by('fechaProgramada').first()
        )
        return context


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

    def get_queryset(self):
        qs = (
            Consulta.objects
            .select_related('perro_id__sucursal', 'empleado_id')
            .order_by('-fechaEntrada', '-id')
        )

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(perro_id__nombre__icontains=q)
                | Q(perro_id__nroHistoriaClinica__icontains=q)
                | Q(nroOrden__icontains=q)
            )

        sucursal = self.request.GET.get('sucursal')
        if sucursal:
            qs = qs.filter(perro_id__sucursal_id=sucursal)

        if self.request.GET.get('internado') == '1':
            qs = qs.filter(internado=True, fechaSalida__isnull=True)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sucursales'] = Sucursal.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['sucursal_sel'] = self.request.GET.get('sucursal', '')
        context['internado_sel'] = self.request.GET.get('internado', '')
        return context


class ConsultaView(DetailView):
    model = Consulta
    template_name = 'consulta.html'


class ConsultaCreateView(CreateView):
    model = Consulta
    template_name = 'consulta_form.html'
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

    def get_estado(self):
        estado = self.request.GET.get('estado', '')
        # "realizadas" es el nombre que usa el menú lateral
        return 'aplicadas' if estado == 'realizadas' else estado

    def get_queryset(self):
        hoy = timezone.localdate()
        qs = CalendarioVacuna.objects.select_related(
            'perro_id__sucursal', 'vacuna_id', 'empleado_id'
        )

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(perro_id__nombre__icontains=q) | Q(vacuna_id__nombre__icontains=q)
            )

        sucursal = self.request.GET.get('sucursal')
        if sucursal:
            qs = qs.filter(perro_id__sucursal_id=sucursal)

        estado = self.get_estado()
        if estado == 'pendientes':
            qs = qs.filter(fechaAplicacion__isnull=True)
        elif estado == 'proximas':
            qs = qs.filter(fechaAplicacion__isnull=True, fechaProgramada__gte=hoy)
        elif estado == 'vencidas':
            qs = qs.filter(fechaAplicacion__isnull=True, fechaProgramada__lt=hoy)
        elif estado == 'aplicadas':
            qs = qs.filter(fechaAplicacion__isnull=False)

        if estado == 'aplicadas':
            return qs.order_by('-fechaAplicacion')
        # Pendientes primero, ordenadas por fecha prevista
        return qs.order_by(F('fechaAplicacion').asc(nulls_first=True), 'fechaProgramada')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        pendientes = CalendarioVacuna.objects.filter(fechaAplicacion__isnull=True)

        context['hoy'] = hoy
        context['estado'] = self.get_estado()
        context['q'] = self.request.GET.get('q', '')
        context['sucursal_sel'] = self.request.GET.get('sucursal', '')
        context['sucursales'] = Sucursal.objects.all()
        context['proximas_count'] = pendientes.filter(fechaProgramada__gte=hoy).count()
        context['vencidas_count'] = pendientes.filter(fechaProgramada__lt=hoy).count()
        context['aplicadas_count'] = CalendarioVacuna.objects.filter(
            fechaAplicacion__isnull=False
        ).count()
        return context


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

    def get_queryset(self):
        qs = (
            StockMedicamento.objects
            .select_related('medicamento_id')
            .order_by('medicamento_id__nombre')
        )

        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(medicamento_id__nombre__icontains=q)
                | Q(medicamento_id__laboratorio__icontains=q)
            )

        if self.request.GET.get('filtro') == 'bajo':
            qs = qs.filter(cantidadExistente__lt=F('cantidadMinima'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['filtro'] = self.request.GET.get('filtro', '')
        context['bajo_count'] = StockMedicamento.objects.filter(
            cantidadExistente__lt=F('cantidadMinima')
        ).count()
        return context


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