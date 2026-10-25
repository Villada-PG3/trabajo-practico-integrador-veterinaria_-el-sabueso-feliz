from django.db import models


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    supervisor = models.ForeignKey(
        'Veterinario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sucursales_supervisadas'
    )
    supervisor_suplente = models.ForeignKey(
        'Veterinario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sucursales_suplentes'
    )

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    tipoDocumento = models.CharField(max_length=20)
    nroDocumento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    fechaIngreso = models.DateField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Veterinario(Empleado):
    matriculaHabilitante = models.CharField(max_length=20)


class Estudiantes(Empleado):
    legajo = models.CharField(max_length=20)


class Raza(models.Model):
    denominacion = models.CharField(max_length=100)
    pesoMinMacho = models.FloatField()
    pesoMaxMacho = models.FloatField()
    alturaMediaMacho = models.FloatField()
    pesoMinHembra = models.FloatField()
    pesoMaxHembra = models.FloatField()
    alturaMediaHembra = models.FloatField()
    cuidadosEspeciales = models.TextField()

    def __str__(self):
        return self.denominacion


class Duenio(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Perro(models.Model):
    nroHistoriaClinica = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    sexo = models.CharField(max_length=10)
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    duenio = models.ForeignKey(Duenio, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    pesoActual = models.FloatField()
    alturaActual = models.FloatField()

    def __str__(self):
        return f"{self.nombre} ({self.nroHistoriaClinica})"


class Vacuna(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CalendarioVacuna(models.Model):
    perro_id = models.ForeignKey(Perro, on_delete=models.CASCADE)
    vacuna_id = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    empleado_id = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fechaProgramada = models.DateField()
    fechaAplicacion = models.DateField(null=True, blank=True)
    laboratorio = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vacuna_id} - {self.perro_id} ({self.fechaProgramada})"


class Consulta(models.Model):
    perro_id = models.ForeignKey(Perro, on_delete=models.CASCADE)
    empleado_id = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    nroOrden = models.CharField(max_length=20)
    fechaEntrada = models.DateField()
    internado = models.BooleanField()
    fechaSalida = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Consulta {self.nroOrden} - {self.perro_id}"


class Sintoma(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class ConsultaSintoma(models.Model):
    consulta_id = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    sintoma_id = models.ForeignKey(Sintoma, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.consulta_id} - {self.sintoma_id}"


class Diagnostico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    laboratorio = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.laboratorio})"


class RecetaMedicamento(models.Model):
    consulta_id = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    medicamento_id = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=50)
    periodisidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.medicamento_id} - {self.consulta_id}"


class StockMedicamento(models.Model):
    medicamento_id = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    fechaUltimaCompra = models.DateField()
    cantidadExistente = models.IntegerField()
    cantidadMinima = models.IntegerField()

    def __str__(self):
        return f"Stock de {self.medicamento_id}"