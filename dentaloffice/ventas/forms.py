from django import forms
from .models import Venta
from pacientes.models import Paciente

class VentaForm(forms.ModelForm):
    paciente_nombre = forms.CharField(max_length=100)

    class Meta:
        model = Venta
        fields = ['paciente_nombre', 'productos']