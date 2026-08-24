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
            
            from django.core.mail import EmailMultiAlternatives
            from django.utils.html import strip_tags

            html_content = f"""
            <html>
            <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; color: #1e293b; margin: 0; padding: 30px 10px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    <div style="background-color: #002855; color: #ffffff; padding: 24px; text-align: center; border-bottom: 4px solid #3b82f6;">
                        <h2 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">TicSystem Mesa de Ayuda</h2>
                    </div>
                    <div style="padding: 32px;">
                        <h3 style="color: #0f172a; margin-top: 0; font-size: 20px;">Prueba de Conexión Exitosa</h3>
                        <p style="font-size: 16px; line-height: 1.6;">Estimado Administrador,</p>
                        <p style="font-size: 16px; line-height: 1.6;">La configuración del servidor de correos se ha validado correctamente. El sistema está listo para enviar notificaciones automáticas.</p>
                        
                        <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6; border-radius: 4px; padding: 20px; margin: 24px 0;">
                            <ul style="list-style: none; padding: 0; margin: 0; font-size: 15px; line-height: 1.6;">
                                <li style='margin-bottom: 8px;'><strong style='color:#002855;'>Servidor SMTP:</strong> <span style='color:#334155;'>{host}:{puerto}</span></li>
                                <li style='margin-bottom: 8px;'><strong style='color:#002855;'>Autenticación:</strong> <span style='color:#334155;'>{usuario}</span></li>
                                <li style='margin-bottom: 8px;'><strong style='color:#002855;'>Seguridad TLS:</strong> <span style='color:#334155;'>{'Activada' if use_tls else 'Desactivada'}</span></li>
                                <li style='margin-bottom: 8px;'><strong style='color:#002855;'>Estado:</strong> <span style='color:#10b981; font-weight: 600;'>Conectado</span></li>
                            </ul>
                        </div>
                    </div>
                    <div style="background-color: #f8fafc; color: #64748b; text-align: center; padding: 20px; font-size: 13px; border-top: 1px solid #e2e8f0;">
                        Este es un correo generado automáticamente. Por favor no responda a este mensaje.<br>
                        <strong style="color: #002855; display: inline-block; margin-top: 8px;">Unidad de Tecnologías de la Información</strong>
                    </div>
                </div>
            </body>
            </html>
            """
            
            email = EmailMultiAlternatives(
                subject='[Mesa de Ayuda] Prueba de Conexión SMTP Exitosa',
                body=strip_tags(html_content),
                from_email=remitente,
                to=[destinatario],
                connection=connection
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            return JsonResponse({'success': True, 'message': 'Correo de prueba enviado con éxito a tu bandeja.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Fallo la conexión SMTP: {str(e)}'}, status=400)


# =============================================================================
# PANEL DE CORREOS — Trazabilidad y Reenvío Manual
# =============================================================================

class CorreoLogPanelView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    """
    Panel de administración de logs de correos.
    Permite filtrar, visualizar estado y reenviar correos fallidos manualmente.
    Solo accesible para Super Administrador.
    """
    permiso_requerido = 'GESTIONAR_ROLES'
    template_name = 'correos/log_correos.html'

    def get_context_data(self, **kwargs):
        from .models import CorreoLog
        ctx = super().get_context_data(**kwargs)

        estado_filtro = self.request.GET.get('estado', '')
        fecha_desde   = self.request.GET.get('fecha_desde', '')
        fecha_hasta   = self.request.GET.get('fecha_hasta', '')

        qs = CorreoLog.objects.all()
        if estado_filtro:
            qs = qs.filter(estado=estado_filtro)
        if fecha_desde:
            qs = qs.filter(fecha_creacion__date__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(fecha_creacion__date__lte=fecha_hasta)

        ctx['logs']          = qs[:500]   # Límite de seguridad
        ctx['total']         = CorreoLog.objects.count()
        ctx['total_enviados'] = CorreoLog.objects.filter(estado=CorreoLog.Estado.ENVIADO).count()
        ctx['total_fallidos'] = CorreoLog.objects.filter(estado=CorreoLog.Estado.FALLIDO).count()
        ctx['total_sin_smtp'] = CorreoLog.objects.filter(estado=CorreoLog.Estado.SIN_SMTP).count()
        ctx['estado_filtro'] = estado_filtro
        ctx['fecha_desde']   = fecha_desde
        ctx['fecha_hasta']   = fecha_hasta
        ctx['estados']       = CorreoLog.Estado.choices
        return ctx


class CorreoReenviarAPIView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    """
    API para reenvío MANUAL de un correo fallido.
    
    Reglas:
    - Solo acepta correos con estado FALLIDO o SIN_SMTP.
    - SIN_SMTP: muestra advertencia en el frontend antes de llamar este endpoint.
    - Crea un NUEVO CorreoLog (no modifica el histórico original) para preservar la trazabilidad.
    - El admin queda registrado en el campo reenviado_manualmente.
    """
    permiso_requerido = 'GESTIONAR_ROLES'

    def post(self, request, correo_log_id, *args, **kwargs):
        from .models import CorreoLog, ConfiguracionSMTP
        from correos.tasks import enviar_correo_task

        try:
            log_original = CorreoLog.objects.get(id=correo_log_id)
        except CorreoLog.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Registro no encontrado.'}, status=404)

        # Solo se permite reenviar FALLIDO o SIN_SMTP
        if log_original.estado == CorreoLog.Estado.ENVIADO:
            return JsonResponse({'success': False, 'message': 'Este correo ya fue enviado exitosamente.'})
        if log_original.estado == CorreoLog.Estado.PENDIENTE:
            return JsonResponse({'success': False, 'message': 'Este correo ya está en cola pendiente.'})

        # Verificar SMTP antes de encolar
        try:
            smtp = ConfiguracionSMTP.load()
            smtp_activo = bool(smtp.host and smtp.activo)
        except Exception:
            smtp_activo = False

        if not smtp_activo:
            return JsonResponse({
                'success': False,
                'message': 'No hay SMTP configurado. Configure el servidor de correo primero.'
            }, status=400)

        # Crear nuevo log (el histórico original se preserva intacto)
        nuevo_log = CorreoLog.objects.create(
            ticket=log_original.ticket,
            tipo=log_original.tipo,
            destinatario=log_original.destinatario,
            asunto=f"[REENVÍO] {log_original.asunto}",
            estado=CorreoLog.Estado.PENDIENTE,
            reenviado_manualmente=True,
        )

        try:
            enviar_correo_task.delay(nuevo_log.id)
            return JsonResponse({
                'success': True,
                'message': f'Correo encolado para reenvío (nuevo log #{nuevo_log.id}).'
            })
        except Exception as e:
            nuevo_log.estado = CorreoLog.Estado.FALLIDO
            nuevo_log.error_detalle = f'Error al encolar: {str(e)}'
            nuevo_log.save(update_fields=['estado', 'error_detalle'])
            return JsonResponse({'success': False, 'message': f'No se pudo encolar: {str(e)}'}, status=500)


class CorreoLimpiarAPIView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    """Elimina logs antiguos de correos enviados (limpieza de histórico)."""
    permiso_requerido = 'GESTIONAR_ROLES'

    def post(self, request, *args, **kwargs):
        from .models import CorreoLog
        from django.utils import timezone
        from datetime import timedelta
        import json as _json

        data = _json.loads(request.body or '{}')
        dias = int(data.get('dias', 30))

        fecha_corte = timezone.now() - timedelta(days=dias)
        eliminados, _ = CorreoLog.objects.filter(
            estado=CorreoLog.Estado.ENVIADO,
            fecha_creacion__lt=fecha_corte
        ).delete()

        return JsonResponse({
            'success': True,
            'message': f'Se eliminaron {eliminados} registros enviados con más de {dias} días.'
        })

