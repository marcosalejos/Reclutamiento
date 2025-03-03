from django import forms
import pyodbc
from django.core import validators


class FormularioSuscriptores(forms.Form):

    try:
        
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=serversage.database.windows.net;DATABASE=Reclutamiento;UID=SageAdmin;PWD=Sistemas.30')
        print("Conexion establecida")
        cursor = conexion.cursor()

        cursor.execute("SELECT id, Nombre FROM webApp_oferta WHERE webApp_oferta.Estado = 'Activo'")
        ofertas = cursor.fetchall()


    except Exception as e:
        print(e)

    OFERTAS_CHOICES = []

    for i in range(len(ofertas)):
        tupla = (ofertas[i][0], ofertas[i][1])
        OFERTAS_CHOICES.append(tupla)

    Suscriptor = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    Telefono = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    Ofertas = forms.ChoiceField(choices=OFERTAS_CHOICES)


    def clean_Telefono(self):
        try:
            suscriptor = self.cleaned_data["Suscriptor"]
        except:
            raise forms.ValidationError("El mail no es valido")
        telefono = self.cleaned_data["Telefono"]
        if not telefono and not suscriptor:
            raise forms.ValidationError("Debe proporcionar al menos un metodo de suscripción")
        if not suscriptor:
            if len(str(telefono)) != 9:
                raise forms.ValidationError("El teléfono debe tener 9 dígitos")
        return telefono