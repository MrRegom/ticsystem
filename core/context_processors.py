from django.contrib.auth.models import User

def global_users_for_impersonation(request):
    """
    Context processor para inyectar 'todos_usuarios' si el usuario es superadmin.
    Usado para el User Switcher (Impersonation) en entorno de desarrollo/pruebas.
    """
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.filter(is_active=True).prefetch_related('grupos_resolutores').order_by('username')
        user_data = []
        for u in users:
            grupos = ", ".join([g.nombre for g in u.grupos_resolutores.all()])
            display = f"{u.username}"
            if u.first_name:
                display += f" ({u.first_name})"
            if grupos:
                display += f" - [{grupos}]"
            user_data.append({'id': u.id, 'display': display})
            
        return {
            'todos_usuarios_dev': user_data
        }
    return {}
