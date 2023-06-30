import json
from django.shortcuts import render, redirect
from django.http import HttpResponse

from webApp.FormAsignacion import FormularioAsignacion
from webApp.FormCandidato import FormularioCandidato
from . import models
from datetime import date
from .FormSolicitud import FormularioSolicitud
from .FormObservaciones import FormularioObservaciones
from .FormSuscriptores import FormularioSuscriptores
import pyodbc
from django.contrib import messages


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

    else:
        form = FormularioSolicitud()

    return render(request, 'solicitud.html', {'form': form})

def observacion(request):
    ofertasDic = {}
    cursor = Conexion()
    cursor.execute("SELECT id, nombre FROM webApp_oferta WHERE Estado = 'Activo'")
    ofertas = cursor.fetchall()
    for oferta in ofertas:
        cursor.execute("SELECT id, Solicitante, Centro, Puesto FROM webApp_peticion WHERE OfertaID_id = ?", (oferta[0]))
        solicitudes = [list(row) for row in cursor.fetchall()] 
        ofertasDic[oferta[1]] = solicitudes
    jsondic = json.dumps(ofertasDic)

    if request.method == 'POST':
        form = FormularioObservaciones(request.POST)
        if form.is_valid():
            cursor = Conexion()
            oferta = request.POST.get('clave')
            solicitud = request.POST.get('valor')
            descripcion = form.cleaned_data["Descripcion"]
            today = date.today()
            of = models.Oferta.objects.get(Nombre=oferta)
            sol = models.Peticion.objects.get(id=solicitud)
            obs = models.Observacion(Descripcion=descripcion, Fecha=today, Oferta=of, Solicitud=sol)
            obs.save()
    else:
        form = FormularioObservaciones()

    return render(request, 'observacion.html', {'form': form, 'diccionario': ofertasDic, 'jsonDic':jsondic})



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
    cursor.execute("DELETE webApp_peticion WHERE id = ?", (id))
    cursor.commit()
    return redirect('/solicitudes')


def asignarOferta(request, id):
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (id))
    solicitud = cursor.fetchall()
    if request.method == 'POST':
        form = FormularioAsignacion(request.POST)
        if form.is_valid():
            oferta = form.cleaned_data["Ofertas"]
            cursor.execute("UPDATE webApp_peticion SET OfertaID_id = ? WHERE id = ?", (oferta, id))
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
    return render(request, 'observacionesSoli.html', {'observaciones':observaciones})