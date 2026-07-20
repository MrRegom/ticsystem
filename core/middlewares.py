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
