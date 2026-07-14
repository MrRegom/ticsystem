from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.DashboardReportesView.as_view(), name='dashboard'),
]
