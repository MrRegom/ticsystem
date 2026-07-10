from django.urls import path
from actas.views import (
    ActasDashboardView,
    ActaListView,
    ActaActionView,
    ActaDetailView,
)

app_name = 'actas'

urlpatterns = [
    path('', ActasDashboardView.as_view(), name='dashboard'),
    path('api/', ActaListView.as_view(), name='list_api'),
    path('api/action/', ActaActionView.as_view(), name='action_api'),
    path('api/<int:acta_id>/', ActaDetailView.as_view(), name='detail_api'),
]
