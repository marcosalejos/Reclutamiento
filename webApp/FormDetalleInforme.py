from django import forms

class FormularioDetalleInforme(forms.Form):

    Email = forms.EmailField(required=False)