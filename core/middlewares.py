from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    """
    Middleware para evitar que el navegador guarde en caché páginas
    cuando el usuario está autenticado. Esto previene que al cerrar
    sesión y darle al botón 'Atrás', se muestre la app cacheada.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Si el usuario está autenticado, no cacheamos la página
        # O si acaba de cerrar sesión (la ruta es /login/ pero venía de la app)
        if hasattr(request, 'user') and request.user.is_authenticated:
            add_never_cache_headers(response)
        elif request.path.startswith('/dashboard') or request.path.startswith('/tickets'):
            add_never_cache_headers(response)
            
        return response

from django.utils.deprecation import MiddlewareMixin
from core.models import LogAuditoria

class AuditoriaMiddleware(MiddlewareMixin):
    """
    Middleware Enterprise para Trazabilidad y Auditoría Continua.
    Registra toda la actividad relevante de los usuarios autenticados.
    """
    
    RUTAS_MODULOS = [
        '/dashboard/', '/tickets/', '/equipos/', '/reportes/',
        '/usuarios/', '/roles/', '/anexos/', '/actas/', '/sla/',
        '/mantenedores/', '/correos/configuracion/'
    ]

    def process_request(self, request):
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return
            
        path = request.path
        if path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/'):
            return

        method = request.method
        
        if method == 'GET':
            if path in self.RUTAS_MODULOS:
                modulo_nombre = path.strip('/').capitalize() or 'Inicio'
                self._registrar_log(request, 'ACCESO', modulo_nombre, f"El usuario accedió al módulo: {modulo_nombre}")
            return

        if method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            if '/login/' in path:
                return
                
            accion = LogAuditoria.Accion.MODIFICAR
            if method == 'POST':
                accion = LogAuditoria.Accion.CREAR
            elif method == 'DELETE':
                accion = LogAuditoria.Accion.ELIMINAR
                
            partes = [p for p in path.split('/') if p and not p.isdigit() and p != 'api']
            tabla = partes[0].capitalize() if partes else 'Sistema'
            detalles = f"Petición {method} a {path}"
            
            self._registrar_log(request, accion, tabla, detalles)

    def _registrar_log(self, request, accion, tabla, detalles):
        try:
            ip = self._get_client_ip(request)
            usuario = request.user.username
            accion_db = accion
            if accion == 'ACCESO':
                accion_db = 'ACCESO'
                
            LogAuditoria.objects.create(
                usuario=usuario, accion=accion_db, tabla=tabla, detalles=detalles, ip_address=ip
            )
        except Exception:
            pass

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
