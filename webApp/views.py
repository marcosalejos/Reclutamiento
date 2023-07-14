import json
from django.shortcuts import render, redirect
from webApp.FormAsignacion import FormularioAsignacion
from webApp.FormCandidato import FormularioCandidato
from . import models
from datetime import date
from .FormSolicitud import FormularioSolicitud
from .FormObservaciones import FormularioObservaciones
from .FormSuscriptores import FormularioSuscriptores
import pyodbc
import requests

def SendMail(body, destinatario, subject):
    tenant_id = '846f6db3-c6a6-4131-b084-cf6b63ab8af5'
    client_id = '5bd04eae-8f60-4d26-9288-4d3cae02c048'
    client_secret = '5WA8Q~cUSLccqcdBZreZB3f-sz-B8WIN22Hu4cHL'

    # Obtener token de acceso
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        # Aquí puedes usar el access_token para realizar llamadas a la API de Microsoft Graph
        print("Token de acceso obtenido correctamente.")

        userId = "5d554bbe-7b0d-4fe1-a2f2-6e39a64691ab"
        endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
        toUserEmail = destinatario

        email_msg = {'Message': {'Subject': subject,
                                    'Body': {'ContentType': 'Text', 'Content': body},
                                    'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}]
                                    },
                        'SaveToSentItems': 'true'}
        r = requests.post(endpoint, headers={'Authorization': 'Bearer ' + access_token}, json=email_msg)

        if r.ok:
            print('Sent email successfully')
        else:
            print(r.json())


    else:
        print("Error al obtener el token de acceso:", response.text)


def Conexion():
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=serversage.database.windows.net;DATABASE=Reclutamiento;UID=SageAdmin;PWD=Sistemas.30')
    cursor = conexion.cursor()
    return cursor


def ofertas(request):
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_oferta WHERE Estado = 'Activo'")
    ofertasActivas = cursor.fetchall()
    cursor.execute("SELECT * FROM webApp_oferta WHERE Estado = 'Inactivo'")
    ofertasInactivas = cursor.fetchall()
    return render(request, 'ofertas.html', {'ofertasActivas': ofertasActivas, 'ofertasInactivas': ofertasInactivas})


def home(request):

    return render(request, 'home.html')


def candidatos(request):

    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_candidato")
    candidatos = cursor.fetchall()

    return render(request, 'candidatos.html', {'candidatos': candidatos})

def registroCandidato(request, id):

    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion")
    solicitudes = cursor.fetchall()
    
    if request.method == 'POST':
        form = FormularioCandidato(request.POST)
        if form.is_valid():
            DNI = form.cleaned_data["DNI"]
            Nombre = form.cleaned_data["Nombre"]
            SolicitudId = request.POST.get("solicitudes")
            solicitud = models.Peticion.objects.get(id=SolicitudId)
            puesto = solicitud.Puesto
            candidato = models.Candidato.objects.get(id=id)
            candidato.DNI = DNI
            candidato.Nombre = Nombre
            candidato.Puesto = puesto
            candidato.PeticionID = solicitud
            candidato.save()

    else:
        form = FormularioCandidato()

    return render(request, 'registroCandidato.html', {'form':form, 'solicitudes':solicitudes, 'candidatoID':id})



def solicitud(request):

    if request.method == 'POST':
        form = FormularioSolicitud(request.POST)
        
        if form.is_valid():

            cursor = Conexion()
            motivo_dict = {

                "option1": "Sustitución por baja voluntaria del empleado/a (abandono de la empresa de manera voluntaria, presentando la carta de baja voluntaria)",
                "option2": "Sustitución por bajo desempeño (se procederá a la sustitución de un empleado por su bajo desempeño por otro nuevo)",
                "option3": "Sustitución por baja laboral o permiso retribuido (accidente laboral, maternidad, paternidad...)",
                "option4": "Incorporación debido a un nuevo proyecto (nueva necesidad de cliente vinculada a un proyecto concreto que requiere de incorporación; se trata de una incorporación fuera de la adenda)",
                "option5": "Incorporación por dimensionamiento del equipo (incorporación por crecimiento de la adenda)",
                "option6": "Incorporación por dimensionamiento del equipo (incorporación por crecimiento de la adenda)",
                "option7": "Sustitución por promoción, cambio de puesto o cambio de planta (empleado/a ha promocionado a otro puesto; empleado/a ha cambiado de puesto de trabajo; empleado/a mantiene sus funciones pero de planta)",
                "option8": "Otras"
            }

            solicitante = form.cleaned_data['Solicitante']
            centro = form.cleaned_data['Centro']
            vacantes = form.cleaned_data['Vacantes']
            observaciones = form.cleaned_data['Observaciones']
            puesto = request.POST.getlist('puestoTecnico')
            motivoValue = request.POST.get('light', '')
            motivo = motivo_dict.get(motivoValue)
            today = date.today()
            cursor.execute("INSERT INTO webApp_peticion(Solicitante, Puesto, Centro, Motivo, Vacantes, Observaciones, FechaSolicitud) VALUES(?, ?, ?, ?, ?, ?, ?)", (solicitante, puesto[0], centro, motivo, vacantes, observaciones, today))
            cursor.commit()
            destinatario = "pepe.montanana@okoa.tech"
            subject = "Nueva solicitud de personal " + str(today)
            body = solicitante + " ha enviado una nueva solicitud de personal para el puesto: " + puesto[0] + "\n\n"
            body += "Número de vacantes: " + str(vacantes) + "\n\n"
            body += "Observaciones:\n" + observaciones + "\n\n\n"
            body += "Por favor recuerde asociar esta solicitud con un proceso de selección existente o crear uno nuevo.\n\n"
            body += "Para mas información de la solicitud por favor acceda al listado de solicitudes: http://192.168.2.252/solicitudes/"
            SendMail(body, destinatario, subject)

    else:
        form = FormularioSolicitud()

    return render(request, 'solicitud.html', {'form': form})

def observacion(request, id):
    cursor = Conexion()
    cursor.execute("SELECT OfertaID_id FROM webApp_peticion WHERE id = ?", (id))
    oferta = cursor.fetchall()
    print(oferta[0][0])
    if request.method == 'POST':
        form = FormularioObservaciones(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data["Descripcion"]
            today = date.today()
            cursor.execute("INSERT INTO webApp_observacion VALUES (?,?,?,?)", (descripcion, today, oferta[0][0], id))
            cursor.commit()
            return redirect('/observacionesSolicitud/' + str(id))

    else:
        form = FormularioObservaciones()

    return render(request, 'observacion.html', {'form': form, "id": id})



def suscripciones(request):
    if request.method == 'POST':
        form = FormularioSuscriptores(request.POST)
        if form.is_valid():

            ofertas_seleccionadas = request.POST.getlist('ofertas_seleccionadas')
            email = form.cleaned_data['Suscriptor']
            telefono = form.cleaned_data['Telefono']
            
            if email == "":
                email = "vacio@vacio.com"

            if telefono == None:
                telefono = 1
            
            for oferta in ofertas_seleccionadas:


                of = models.Oferta.objects.get(id=oferta)
                
                try:
                    sus = models.Suscriptores.objects.get(mail=email, tlf=telefono, Oferta=of)
                    existe = True
                except Exception as e:
                    existe = False

                if not existe:
                    sus = models.Suscriptores(mail=email, tlf=telefono, Oferta=of)
                    sus.save()
                else:
                    print("El usuario ya esta registrado")
            
            

    else:
        form = FormularioSuscriptores()

    return render(request, 'suscripciones.html', {'form': form})

def solicitudesList(request):
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion")
    solicitudes = cursor.fetchall()
    contrataciones = 0

    return render(request, 'solicitudesList.html', {'solicitudes': solicitudes, 'contrataciones': contrataciones})

def deleteSolicitud(request, id):
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
    if len(observaciones) > 0:
        cursor.execute("DELETE webApp_observacion WHERE Solicitud_id = ?",(id))
        cursor.commit()
    cursor.execute("DELETE webApp_peticion WHERE id = ?", (id))
    cursor.commit()
    return redirect('/solicitudes')

def deleteObservacion(request, id, solicitudID):
    cursor = Conexion()
    cursor.execute("DELETE webApp_observacion WHERE id = ?", (id))
    cursor.commit()
    return redirect('/observacionesSolicitud/' + str(solicitudID))


def asignarOferta(request, id):
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (id))
    solicitud = cursor.fetchall()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
    print(observaciones)
    if request.method == 'POST':
        form = FormularioAsignacion(request.POST)
        if form.is_valid():
            oferta = form.cleaned_data["Ofertas"]
            cursor.execute("UPDATE webApp_peticion SET OfertaID_id = ? WHERE id = ?", (oferta, id))
            cursor.commit()
            if len(observaciones) > 0:
                for observacion in observaciones:
                    cursor.execute("UPDATE webApp_observacion SET Oferta_id = ? WHERE id = ?", (oferta, observacion[0]))
                    cursor.commit()
            return redirect('/solicitudes')

    else:
        form = FormularioAsignacion()
            
    
    return render(request, 'asignarOferta.html', {'solicitud':solicitud[0], 'form':form})

def observacionesSolicitud(request, id):

    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
    observaciones = sorted(observaciones, key=lambda x: x[2], reverse=True)
    #observaciones = ["alksdnlas", "aslkhdjasl", "Alsdhas", "ñlaksd", "Askdma", "alksdnlas", "aslkhdjasl", "Alsdhas", "ñlaksd", "Askdma"]
    return render(request, 'observacionesSoli.html', {'observaciones':observaciones, "id":id})