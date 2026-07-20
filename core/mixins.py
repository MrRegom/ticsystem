from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from core.services.rol_service import RolService

class PermisoRequeridoMixin(AccessMixin):
    """
    Verifica que el usuario logueado tenga el permiso requerido en su Rol.
    Rechaza con 403 si no lo tiene.
    """
    permiso_requerido = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.permiso_requerido:
            # Soportar validación de una lista/tupla de permisos (OR logic)
            if isinstance(self.permiso_requerido, (list, tuple)):
                tiene_permiso = any(RolService.validar_permiso(request.user, p) for p in self.permiso_requerido)
            else:
                tiene_permiso = RolService.validar_permiso(request.user, self.permiso_requerido)

            if not tiene_permiso:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or '/api/' in request.path:
                    return JsonResponse({'success': False, 'message': 'Acceso Denegado. No tiene permisos suficientes.'}, status=403)
                
                # Renderizar una plantilla 403 amigable si existe
                return render(request, 'core/403.html', status=403)

        return super().dispatch(request, *args, **kwargs)
