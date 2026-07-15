from django.urls import path
from sla.views import (
    SlaConfigView,
    SlaMatrixApiView,
    PrioridadListApiView,
    PrioridadApiView,
)

app_name = 'sla'

urlpatterns = [
    path('', SlaConfigView.as_view(), name='config'),
    path('api/matrix/', SlaMatrixApiView.as_view(), name='matrix_api'),
    path('api/prioridades/', PrioridadListApiView.as_view(), name='prioridades_list_api'),
    path('api/prioridades/action/', PrioridadApiView.as_view(), name='prioridades_action_api'),
]
