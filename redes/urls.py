from django.urls import path
from redes.views import RedesDashboardView, IpListView, IpActionView, IpDetailView

app_name = 'redes'

urlpatterns = [
    path('', RedesDashboardView.as_view(), name='dashboard'),
    path('api/', IpListView.as_view(), name='list_api'),
    path('api/action/', IpActionView.as_view(), name='action_api'),
    path('api/<int:ip_id>/', IpDetailView.as_view(), name='detail_api'),
]
