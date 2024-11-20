from os import name

from django.urls import path, include

from cotizaciones import views

urlpatterns = [

    path('list-services-coincidencia/', views.ServiceCoincidencia),
    path('list-tarifas-coincidencia/', views.tarifaCoincidencia),
    path('list-kilometraje-coincidencia/', views.rutasCoincidencia),
    path('list-cotizacion-filtro/', views.ListCotizacionFiltro),
    path('list-cotizacion-filtro-vig/', views.ListCotizacionFiltroContesta),
    path('list-cotizacion-filtro-sn/', views.ListCotizacionFiltroNoContesta),
    path('consecutivo/', views.getConsecutivo),
    path('consecutivo/<int:pk>/', views.updateConsecutivo),
    path('iconsecutivo/', views.insertConsecutivo),
    
    # path('list-cotizacion-filtro/', views.ListCotizacionFiltro),
    path('service-filtro/', views.ServicePrice),
    path('consultar-servicios-agregados/', views.ConsultarServiciosAgregados),
    path('consultar-contacto-agregado/', views.ConsultarContactoAgregado),

    path('consultar-folio/', views.ConsultarFolio.as_view()),
    path('cotiza-pdf/<int:pk>/', views.PDFCotizacion.as_view(), name='pdf'), #Generar PDF
    path('sendEmailCotiza/', views.send_email),
    path('getFolioServicio/', views.folioServicio),
    path('editarServicios/', views.editarServicios),
    path('getTarifario/', views.getTarifario),

    path('list-tarifario-filtro/', views.ListTarifarioFiltro),
    path('list-tarifarioActivo-filtro/', views.ListTarifarioActivoFiltro),
    path('list-tarifarioInactivo-filtro/', views.ListTarifarioInactivoFiltro),
    path('nueva-tarifa/', views.insertTarifa),
    path('eliminar-tarifa/<int:pk>/', views.deleteTarifa),
    path('infoTarifa/<int:pk>/', views.getTarifa),
    path('actualiza-tarifa/', views.updateTarifa),

    path('getMercancias/<int:pk>/', views.getMercancias),
    path('getPlanes/<int:pk>/', views.getPlanes),
    path('detalles-ubicacion/', views.obtener_detalles_ubicacion),
    path('detalles-geocerca/', views.obtener_detalles_geocerca),
    path('geocerca-detalles/', views.detalles_geocerca),
    path('detalles-geocerca-puertos/', views.obtener_detalles_geocerca_puertos),
    path('agente-aviso/', views.send_email_agente),
    path('pdfTarifarioLtl/', views.pdf_tarifario_ltl),
    path('pdfTarifarioLtl2/', views.pdf_tarifario_ltl_2),
    
]
