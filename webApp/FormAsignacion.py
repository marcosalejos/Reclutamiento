from django import forms
import pyodbc


class FormularioAsignacion(forms.Form):

    try:
        
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=serversage.database.windows.net;DATABASE=Reclutamiento;UID=SageAdmin;PWD=Sistemas.30')
        cursor = conexion.cursor()

        cursor.execute("SELECT id, Nombre FROM webApp_oferta WHERE webApp_oferta.Estado = 'Activo'")
        ofertas = cursor.fetchall()


    except Exception as e:
        print(e)

    OFERTAS_CHOICES = []

    for i in range(len(ofertas)):
        tupla = (ofertas[i][0], ofertas[i][1])
        OFERTAS_CHOICES.append(tupla)
    print(OFERTAS_CHOICES)

    Ofertas = forms.ChoiceField(choices=OFERTAS_CHOICES)
