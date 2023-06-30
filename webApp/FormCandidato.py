from django import forms

class FormularioCandidato(forms.Form):

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

    DNI = forms.CharField(max_length=9, required=True)
    Nombre = forms.CharField(max_length=200, required=True)