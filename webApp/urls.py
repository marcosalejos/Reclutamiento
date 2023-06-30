from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('candidatos/', views.candidatos, name='candidatos'),
    path('registroCandidato/<id>', views.registroCandidato, name='registroCandidato'),
    path('solicitud/', views.solicitud, name='solicitud'),
    path('observacion/', views.observacion, name='observacion'),
    path('suscripcion/', views.suscripciones, name='suscripcion'),
    path('solicitudes/', views.solicitudesList, name='solicitudes'),
    path('deleteSolicitud/<id>', views.deleteSolicitud ,name='deleteSolicitud'),
    path('asignarOferta/<id>', views.asignarOferta, name='asignarOferta'),
    path('observacionesSolicitud/<id>', views.observacionesSolicitud, name='observacinesSolicitud')
]
