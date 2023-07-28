from django import forms
from datetime import date

class FormularioCandidato(forms.Form):

    SEXO_CHOICES = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer')
    )
    TURNO_CHOICES = (
        ("Mañana", "Mañana"),
        ("Tarde", "Tarde"),
        ("Noche", "Noche"),
        ("Central", "Central")
    )
    CENTROCOMP_CHOICES = (
        ("Mecanico", "Mecanico"),
        ("Electrico", "Electrico"),
        ("Ingenieria", "Ingenieria")
    )


    DNI = forms.CharField(max_length=9, required=True)
    Nombre = forms.CharField(max_length=200, required=True)
    FechaNacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'max': str(date.today())})
    )
    Telefono = forms.IntegerField(required=True)
    Mail = forms.EmailField(required=True)
    Sexo = forms.ChoiceField(choices=SEXO_CHOICES, required=True)
    Nacionalidad = forms.CharField(max_length=100, required=True)
    SIP = forms.IntegerField(required=True)
    Municipio = forms.CharField(max_length=150, required=True)
    Provincia = forms.CharField(max_length=100, required=True)
    Domicilio = forms.CharField(max_length=255, required=True)
    CP = forms.IntegerField(required=True)

    EntidadBank = forms.CharField(max_length=100, required=True)
    IBAN = forms.IntegerField(required=True)

    Sociedad = forms.CharField(max_length=75, required=True)
    Seccion = forms.CharField(max_length=100, required=True)
    FechaIncorporacion = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'min': str(date.today())})
    )
    Categoria = forms.CharField(max_length=100, required=True)
    Convenio = forms.CharField(max_length=100, required=True)
    SBA = forms.CharField(max_length=255, required=True)
    Centro = forms.CharField(max_length=40, required=True)
    CentroComp = forms.ChoiceField(choices=CENTROCOMP_CHOICES, required=False)
    Puesto = forms.CharField(max_length=200, required=True)

    TurnoInicial = forms.ChoiceField(choices=TURNO_CHOICES, required=True)
