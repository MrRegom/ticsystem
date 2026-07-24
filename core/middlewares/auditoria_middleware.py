import json
from django.utils.deprecation import MiddlewareMixin
from core.models import LogAuditoria

class AuditoriaMiddleware(MiddlewareMixin):
    """
    Middleware Enterprise para Trazabilidad y Auditoría Continua.
    Registra toda la actividad relevante de los usuarios autenticados.
    """
    
    # Rutas clave (módulos) donde nos interesa registrar el acceso (GET)
    RUTAS_MODULOS = [
        '/dashboard/', '/tickets/', '/equipos/', '/reportes/',
        '/usuarios/', '/roles/', '/anexos/', '/actas/', '/sla/',
        '/mantenedores/', '/correos/configuracion/'
    ]

    def process_request(self, request):
        # Ignorar peticiones de usuarios no autenticados o rutas estáticas/admin
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return
            
        path = request.path
        if path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/'):
            return

        method = request.method
        
        # 1. Registrar accesos a módulos (GETs principales)
        if method == 'GET':
            if path in self.RUTAS_MODULOS:
                modulo_nombre = path.strip('/').capitalize() or 'Inicio'
                self._registrar_log(
                    request, 
                    'ACCESO', 
                    modulo_nombre, 
                    f"El usuario accedió al módulo: {modulo_nombre}"
                )
            return

        # 2. Registrar acciones que modifican datos (POST, PUT, DELETE, PATCH)
        if method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            # Ignorar el login para no ensuciar (Axess ya lo maneja o se puede manejar en signals)
            if '/login/' in path:
                return
                
            # Determinar acción
            accion = LogAuditoria.Accion.MODIFICAR
            if method == 'POST':
                accion = LogAuditoria.Accion.CREAR
            elif method == 'DELETE':
                accion = LogAuditoria.Accion.ELIMINAR
                
            # Intentar deducir la tabla o módulo afectado basado en la URL
            partes = [p for p in path.split('/') if p and not p.isdigit() and p != 'api']
            tabla = partes[0].capitalize() if partes else 'Sistema'
            
            # Construir detalles (evitando guardar payloads muy grandes o sensibles como passwords)
            detalles = f"Petición {method} a {path}"
            
            self._registrar_log(
                request, 
                accion, 
                tabla, 
                detalles
            )

    def _registrar_log(self, request, accion, tabla, detalles):
        try:
            ip = self._get_client_ip(request)
            usuario = request.user.username
            
            # Como LogAuditoria.Accion no tiene 'ACCESO', podemos usar algo genérico o 
            # forzarlo en el campo char
            accion_db = accion
            if accion == 'ACCESO':
                accion_db = 'ACCESO' # Aunque no esté en choices, el CharField lo acepta en BD SQLite/Postgres
                
            LogAuditoria.objects.create(
                usuario=usuario,
                accion=accion_db,
                tabla=tabla,
                detalles=detalles,
                ip_address=ip
            )
        except Exception:
            # Silenciar errores de auditoría para no romper la app principal en caso de fallo
            pass

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
