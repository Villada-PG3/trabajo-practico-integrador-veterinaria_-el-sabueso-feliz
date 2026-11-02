from django.contrib import admin
from .models import (
    Sucursal,
    Empleado,
    Veterinario,
    Estudiantes,
    Raza,
    Duenio,
    Perro,
    Vacuna,
    CalendarioVacuna,
    Consulta,
    Sintoma,
    ConsultaSintoma,
    Diagnostico,
    Medicamento,
    RecetaMedicamento,
    StockMedicamento,
)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'supervisor', 'supervisor_suplente')
    search_fields = ('nombre', 'direccion', 'telefono')
    list_select_related = ('supervisor', 'supervisor_suplente')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'apellido',
        'nombre',
        'tipo_empleado_badge',
        'tipoDocumento',
        'nroDocumento',
        'sucursal',
        'fechaIngreso',
    )
    list_filter = ('sucursal', 'fechaIngreso')
    search_fields = ('nombre', 'apellido', 'nroDocumento')
    list_select_related = ('sucursal',)

    @admin.display(description="Rol / Función")
    def tipo_empleado_badge(self, obj):
        return obj.tipo_empleado


@admin.register(Veterinario)
class VeterinarioAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'matriculaHabilitante', 'get_sucursal')
    search_fields = ('empleado__nombre', 'empleado__apellido', 'matriculaHabilitante', 'empleado__nroDocumento')
    list_select_related = ('empleado', 'empleado__sucursal')

    @admin.display(description="Sucursal")
    def get_sucursal(self, obj):
        return obj.empleado.sucursal


@admin.register(Estudiantes)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'legajo', 'get_sucursal')
    search_fields = ('empleado__nombre', 'empleado__apellido', 'legajo', 'empleado__nroDocumento')
    list_select_related = ('empleado', 'empleado__sucursal')

    @admin.display(description="Sucursal")
    def get_sucursal(self, obj):
        return obj.empleado.sucursal


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ('denominacion', 'pesoMinMacho', 'pesoMaxMacho', 'alturaMediaMacho')
    search_fields = ('denominacion',)


@admin.register(Duenio)
class DuenioAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'telefono')
    search_fields = ('apellido', 'nombre', 'telefono')


@admin.register(Perro)
class PerroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nroHistoriaClinica', 'raza', 'duenio', 'sucursal', 'activo')
    list_filter = ('raza', 'sucursal', 'sexo', 'activo')
    search_fields = ('nombre', 'nroHistoriaClinica', 'duenio__nombre', 'duenio__apellido')
    list_select_related = ('raza', 'duenio', 'sucursal')


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(CalendarioVacuna)
class CalendarioVacunaAdmin(admin.ModelAdmin):
    list_display = (
        'vacuna_id',
        'perro_id',
        'empleado_id',
        'fechaProgramada',
        'fechaAplicacion',
        'laboratorio',
        'dosis',
    )
    list_filter = ('fechaProgramada', 'fechaAplicacion', 'vacuna_id')
    search_fields = ('perro_id__nombre', 'laboratorio', 'empleado_id__nombre', 'empleado_id__apellido')
    list_select_related = ('vacuna_id', 'perro_id', 'empleado_id')


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'nroOrden',
        'perro_id',
        'empleado_id',
        'fechaEntrada',
        'internado',
        'fechaSalida',
    )
    list_filter = ('internado', 'fechaEntrada')
    search_fields = ('nroOrden', 'perro_id__nombre', 'empleado_id__nombre', 'empleado_id__apellido')
    list_select_related = ('perro_id', 'empleado_id')


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'laboratorio', 'activo')
    list_filter = ('activo', 'laboratorio')
    search_fields = ('nombre', 'laboratorio')


@admin.register(StockMedicamento)
class StockMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('medicamento_id', 'cantidadExistente', 'cantidadMinima', 'fechaUltimaCompra')
    list_filter = ('fechaUltimaCompra',)
    list_select_related = ('medicamento_id',)


@admin.register(Sintoma)
class SintomaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(ConsultaSintoma)
class ConsultaSintomaAdmin(admin.ModelAdmin):
    list_display = ('consulta_id', 'sintoma_id')
    list_select_related = ('consulta_id', 'sintoma_id')


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(RecetaMedicamento)
class RecetaMedicamentoAdmin(admin.ModelAdmin):
    list_display = ('consulta_id', 'medicamento_id', 'dosis', 'periodisidad')
    list_select_related = ('consulta_id', 'medicamento_id')
