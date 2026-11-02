from django.utils import timezone
from django.db.models import F
from .models import Sucursal, Raza, StockMedicamento, Consulta, Perro, Empleado


def sabueso_context(request):
    hoy = timezone.localdate()
    return {
        'menu_sucursales': Sucursal.objects.all(),
        'menu_razas': Raza.objects.all(),
        'total_alertas_stock': StockMedicamento.objects.filter(
            cantidadExistente__lt=F('cantidadMinima')
        ).count(),
        'consultas_hoy_count': Consulta.objects.filter(fechaEntrada=hoy).count(),
        'total_pacientes_global': Perro.objects.count(),
        'total_empleados_global': Empleado.objects.count(),
        'total_veterinarios_global': Empleado.objects.veterinarios().count(),
    }

