from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Sucursal, Empleado, Veterinario, Estudiantes, Raza, Duenio, Perro
from .forms import EmpleadoForm


class ModelosYRolesTestCase(TestCase):
    def setUp(self):
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal Centro",
            direccion="Av. Colón 100",
            telefono="351-111111"
        )
        self.emp_general = Empleado.objects.create(
            tipoDocumento="DNI",
            nroDocumento="10000001",
            nombre="Carlos",
            apellido="Gomez",
            fechaNacimiento=timezone.datetime(1990, 1, 1).date(),
            fechaIngreso=timezone.datetime(2023, 1, 1).date(),
            sucursal=self.sucursal
        )
        self.emp_vet = Empleado.objects.create(
            tipoDocumento="DNI",
            nroDocumento="20000002",
            nombre="Dra. Laura",
            apellido="Martinez",
            fechaNacimiento=timezone.datetime(1985, 5, 10).date(),
            fechaIngreso=timezone.datetime(2020, 3, 1).date(),
            sucursal=self.sucursal
        )
        self.vet = Veterinario.objects.create(
            empleado=self.emp_vet,
            matriculaHabilitante="MP-9988"
        )
        self.emp_est = Empleado.objects.create(
            tipoDocumento="DNI",
            nroDocumento="30000003",
            nombre="Tomas",
            apellido="Fernandez",
            fechaNacimiento=timezone.datetime(2001, 8, 20).date(),
            fechaIngreso=timezone.datetime(2024, 2, 1).date(),
            sucursal=self.sucursal
        )
        self.est = Estudiantes.objects.create(
            empleado=self.emp_est,
            legajo="EST-1234"
        )

    def test_roles_y_propiedades_empleado(self):
        self.assertEqual(self.emp_general.tipo_empleado, "Personal General")
        self.assertFalse(self.emp_general.es_veterinario)
        self.assertFalse(self.emp_general.es_estudiante)

        # Veterinario
        self.assertEqual(self.emp_vet.tipo_empleado, "Veterinario")
        self.assertTrue(self.emp_vet.es_veterinario)
        self.assertEqual(self.emp_vet.matricula, "MP-9988")
        self.assertEqual(self.vet.empleado.pk, self.emp_vet.pk)

        # Estudiante
        self.assertEqual(self.emp_est.tipo_empleado, "Estudiante")
        self.assertTrue(self.emp_est.es_estudiante)
        self.assertEqual(self.emp_est.legajo, "EST-1234")
        self.assertEqual(self.est.empleado.pk, self.emp_est.pk)

    def test_custom_queryset_empleados(self):
        self.assertEqual(Empleado.objects.veterinarios().count(), 1)
        self.assertEqual(Empleado.objects.estudiantes().count(), 1)
        self.assertEqual(Empleado.objects.generales().count(), 1)
        self.assertEqual(Empleado.objects.count(), 3)

    def test_formulario_unificado_empleado(self):
        # Crear veterinario con el formulario unificado
        data_vet = {
            'tipo_empleado': 'veterinario',
            'matriculaHabilitante': 'MP-7777',
            'legajo': '',
            'tipoDocumento': 'DNI',
            'nroDocumento': '44444444',
            'nombre': 'Valeria',
            'apellido': 'Paz',
            'fechaNacimiento': '1988-04-12',
            'fechaIngreso': '2022-06-01',
            'sucursal': self.sucursal.pk
        }
        form = EmpleadoForm(data=data_vet)
        self.assertTrue(form.is_valid(), form.errors)
        nuevo_vet = form.save()
        self.assertTrue(nuevo_vet.es_veterinario)
        self.assertEqual(nuevo_vet.matricula, 'MP-7777')
        self.assertEqual(nuevo_vet.tipo_empleado, 'Veterinario')


class VistasYContextProcessorsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.sucursal = Sucursal.objects.create(
            nombre="Sucursal Norte",
            direccion="Av. Rafael Nuñez 500",
            telefono="351-222222"
        )

    def test_vistas_publicas_y_context_processor(self):
        response = self.client.get(reverse('sabueso_feliz:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('menu_sucursales', response.context)
        self.assertIn('menu_razas', response.context)
        self.assertIn('total_alertas_stock', response.context)

    def test_filtro_empleados_por_tipo(self):
        response_vets = self.client.get(reverse('sabueso_feliz:empleados') + '?tipo=veterinario')
        self.assertEqual(response_vets.status_code, 200)

        response_est = self.client.get(reverse('sabueso_feliz:empleados') + '?tipo=estudiante')
        self.assertEqual(response_est.status_code, 200)

    def test_proteccion_vistas_crud(self):
        url_crear = reverse('sabueso_feliz:paciente_crear')
        response = self.client.get(url_crear)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
