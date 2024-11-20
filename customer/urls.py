from os import name

from django.urls import path, include

from customer import views

from customer.views import ReportePersonalizadoExcel


urlpatterns = [
    path('list-customer/', views.ListCustomer.as_view()),
    # path('list-customer-filtro/', views.ListCustomerFiltro.as_view()), #Agregado solo muestra nombre, fecha, estatus 100621
    path('list-customer-filtro/', views.ListCustomerFiltro), #Agregado solo muestra nombre, fecha, estatus 100621
    path('cp/', views.CodigoPostalViewSet),
    path('cpCat/', views.CodigoPostalCat),
    
    path('municipio/', views.MunicipioViewSet),
    
    path('customer/<int:idCliente>/', views.CustomerDetail.as_view()),
    path('list-country/', views.ListCountry.as_view()),
    path('list-estates/<int:idPais>/', views.ListEstates.as_view()),
    path('list-empresa/', views.ListEmpresas.as_view()),
    path('list-usocfdi/', views.ListUsoCfdi.as_view()),
    path('list-formapago/', views.ListFormaPago.as_view()),
    path('list-metodopago/', views.ListMetodoPago.as_view()),
    path('list-areas/', views.ListAreas.as_view()),
    #ruta para el listado de contacto Ismael 260521
    path('list-contacts/<int:idCliente>/', views.ListContacts.as_view()),
    path('contac-details/<int:idContact>/', views.ContactDetail.as_view()),
    # path('contac-details/<int:idContact>/', views.ContactDetail.as_view()),
    path('customer/addFiles/', views.addFiles),
    # path('','customer/addFiles/', views.addFiles), //original
    #listado de los archivos ismael 250521
    path('list-files/<int:idCliente>/', views.ListFiles.as_view()),
    path('consultaFiles/', views.consultarFiles),
    path('files-details/<int:idFile>/', views.DetailsFiles.as_view()),
    path('list-datacomplementary/<int:idCliente>/', views.ListDataComplementary.as_view()), 
    # path('datacomplementary-details/<int:idFile>/', views.DataComplementaryDetail.as_view()),
    path('list-business/', views.ListBusiness.as_view()),
    path('list-ladas/', views.ListLada.as_view()),     
    # //===
    path('customer/showpDF/', views.showpDF),
    # path('customer/', views.CustomersViewSet.as_view()),
    # path('new-add/', views.ListAreas.as_view()),
    path('list-rutas/<int:idCliente>/', views.ListRutas.as_view()), 
    path('search-zipcode/', views.searchZIP), 

    # path('search-customer/', views.searchCustomer),  #130621
    # path('senEmail/', views.TestView.as_view(), name='test'), 
    path('senEmail/', views.send_email),

    path('list-pdf/', views.PDFCustomer.as_view(), name='pdf'), #Generar PDF
    path('list-excel/', views.ReportePersonalizadoExcel.as_view(), name = 'reporte_excel'), #Generar Excel

    #SECCION ZONAS
    
    path('nueva-zona/', views.nuevaZona), #Generar Zonas
    path('zonas-obtenerid/', views.getId), #Obtener ultimo Id
    path('list-zonas-filtro/', views.ListZonasFiltro), #Obtener lista de Zonas
    path('nueva-zona-hijos/', views.nuevaZonaHijos), #Generar Zonas hijo
    path('zonas-hijos-consulta/', views.consultaHijos), #Obtener lista de zonas hijo
    path('get-zona/<int:idZona>/', views.getZonas), #Obtener zona hijo
    path('eliminarZona/', views.deleteZona), #Elimina Zona
    path('eliminarHijo/', views.deleteHijo), #Elimina zona hijo
    path('buscaZonaCP/', views.getCoincidenciaZona), #Elimina zona hijo
    path('valida-cp-geocerca/', views.validaCPGeocerca),
    path('ZonaCP/', views.coincidenciaZona), #Elimina zona hijo
    path('search-address/', views.searchAddress), #Elimina zona hijo
    path('search-address-detalles/', views.searchAddressDetalles), #Elimina zona hijo

    path('get-select-zonas/', views.getSelectZonas), #Obtiene la informacion para seleccionar tipo de zona
    path('update-select-zonas/', views.updateSelectZonas), #Obtiene la informacion para seleccionar tipo de zona
    path('obtener-datos-tabla-zonas-select/', views.datos_select),
    path('procesa-datos-zona-geocercas/', views.zona_geocercas),
    
]
