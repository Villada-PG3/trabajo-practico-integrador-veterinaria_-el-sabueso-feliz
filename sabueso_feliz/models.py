from django.db import models

# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)

class Empleado(models.Model):
    tipoDocumento = models.CharField(max_length=20)
    nroDocumento = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fechaNacimiento = models.DateField()
    fechaIngreso = models.DateField()

class Veterinario(Empleado):
    matriculaHabilitante = models.CharField(max_length=20)

class Estudiantes(Empleado):
    legajo = models.CharField(max_length=20)

class Raza(models.Model):
    denomicacion = models.CharField(max_length=100)
    pesoMinMacho = models.FloatField()
    pesoMaxMacho = models.FloatField()
    alturaMediaMacho = models.FloatField()
    pesoMinHembra = models.FloatField()
    pesoMaxHembra = models.FloatField()
    alturaMediaHembra = models.FloatField()
    cuidadosEspeciales = models.TextField()
class Duenio(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
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

class Vacuna(models.Model):
    nombre = models.CharField(max_length=100)
    
class CalendarioVacuna(models.Model):
    fechaProgramada = models.DateField()
    fechaAplicacion = models.DateField(null=True, blank=True)
    laboratorio = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)

class Consulta(models.Model):
    nroOrden = models.CharField(max_length=20)
    fechaEntrada = models.DateField()
    internado = models.BooleanField()
    fechaSalida = models.DateField(null=True, blank=True)

class Sintoma(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Diagnostico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    laboratorio = models.CharField(max_length=100)

class RecetaMedicamento(models.Model):
    dosis = models.CharField(max_length=50)
    periodisidad = models.CharField(max_length=50)

class StockMedicamento(models.Model):
    fechaUltimaCompra = models.DateField()
    cantidadExistente = models.IntegerField()
    cantidadMinima = models.IntegerField()

