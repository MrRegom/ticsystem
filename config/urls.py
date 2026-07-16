"""
URL configuration for config project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('equipos/', include('equipos.urls')),
    path('anexos/', include('anexos.urls')),
    path('actas/', include('actas.urls')),
    path('mantenedores/', include('mantenedores.urls')),
    path('tickets/', include('tickets.urls')),
    path('reportes/', include('reportes.urls')),
    path('sla/', include('sla.urls')),
    path('correos/', include('correos.urls')),
]

if settings.DEBUG:
    # Solo agregar la ruta si debug_toolbar está disponible
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
        ]
    except ImportError:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
