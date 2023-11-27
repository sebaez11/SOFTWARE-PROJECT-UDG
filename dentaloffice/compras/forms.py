from django import forms
from .models import Compra

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['productos']

class EditCompraStatusForm(forms.Form):
    ESTADO_CHOICES = [
        ('solicitado', 'Solicitado'),
        ('entregado', 'Entregado'),
    ]

    compra_id = forms.IntegerField(widget=forms.HiddenInput())
    nuevo_estado = forms.ChoiceField(choices=ESTADO_CHOICES)
