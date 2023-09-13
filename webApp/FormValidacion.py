from django import forms

class FormularioValidacion(forms.Form):

    EstadoValidacion = forms.CharField(widget=forms.Textarea, required=True)