from os import name

from django.urls import path, include

from proveedores import views

urlpatterns = [
    path('search-proveedor/', views.searchProveedor),
    path('provider/addFiles/', views.addFiles),
    path('provider-list-files/<int:idProvider>/', views.ListFiles.as_view()),
    path('provider/showpDF/', views.showpDF),

    path('provider-list-contacts/<int:idProvider>/', views.ListContacts.as_view()),
    path('provider-contac-details/<int:idProvider>/', views.ContactDetail.as_view()),
    path('provider-list-rutas/<int:idProvider>/', views.ListRutas.as_view()),

    path('pconsultaFiles/', views.consultarFiles),
    path('list-provider-filtro/', views.ListProviderFiltro),
    path('provider/<int:idProvider>/', views.ProviderDetail.as_view()),
    path('provider-list-datacomplementary/<int:idProvider>/', views.ListDataComplementary.as_view()),
]