from django import forms
from datetime import date

class FormularioCandidato(forms.Form):

    TALLASCHOICES = (
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )
    AREAFIRMACHOICES = (
        ('Ingenieria', 'Ingenieria'),
        ('Fabricación', 'Fabricación'),
        ('MTEA', 'MTEA'),
        ('Valores y Personas', 'Valores y Personas'),
        ('Administración y Finanzas', 'Administración y Finanzas'),
        ('Tecnologías de la Información', 'Tecnologías de la Información'),
        ('Comercial', 'Comercial'),
        ('Compras y Aprovisionamiento', 'Compras y Aprovisionamiento'),
    )

    HORASEXTRACHOICES = (
        ("Tecnico 1", "Tecnico 1"),
        ("Tecnico 2", "Tecnico 2"),
        ("Tecnico 3", "Tecnico 3"),
        ("Jefe Equipo", "Jefe Equipo"),
        ("Tecnico Junior", "Tecnico Junior"),
        ("Tecnico Semi Senior", "Tecnico Semi Senior"),
        ("Tecnico Master", "Tecnico Master")
    )

    SEXO_CHOICES = (
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer')
    )
    TURNO_CHOICES = (
        ("Mañana", "Mañana"),
        ("Tarde", "Tarde"),
        ("Noche", "Noche"),
        ("Central", "Central"),
        ("Qunto turno", "Quinto turno")
    )
    CENTROCOMP_CHOICES = (
        ("Mecanico", "Mecanico"),
        ("Electrico", "Electrico"),
        ("Ingenieria", "Ingenieria")
    )
    JORNADA_CHOICES = (
        ("Parcial", "Parcial"),
        ("Completa", "Completa")
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
    CodPais = forms.CharField(max_length=2, required=True)
    ControlDig = forms.CharField(max_length=2, required=True)
    EntBanc = forms.CharField(max_length=4, required=True)
    SucBanc = forms.CharField(max_length=4, required=True)
    ControlDig2 = forms.CharField(max_length=2, required=True)
    Cuenta = forms.CharField(max_length=10, required=True)

    Sociedad = forms.CharField(max_length=75, required=True)
    Seccion = forms.CharField(max_length=100, required=True)
    FechaIncorporacion = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    Categoria = forms.CharField(max_length=100, required=True)
    CategoriaSage = forms.CharField(max_length=100, required=True)
    Convenio = forms.CharField(max_length=100, required=True)
    SBA = forms.CharField(max_length=255, required=True)
    Centro = forms.CharField(max_length=40, required=True)
    CentroComp = forms.ChoiceField(choices=CENTROCOMP_CHOICES, required=False)
    Puesto = forms.CharField(max_length=200, required=True)

    TurnoInicial = forms.ChoiceField(choices=TURNO_CHOICES, required=True)
    Jornada = forms.ChoiceField(choices=JORNADA_CHOICES, required=True)
    Horas = forms.IntegerField(required=True)

    TallaPolo = forms.ChoiceField(choices=TALLASCHOICES, required=True, initial='M')
    TallaPantalon = forms.ChoiceField(choices=TALLASCHOICES, required=True, initial='M')
    TallaChaqueta =  forms.ChoiceField(choices=TALLASCHOICES, required=True, initial='M')
    TallaZapatos = forms.IntegerField(required=True, initial=43)
    HorasExtra = forms.ChoiceField(choices=HORASEXTRACHOICES, required=True)
    AreaFirma = forms.ChoiceField(required=True, choices=AREAFIRMACHOICES, widget = forms.Select(attrs = {'onchange' : "setPuestoFirma();"}))
