from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('candidatos/', views.candidatos, name='candidatos'),
    path('registroCandidato/<id>', views.registroCandidato, name='registroCandidato'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('observacion/<id>', views.observacion, name='observacion'),
    path('suscripcion/', views.suscripciones, name='suscripcion'),
    path('solicitudes/', views.solicitudesList, name='solicitudes'),
    path('deleteSolicitud/<id>', views.deleteSolicitud ,name='deleteSolicitud'),
    path('deleteObservacion/<id>/<solicitudID>', views.deleteObservacion, name='deleteObservacion'),
    path('asignarOferta/<id>', views.asignarOferta, name='asignarOferta'),
    path('observacionesSolicitud/<id>', views.observacionesSolicitud, name='observacionesSolicitud'),
    path('validarSolicitud/<id>', views.validarSoli, name='validarSoli'),
    path('detalleSoli/<id>', views.detalleSoli, name='detalleSoli'),
    path('detalleInforme/<id>', views.detalleInforme, name='detalleInforme'),
    path('calendario', views.CalendarioInc, name='calendario')
]
