from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from chatboot import views

urlpatterns = [
    path('chatboot-valida/', views.validaUsuarioChatboot),
    path('chatboot-cotizacion/', views.generaCotizacionChatboot),
    path('chatboot-elimina-pdf/', views.eliminaPDF),
    path('chatboot-valida-curriculum/', views.validaCurriculumChatboot),
    path('chatboot-envia-datos-agente/', views.enviaDatosAgenteChatboot),
    path('chatboot-envia-mensajes-agente/', views.obtener_agente_rotativo),
    path('chatboot-reporte-leads/', views.ListLeadsFiltro),
    path('chatboot-numeros-agentes/', views.ListNumerosFiltro),
    path('chatboot-alta-numeros-agentes/', views.numerosAgentesAlta),
    path('chatboot-leads-rango-reporte/', views.leadsReporte),
    path('chatboot-numeros-agentes-list/', views.listNumeros),
    path('chatboot-alta-lead/', views.leadAlta),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


