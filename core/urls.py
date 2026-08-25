from django.urls import path
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
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
    ManualUsuarioView,
    DocumentacionView
)

urlpatterns = [
    # Redirección de la raíz del módulo
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
    
    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # --- Autogestión de contraseñas (Recuperación) ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Vistas de aplicación
    path('dashboard/', DashboardGeneralView.as_view(), name='dashboard'),
    path('switch_user/', SwitchUserView.as_view(), name='switch_user'),
    path('manual/', ManualUsuarioView.as_view(), name='manual_usuario'),
    path('documentacion/docs/', DocumentacionView.as_view(), name='documentacion_docs'),

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
