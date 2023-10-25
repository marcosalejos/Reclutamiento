from django import forms

class FormularioDetalleInforme(forms.Form):

    Email = forms.EmailField(required=False)
    DNI = forms.FileField(required=False)
    SIP = forms.FileField(required=False)
    Titularidad = forms.FileField(required=False)