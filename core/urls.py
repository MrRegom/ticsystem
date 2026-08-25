from django.urls import path
from django.views.generic import RedirectView, TemplateView
from core.views import (
    CustomLoginView, 
    CustomLogoutView, 
    DashboardGeneralView,
    UsuariosDashboardView,
    RolesDashboardView,
    RolesAPIView,
    RolesDetailAPIView,
    UsuarioListView,
    UsuarioActionView,
    UsuarioCrearAPIView,
    UsuarioEditarAPIView,
    UsuarioDisableRestoreAPIView,
    SwitchUserView,
    FuncionarioSearchAPIView,
    FuncionarioCreateAPIView,
    ManualUsuarioView
)

urlpatterns = [
    # Redirección de la raíz del módulo
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    
    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Vistas de aplicación
    path('dashboard/', DashboardGeneralView.as_view(), name='dashboard'),
    path('switch_user/', SwitchUserView.as_view(), name='switch_user'),
    path('manual/', ManualUsuarioView.as_view(), name='manual_usuario'),
    path('documentacion/docs/', TemplateView.as_view(template_name='core/documentacion.html'), name='documentacion_docs'),

    path('usuarios/', UsuariosDashboardView.as_view(), name='usuarios_dashboard'),
    path('roles/', RolesDashboardView.as_view(), name='roles_dashboard'),
    
    # APIs para AJAX
    path('api/roles/', RolesAPIView.as_view(), name='roles_api'),
    path('api/roles/<int:rol_id>/', RolesDetailAPIView.as_view(), name='roles_detail_api'),

    path('api/usuarios/', UsuarioListView.as_view(), name='usuario_list_api'),
    path('api/usuarios/crear/', UsuarioCrearAPIView.as_view(), name='usuario_crear_api'),
    path('api/usuarios/editar/', UsuarioEditarAPIView.as_view(), name='usuario_editar_api'),
    path('api/usuarios/action/', UsuarioActionView.as_view(), name='usuario_action_api'),
    path('api/usuarios/disable-restore/', UsuarioDisableRestoreAPIView.as_view(), name='usuario_disable_restore_api'),
    path('api/funcionarios/search/', FuncionarioSearchAPIView.as_view(), name='funcionario_search_api'),
    path('api/funcionarios/crear/', FuncionarioCreateAPIView.as_view(), name='funcionario_create_api'),
]
