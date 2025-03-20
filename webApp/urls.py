from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static
from ms_identity_web.django.msal_views_and_urls import MsalViews

msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
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
    path('calendario/', views.CalendarioInc, name='calendario'),
    path('welcome/<id>', views.welcome, name='welcome'),
    path('updateObservacion/<int:id>/<str:descripcion>/<int:solicitudID>', views.updateObservacion, name='updateObservacion'),
    path('indicadores/<id>', views.indicadores, name='indicadores'),
    path('updateData/', views.updateData, name='updateData'),
    path('getStatus/', views.getStatus, name='getStatus'),
    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
