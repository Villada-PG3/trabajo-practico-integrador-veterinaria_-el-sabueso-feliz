from django import forms
from .models import Sucursal


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