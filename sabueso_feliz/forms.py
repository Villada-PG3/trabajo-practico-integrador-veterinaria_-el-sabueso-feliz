from django import forms
from .models import Sucursal, Empleado, Veterinario, Estudiantes, Raza, Duenio, Perro, Consulta, CalendarioVacuna, Medicamento, StockMedicamento


class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal

        fields = [
            'nombre',
            'direccion',
            'telefono',
            'supervisor',
            'supervisor_suplente',
        ]

        widgets = {
            'nombre': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'direccion': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'telefono': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'supervisor': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'supervisor_suplente': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }

        labels = {
            'nombre': 'Nombre de la sucursal',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'supervisor': 'Supervisor',
            'supervisor_suplente': 'Supervisor suplente',
        }

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'fechaNacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
    },
),
            'fechaIngreso': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                },
            ),
        }