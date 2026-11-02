from django.utils import timezone
from django.db.models import F
from .models import Sucursal, Raza, StockMedicamento, Consulta, Perro, Empleado


def sabueso_context(request):
    """
    Context processor global (Clase 11).
    Proporciona variables accesibles en TODOS los templates del proyecto:
    - Listado de sucursales para dropdowns de navegación
    - Listado de razas
    - Alertas de stock crítico
    - Consultas programadas / realizadas hoy
    - Métricas globales rápidas
    """
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

