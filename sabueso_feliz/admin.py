from django.contrib import admin
from .models import (
    Sucursal, Empleado, Veterinario, Estudiantes, Raza, Duenio, Perro,
    Vacuna, CalendarioVacuna, Consulta, Sintoma, ConsultaSintoma,
    Diagnostico, Medicamento, RecetaMedicamento, StockMedicamento,
)

admin.site.register(Sucursal)
admin.site.register(Empleado)
admin.site.register(Veterinario)
admin.site.register(Estudiantes)
admin.site.register(Raza)
admin.site.register(Duenio)
admin.site.register(Perro)
admin.site.register(Vacuna)
admin.site.register(CalendarioVacuna)
admin.site.register(Consulta)
admin.site.register(Sintoma)
admin.site.register(ConsultaSintoma)
admin.site.register(Diagnostico)
admin.site.register(Medicamento)
admin.site.register(RecetaMedicamento)
admin.site.register(StockMedicamento)