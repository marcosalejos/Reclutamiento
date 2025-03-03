import base64
import json
from django.conf import settings
from django.shortcuts import render, redirect
from webApp.FormAsignacion import FormularioAsignacion
from webApp.FormCandidato import FormularioCandidato
from . import models
from datetime import date
from .FormSolicitud import FormularioSolicitud
from .FormObservaciones import FormularioObservaciones
from .FormSuscriptores import FormularioSuscriptores
from .FormValidacion import FormularioValidacion
from .FormDetalleInforme import FormularioDetalleInforme
from .FormDetalleSoli import FormularioDetalleSoli
from .FormBienvenida import FormularioBienvenida
from .FormIndicadores import FormularioIndicadores
import pyodbc
import pip._vendor.requests as requests
from django.shortcuts import get_object_or_404
import datetime
import os
import shutil

ms_identity_web = settings.MS_IDENTITY_WEB


adminList = []

solicitanteList = []


def GetGroupsMembers():
    token = Microsoft_Token()
    endpointGrupos = "https://graph.microsoft.com/v1.0/groups"

    r = requests.get(endpointGrupos, headers={'Authorization': 'Bearer ' + token})
    if r.ok:
        grupos = r.json()["value"]
        for grupo in grupos:
            if grupo["displayName"] == "VYP Permisos Minimos":
                id_grupo_min = grupo["id"]
            if grupo["displayName"] == "VYP Permisos Admin":
                id_grupo_admin = grupo["id"]
        
        endpointMembersMin = f"https://graph.microsoft.com/v1.0/groups/{id_grupo_min}/members"
        endpointMembersAdmin = f"https://graph.microsoft.com/v1.0/groups/{id_grupo_admin}/members"
        r1 = requests.get(endpointMembersMin, headers={'Authorization': 'Bearer ' + token})
        if r1.ok:
            usuariosMin = r1.json()["value"]
            for usuario in usuariosMin:
                if usuario["displayName"] not in solicitanteList:
                    solicitanteList.append(usuario["displayName"])
        
        r2 = requests.get(endpointMembersAdmin, headers={'Authorization': 'Bearer ' + token})
        if r2.ok:
            usuariosAdmin = r2.json()["value"]
            for usuario in usuariosAdmin:
                if usuario["displayName"] not in adminList:
                    adminList.append(usuario["displayName"])


#LOGIN
def index(request):
    GetGroupsMembers()
    if request.identity_context_data.authenticated:
        nombre = request.identity_context_data.username
        if nombre in adminList or nombre in solicitanteList:
            return redirect('home')
        else:
            return render(request, 'auth/401.html', {'nombre': nombre})
    else:
        return render(request, "login.html")
    
def MailErrorLog(destinatario):
    log = open("C:/Reclutamiento/mail_log.txt", "a")
    now = datetime.datetime.now()
    log.write(str(now))
    log.write("\n")
    log.write("Se ha intentado enviar un mail a " + destinatario)
    log.write("\n")
    log.write("\n")
    log.close()

def Microsoft_Token():
    tenant_id = '846f6db3-c6a6-4131-b084-cf6b63ab8af5'
    client_id = '5bd04eae-8f60-4d26-9288-4d3cae02c048'

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
        return access_token
    else:
        print("Error al obtener el token de acceso:", response.text)

def SendMail(body, destinatario, subject):
    
    access_token = Microsoft_Token()

    if access_token is not None:
        userId = "14303bd0-b1b6-4e7e-96ce-b51f4ae306c9"
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
            MailErrorLog(destinatario)
            print(r.json())

def SendMailAdj(body, destinatario, subject, adjuntos):

    access_token = Microsoft_Token()

    if access_token is not None:
        userId = "14303bd0-b1b6-4e7e-96ce-b51f4ae306c9"
        endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
        toUserEmail = destinatario

        email_msg = {
            'Message': 
                {
                    'Subject': subject,
                    'Body': {'ContentType': 'Text', 'Content': body},
                    'ToRecipients': [{'EmailAddress': {'Address': toUserEmail}}],
                    'attachments': []
                },
            'SaveToSentItems': 'true'
        }
        for adj in adjuntos:
            file_name = adj.split("\\")[-1]
            file_content = open(adj, 'rb').read()
            adjunto = {
                '@odata.type': '#microsoft.graph.fileAttachment',
                'name': file_name,
                'contentBytes': base64.b64encode(file_content).decode('utf-8')
            }
            email_msg['Message']['attachments'].append(adjunto)

        r = requests.post(endpoint, headers={'Authorization': 'Bearer ' + access_token}, json=email_msg)
        if r.ok:
            print('Sent email successfully')
        else:
            MailErrorLog(destinatario)
            print(r.json())
    
def Reenvio(destinatario):
    token = Microsoft_Token()
    userId = "14303bd0-b1b6-4e7e-96ce-b51f4ae306c9"
    messageId = "AAMkADAwZjIwOGI4LTEzMWItNDMxMS05NDU1LWViZTAwNWMxM2U0YgBGAAAAAAA3qt44l6VsSZkSLLEHTbzqBwACQi3UMN5pTpNHztilKT37AAAAAAEMAAACQi3UMN5pTpNHztilKT37AACJPMexAAA="
    endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/messages/{messageId}/forward'
    email_msg = {
        'toRecipients': [{'emailAddress': {'address': destinatario}}],
        }
    
    r = requests.post(endpoint, headers={'Authorization': 'Bearer ' + token}, json=email_msg)
    if r.ok:
        print('Sent email successfully')
    else:
        MailErrorLog(destinatario)
        print(r.json())

def Conexion():
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=serversage.database.windows.net;DATABASE=Reclutamiento;UID=SageAdmin;PWD=Sistemas.30')
    cursor = conexion.cursor()
    return cursor

@ms_identity_web.login_required
def ofertas(request):

    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_oferta WHERE Estado = 'Activo'")
    ofertasActivas = cursor.fetchall()
    cursor.execute("SELECT * FROM webApp_oferta WHERE Estado = 'Inactivo'")
    ofertasInactivas = cursor.fetchall()
    cursor.close()
    return render(request, 'auth/ofertas.html', {'ofertasActivas': ofertasActivas, 'ofertasInactivas': ofertasInactivas, 'nombre':nombre, 'adminList':adminList})

@ms_identity_web.login_required
def home(request):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    

    return render(request, 'auth/home.html', {'nombre': nombre, 'adminList':adminList})

@ms_identity_web.login_required
def candidatos(request):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_candidato")
    candidatos = cursor.fetchall()
    candidatos.sort(reverse=True)
    cursor.close()
    return render(request, 'auth/candidatos.html', {'candidatos': candidatos})

@ms_identity_web.login_required
def validarSoli(request, id):
    
    nombre = request.identity_context_data.username
    if nombre != "Reijer Domingo" and nombre != "Marcos Alejos":
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (id))
    solicitud = cursor.fetchall()
    solicitud = solicitud[0]
    solicitante = solicitud[1]
    puesto = solicitud[2]
    centro = solicitud[3]

    if request.method == 'POST':
        form = FormularioValidacion(request.POST)
        if form.is_valid():
            destinatario = 'valoresypersonas@okoa.tech'
            toggleValue = request.POST.get("rdo")
            subject = "Solicitud " + str(id) + toggleValue
            body = "La solicitud de " + solicitante + " para el puesto " + puesto + " en el centro " + centro + " ha sido " + toggleValue
            SendMail(body, destinatario, subject)
            estadoValidacion = form.cleaned_data["EstadoValidacion"]
            cursor.execute("UPDATE webApp_peticion SET Validado = 'True', EstadoValidacion = ?, EstadoMotivo = ? WHERE id = ?", (toggleValue, estadoValidacion, id))
            cursor.commit()
            cursor.close()
            return redirect('/solicitudes')
    else:
        form = FormularioValidacion()


    return render(request, 'auth/validarSoli.html',{"form":form , "solicitud": solicitud, "solicitudID": solicitud[0]})

def DestPlanta(Centro, CentroComp):

    dest_planta = ""

    if Centro == "COBOPA":
        dest_planta = "francisco.samper@okoa.tech"
    elif Centro == "ANITIN":
        dest_planta = "ivan.minana@okoa.tech"
    elif Centro == "COMEX BAKERY":
        dest_planta = "carlos.desco@okoa.tech"
    elif Centro == "FRESCOS DELISANO":
        dest_planta = "enrique.verdu@okoa.tech"
    elif Centro == "PACFREN":
        dest_planta = "luis.malonda@okoa.tech"
    elif Centro == "OKOA":
        if CentroComp == "Mecanico":
            dest_planta = "jordi.lisarde@okoa.tech"
        elif CentroComp == "Electrico":
            dest_planta = "patricia.peiro@okoa.tech"
        elif CentroComp == "Ingenieria":
            dest_planta = "rafael.noverjes@okoa.tech"

    return dest_planta

@ms_identity_web.login_required
def detalleInforme(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_candidato WHERE id = ?", (id))
    candidato = cursor.fetchall()
    candidato = candidato[0]
    ofertaId = candidato[14]
    cursor.execute("SELECT Nombre FROM webApp_oferta WHERE id = ?", (ofertaId))
    oferta = cursor.fetchall()
    oferta = oferta[0][0]
    cursor.close()
    
    Centro = candidato[24]
    CentroComp = candidato[31]

    dest_planta = DestPlanta(Centro, CentroComp)
    dest_asesoria = "marta.juan@okoa.tech"
    dest_prl = "prevencion@okoa.tech"
    dest_soporte = "soporte@okoa.tech"
    dest_factorial = "lorena.cano@okoa.tech"
    dest_administracion2 = 'ivon.gasco@okoa.tech'
    mails = []
    secciones = []

    if request.method == 'POST':
        form = FormularioDetalleInforme(request.POST, request.FILES)
        if form.is_valid():

            adjuntos = []
            try:
                file_dni = request.FILES['DNI']
                adjuntos.append(file_dni)
            except:
                adjuntos.append(None)
            try:
                file_sip = request.FILES['SIP']
                adjuntos.append(file_sip)
            except:
                adjuntos.append(None)
            try:
                file_titularidad = request.FILES['Titularidad']
                adjuntos.append(file_titularidad)
            except:
                adjuntos.append(None)
            
            rutas = []
            for adj in adjuntos:
                if adj is not None:
                    save_path = os.path.join(settings.MEDIA_ROOT, 'uploadFiles', adj.name) # Define la ruta de destino
                    rutas.append(save_path)
                    with open(save_path, 'wb') as destination:
                        for chunk in adj.chunks():
                            destination.write(chunk)

            if 'asesoriaMail' in request.POST:
                mails.append(dest_asesoria)
            else:
                mails.append("")
            if 'prlMail' in request.POST:
                mails.append(dest_prl)
            else:
                mails.append("")
            if 'plantaMail' in request.POST:
                mails.append(dest_planta)
            else:
                mails.append("") 
            if 'soporteMail' in request.POST:
                mails.append(dest_soporte)
            else:
                mails.append("")
            if 'factorialMail' in request.POST:
                mails.append(dest_factorial)
            else:
                mails.append("")

            extraMail = form.cleaned_data["Email"]
            mails.append(extraMail)
            mails.append(dest_administracion2)

            # Mails = [asesoria, prl, planta, soporte, factorial, extra, administracion2] 0-6
            #Para comprobar el valor del Checkbox
            if 'asesoria' in request.POST:
                secciones.append(True)
            else:
                secciones.append(False)
            
            if 'prl' in request.POST:
                secciones.append(True)
            else:
                secciones.append(False)

            if 'planta' in request.POST:
                secciones.append(True)
            else:
                secciones.append(False)

            InformeCandidato2(candidato, oferta, mails, secciones, rutas)

            return redirect('/candidatos')
            
    else:
        form = FormularioDetalleInforme()

    return render(request, 'auth/detalleInforme.html', 
                  {
                    'form': form,
                    'candidato': candidato,
                    'oferta':oferta,
                    'mailAsesoria': dest_asesoria,
                    'mailPRL': dest_prl,
                    'mailPlanta': dest_planta,
                    'mailSoporte': dest_soporte,
                    'mailFactorial': dest_factorial
                    })

@ms_identity_web.login_required
def CalendarioInc(request):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    cursor.execute("SELECT id, Nombre, FechaIncorporacion FROM webApp_candidato WHERE Estado = 'Registrado'")
    candidatos = cursor.fetchall()
    data = []

    for candidato in candidatos:
        fecha = candidato[2].strftime("%Y-%m-%d")
        tupla = (candidato[0], candidato[1], fecha)
        data.append(tupla)

    json_data = json.dumps(data)

    return render(request, 'auth/calendario.html', {'data': json_data})

def InformeCandidato2(candidato, oferta, mails, secciones, rutas):

    Nombre = candidato[1]
    DNI = candidato[2]
    FechaNacimiento = candidato[3]
    Nacionalidad = candidato[5]
    Mail = candidato[7]
    Puesto = candidato[21]
    FechaContrata = candidato[17]
    FechaInc = candidato[19]
    Sociedad = candidato[29]
    Categoria = candidato[23]
    Convenio = candidato[25]
    Seccion = candidato[28]
    Centro = candidato[24]
    CentroComp = candidato[31]
    SBA = candidato[26]
    EntidadBank = candidato[11]
    IBAN = candidato[12]
    SIP = candidato[27]
    TurnoIni = candidato[30]
    TallaPolo = candidato[37]
    TallaPantalon = candidato[36]
    TallaChaqueta = candidato[35]
    TallaZapatos = candidato[38]
    HorasExtra = candidato[39]
    CategoriaSage = candidato[40]
    AreaOutlook = candidato[41]
    PuestoOutlook = candidato[42]
    
    data_asesoria = [Nombre, DNI, SIP, FechaNacimiento, Nacionalidad, oferta, Puesto, 
                     FechaContrata, Sociedad, Categoria, Convenio, Seccion, Centro, FechaInc, SBA,
                     EntidadBank, IBAN, CategoriaSage]
    
    dataPRL = [Nombre, DNI, Sociedad, Centro, FechaInc,TallaPolo ,TallaPantalon ,TallaChaqueta ,TallaZapatos, CategoriaSage]

    dataPlanta = [Nombre, DNI, oferta, Puesto, FechaContrata, FechaInc, TurnoIni]


    Subject = "Información Nueva Contratación"

    body = IntroMsg()
    body += AsesoriaMsg(data_asesoria, False)
    body += EndMsg()
    if mails[0] != "":
        if len(rutas) > 0:
            SendMailAdj(body, mails[0], Subject, rutas)
        else:
            SendMail(body, mails[0], Subject)

    if mails[5] != "":
        if secciones[0] == True: #Asesoria
            SendMail(body, mails[5], Subject)

    body = IntroMsg()
    body += AsesoriaMsg(data_asesoria, True)
    body += EndMsg()
    if mails[4] != "":
        SendMail(body, mails[4], Subject)
    
    body = IntroMsg()
    body += PrlMsg(dataPRL, False)
    body += EndMsg()
    if mails[1] != "":
        SendMail(body, mails[1], Subject)

    if mails[5] != "":
        if secciones[1] == True: #PRL
            SendMail(body, mails[5], Subject)

    #Mail para Ivon
    body = IntroMsg()
    body += PrlMsg(dataPRL, True)
    body += EndMsg()
    if mails[6] != "":
        SendMail(body, mails[6], Subject)


    body = IntroMsg()
    body += PlantaMsg(dataPlanta)
    body += EndMsg()
    if mails[2] != "":
        SendMail(body, mails[2], Subject)
        SendMail(body, mails[6], Subject)

    if mails[5] != "":
        if secciones[2] == True: #Planta
            SendMail(body, mails[5], Subject)

    body = IntroMsg()
    body += "Por favor prepara todo el equipo necesario para la nueva incorporación." + "\n"
    body += "Nombre comlpeto: " + Nombre + "\n"
    body += "Mail personal: " + str(Mail) + "\n"
    body += "Fecha Incorporación: " + str(FechaInc) + "\n"
    body += "Sección/Área: " + Seccion + "\n"
    body += "Puesto de Trabajo: " + Puesto + "\n"
    body += "Centro: " + Centro + "\n" 
    body += "Área Firma: " + str(AreaOutlook) + "\n"
    body += "Puesto Firma: " + str(PuestoOutlook) + "\n"
    if mails[2] != "":
        body += "Responsable: " + mails[2] + "\n"
    elif mails[2] == "":
        mails[2] = DestPlanta(Centro, CentroComp)
        body += "Responsable: " + mails[2] + "\n"
    body += EndMsg()
    if mails[3] != "":
        SendMail(body, mails[3], Subject)
        SendMail(body, "soporte.okoa@civired.com", Subject)
    
    if mails[5] == "ivon.gasco@okoa.tech":
        body = IntroMsg()
        body += "Nombre completo: " + data_asesoria[0] + "\n"
        body += "DNI: " + data_asesoria[1] + "\n"
        body += "Convenio de Horas Extra: " + str(HorasExtra) + "\n"
        body += EndMsg()
        SendMail(body, mails[5], Subject)
    
def IntroMsg():
    intro = ""
    hora = datetime.datetime.now().time()
    mediodia = datetime.time(14,0)
    if hora >= mediodia:
        intro = "Buenas tardes," + "\n"
    else:
        intro = "Buenos días," + "\n"

    intro += "Comunicamos que se va a incorporar con nosotros un nuevo empleado, os adjuntamos los datos referentes en la ficha." + "\n\n"
    return intro

def EndMsg():
    end = "Muchas gracias," + "\n\n"
    end += "Cualquier duda contactar con valoresypersonas@okoa.tech" + "\n\n"
    end += "Un saludo." "\n"
    return end

def AsesoriaMsg(data, factorial):
    body_asesoria = "Nombre completo: " + data[0] + "\n"
    body_asesoria += "DNI: " + data[1] + "\n"
    body_asesoria += "Número SIP: " + str(data[2]) + "\n"
    body_asesoria += "Fecha de Nacimiento: " + str(data[3]) + "\n"
    body_asesoria += "Nacionalidad: " + data[4] + "\n"
    body_asesoria += "Proceso de Selección: " + data[5] + "\n"
    body_asesoria += "Puesto de Trabajo: " + data[6] + "\n"
    body_asesoria += "Fecha de Aceptación: " + str(data[7]) + "\n"
    body_asesoria += "Sociedad: " + data[8] + "\n"
    body_asesoria += "Categoria: " + data[9] + "\n"
    body_asesoria += "Categoria Sage: " + data[17] + "\n"
    body_asesoria += "Convenio: " + data[10] + "\n"
    body_asesoria += "Sección/Área: " + data[11] + "\n"
    body_asesoria += "Centro de Trabajo: " + data[12] + "\n"
    body_asesoria += "Fecha de Incorporación: " + str(data[13]) + "\n"
    if not factorial:
        body_asesoria += "S.B.A Pactado: " + data[14] + "\n"
    body_asesoria += "Entidad Bancária: " + data[15] + "\n"
    body_asesoria += "IBAN: " + str(data[16]) + "\n\n"

    return body_asesoria

def PrlMsg(data, carol):
    body_prl = "Nombre completo: " + data[0] + "\n"
    body_prl += "DNI: " + data[1] + "\n"
    body_prl += "Sociedad: " + data[2] + "\n"
    body_prl += "Centro de Trabajo: " + data[3] + "\n"
    body_prl += "Fecha de Incorporación: " + str(data[4]) + "\n"
    body_prl += "Talla Polo: " + str(data[5]) + "\n"
    body_prl += "Talla Pantalon: " + str(data[6]) + "\n"
    body_prl += "Talla Chaqueta: " + str(data[7]) + "\n"
    body_prl += "Talla Zapatos: " + str(data[8]) + "\n"
    if carol:
        body_prl += "Categoria Sage: " + str(data[-1]) + "\n"

    return body_prl

def PlantaMsg(data):
    body_planta = "Nombre completo: " + data[0] + "\n"
    body_planta += "DNI: " + data[1] + "\n"
    body_planta += "Proceso de Selección: " + data[2] + "\n"
    body_planta += "Puesto de Trabajo: " + data[3] + "\n"
    body_planta += "Fecha de Aceptación: " + str(data[4]) + "\n"
    body_planta += "Fecha de Incorporación: " + str(data[5]) + "\n"
    body_planta += "Turno Incial: " + data[6] + "\n\n"
    return body_planta

@ms_identity_web.login_required 
def registroCandidato(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    
    cursor.execute("SELECT * FROM webApp_candidato WHERE id = ?", (id))
    candidato = cursor.fetchall()
    candidato = candidato[0]
    ofertaID = candidato[14] #Oferta desde la que se contrata
    puestoFirma = candidato[42]

    cursor.execute("SELECT * FROM webApp_peticion WHERE Estado = 'Abierta' and EstadoValidacion = 'Aprobada' and OfertaID_id = ?", (ofertaID))
    solicitudes = cursor.fetchall()

    soliID = candidato[15] #Solicitud asignada al candidato
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (soliID))
    candidatoSolicitud = cursor.fetchall()
    cursor.close()
    if len(candidatoSolicitud) > 0:
        candidatoSolicitud = candidatoSolicitud[0]
    if request.method == 'POST':
        form = FormularioCandidato(request.POST)
        if form.is_valid():
            DNI = form.cleaned_data["DNI"]
            Nombre = form.cleaned_data["Nombre"]
            FechaNacimiento = form.cleaned_data["FechaNacimiento"]
            Sexo = form.cleaned_data["Sexo"]
            Mail = form.cleaned_data["Mail"]
            Telefono = form.cleaned_data["Telefono"]
            Nacionalidad = form.cleaned_data["Nacionalidad"]
            SIP = form.cleaned_data["SIP"]
            Municipio = form.cleaned_data["Municipio"]
            Provincia = form.cleaned_data["Provincia"]
            Domicilio = form.cleaned_data["Domicilio"]
            CP = form.cleaned_data["CP"]
            EntidadBank = form.cleaned_data["EntidadBank"]
            
            Sociedad = form.cleaned_data["Sociedad"]
            Categoria = form.cleaned_data["Categoria"]
            Seccion = form.cleaned_data["Seccion"]
            Convenio = form.cleaned_data["Convenio"]
            FechaIncorporacion = form.cleaned_data["FechaIncorporacion"]
            SBA = form.cleaned_data["SBA"]
            TurnoIni = form.cleaned_data["TurnoInicial"]

            SolicitudData = request.POST.get("solicitudes")
            SolicitudId, sobrante = SolicitudData.split('-')
            Centro = form.cleaned_data["Centro"]
            CentroComp = form.cleaned_data["CentroComp"]
            Puesto = form.cleaned_data["Puesto"]

            CodPais = form.cleaned_data["CodPais"]
            ControlDig = form.cleaned_data["ControlDig"]
            EntBanc = form.cleaned_data["EntBanc"]
            SucBanc = form.cleaned_data["SucBanc"]
            ControlDig2 = form.cleaned_data["ControlDig2"]
            Cuenta = form.cleaned_data["Cuenta"]
            IBAN = CodPais + str(ControlDig) + str(EntBanc) + str(SucBanc) + str(ControlDig2) + str(Cuenta)

            Jornada = form.cleaned_data["Jornada"]
            Horas = form.cleaned_data["Horas"]

            TallaPolo = form.cleaned_data["TallaPolo"]
            TallaPantalon = form.cleaned_data["TallaPantalon"]
            TallaChaqueta = form.cleaned_data["TallaChaqueta"]
            TallaZapatos = form.cleaned_data["TallaZapatos"]
            HorasExtra = form.cleaned_data["HorasExtra"]
            CategoriaSage = form.cleaned_data["CategoriaSage"]
            AreaFirma = form.cleaned_data["AreaFirma"]
            PuestoFirma = request.POST.get("puestoFirma")
    
            if Centro != "OKOA":
                CentroComp = None

            cursor2 = Conexion()
            cursor2.execute("SELECT Puesto FROM webApp_peticion WHERE id = ?", (SolicitudId))
            puesto = cursor2.fetchall()
            puesto = puesto[0][0]
            if soliID is None:
                cursor2.execute("UPDATE webApp_peticion SET Contratados = Contratados + 1 WHERE id = ?", (SolicitudId))

                cursor2.execute("""UPDATE webApp_candidato SET Nombre = ?, DNI = ?, FechaNacimiento = ?, Sexo = ?, 
                                Nacionalidad = ?, Telefono = ?, Mail = ?, Municipio = ?, CP = ?, Provincia = ?,
                                EntidadBancaria = ?, IBAN = ?, Domicilio = ?, PeticionID_id = ?, Estado = 'Registrado',
                                FechaIncorporacion = ?, Puesto = ?, Categoria = ?, CategoriaSage = ?, Centro = ?, Convenio = ?,
                                SBA = ?, SIP = ?, Seccion = ?, Sociedad = ?, TurnoInicial = ?, CentroComp = ?, Horas = ?, Jornada = ?,
                                TallaPolo = ?, TallaPantalon = ?, TallaChaqueta = ?, TallaZapatos = ?, HorasExtra = ?, AreaOutlook = ?,
                                PuestoOutlook = ?
                                 WHERE id = ?""", 
                                (Nombre, DNI, FechaNacimiento, Sexo, Nacionalidad, Telefono, Mail, Municipio, CP, Provincia,
                                 EntidadBank, IBAN, Domicilio, SolicitudId, FechaIncorporacion, Puesto, Categoria, CategoriaSage, Centro,
                                 Convenio, SBA, SIP, Seccion, Sociedad, TurnoIni, CentroComp, Horas, Jornada, TallaPolo, TallaPantalon,
                                 TallaChaqueta, TallaZapatos, HorasExtra, AreaFirma, PuestoFirma,  id))
                
            elif soliID == SolicitudId:
                cursor2.execute("""UPDATE webApp_candidato SET Nombre = ?, DNI = ?, FechaNacimiento = ?, Sexo = ?, 
                                Nacionalidad = ?, Telefono = ?, Mail = ?, Municipio = ?, CP = ?, Provincia = ?,
                                EntidadBancaria = ?, IBAN = ?, Domicilio = ?, PeticionID_id = ?, Estado = 'Registrado',
                                FechaIncorporacion = ?, Puesto = ?, Categoria = ?, CategoriaSage = ?, Centro = ?, Convenio = ?,
                                SBA = ?, SIP = ?, Seccion = ?, Sociedad = ?, TurnoInicial = ?, CentroComp = ?, Horas = ?, Jornada = ?,
                                TallaPolo = ?, TallaPantalon = ?, TallaChaqueta = ?, TallaZapatos = ?, HorasExtra = ?, AreaOutlook = ?,
                                PuestoOutlook = ?
                                 WHERE id = ?""", 
                                (Nombre, DNI, FechaNacimiento, Sexo, Nacionalidad, Telefono, Mail, Municipio, CP, Provincia,
                                 EntidadBank, IBAN, Domicilio, SolicitudId, FechaIncorporacion, Puesto, Categoria, CategoriaSage, Centro,
                                 Convenio, SBA, SIP, Seccion, Sociedad, TurnoIni, CentroComp, Horas, Jornada, TallaPolo, TallaPantalon,
                                 TallaChaqueta, TallaZapatos, HorasExtra, AreaFirma, PuestoFirma,  id))
                
            elif soliID != SolicitudId:
                cursor2.execute("UPDATE webApp_peticion SET Contratados = Contratados + 1 WHERE id = ?", (SolicitudId))
                cursor2.execute("UPDATE webApp_peticion SET Contratados = Contratados + -1 WHERE id = ?", (soliID))

                cursor2.execute("""UPDATE webApp_candidato SET Nombre = ?, DNI = ?, FechaNacimiento = ?, Sexo = ?, 
                                Nacionalidad = ?, Telefono = ?, Mail = ?, Municipio = ?, CP = ?, Provincia = ?,
                                EntidadBancaria = ?, IBAN = ?, Domicilio = ?, PeticionID_id = ?, Estado = 'Registrado',
                                FechaIncorporacion = ?, Puesto = ?, Categoria = ?, CategoriaSage = ?, Centro = ?, Convenio = ?,
                                SBA = ?, SIP = ?, Seccion = ?, Sociedad = ?, TurnoInicial = ?, CentroComp = ?, Horas = ?, Jornada = ?,
                                TallaPolo = ?, TallaPantalon = ?, TallaChaqueta = ?, TallaZapatos = ?, HorasExtra = ?, AreaOutlook = ?,
                                PuestoOutlook = ?
                                 WHERE id = ?""", 
                                (Nombre, DNI, FechaNacimiento, Sexo, Nacionalidad, Telefono, Mail, Municipio, CP, Provincia,
                                 EntidadBank, IBAN, Domicilio, SolicitudId, FechaIncorporacion, Puesto, Categoria, CategoriaSage, Centro,
                                 Convenio, SBA, SIP, Seccion, Sociedad, TurnoIni, CentroComp, Horas, Jornada, TallaPolo, TallaPantalon,
                                 TallaChaqueta, TallaZapatos, HorasExtra, AreaFirma, PuestoFirma,  id))
                
            cursor2.commit()
            cursor2.execute("SELECT Vacantes, Contratados FROM webApp_peticion WHERE id = ?", (SolicitudId))
            data = cursor2.fetchall()
            vacantes = data[0][0]
            contrataciones = data[0][1]
            if contrataciones == vacantes:
                cursor2.execute("UPDATE webApp_peticion SET Estado = 'Cerrada' WHERE id = ?", (SolicitudId))
            else:
                cursor2.execute("UPDATE webApp_peticion SET Estado = 'Abierta' WHERE id = ?", (SolicitudId))
            cursor2.commit()
            if soliID is not None:
                cursor2.execute("SELECT Vacantes, Contratados FROM webApp_peticion WHERE id = ?", (soliID))
                data = cursor2.fetchall()
                vacantes = data[0][0]
                contrataciones = data[0][1]
                if contrataciones == vacantes:
                    cursor2.execute("UPDATE webApp_peticion SET Estado = 'Cerrada' WHERE id = ?", (soliID))
                else:
                    cursor2.execute("UPDATE webApp_peticion SET Estado = 'Abierta' WHERE id = ?", (soliID))
                cursor2.commit()
            cursor2.close()
            return redirect('/candidatos')

    else:
        initial_data = {}
        if candidato is not None:
            iban = candidato[12]
            if iban is not None:
                initial_data['CodPais'] = iban[0:2]
                initial_data['ControlDig'] = iban[2:4]
                initial_data['EntBanc'] = iban[4:8]
                initial_data['SucBanc'] = iban[8:12]
                initial_data['ControlDig2'] = iban[12:14]
                initial_data['Cuenta'] = iban[14:24]

            initial_data['Nombre'] = candidato[1]
            initial_data['DNI'] = candidato[2]
            initial_data['FechaNacimiento'] = candidato[3]
            initial_data['Sexo'] = candidato[4]
            initial_data['Nacionalidad'] = candidato[5]
            initial_data['Telefono'] = candidato[6]
            initial_data['Mail'] = candidato[7]
            initial_data['Municipio'] = candidato[8]
            initial_data['CP'] = candidato[9]
            initial_data['Provincia'] = candidato[10]
            initial_data['EntidadBank'] = candidato[11]
            #initial_data['IBAN'] = candidato[12]
            initial_data['Domicilio'] = candidato[13]
            initial_data['FechaIncorporacion'] = candidato[19]
            initial_data['Puesto'] = candidato[21]
            initial_data['Categoria'] = candidato[23]
            initial_data['CategoriaSage'] = candidato[40]
            initial_data['Centro'] = candidato[24]
            initial_data['Convenio'] = candidato[25]
            initial_data['SBA'] = candidato[26]
            initial_data['SIP'] = candidato[27]
            initial_data['Seccion'] = candidato[28]
            initial_data['Sociedad'] = candidato[29]
            initial_data['TurnoInicial'] = candidato[30]
            initial_data["centroComp"] = candidato[31]
            initial_data['Jornada'] = candidato[33]
            initial_data['Horas'] = candidato[32]
            if candidato[37] != None:
                initial_data["TallaPolo"] = candidato[37]
            if candidato[36] != None:    
                initial_data["TallaPantalon"] = candidato[36]
            if candidato[35] != None:
                initial_data["TallaChaqueta"] = candidato[35]
            if candidato[38] != None:
                initial_data["TallaZapatos"] = candidato[38]
            initial_data["HorasExtra"] = candidato[39]
            initial_data["AreaFirma"] = candidato[41]


        form = FormularioCandidato(initial=initial_data)

    return render(request, 'auth/registroCandidato2.html', {'form':form, 'solicitudes':solicitudes, 'candidatoID':id, 'candidatoSolicitud':candidatoSolicitud, 'puestoFirma': puestoFirma})

@ms_identity_web.login_required
def solicitud(request):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
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

            solicitante = nombre
            centro = form.cleaned_data['Centro']
            vacantes = form.cleaned_data['Vacantes']
            observaciones = form.cleaned_data['Observaciones']
            fechaInc = form.cleaned_data['FechaIncorporacion']
            puesto = request.POST.getlist('puestoTecnico')
            motivoValue = request.POST.get('light', '')
            motivo = motivo_dict.get(motivoValue)
            today = date.today()
            cursor.execute("INSERT INTO webApp_peticion(Solicitante, Puesto, Centro, Motivo, Vacantes, Observaciones, FechaSolicitud, Contratados, Estado, Validado, FechaIncEstimada) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (solicitante, puesto[0], centro, motivo, vacantes, observaciones, today, 0, "Abierta", False, fechaInc))
            cursor.commit()
            cursor.close()

            destinatario = "valoresypersonas@okoa.tech"
            subject = "Nueva solicitud de personal " + str(today)
            body = solicitante + " ha enviado una nueva solicitud de personal para el puesto: " + puesto[0] + "\n\n"
            body += "Número de vacantes: " + str(vacantes) + "\n\n"
            body += "Observaciones:\n" + observaciones + "\n\n\n"
            body += "Por favor recuerde asociar esta solicitud con un proceso de selección existente o crear uno nuevo.\n\n"
            body += "Para más información de la solicitud por favor acceda al listado de solicitudes: https://192.168.2.252/solicitudes/"
            SendMail(body, destinatario, subject)

            destinatario = "reijer.domingo@okoa.tech"
            subject = "Nueva solicitud de personal " + str(today)
            body = solicitante + " ha enviado una nueva solicitud de personal para el puesto: " + puesto[0] + "\n\n"
            body += "Número de vacantes: " + str(vacantes) + "\n\n"
            body += "Observaciones:\n" + observaciones + "\n\n\n"
            body += "Por favor recuerde validar esta solicitud.\n\n"
            body += "Para más información de la solicitud por favor acceda al listado de solicitudes: https://192.168.2.252/solicitudes/"
            SendMail(body, destinatario, subject)
            return redirect('/solicitudes')

    else:
        form = FormularioSolicitud()

    return render(request, 'auth/solicitud2.html', {'form': form, 'nombre': nombre})

@ms_identity_web.login_required
def observacion(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
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
            cursor.close()
            return redirect('/observacionesSolicitud/' + str(id))

    else:
        form = FormularioObservaciones()

    return render(request, 'auth/observacion.html', {'form': form, "id": id})

@ms_identity_web.login_required
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
            
            return redirect('/ofertas')
            
    else:
        form = FormularioSuscriptores()

    return render(request, 'auth/suscripciones.html', {'form': form})

@ms_identity_web.login_required
def solicitudesList(request):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    
    if nombre in adminList:
        cursor.execute("SELECT * FROM webApp_peticion")
        solicitudes = cursor.fetchall()
        solicitudes.sort(reverse=True)
    elif nombre in solicitanteList:
        cursor.execute("SELECT * FROM webApp_peticion WHERE Solicitante = ?", (nombre))
        solicitudes = cursor.fetchall()
        solicitudes.sort(reverse=True)
    cursor.close()
    return render(request, 'auth/solicitudesList.html', {'solicitudes': solicitudes, 'nombre':nombre, 'adminList':adminList})

@ms_identity_web.login_required
def detalleSoli(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (id))
    solicitud = cursor.fetchall()
    
    solicitud = solicitud[0]
    if request.method == 'POST':
        form = FormularioDetalleSoli(request.POST)
        if form.is_valid():
            fechaRevisada = form.cleaned_data["FechaRevisada"]
            comentarios = form.cleaned_data["Comentarios"]

            cursor.execute("UPDATE webApp_peticion SET fechaIncRevisada = ?, Comentarios = ? WHERE id = ?", (fechaRevisada, comentarios, solicitud[0]))
            cursor.commit()
            cursor.close()
            return redirect('/solicitudes')
    else:
        initial_data = {}
        if solicitud is not None:
            initial_data['FechaRevisada'] = solicitud[16]
            initial_data['Comentarios'] = solicitud[14]
            form = FormularioDetalleSoli(initial=initial_data)

    return render(request, 'auth/detalleSoli.html', {'form': form, 'solicitud': solicitud})

@ms_identity_web.login_required
def deleteSolicitud(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
    if len(observaciones) > 0:
        cursor.execute("DELETE webApp_observacion WHERE Solicitud_id = ?",(id))
        cursor.commit()
    cursor.execute("DELETE webApp_peticion WHERE id = ?", (id))
    cursor.commit()
    cursor.close()
    return redirect('/solicitudes')

@ms_identity_web.login_required
def deleteObservacion(request, id, solicitudID):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    cursor.execute("DELETE webApp_observacion WHERE id = ?", (id))
    cursor.commit()
    cursor.close()
    return redirect('/observacionesSolicitud/' + str(solicitudID))

@ms_identity_web.login_required
def asignarOferta(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (id))
    solicitud = cursor.fetchall()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
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
            cursor.close()
            return redirect('/solicitudes')

    else:
        form = FormularioAsignacion()
            
    
    return render(request, 'auth/asignarOferta.html', {'solicitud':solicitud[0], 'form':form})

@ms_identity_web.login_required
def observacionesSolicitud(request, id):
    
    nombre = request.identity_context_data.username
    if nombre not in adminList and nombre not in solicitanteList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_observacion WHERE Solicitud_id = ?", (id))
    observaciones = cursor.fetchall()
    cursor.close()
    observaciones = sorted(observaciones, key=lambda x: x[2], reverse=True)
    #observaciones = ["alksdnlas", "aslkhdjasl", "Alsdhas", "ñlaksd", "Askdma", "alksdnlas", "aslkhdjasl", "Alsdhas", "ñlaksd", "Askdma"]
    return render(request, 'auth/observacionesSoli.html', {'observaciones':observaciones, "id":id, 'nombre':nombre, 'adminList':adminList})

@ms_identity_web.login_required
def welcome(request, id):

    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})

    cursor = Conexion()
    cursor.execute("SELECT id, Nombre, DNI, Mail FROM webApp_candidato WHERE id = ?", (id))
    candidato = cursor.fetchall()
    candidato = candidato[0]

    if request.method == 'POST':
        form = FormularioBienvenida(request.POST)
        if form.is_valid():
            Nombre = form.cleaned_data['Nombre']
            DNI = form.cleaned_data['DNI']
            Mail = form.cleaned_data['Mail']

            cursor.execute("UPDATE webApp_candidato SET Nombre = ?, DNI = ?, Mail = ?, Bienvenida = 1 WHERE id = ?", (Nombre, DNI, Mail, id)) 
            cursor.commit()
            cursor.close()
            Reenvio(Mail)
            return redirect('/candidatos')
    else:
        initial_data = {}
        if candidato is not None:
            initial_data['Nombre'] = candidato[1]
            initial_data['DNI'] = candidato[2]
            initial_data['Mail'] = candidato[3]
        form = FormularioBienvenida(initial=initial_data)
        
    return render(request, 'auth/welcome.html', {'form': form, 'candidato': candidato})

@ms_identity_web.login_required
def updateObservacion(request, id, descripcion, solicitudID):
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("UPDATE webApp_observacion SET Descripcion = ? WHERE id = ?", (descripcion, id))
    cursor.commit()
    return redirect('/observacionesSolicitud/' + str(solicitudID))

@ms_identity_web.login_required
def indicadores(request, id):
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_paso WHERE Solicitud_id = ? and Tipo = ?", (id, "Telefono"))
    dataTlf = cursor.fetchall()
    
    if len(dataTlf) == 0:
        contactoTelefono = 0
    else:
        dataTlf = dataTlf[0]
        contactoTelefono = dataTlf[1]

    cursor.execute("SELECT * FROM webApp_paso WHERE Solicitud_id = ? and Tipo = ?", (id, "Teams"))
    dataTeams = cursor.fetchall()
    if len(dataTeams) == 0:
        entrevistaTeams = 0
    else:
        dataTeams = dataTeams[0]
        entrevistaTeams = dataTeams[1]
    cursor.execute("SELECT * FROM webApp_paso WHERE Solicitud_id = ? and Tipo = ?", (id, "Tecnica"))
    dataTecnica = cursor.fetchall()
    if len(dataTecnica) == 0:
        entrevistaTecnica = 0
    else:
        dataTecnica = dataTecnica[0]
        entrevistaTecnica = dataTecnica[1]

    data = {
        'tlf': contactoTelefono,
        'teams': entrevistaTeams,
        'tecnica': entrevistaTecnica
    }

    if request.method == 'POST':
        form = FormularioIndicadores(request.POST)
        if form.is_valid():
            tipo = request.POST.get('tiposIndicadores')
            cantidad = request.POST.get('cantidad')
            if 'add_button' in request.POST:
                if tipo == "Telefono":
                    if len(dataTlf) == 0:
                        cursor.execute("INSERT INTO webApp_paso(Cantidad, Tipo, Solicitud_id) VALUES(?,?,?)", (cantidad, tipo, id))
                    else:
                        cantidad = int(cantidad) + contactoTelefono
                        cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
                elif tipo == "Teams":
                    if len(dataTeams) == 0:
                        cursor.execute("INSERT INTO webApp_paso(Cantidad, Tipo, Solicitud_id) VALUES(?,?,?)", (cantidad, tipo, id))
                    else:
                        cantidad = int(cantidad) + entrevistaTeams
                        cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
                elif tipo == "Tecnica":
                    if len(dataTecnica) == 0:
                        cursor.execute("INSERT INTO webApp_paso(Cantidad, Tipo, Solicitud_id) VALUES(?,?,?)", (cantidad, tipo, id))
                    else:
                        cantidad = int(cantidad) + entrevistaTecnica
                        cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
            elif 'remove_button' in request.POST:
                if tipo == "Telefono":
                    cantidad = contactoTelefono - int(cantidad)
                    cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
                elif tipo == "Teams":
                    cantidad = entrevistaTeams - int(cantidad)
                    cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
                elif tipo == "Tecnica":
                    cantidad = entrevistaTecnica - int(cantidad)
                    cursor.execute("UPDATE webApp_paso SET Cantidad = ? WHERE Solicitud_id = ? and Tipo = ?", (cantidad, id, tipo))
            
            cursor.commit()
            cursor.close()
            return redirect('/indicadores/' + str(id))

    return render(request, 'auth/indicadores.html', {'solicitudID': id, 'data': data})


@ms_identity_web.login_required
def updateSoli(request,solicitudID):
    nombre = request.identity_context_data.username
    if nombre not in adminList:
        return render(request, 'auth/401.html', {'nombre': nombre})
    
    cursor = Conexion()
    cursor.execute("SELECT * FROM webApp_peticion WHERE id = ?", (solicitudID))
    solicitud = cursor.fetchall()
    solicitud = solicitud[0]
    return render(request, 'auth/modificarSolicitud.html', {'solicitud': solicitud})
