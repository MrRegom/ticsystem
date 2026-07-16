from django.urls import path
from .views import ConfiguracionSMTPDashboardView, ConfiguracionSMTPAPIView, TestSMTPAPIView

app_name = 'correos'

urlpatterns = [
    path('configuracion/', ConfiguracionSMTPDashboardView.as_view(), name='configuracion_smtp'),
    path('api/config/', ConfiguracionSMTPAPIView.as_view(), name='api_config_smtp'),
    path('api/test/', TestSMTPAPIView.as_view(), name='api_test_smtp'),
]
