from django.urls import path
from .views import (
    ConfiguracionSMTPDashboardView, 
    ConfiguracionSMTPAPIView, 
    TestSMTPAPIView,
    CorreoLogPanelView,
    CorreoReenviarAPIView,
    CorreoLimpiarAPIView
)

app_name = 'correos'

urlpatterns = [
    # SMTP Config
    path('configuracion/', ConfiguracionSMTPDashboardView.as_view(), name='configuracion_smtp'),
    path('api/config/', ConfiguracionSMTPAPIView.as_view(), name='api_config_smtp'),
    path('api/test/', TestSMTPAPIView.as_view(), name='api_test_smtp'),
    
    # Panel de Correos (Trazabilidad)
    path('logs/', CorreoLogPanelView.as_view(), name='log_correos'),
    path('api/logs/<int:correo_log_id>/reenviar/', CorreoReenviarAPIView.as_view(), name='api_reenviar_correo'),
    path('api/logs/limpiar/', CorreoLimpiarAPIView.as_view(), name='api_limpiar_correos'),
]

