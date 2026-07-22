import json
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisoRequeridoMixin
from django.core.mail import get_connection, EmailMessage
from .models import ConfiguracionSMTP

class ConfiguracionSMTPDashboardView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    permiso_requerido = 'GESTIONAR_ROLES'
    """Renderiza la pantalla frontend para configurar el SMTP."""
    template_name = 'correos/configuracion.html'

class ConfiguracionSMTPAPIView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ROLES'
    """API para obtener y guardar la configuración SMTP."""
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'Acceso denegado.'}, status=403)
        
        config = ConfiguracionSMTP.load()
        return JsonResponse({
            'success': True,
            'data': {
                'host': config.host,
                'puerto': config.puerto,
                'usuario': config.usuario or '',
                'password': config.password or '',
                'use_tls': config.use_tls,
                'remitente_por_defecto': config.remitente_por_defecto or ''
            }
        })

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'Acceso denegado.'}, status=403)
        
        try:
            data = json.loads(request.body)
            config = ConfiguracionSMTP.load()
            
            config.host = data.get('host', 'smtp.office365.com')
            config.puerto = int(data.get('puerto', 587))
            config.usuario = data.get('usuario', '')
            config.password = data.get('password', '')
            config.use_tls = bool(data.get('use_tls', True))
            config.remitente_por_defecto = data.get('remitente_por_defecto', '')
            
            config.save()
            return JsonResponse({'success': True, 'message': 'Configuración guardada correctamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

class TestSMTPAPIView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ROLES'
    """API para probar la conexión SMTP con las credenciales enviadas desde el UI."""
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'Acceso denegado.'}, status=403)
        
        try:
            data = json.loads(request.body)
            host = data.get('host', '')
            puerto = int(data.get('puerto', 587))
            usuario = data.get('usuario', '')
            password = data.get('password', '')
            use_tls = bool(data.get('use_tls', True))
            remitente = data.get('remitente_por_defecto', usuario)
            destinatario = data.get('test_email_to')
            if not destinatario:
                destinatario = request.user.email
            
            # Intentar conexión
            connection = get_connection(
                host=host,
                port=puerto,
                username=usuario,
                password=password,
                use_tls=use_tls,
                fail_silently=False
            )
            
            email = EmailMessage(
                subject='TicSystem: Prueba de Conexión Exitosa',
                body='Si estás leyendo esto, la configuración SMTP es correcta.',
                from_email=remitente,
                to=[destinatario],
                connection=connection
            )
            email.send()
            
            return JsonResponse({'success': True, 'message': 'Correo de prueba enviado con éxito a tu bandeja.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fallo la conexión SMTP: {str(e)}'}, status=400)
