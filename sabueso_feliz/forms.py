from django import forms

from .models import (
    Sucursal,
    Empleado,
    Veterinario,
    Estudiantes,
    Raza,
    Duenio,
    Perro,
    Consulta,
    CalendarioVacuna,
    Medicamento,
    StockMedicamento,
)


class FormularioBase(forms.ModelForm):
    """Formulario reutilizable: aplica Bootstrap a cualquier ModelForm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            widget = campo.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'

            if isinstance(campo, forms.DateField):
                campo.widget = forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={'type': 'date', 'class': 'form-control'},
                )
                campo.input_formats = ['%Y-%m-%d', '%d/%m/%Y']


class SucursalForm(FormularioBase):
    class Meta:
        model = Sucursal
        fields = '__all__'


class EmpleadoForm(FormularioBase):
    class Meta:
        model = Empleado
        fields = '__all__'


class VeterinarioForm(FormularioBase):
    class Meta:
        model = Veterinario
        fields = '__all__'


class EstudianteForm(FormularioBase):
    class Meta:
        model = Estudiantes
        fields = '__all__'


class RazaForm(FormularioBase):
    class Meta:
        model = Raza
        fields = '__all__'


class DuenioForm(FormularioBase):
    class Meta:
        model = Duenio
        fields = '__all__'


class PacienteForm(FormularioBase):
    class Meta:
        model = Perro
        fields = '__all__'


class ConsultaForm(FormularioBase):
    class Meta:
        model = Consulta
        fields = '__all__'


class VacunacionForm(FormularioBase):
    class Meta:
        model = CalendarioVacuna
        fields = '__all__'


class MedicamentoForm(FormularioBase):
    class Meta:
        model = Medicamento
        fields = '__all__'


class StockForm(FormularioBase):
    class Meta:
        model = StockMedicamento
        fields = '__all__'
