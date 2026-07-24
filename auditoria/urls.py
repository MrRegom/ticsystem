from django.urls import path
from . import views

app_name = 'auditoria'

urlpatterns = [
    path('', views.AuditoriaDashboardView.as_view(), name='dashboard'),
    path('api/logs/', views.AuditoriaLogsAPIView.as_view(), name='logs_api'),
]
