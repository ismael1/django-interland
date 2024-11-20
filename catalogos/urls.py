from os import name
from django.urls import path, include
from catalogos import views

urlpatterns = [
    path('list-box/', views.listBox),   
    path('search-aduana/', views.searchAduana),
    path('get-aduana/', views.getNameAduana),

    path('list-producto-filtro/', views.ListProductoFiltro),
    path('list-servicio-filtro/', views.ListServicioFiltro),
    path('list-clave-filtro/', views.ListClaveFiltro),
    path('list-clave-unidad-filtro/', views.ListClaveUnidadFiltro),
    path('list-puesto-filtro/', views.ListPuestoFiltro),
    path('list-responsable-filtro/', views.ListResponsableFiltro),
    path('list-envio-filtro/', views.ListEnvioFiltro),
    path('list-embalajes-filtro/', views.ListEmbalajeFiltro),

    path('search-proser/', views.searchPS), 
    path('search-unidad/', views.searchUnit),
    path('list-unit-filtro/', views.ListUnidadFiltro), 
    path('detalleUnit/', views.detalleUnit),

    #INICIA SECCION DE UNIDADES
    path('catalogo-getUnidad/<int:pk>/', views.getUnidad),
    path('catalogo-updateUnidad/', views.updateUnidad),
    path('catalogo-deleteUnidad/<int:pk>/', views.deleteUnidad),
    #TERMINA SECCION DE UNIDADES

    path('modulos/', views.getModulos),
    path('permisosUsuarios/', views.getPermisosUsuario),
    path('asignaPermisos/', views.asignaPermisos),
    path('accionesPermisos/', views.accionesPermisos),
    path('permisosModuloUsuario/', views.perModUsr),

    path('list-modulo-filtro/', views.ListModulosFiltro),
    path('lista-modulo/', views.ListaModulos),

    path('infoModulo/<int:pk>/', views.getModulo),
    path('addModulo/', views.newModulo),

    path('addEmbalaje/', views.newEmbalaje),
    path('infoEmbalaje/<int:pk>/', views.getEmbalaje),
    path('catalogo-updateEmbalaje/', views.updateEmbalaje),
    path('catalogo-deleteEmbalaje/<int:pk>/', views.deleteEmbalaje),
    path('list-terminos-filtro/', views.ListTerminosFiltro), 
    path('list-terminos-filtro-ftl/', views.ListTerminosFTLFiltro),
    path('list-terminos-filtro-fcl/', views.ListTerminosFCLFiltro),
    
    path('list-geocercas/', views.ListGeocercas),
    path('geocercas-manual/', views.GeocercasViewSet),
    path('geocercas-estados/', views.geocercasEstados),
    path('geocercas-cp/', views.geocercasCP),
    path('geocercas-centro/', views.geocercasCentro),
    path('geocercas-eliminar/', views.geocercasElimina),
    path('get-estados-geocercas/', views.geocercasEstaados),
    path('get-datos-geocercas/', views.getInfoEstados),
    path('get-datos-geocercas-info/', views.getInfoEstadosGeo),    
    path('get-datos-geocercas-cotizacion/', views.getInfoEstadosCotizacion),
    path('get-distancias-maps/', views.getDistanciasMaps),
    path('get-distancias-maps-cordenadas/', views.getDistanciasMapsCordenadas),

    path('tipo-cliente/', views.tipo_clienteViewSet),
    path('tipo-persona/', views.tipo_personaViewSet),
    path('tipo-empresa/', views.tipo_empresaViewSet),
    path('regimen-fiscal/', views.regimen_fiscalViewSet),
    path('metodo-pago/', views.metodo_pagoViewSet),
    path('forma-pago/', views.forma_pagoViewSet),
    path('list-zona-tarifa-filtro/', views.ListZonasTarifasFiltro),
    path('addZonaTarifa/', views.newZonaTarifa),
    path('valida-tipo-zona/', views.ValidaZonasTarifas),
    path('extraer-info-gmaps/', views.obtener_direccion_gmaps),
    
    
    
]
