from os import name
from django.urls import path, include
from usuarios import views
from .views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('list-user-filtro/', views.ListUsuarios),
    path('validar-usuario/', views.ValidaUsuario),
    path('valida/', views.ValidUser),
    path('login/', views.authenticate_user),
    path('loginInvitado/', views.authenticate_user_invited),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('validateUsername/', views.validarUsuario),
    path('registerUser/', views.registraUsuario),
    path('get-usuario/<int:pk>/', views.getUsuarios),
    path('editUsuario/', views.editarUsuario),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
