# Consultas ORM de Django — Veterinaria "El Sabueso Feliz"
*Proyecto Integrador - Cátedra de Programación 3 (Clase 5 y Checklist Clase 18)*

Este documento contiene 10 ejemplos de consultas al ORM de Django (`django.db.models`) ejecutadas y probadas en el shell interactivo (`python manage.py shell`).

---

### 1. Listar todos los registros (`all()`)
Obtiene todos los pacientes caninos registrados en el sistema.
```python
from sabueso_feliz.models import Perro

perros = Perro.objects.all()
for p in perros:
    print(f"{p.nombre} (HC: {p.nroHistoriaClinica}) - Raza: {p.raza.denominacion}")
```
* **Método empleado:** `all()`
* **Concepto:** Retorna un `QuerySet` que evalúa todos los registros de la tabla `sabueso_feliz_perro`.

---

### 2. Filtrado con lookup insensible a mayúsculas (`filter` + `__icontains`)
Búsqueda de medicamentos por nombre o parte de su nombre sin distinguir mayúsculas de minúsculas.
```python
from sabueso_feliz.models import Medicamento

meds = Medicamento.objects.filter(nombre__icontains="anti")
for m in meds:
    print(f"Medicamento encontrado: {m.nombre} - Laboratorio: {m.laboratorio}")
```
* **Método y Lookup:** `filter()`, `__icontains` (SQL: `LIKE '%anti%'`)

---

### 3. Filtrado por comparación numérica (`__lt` y `__gt`)
Detectar medicamentos con stock crítico (cantidad existente menor al stock mínimo permitido) utilizando expresiones `F()`.
```python
from django.db.models import F
from sabueso_feliz.models import StockMedicamento

stock_critico = StockMedicamento.objects.filter(cantidadExistente__lt=F('cantidadMinima'))
for s in stock_critico:
    print(f"ALERTA: {s.medicamento_id.nombre} tiene {s.cantidadExistente} unid. (Mínimo: {s.cantidadMinima})")
```
* **Lookups:** `__lt` (menor que) y `F()` para comparar dos columnas de la misma tabla a nivel de base de datos.

---

### 4. Filtrar empleados por función o rol (Veterinarios vs Estudiantes vs Personal General)
Filtrar los empleados según si poseen perfil de veterinario o de estudiante universitario.
```python
from sabueso_feliz.models import Empleado

# Usando el QuerySet personalizado
veterinarios = Empleado.objects.veterinarios()
estudiantes = Empleado.objects.estudiantes()
generales = Empleado.objects.generales()

print(f"Veterinarios ({veterinarios.count()}):", [v.nombre for v in veterinarios])
print(f"Estudiantes ({estudiantes.count()}):", [e.nombre for e in estudiantes])
print(f"Personal general ({generales.count()}):", [g.nombre for g in generales])

# O directamente mediante relaciones inversas del ORM:
vets_orm = Empleado.objects.filter(veterinario__isnull=False)
```
* **Concepto:** `filter(veterinario__isnull=False)` explota la herencia multi-tabla y relación 1 a 1 de Django.

---

### 5. Exclusión de registros (`exclude()`)
Obtener los pacientes que no pertenezcan a una sucursal específica (por ejemplo, excluir la Sucursal Central).
```python
from sabueso_feliz.models import Perro

perros_otras_sucursales = Perro.objects.exclude(sucursal__nombre="Sucursal Central")
for p in perros_otras_sucursales:
    print(f"Paciente: {p.nombre} - Sucursal: {p.sucursal.nombre}")
```
* **Método:** `exclude()` invierte la condición (SQL: `NOT (...)`).

---

### 6. Obtención de un único objeto (`get()`) con manejo de excepción
Obtener un paciente específico por su número único de historia clínica.
```python
from django.core.exceptions import ObjectDoesNotExist
from sabueso_feliz.models import Perro

try:
    paciente = Perro.objects.get(nroHistoriaClinica="HC-001")
    print(f"Paciente hallado: {paciente.nombre}, Dueño: {paciente.duenio}")
except ObjectDoesNotExist:
    print("La historia clínica solicitada no existe.")
```
* **Diferencia crítica:** `get()` devuelve una única instancia del modelo y arroja excepción si no existe o si existen múltiples resultados; a diferencia de `filter()` que devuelve un `QuerySet` (iterable).

---

### 7. Ordenamiento y límite (`order_by()` y slicing)
Obtener las últimas 5 consultas médicas ingresadas, ordenadas de forma descendente por fecha de entrada.
```python
from sabueso_feliz.models import Consulta

ultimas_consultas = Consulta.objects.order_by('-fechaEntrada')[:5]
for c in ultimas_consultas:
    print(f"Consulta N° {c.nroOrden} - Fecha: {c.fechaEntrada} - Paciente: {c.perro_id.nombre}")
```
* **Método:** `order_by('-campo')` (el prefijo `-` indica orden descendente `DESC`). `[:5]` aplica `LIMIT 5` en SQL.

---

### 8. Filtrado con lista de valores (`__in`)
Buscar consultas que pertenezcan a un conjunto específico de pacientes.
```python
from sabueso_feliz.models import Consulta, Perro

ids_perros = [1, 2, 3]
consultas = Consulta.objects.filter(perro_id__in=ids_perros)
print(f"Total de consultas para los perros {ids_perros}: {consultas.count()}")
```
* **Lookup:** `__in` traduce a la cláusula SQL `IN (...)`.

---

### 9. Navegación hacia adelante con optimización (`select_related`)
Cargar en una sola consulta SQL (`JOIN`) el paciente, su raza, su dueño y su sucursal, evitando el problema de rendimiento N+1.
```python
from sabueso_feliz.models import Perro

pacientes = Perro.objects.select_related('raza', 'duenio', 'sucursal')
for p in pacientes:
    print(f"{p.nombre} | Raza: {p.raza.denominacion} | Dueño: {p.duenio.nombre} {p.duenio.apellido} | Sucursal: {p.sucursal.nombre}")
```
* **Concepto:** `select_related()` realiza un `INNER JOIN` o `LEFT OUTER JOIN` de claves foráneas directas.

---

### 10. Navegación hacia atrás (Reverse Relations / Related Name)
Desde una sucursal, acceder a todos los empleados y a todos los perros asociados sin consultar manualmente por ID.
```python
from sabueso_feliz.models import Sucursal

for suc in Sucursal.objects.all():
    empleados_suc = suc.empleados.all()
    pacientes_suc = suc.perro_set.all()
    print(f"Sucursal: {suc.nombre}")
    print(f" -> Empleados ({empleados_suc.count()}): {[e.nombre for e in empleados_suc]}")
    print(f" -> Pacientes ({pacientes_suc.count()}): {[p.nombre for p in pacientes_suc]}")
```
* **Concepto:** En relaciones 1 a N, el modelo padre accede a sus hijos mediante `related_name` (e.g. `suc.empleados.all()`) o el administrador reverso por defecto (`suc.perro_set.all()`).

