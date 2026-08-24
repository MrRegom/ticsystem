from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.TicketsDashboardView.as_view(), name='dashboard'),
    path('api/action/', views.TicketActionView.as_view(), name='api_action'),
    path('api/ticket/<int:ticket_id>/', views.TicketDetailApiView.as_view(), name='api_ticket_detail'),
    path('api/ticket/<int:ticket_id>/assign/', views.TicketAssignApiView.as_view(), name='api_ticket_assign'),
    path('api/ticket/<int:ticket_id>/comment/', views.TicketCommentApiView.as_view(), name='api_ticket_comment'),
    path('api/ticket/<int:ticket_id>/resolve/', views.TicketResolveApiView.as_view(), name='api_ticket_resolve'),
    path('api/ticket/<int:ticket_id>/take/', views.TicketTakeApiView.as_view(), name='api_ticket_take'),
    path('api/ticket/<int:ticket_id>/reactivate/', views.TicketReactivateApiView.as_view(), name='api_ticket_reactivate'),
    path('api/dev/switch-user/', views.SwitchUserView.as_view(), name='api_dev_switch_user'),
    path('api/search/users/', views.UserSearchApiView.as_view(), name='api_search_users'),
    path('api/search/users/create/', views.UserCreateApiView.as_view(), name='api_create_user'),
    path('api/search/kedb/', views.KEDBSearchApiView.as_view(), name='api_search_kedb'),
    path('api/sync/', views.TicketSyncApiView.as_view(), name='api_ticket_sync'),
    path('api/notificaciones/', views.TicketNotificacionesApiView.as_view(), name='api_ticket_notificaciones'),
    path('api/notificaciones/<int:notificacion_id>/leida/', views.NotificacionMarcarLeidaApiView.as_view(), name='api_notificacion_leida'),
    path('api/notificaciones/todas-leidas/', views.NotificacionMarcarTodasLeidasApiView.as_view(), name='api_notificacion_todas_leidas'),
    path('api/historial/dt/', views.TicketHistorialDataTablesView.as_view(), name='api_historial_dt'),
]
