from django.urls import path
from mantenedores.views import (
    MantenedoresDashboardView, MantenedorListView, MantenedorActionView, MantenedorDetailView,
)

app_name = 'mantenedores'
urlpatterns = [
    path('', MantenedoresDashboardView.as_view(), name='dashboard'),
    path('api/', MantenedorListView.as_view(), name='list_api'),
    path('api/action/', MantenedorActionView.as_view(), name='action_api'),
    path('api/<int:item_id>/', MantenedorDetailView.as_view(), name='detail_api'),
]
