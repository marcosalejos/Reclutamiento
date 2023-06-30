from django.db import models

# Create your models here.
class Oferta(models.Model):
    Nombre = models.CharField(max_length=200, null=False)
    lastUpdate = models.DateField(null=True)
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ESTADOS_CHOICES = [
        (ACTIVO, "Activo"),
        (INACTIVO, "Inactivo")
    ]
    Estado = models.CharField(
        max_length=8,
        choices=ESTADOS_CHOICES,
        default=ACTIVO,
        null=False
    )
    Interno = models.BooleanField(null=False, default=False) #Modificado

class Suscriptores(models.Model):
    mail = models.EmailField()
    Oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    tlf = models.IntegerField()

class Registro(models.Model):
    FechaRegistro = models.DateField()
    FechaIni = models.DateField()
    Inscritos = models.IntegerField(null=True)
    I_EP = models.IntegerField(null=True)
    EP_F = models.IntegerField(null=True)
    F_C = models.IntegerField(null=True)
    Descartados = models.IntegerField(null=True)
    Oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    
class EntradaOferta(models.Model):
    Inscritos = models.IntegerField(null=False)
    EnProceso = models.IntegerField(null=False)
    Finalistas = models.IntegerField(null=False)
    Contratados = models.IntegerField(null=False)
    Descartados = models.IntegerField(null=False)
    fechaPublicacion = models.DateField(null=False)
    fechaActual = models.DateField(null=False)
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    ESTADOS_CHOICES = [
        (ACTIVO, "Activo"),
        (INACTIVO, "Inactivo")
    ]
    Estado = models.CharField(
        max_length=8,
        choices=ESTADOS_CHOICES,
        default=ACTIVO,
        null=False
    )
    OfertaID = models.ForeignKey(Oferta, on_delete=models.CASCADE, null=False)
    InscTot = models.IntegerField(null=False)

class Peticion(models.Model):
    Solicitante = models.CharField(max_length=200, null=False)
    Puesto = models.CharField(max_length=200, null=False)
    Centro = models.CharField(max_length=100, null=False)
    Motivo = models.TextField(null=False)
    Vacantes = models.IntegerField(null=False)
    Observaciones = models.TextField(null=True)
    OfertaID = models.ForeignKey(Oferta, on_delete=models.CASCADE, null=True)
    FechaSolicitud = models.DateField(null=False)

class Observacion(models.Model):
    Descripcion = models.TextField()
    Fecha = models.DateField()
    Oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE)
    Solicitud = models.ForeignKey(Peticion, on_delete=models.DO_NOTHING)


class Candidato(models.Model):
    Nombre = models.CharField(max_length=100, null=False)
    DNI = models.CharField(max_length=9, null=True)
    FechaNacimiento = models.DateField(null=True)
    Sexo = models.CharField(max_length=20, null=True)
    Nacionalidad = models.CharField(max_length=50, null=True)
    Telefono = models.IntegerField(null=True)
    Mail = models.CharField(max_length=150, null=True)
    ImgDNI = models.CharField(max_length=500, null=True)
    ImgSIP = models.CharField(max_length=500, null=True)
    Municipio = models.CharField(max_length=100, null=True)
    CP = models.IntegerField(null=True)
    Provincia = models.CharField(max_length=75, null=True)
    EntidadBancaria = models.CharField(max_length=200, null=True)
    IBAN = models.CharField(max_length=24, null=True)
    OfertaID = models.ForeignKey(Oferta, on_delete=models.CASCADE, null=True)
    PeticionID = models.ForeignKey(Peticion, on_delete=models.CASCADE, null=True)
    Domicilio = models.CharField(max_length=300, null=True)
    FechaRegistro = models.DateField(null=False)
    REGISTRADO = "Registrado"
    PENDIENTE = "Pendiente"
    CHOICES = [
        (PENDIENTE, "Pendiente"),
        (REGISTRADO, "Registrado")
    ]
    Estado = models.CharField(
        max_length=10,
        choices=CHOICES,
        default=PENDIENTE,
        null=False
    )
    EmpresaOrigen = models.CharField(max_length=100, null=True) #Modificado
    PuestoOrigen = models.CharField(max_length=200, null=True) #Modificado
    Puesto = models.CharField(max_length=200, null=True) #Modificado
    FechaIncorporacion = models.DateField(null=True) #Modificado
    FechaIncorporacionEstimada = models.DateField(null=True) #Modificado

class Externo(models.Model):
    DNI = models.CharField(max_length=9, null=True) 

    LIN = "LinkedIn"
    C_IN = "Contacto Interno"
    WEB_CORP = "Web Corporativa"
    P_EXT = "Proveedor Externo"
    FUENTES_CHOICES = [
        (LIN, "LinkedIn"),
        (C_IN,"Contacto Interno"),
        (WEB_CORP,"Web Corporativa"),
        (P_EXT,"Proveedor Externo")
    ]
    FuenteOrigen = models.CharField(
        max_length=20,
        choices=FUENTES_CHOICES,
        default=LIN,
        null=False
    )
    Oferta = models.ForeignKey(Oferta, on_delete=models.DO_NOTHING)
    Solicitud = models.ForeignKey(Peticion, on_delete=models.DO_NOTHING)


class Motivo(models.Model):
    DNI = models.CharField(max_length=9, null=True)

    DESP = "Desplazamiento de residencia a CT"
    TURN = "Turnistica"
    RETR = "Retribucion"
    OFERTA_EXT = "Aceptar otra oferta de incorporacion"
    CONTRAOFERTA ="Contraoferta empresa actual"
    OTROS = "Otros"
    TIPOS_CHOICES = [
        (DESP ,"Desplazamiento de residencia a CT"),
        (TURN ,"Turnistica"),
        (RETR ,"Retribucion"),
        (OFERTA_EXT ,"Aceptar otra oferta de incorporacion"),
        (CONTRAOFERTA ,"Contraoferta empresa actual"),
        (OTROS ,"Otros")
    ] 
    Tipo = models.CharField(
        max_length=50,
        choices=TIPOS_CHOICES,
        default=DESP,
        null=False
    )
    Oferta = models.ForeignKey(Oferta, on_delete=models.DO_NOTHING)

class Paso(models.Model):
    Cantidad = models.IntegerField(null=False)

    TLF = "Contacto Telefonico"
    ENT_RRHH = "Entrevista de RRHH"
    ENT_TECN = "Entrevista Tecnica"
    PRUEBA_TEC = "Prueba Tecnica"
    OF = "Oferta"

    TIPOS_CHOICES = [
        (TLF,"Contacto Telefonico"),
        (ENT_RRHH,"Entrevista de RRHH"),
        (ENT_TECN,"Entrevista Tecnica"),
        (PRUEBA_TEC,"Prueba Tecnica"),
        (OF,"Oferta")
    ] 
    Tipo = models.CharField(
        max_length=30,
        choices=TIPOS_CHOICES,
        default=TLF,
        null=False
    )
    Apto = models.IntegerField(null=True)
    NoApto = models.IntegerField(null=True)
    Citado = models.IntegerField(null=True)
    Dudoso = models.IntegerField(null=True)
    NoInteresado = models.IntegerField(null=True)
    NoContesta = models.IntegerField(null=True)
    Criba = models.IntegerField(null=True)
    Oferta = models.ForeignKey(Oferta, on_delete=models.DO_NOTHING)
    Solicitud = models.ForeignKey(Peticion, on_delete=models.DO_NOTHING)

class Promocion(models.Model):
    DNI = models.CharField(max_length=9)
    Nombre = models.CharField(max_length=50)
    FechaEvolucion = models.DateField()
    FechaAplicacion = models.DateField()
    PuestoOrigen = models.CharField(max_length=75)
    PuestoDest = models.CharField(max_length=75)
    SBA_origen = models.IntegerField()
    SBA_dest = models.IntegerField()
    Coste = models.IntegerField()

    ENT_EV = "Entrevista Evolucion"
    CONTRAOFERTA = "Contraoferta"
    RET = "Metodo Retencion"

    TIPOS_CHOICES = [
        (ENT_EV,"Entrevista Evolucion"),
        (CONTRAOFERTA,"Contraoferta"),
        (RET,"Metodo Retencion")

    ] 
    Tipo = models.CharField(
        max_length=30,
        choices=TIPOS_CHOICES,
        default=ENT_EV,
        null=False
    )
class Comunicado(models.Model):
    Nombre = models.CharField(max_length=50)
    Fecha = models.DateField()

    FIS = "Fisico"
    DIG = "Digital"
    TB = "TeamBuildings"

    CANAL_CHOICES = [
        (FIS,"Fisico"),
        (DIG,"Digital"),
        (TB,"TeamBuildings")
    ] 
    Tipo = models.CharField(
        max_length=20,
        choices=CANAL_CHOICES,
        default=FIS,
        null=False
    )
    Tema = models.CharField(max_length=50)
    Eje = models.CharField(max_length=50)
    Impacto = models.TextField()

class Evolucion(models.Model):
    Participantes = models.IntegerField()
    Trabajadores = models.IntegerField()
    Centro = models.CharField(max_length=50)


class SatisfacionSeleccion(models.Model):
    #Pregunta 1
    Definicion = models.CharField(max_length=75)
    
    #Pregunta 2
    POCO = "Poco"
    ALGO = "Algo"
    BASTANTE = "Bastante"
    TOT = "Totalmente"
    RESPUESTAS_CHOICES = (
        (POCO, "Poco"),
        (ALGO,"Algo"),
        (BASTANTE,"Bastante"),
        (TOT, "Totalmente")
    )

    RIG = "Riguroso"
    UT = "Útil"
    AM = "Ameno"
    TP = "Transparente"
    PROF = "Profesional"
    TEC = "Técnico"
    LARGO = "Largo"
    AGIL = "Ágil"

    GRADO_CHOICES = (
        (RIG, "Riguroso"),
        (UT, "Útil"),
        (AM, "Ameno"),
        (TP, "Transparente"),
        (PROF, "Profesional"),
        (TEC, "Técnico"),
        (LARGO, "Largo"),
        (AGIL, "Ágil")
    )


    Grado = models.CharField(
        max_length=12,
        choices=GRADO_CHOICES,
        default=RIG,
        null=False
    )
    Respuesta = models.CharField(
        max_length=10,
        choices=RESPUESTAS_CHOICES,
        default=POCO,
        null=False
    )

    #Pregunta 3
    Mejora = models.CharField(max_length=500)

    #Pregunta 4/5/6
    NR = "No lo recuerdo"
    NO = "No"
    NO_EXP = "Lo mencionaron pero no lo explicaron al detalle"
    S_DET = "Sí, con mucho detalle"
    S_NDET = "Sí, con algo de detalle"

    OPCIONES = (
        (NR, "No lo recuerdo"),
        (NO, "No"),
        (NO_EXP, "Lo mencionaron pero no lo explicaron al detalle"),
        (S_DET, "Sí, con mucho detalle"),
        (S_NDET, "Sí, con algo de detalle")
    )

    Valores = models.CharField(
        max_length=200,
        choices=OPCIONES,
        default=NR,
        null=False
    )

    Expectativas = models.CharField(
        max_length=200,
        choices=OPCIONES,
        default=NR,
        null=False
    )

    Condiciones = models.CharField(
        max_length=200,
        choices=OPCIONES,
        default=NR,
        null=False
    )

    #Pregunta 7
    Utilidad = models.IntegerField()

    #Pregunta 8
    MotivoAceptacion = models.CharField(max_length=500)

    #Pregunta 9
    Centro = models.CharField(max_length=15)

    #Pregunta 10
    Expetiencia = models.CharField(max_length=50)

    #Pregunta 11
    FechaEntrevista = models.DateField()
'''
class SatisfaccionBienvenida(models.Model):

    FIRST = "15 dias"
    SECOND = "45 dias"
    
    DIAS_CHOICES = [
        (FIRST,"15 dias"),
        (SECOND, "45 dias")
    ]
    Tipo = models.CharField(
        max_length=10,
        choices=DIAS_CHOICES,
        default=FIRST,
        null=False
    )
    #Pregunta 1
    GradoTipo = models.CharField(max_length=20)
    GradoRes = models.CharField(max_length=30)
    #Pregunta 2

'''

'''
class SatisfaccionFormacion(models.Model):
    COMPLETAR
    pass'''

class Empleado(models.Model):
    #DATOS BASICOS
    Centro = models.CharField(max_length=75)
    Domicilio = models.CharField(max_length=250)

class Entradas_Salidas(models.Model):
    DNI = models.CharField(max_length=9, null=True)
    FechaBienvenida = models.DateField()
    FechaContratoIni = models.DateField()
    FechaContratoFin = models.DateField()
    Centro = models.CharField(max_length=75)
    '''COMPLETAR'''
    VOL = "Baja Voluntaria"
    DESP = "Despido"
    TIPO_MOTIVO = [
        (VOL,"Baja Voluntaria"),
        (DESP,"Despido")
    ]
    TipoMotivo = models.CharField(
        max_length=20,
        choices=TIPO_MOTIVO,
        default=VOL,
        null=False
    )
    
    
    DESP = "Desplazamiento a ct"
    TUR = "Turnistica"
    RET = "Retribucion"
    OF_EXT = "Oferta de otra empresa"
    PROY = "Proyecto personal/familiar"
    OTROS = "Otros"

    MOTIVO_CHOICES = [

    (DESP,"Desplazamiento a ct"),
    (TUR,"Turnistica"),
    (RET,"Retribucion"),
    (OF_EXT,"Oferta otra empresa"),
    (PROY,"Proyecto personal/familiar"),
    (OTROS,"Otros")
    ]

    Motivo = models.CharField(
        max_length=50,
        choices=MOTIVO_CHOICES,
        default=DESP,
        null=False
    )
    

    DESP = "Bajo desempeño"
    ACT = "Actitud"
    NORM = "Incumplimiento Normas y/o falta grave"
    OTROS = "Otros"
    FORZADA_CHOICES = [
        (DESP,"Bajo desempeño"),
        (ACT,"Actitud"),
        (NORM,"Incumplimiento Normas y/o falta grave"),
        (OTROS,"Otros")
    ]

    TipoSalidaForzada = models.CharField(max_length=1) #Motivo de Despido

    Grupo = models.CharField(max_length=50)
    Convenio = models.CharField(max_length=50)

'''class Desvinculaciones(models.Model):
    #Datos Formulario
    ES = models.ForeignKey(Entradas_Salidas, on_delete=models.DO_NOTHING)'''