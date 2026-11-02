from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Soporte para ImageField (con fallback a FileField si Pillow no estuviera presente)
try:
    import PIL  # noqa: F401
    FotoField = models.ImageField
except ImportError:
    FotoField = models.FileField


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    supervisor = models.ForeignKey(
        'Veterinario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sucursales_supervisadas',
        verbose_name="Supervisor titular"
    )
    supervisor_suplente = models.ForeignKey(
        'Veterinario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sucursales_suplentes',
        verbose_name="Supervisor suplente"
    )

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('sabueso_feliz:sucursal', kwargs={'pk': self.pk})


class EmpleadoQuerySet(models.QuerySet):
    """QuerySet personalizado para filtrar empleados según su rol (Clase 5 y 11)."""

    def veterinarios(self):
        return self.filter(veterinario__isnull=False)

    def estudiantes(self):
        return self.filter(estudiantes__isnull=False)

    def generales(self):
        return self.filter(veterinario__isnull=True, estudiantes__isnull=True)


class Empleado(models.Model):
    tipoDocumento = models.CharField(max_length=20, verbose_name="Tipo de documento")
    nroDocumento = models.CharField(max_length=20, verbose_name="Número de documento")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    fechaIngreso = models.DateField(verbose_name="Fecha de ingreso")
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="empleados",
        verbose_name="Sucursal"
    )

    objects = EmpleadoQuerySet.as_manager()

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:empleado', kwargs={'pk': self.pk})

    @property
    def tipo_empleado(self):
        """Devuelve el rol o tipo del empleado."""
        if hasattr(self, 'veterinario'):
            return 'Veterinario'
        if hasattr(self, 'estudiantes'):
            return 'Estudiante'
        return 'Personal General'

    @property
    def es_veterinario(self):
        return hasattr(self, 'veterinario')

    @property
    def es_estudiante(self):
        return hasattr(self, 'estudiantes')

    @property
    def matricula(self):
        if hasattr(self, 'veterinario'):
            return self.veterinario.matriculaHabilitante
        return None

    @property
    def legajo(self):
        if hasattr(self, 'estudiantes'):
            return self.estudiantes.legajo
        return None


class Veterinario(models.Model):
    """
    Veterinario: posee relación 1 a 1 (FK / OneToOne) con Empleado.
    Permite registrar la matrícula habilitante del profesional.
    """
    empleado = models.OneToOneField(
        Empleado,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='empleado_ptr_id',
        related_name='veterinario',
        verbose_name="Empleado asignado"
    )
    matriculaHabilitante = models.CharField(
        max_length=20,
        verbose_name="Matrícula habilitante"
    )

    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"
        ordering = ["empleado__apellido", "empleado__nombre"]

    def __str__(self):
        return f"Dr/a. {self.empleado} (Mat: {self.matriculaHabilitante})"

    @property
    def nombre(self):
        return self.empleado.nombre

    @property
    def apellido(self):
        return self.empleado.apellido

    @property
    def sucursal(self):
        return self.empleado.sucursal

    @property
    def nroDocumento(self):
        return self.empleado.nroDocumento


class Estudiantes(models.Model):
    """
    Estudiante / Pasante: posee relación 1 a 1 (FK / OneToOne) con Empleado.
    Permite registrar el legajo universitario.
    """
    empleado = models.OneToOneField(
        Empleado,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='empleado_ptr_id',
        related_name='estudiantes',
        verbose_name="Empleado asignado"
    )
    legajo = models.CharField(
        max_length=20,
        verbose_name="Legajo universitario"
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["empleado__apellido", "empleado__nombre"]

    def __str__(self):
        return f"{self.empleado} (Leg: {self.legajo})"

    @property
    def nombre(self):
        return self.empleado.nombre

    @property
    def apellido(self):
        return self.empleado.apellido

    @property
    def sucursal(self):
        return self.empleado.sucursal

    @property
    def nroDocumento(self):
        return self.empleado.nroDocumento


# Alias singular por compatibilidad con el diagrama de clases
Estudiante = Estudiantes


class Raza(models.Model):
    denominacion = models.CharField(max_length=100, verbose_name="Denominación")
    pesoMinMacho = models.FloatField(verbose_name="Peso mín. macho (kg)")
    pesoMaxMacho = models.FloatField(verbose_name="Peso máx. macho (kg)")
    alturaMediaMacho = models.FloatField(verbose_name="Altura media macho (cm)")
    pesoMinHembra = models.FloatField(verbose_name="Peso mín. hembra (kg)")
    pesoMaxHembra = models.FloatField(verbose_name="Peso máx. hembra (kg)")
    alturaMediaHembra = models.FloatField(verbose_name="Altura media hembra (cm)")
    cuidadosEspeciales = models.TextField(verbose_name="Cuidados especiales")

    class Meta:
        verbose_name = "Raza"
        verbose_name_plural = "Razas"
        ordering = ["denominacion"]

    def __str__(self):
        return self.denominacion

    def get_absolute_url(self):
        return reverse('sabueso_feliz:raza', kwargs={'pk': self.pk})


class Duenio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Dueño"
        verbose_name_plural = "Dueños"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:duenio', kwargs={'pk': self.pk})


class Perro(models.Model):
    nroHistoriaClinica = models.CharField(
        max_length=20,
        verbose_name="N° Historia Clínica"
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    fechaNacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    sexo = models.CharField(max_length=10, verbose_name="Sexo")
    raza = models.ForeignKey(
        Raza,
        on_delete=models.CASCADE,
        verbose_name="Raza"
    )
    duenio = models.ForeignKey(
        Duenio,
        on_delete=models.CASCADE,
        verbose_name="Dueño"
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        verbose_name="Sucursal"
    )
    pesoActual = models.FloatField(verbose_name="Peso actual (kg)")
    alturaActual = models.FloatField(verbose_name="Altura actual (cm)")
    imagen = FotoField(
        upload_to='pacientes/',
        null=True,
        blank=True,
        verbose_name="Foto del paciente"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pacientes_creados",
        verbose_name="Registrado por"
    )

    class Meta:
        verbose_name = "Paciente (Perro)"
        verbose_name_plural = "Pacientes (Perros)"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.nroHistoriaClinica})"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:paciente', kwargs={'pk': self.pk})


class Vacuna(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de vacuna")

    class Meta:
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class CalendarioVacuna(models.Model):
    perro_id = models.ForeignKey(
        Perro,
        on_delete=models.CASCADE,
        verbose_name="Paciente",
        related_name="vacunaciones"
    )
    vacuna_id = models.ForeignKey(
        Vacuna,
        on_delete=models.CASCADE,
        verbose_name="Vacuna"
    )
    empleado_id = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        verbose_name="Profesional a cargo"
    )
    fechaProgramada = models.DateField(verbose_name="Fecha programada")
    fechaAplicacion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de aplicación"
    )
    laboratorio = models.CharField(max_length=100, verbose_name="Laboratorio")
    dosis = models.CharField(max_length=50, verbose_name="Dosis")

    class Meta:
        verbose_name = "Calendario de Vacunación"
        verbose_name_plural = "Calendarios de Vacunación"
        ordering = ["fechaProgramada"]

    def __str__(self):
        return f"{self.vacuna_id} - {self.perro_id} ({self.fechaProgramada})"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:vacunacion', kwargs={'pk': self.pk})


class Consulta(models.Model):
    perro_id = models.ForeignKey(
        Perro,
        on_delete=models.CASCADE,
        verbose_name="Paciente",
        related_name="consultas"
    )
    empleado_id = models.ForeignKey(
        Empleado,
        on_delete=models.CASCADE,
        verbose_name="Veterinario / Profesional"
    )
    nroOrden = models.CharField(max_length=20, verbose_name="N° de orden")
    fechaEntrada = models.DateField(verbose_name="Fecha de entrada")
    internado = models.BooleanField(verbose_name="¿Requiere internación?")
    fechaSalida = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de salida"
    )

    class Meta:
        verbose_name = "Consulta Médica"
        verbose_name_plural = "Consultas Médicas"
        ordering = ["-fechaEntrada"]

    def __str__(self):
        return f"Consulta {self.nroOrden} - {self.perro_id}"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:consulta', kwargs={'pk': self.pk})


class Sintoma(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "Síntoma"
        verbose_name_plural = "Síntomas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class ConsultaSintoma(models.Model):
    consulta_id = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        verbose_name="Consulta",
        related_name="sintomas"
    )
    sintoma_id = models.ForeignKey(
        Sintoma,
        on_delete=models.CASCADE,
        verbose_name="Síntoma"
    )

    class Meta:
        verbose_name = "Síntoma de Consulta"
        verbose_name_plural = "Síntomas de Consultas"

    def __str__(self):
        return f"{self.consulta_id} - {self.sintoma_id}"


class Diagnostico(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción")

    class Meta:
        verbose_name = "Diagnóstico"
        verbose_name_plural = "Diagnósticos"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre comercial")
    laboratorio = models.CharField(max_length=100, verbose_name="Laboratorio")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.laboratorio})"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:medicamentos')


class RecetaMedicamento(models.Model):
    consulta_id = models.ForeignKey(
        Consulta,
        on_delete=models.CASCADE,
        verbose_name="Consulta",
        related_name="recetas"
    )
    medicamento_id = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name="Medicamento"
    )
    dosis = models.CharField(max_length=50, verbose_name="Dosis")
    periodisidad = models.CharField(max_length=50, verbose_name="Periodicidad")

    class Meta:
        verbose_name = "Receta de Medicamento"
        verbose_name_plural = "Recetas de Medicamentos"

    def __str__(self):
        return f"{self.medicamento_id} - {self.consulta_id}"


class StockMedicamento(models.Model):
    medicamento_id = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        verbose_name="Medicamento"
    )
    fechaUltimaCompra = models.DateField(verbose_name="Fecha de última compra")
    cantidadExistente = models.IntegerField(verbose_name="Cantidad existente")
    cantidadMinima = models.IntegerField(verbose_name="Cantidad mínima de alerta")

    class Meta:
        verbose_name = "Stock de Medicamento"
        verbose_name_plural = "Stock de Medicamentos"
        ordering = ["medicamento_id__nombre"]

    def __str__(self):
        return f"Stock de {self.medicamento_id}"

    def get_absolute_url(self):
        return reverse('sabueso_feliz:compras')
