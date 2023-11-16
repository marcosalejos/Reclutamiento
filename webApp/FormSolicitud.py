from django import forms

class FormularioSolicitud(forms.Form):

    CENTRO_CHOICES = (
        ('FRESCOS DELISANO', 'FRESCOS DELISANO'),
        ('ANITIN', 'ANITIN'),
        ('COMEX BAKERY', 'COMEX BAKERY'),
        ('COBOPA', 'COBOPA'),
        ('PACFREN', 'PACFREN'),
        ('OKOA', 'OKOA'),
        ('DOLZ', 'DOLZ'),
        ('RAMAFRUT', 'RAMAFRUT'),
        ('Otro', 'Otro'),
    )

    #Solicitante = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    Centro = forms.ChoiceField(choices=CENTRO_CHOICES, required=True)
    Vacantes = forms.IntegerField(required=True)
    Observaciones = forms.CharField(widget=forms.Textarea, required=False)
    FechaIncorporacion = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )