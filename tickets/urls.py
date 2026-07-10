from django.urls import path
from tickets.views import (
    TicketsDashboardView,
    TicketListView,
    TicketActionView,
    TicketDetailView,
)

app_name = 'tickets'

urlpatterns = [
    path('', TicketsDashboardView.as_view(), name='dashboard'),
    path('api/', TicketListView.as_view(), name='list_api'),
    path('api/action/', TicketActionView.as_view(), name='action_api'),
    path('api/<int:ticket_id>/', TicketDetailView.as_view(), name='detail_api'),
]
