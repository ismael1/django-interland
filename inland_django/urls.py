"""inland_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from customer.views import CustomersViewSet, ContactosViewSet, DataComplementaryViewSet, FilesViewSet,RutaViewSet,PaisesViewSet,EstadosViewSet
from rest_framework import routers

from django.conf.urls.static import static
from django.conf import settings

# from servicioVenta.views import ServicioVentas
from servicioVenta.views import ServicioVentas
# Importar views del Modulo Cotizacion
from cotizaciones.views import ServicioCotizaciones, ContactoCotizaciones, ServiciosAgregadosCotizaciones, MercanciasCotizaciones, PlanesCotizaciones, DireccionCotizaciones
# Importar views del Modulo Servicios
from servicios.views import ServicesViewSet
#Importar views del Modulo Catalogo
from catalogos.views import UnitBoxtViewSet, ClaveProdServViewSet, ClaveUnidadViewSet, ProductoViewSet, ServicioViewSet, PuestoViewSet, ResponsableViewSet, EnvioViewSet, EmbalajesViewSet, GeocercasViewSet
# Importar views del Modulo Proveedores
from proveedores.views import ProveedorViewSet, ContactoPViewSet, FilesPViewSet, DataComplementaryPViewSet, RutasPViewSet
# Importar views del Modulo AjustesRuta
from ajustesRutas.views import ajustesRutasViewSet
# Importar views del Modulo Usuarios
from usuarios.views import UsuariosViewSet
# Importar views del Modulo Administracion
from administracion.views import EmailDatos


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# //para el usuarios
from user.views import UsersViewSet


router = routers.DefaultRouter()
router.register(r'customers', CustomersViewSet)
router.register(r'contactos', ContactosViewSet)
router.register(r'files', FilesViewSet) 
router.register(r'datacomplementary', DataComplementaryViewSet)
router.register(r'rutas', RutaViewSet) 
router.register(r'paises', PaisesViewSet) 
router.register(r'estados', EstadosViewSet)

router.register(r'servicioVenta', ServicioVentas) 
router.register(r'servicioCotizaciones', ServicioCotizaciones)
router.register(r'servicioAgregados', ServiciosAgregadosCotizaciones)
router.register(r'contactoCotizaciones', ContactoCotizaciones)
router.register(r'mercanciasCotizaciones', MercanciasCotizaciones)
router.register(r'planesCotizaciones', PlanesCotizaciones)
router.register(r'direccionCotizaciones', DireccionCotizaciones)
router.register(r'geocercas', GeocercasViewSet)

#Proveedores
router.register(r'proveedores', ProveedorViewSet)
router.register(r'pcontacto', ContactoPViewSet)
router.register(r'pfiles', FilesPViewSet)
router.register(r'pdatacomplementary', DataComplementaryPViewSet)
router.register(r'prutas', RutasPViewSet)

#Servicios 
router.register(r'servicios', ServicesViewSet)
router.register(r'services', ServicesViewSet)

#Catalogos 
router.register(r'unitbox', UnitBoxtViewSet)
router.register(r'embalajes', EmbalajesViewSet)
router.register(r'user', UsersViewSet)
router.register(r'producto_servicio', ClaveProdServViewSet)
router.register(r'clave_unidad', ClaveUnidadViewSet)
router.register(r'producto', ProductoViewSet)
router.register(r'servicio', ServicioViewSet)
router.register(r'puesto', PuestoViewSet)
router.register(r'responsable', ResponsableViewSet)
router.register(r'envio', EnvioViewSet)

#Rutas 
router.register(r'ajusteRuta', ajustesRutasViewSet)

#Usuarios
router.register(r'usuarios', UsuariosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('customer.urls')),
    path('api/v1/', include('catalogos.urls')),
    path('api/v1/', include('servicioVenta.urls')),
    path('api/v1/', include('servicios.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('cotizaciones.urls')),
    path('api/v1/', include('proveedores.urls')),
    path('api/v1/', include('ajustesRutas.urls')),
    path('api/v1/', include('usuarios.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('administracion.urls')),
    path('api/v1/', include('chatboot.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


