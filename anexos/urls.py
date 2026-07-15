from django.urls import path
from anexos.views import (
    AnexosDashboardView, AnexoListView, AnexoActionView
)

app_name = 'anexos'

urlpatterns = [
    path('', AnexosDashboardView.as_view(), name='dashboard'),
    path('api/', AnexoListView.as_view(), name='list_api'),
    path('api/action/', AnexoActionView.as_view(), name='action_api'),
]
