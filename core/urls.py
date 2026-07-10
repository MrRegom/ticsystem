from django.urls import path
from django.views.generic import RedirectView
from core.views import (
    CustomLoginView, 
    CustomLogoutView, 
    DashboardGeneralView,
    UsuariosDashboardView,
    UsuarioListView,
    UsuarioActionView
)

urlpatterns = [
    # Redirección de la raíz del módulo
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    
    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Vistas de aplicación
    path('dashboard/', DashboardGeneralView.as_view(), name='dashboard'),

    path('usuarios/', UsuariosDashboardView.as_view(), name='usuarios_dashboard'),
    
    # APIs para AJAX

    path('api/usuarios/', UsuarioListView.as_view(), name='usuario_list_api'),
    path('api/usuarios/action/', UsuarioActionView.as_view(), name='usuario_action_api'),
]
