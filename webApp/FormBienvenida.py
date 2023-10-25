from django import forms

class FormularioBienvenida(forms.Form):
    Nombre = forms.CharField(max_length=200, required=True)
    DNI = forms.CharField(max_length=9, required=True)
    Mail = forms.EmailField(required=True)