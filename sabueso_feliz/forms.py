from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            widget = campo.widget

            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs['class'] = 'form-select'
            elif isinstance(widget, forms.FileInput):
                widget.attrs['class'] = 'form-control'
            else:
                widget.attrs['class'] = 'form-control'

            if isinstance(campo, forms.DateField):
                campo.widget = forms.DateInput(
                    format='%Y-%m-%d',
                    attrs={
                        'type': 'text',
                        'class': 'form-control campo-fecha',
                        'placeholder': 'Seleccionar fecha...',
                        'autocomplete': 'off',
                    },
                )
                campo.input_formats = ['%Y-%m-%d', '%d/%m/%Y']


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre y apellido'})
    )
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono (opcional)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 351-5551234'})
    )
    asunto = forms.CharField(
        max_length=120,
        label="Asunto",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del contacto'})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribí tu consulta aquí...'})
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        help_text="Requerido para notificaciones del sistema."
    )
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellido")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs['class'] = 'form-control'


# ------------------------------------------------------------
# MODEL FORMS (Clase 13)
# ------------------------------------------------------------

class SucursalForm(FormularioBase):
    class Meta:
        model = Sucursal
        fields = '__all__'


class EmpleadoForm(FormularioBase):
    TIPO_CHOICES = [
        ('general', 'Personal General'),
        ('veterinario', 'Veterinario'),
        ('estudiante', 'Estudiante / Pasante'),
    ]

    tipo_empleado = forms.ChoiceField(
        choices=TIPO_CHOICES,
        initial='general',
        label="1. ¿Qué tipo de empleado desea registrar?",
        widget=forms.Select(attrs={'class': 'form-select fw-bold border-primary', 'id': 'id_tipo_empleado'}),
        help_text="Seleccione la función del empleado para habilitar los campos específicos."
    )

    matriculaHabilitante = forms.CharField(
        max_length=20,
        required=False,
        label="Matrícula Habilitante",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: MP-1234', 'id': 'id_matriculaHabilitante'}),
        help_text="Requerido para profesionales Veterinarios."
    )

    legajo = forms.CharField(
        max_length=20,
        required=False,
        label="Legajo Universitario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: EST-5678', 'id': 'id_legajo'}),
        help_text="Requerido para Estudiantes o Pasantes universitarios."
    )

    class Meta:
        model = Empleado
        fields = [
            'tipo_empleado',
            'matriculaHabilitante',
            'legajo',
            'tipoDocumento',
            'nroDocumento',
            'nombre',
            'apellido',
            'fechaNacimiento',
            'fechaIngreso',
            'sucursal',
        ]
        labels = {
            'tipoDocumento': 'Tipo de documento',
            'nroDocumento': 'Número de documento',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fechaNacimiento': 'Fecha de nacimiento',
            'fechaIngreso': 'Fecha de ingreso',
            'sucursal': 'Sucursal de trabajo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.es_veterinario:
                self.fields['tipo_empleado'].initial = 'veterinario'
                self.fields['matriculaHabilitante'].initial = self.instance.matricula
            elif self.instance.es_estudiante:
                self.fields['tipo_empleado'].initial = 'estudiante'
                self.fields['legajo'].initial = self.instance.legajo
            else:
                self.fields['tipo_empleado'].initial = 'general'

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_empleado')
        matricula = cleaned_data.get('matriculaHabilitante', '').strip()
        legajo = cleaned_data.get('legajo', '').strip()

        if tipo == 'veterinario' and not matricula:
            self.add_error('matriculaHabilitante', 'Debe ingresar la matrícula habilitante para registrar a un Veterinario.')
        elif tipo == 'estudiante' and not legajo:
            self.add_error('legajo', 'Debe ingresar el número de legajo para registrar a un Estudiante.')

        return cleaned_data

    def save(self, commit=True):
        tipo = self.cleaned_data.get('tipo_empleado')
        matricula = self.cleaned_data.get('matriculaHabilitante', '').strip()
        legajo = self.cleaned_data.get('legajo', '').strip()

        empleado = super().save(commit=commit)

        if commit:
            self.aplicar_rol(empleado, tipo, matricula, legajo)

        return empleado

    @staticmethod
    def aplicar_rol(empleado, tipo, matricula, legajo):
        if tipo == 'veterinario':
            if hasattr(empleado, 'estudiantes'):
                Estudiantes.objects.filter(pk=empleado.pk).delete()

            vet, created = Veterinario.objects.get_or_create(
                empleado=empleado,
                defaults={'matriculaHabilitante': matricula}
            )
            if not created and vet.matriculaHabilitante != matricula:
                vet.matriculaHabilitante = matricula
                vet.save()

        elif tipo == 'estudiante':
            # Si antes era veterinario, remover ese rol
            if hasattr(empleado, 'veterinario'):
                Veterinario.objects.filter(pk=empleado.pk).delete()

            est, created = Estudiantes.objects.get_or_create(
                empleado=empleado,
                defaults={'legajo': legajo}
            )
            if not created and est.legajo != legajo:
                est.legajo = legajo
                est.save()

        else:  # Personal General
            if hasattr(empleado, 'veterinario'):
                Veterinario.objects.filter(pk=empleado.pk).delete()
            if hasattr(empleado, 'estudiantes'):
                Estudiantes.objects.filter(pk=empleado.pk).delete()


# Formularios de modelos
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
        fields = [
            'nroHistoriaClinica',
            'nombre',
            'fechaNacimiento',
            'sexo',
            'raza',
            'duenio',
            'sucursal',
            'pesoActual',
            'alturaActual',
            'imagen',
            'activo',
        ]

    def clean_pesoActual(self):
        peso = self.cleaned_data.get('pesoActual')
        if peso is not None and peso <= 0:
            raise forms.ValidationError("El peso debe ser mayor a 0 kg.")
        return peso

    def clean_alturaActual(self):
        altura = self.cleaned_data.get('alturaActual')
        if altura is not None and altura <= 0:
            raise forms.ValidationError("La altura debe ser mayor a 0 cm.")
        return altura


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

    def clean(self):
        cleaned_data = super().clean()
        existente = cleaned_data.get('cantidadExistente')
        minima = cleaned_data.get('cantidadMinima')
        if existente is not None and minima is not None:
            if existente < 0 or minima < 0:
                raise forms.ValidationError("Las cantidades de stock no pueden ser números negativos.")
        return cleaned_data
