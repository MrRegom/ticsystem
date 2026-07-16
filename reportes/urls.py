from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.DashboardReportesView.as_view(), name='dashboard'),
    path('exportar/tickets/', views.ExportarTicketsView.as_view(), name='exportar_tickets'),
    path('exportar/activos/', views.ExportarActivosView.as_view(), name='exportar_activos'),
]
