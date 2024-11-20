from os import name

from django.urls import path, include

from servicioVenta import views

urlpatterns = [
    path('servicioVenta/', views.ServicioVentas),
    path('list-services-filtro/', views.ListServiceFiltro),
    path('list-services-filtro-incompleto/', views.ListServiceFiltroIncompleto),
    path('list-services-filtro-expirado/', views.ListServiceFiltroExpirados),
    path('list-services-filtro-nocontestados/', views.ListServiceFiltroNoContestados),
    path('list-services/', views.ListService),
    path('servicioVenta/<int:idServicio>/', views.ServiceSaleDetail.as_view()),

    path('consultar-cotizaion-add/', views.ConsultarCotizacionAgregada),
    path('consultar-servicios-add/', views.ConsultarServiciosAgregados),
    path('consultar-servicios/', views.ConsultarServiciosAgregar),
    path('sendEmailNuevoServicio/', views.emailNuevoServicio),
    path('cerrar-servicio/', views.cerrarServicio),
    path('editar-servicio-cotiza/', views.editarServicios),
    
]