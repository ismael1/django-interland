from os import name

from django.urls import path, include

from ajustesRutas import views
# from catalogos import views

urlpatterns = [

    path('list-ruta-filtro/', views.ListRutaFiltro),

]
