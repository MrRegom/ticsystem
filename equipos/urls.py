from django.urls import path
from equipos.views import (
    EquiposDashboardView,
    EquipoListView,
    EquipoActionView,
    EquipoDetailView,
    EquipoDetailReadView,
    EquipoHistorialView,
    EquipoBitacoraView,
    BitacoraRegistroView,
    ModelosPorMarcaView,
    EquipoCheckView,
    ImportarMargaMargaView,
    EquiposPanelControlView,
)

app_name = 'equipos'

urlpatterns = [
    path('', EquiposDashboardView.as_view(), name='dashboard'),
    path('panel/', EquiposPanelControlView.as_view(), name='panel'),
    path('api/', EquipoListView.as_view(), name='list_api'),
    path('api/action/', EquipoActionView.as_view(), name='action_api'),
    path('api/<int:equipo_id>/', EquipoDetailView.as_view(), name='detail_api'),
    path('api/<int:equipo_id>/ver/', EquipoDetailReadView.as_view(), name='detail_read'),
    path('api/<int:equipo_id>/historial/', EquipoHistorialView.as_view(), name='historial'),
    path('api/<int:equipo_id>/bitacora/', EquipoBitacoraView.as_view(), name='bitacora'),
    path('api/bitacora/<int:bitacora_id>/', BitacoraRegistroView.as_view(), name='bitacora_registro'),
    path('api/modelos/<int:marca_id>/', ModelosPorMarcaView.as_view(), name='modelos_por_marca'),
    path('api/check/', EquipoCheckView.as_view(), name='check'),
    path('importar-marga-marga/', ImportarMargaMargaView.as_view(), name='importar_marga_marga'),
]
