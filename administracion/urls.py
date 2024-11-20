from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from administracion import views

urlpatterns = [
    path('datosEmail/', views.datosEmail),
    path('getDatosEmail/', views.obtenerDatosEmail),
    path('list-oferta-filtro/', views.ListOfertaFiltro),
    path('addOferta/', views.AgregarOferta),
    path('getCSRF/', views.get_csrf_token),
    path('get-oferta/<int:pk>/', views.getOferta),
    path('editOferta/', views.editarOferta),
    path('ofertas-publico/', views.ListOfertaPublico),
    path('list-rango-kilometraje/', views.ListRangoKilometraje),
    path('new-rango/', views.AgregarRango),
    path('list-porcentajes/', views.ListPorcentajesOperacion),
    path('new-porcentaje/', views.AgregarPorcentajes),
    path('getRangos/', views.ListRangos),
    path('obtener-porcentajes/', views.getPorcentajesOperacion),
    path('get-incremento/<int:pk>/', views.getIncremento),
    path('edit-incremento/', views.editarIncremento),
    path('list-rango-mercancias/', views.ListRangosMercancias),
    path('new-rango-mercancia/', views.AgregarRangoMercancia),
    path('get-rangos-cargas/', views.ListRangosCargas),
    path('email_c/', views.send_email_carlos),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
