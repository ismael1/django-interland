from os import name

from django.urls import path, include

from servicios import views

urlpatterns = [
    path('search-service/', views.searchService),
    path('services-grid/', views.ListServicioCotizacionesFiltro),
    path('services-obtenerid/', views.obtenerId),
    path('services-insert/', views.insertServicio),
    path('services-get/<int:pk>/', views.getServicio),
    path('services-update/', views.updateServicios),
    path('services-delete/<int:pk>/', views.deleteServicios),
    path('services-lista/', views.serviciosLista),
    
]
