from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

class NotificacionService:
    @staticmethod
    def _build_html_email(titulo, nombre_usuario, mensaje_principal, detalles_lista, footer_msg):
        detalles_html = ""
        for key, val in detalles_lista:
            detalles_html += f"<tr><td style='padding: 6px 0;'><strong style='color:#002855;'>{key}:</strong> <span style='color:#334155;'>{val}</span></td></tr>"
            
        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 30px 10px;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f1f5f9">
                <tr>
                    <td align="center">
                        <!-- Contenedor Principal (Tabla) para Outlook -->
                        <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;">
                            <!-- Header -->
                            <tr>
                                <td align="center" style="background-color: #002855; color: #ffffff; padding: 24px; border-bottom: 4px solid #3b82f6;">
                                    <h2 style="margin: 0; font-size: 24px; font-weight: 600;">TicSystem Mesa de Ayuda</h2>
                                </td>
                            </tr>
                            <!-- Body -->
                            <tr>
                                <td style="padding: 32px;">
                                    <h3 style="color: #0f172a; margin-top: 0; font-size: 20px;">{titulo}</h3>
                                    <p style="font-size: 16px; line-height: 1.6; color: #1e293b;">Estimado(a) <strong>{nombre_usuario}</strong>,</p>
                                    <p style="font-size: 16px; line-height: 1.6; color: #1e293b;">{mensaje_principal}</p>
                                    
                                    <!-- Detalles Box -->
                                    <table width="100%" border="0" cellspacing="0" cellpadding="20" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6; margin: 24px 0;">
                                        <tr>
                                            <td style="font-size: 15px; line-height: 1.6;">
                                                <table border="0" cellspacing="0" cellpadding="0">
                                                    {detalles_html}
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                    <p style="font-size: 15px; line-height: 1.6; color: #475569;">{footer_msg}</p>
                                </td>
                            </tr>
                            <!-- Footer -->
                            <tr>
                                <td align="center" style="background-color: #f8fafc; color: #64748b; padding: 20px; font-size: 13px; border-top: 1px solid #e2e8f0;">
                                    Este es un correo generado automáticamente. Por favor no responda a este mensaje.<br>
                                    <strong style="color: #002855;">Unidad de Tecnologías de la Información</strong>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    @staticmethod
    def crear_notificacion_interna(usuario, ticket, mensaje):
        from tickets.models import Notificacion
        # Evitar crear más de 100 notificaciones por usuario y limpiar antiguas
        if Notificacion.objects.filter(usuario=usuario).count() >= 100:
            viejas = Notificacion.objects.filter(usuario=usuario).order_by('-fecha_creacion')[99:]
            for v in viejas:
                v.delete()
                
        Notificacion.objects.create(
            usuario=usuario,
            ticket=ticket,
            mensaje=mensaje
        )

    @staticmethod
    def notificar_creacion(ticket):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (ticket.solicitante.correo if ticket.solicitante else None)
        if not correo_destino:
            return
            
        asunto = f"[Mesa de Ayuda] Ticket Creado: {ticket.correlativo}"
        detalles = [
            ("Número de Ticket", ticket.correlativo),
            ("Descripción", ticket.descripcion),
            ("Categoría", ticket.categoria.nombre if ticket.categoria else 'N/A'),
            ("Prioridad Asignada", ticket.prioridad.nombre if ticket.prioridad else 'Pendiente')
        ]
        
        html_content = NotificacionService._build_html_email(
            titulo="Su Ticket ha sido ingresado con éxito",
            nombre_usuario=ticket.solicitante.nombre_completo if ticket.solicitante else 'Usuario',
            mensaje_principal="Hemos registrado exitosamente su requerimiento/incidente en nuestro sistema. A continuación los detalles de su solicitud:",
            detalles_lista=detalles,
            footer_msg="Nuestro equipo técnico revisará su caso a la brevedad posible."
        )
        try:
            from correos.models import ConfiguracionSMTP
            config = ConfiguracionSMTP.load()
            from_email = config.remitente_por_defecto or settings.DEFAULT_FROM_EMAIL
            
            msg = EmailMultiAlternatives(asunto, strip_tags(html_content), from_email, [correo_destino])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass
    @staticmethod
    def notificar_resolucion(ticket, comentario):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (ticket.solicitante.correo if ticket.solicitante else None)
        if not correo_destino:
            return
            
        asunto = f"[Mesa de Ayuda] Ticket Resuelto: {ticket.correlativo}"
        detalles = [
            ("Número de Ticket", ticket.correlativo),
            ("Técnico Asignado", ticket.responsable.get_full_name() if ticket.responsable else 'Soporte TI'),
            ("Solución Técnica", comentario)
        ]
        
        html_content = NotificacionService._build_html_email(
            titulo="Su Ticket ha sido resuelto",
            nombre_usuario=ticket.solicitante.nombre_completo if ticket.solicitante else 'Usuario',
            mensaje_principal="Le informamos que el equipo técnico ha marcado su ticket como resuelto. Detalles de la solución:",
            detalles_lista=detalles,
            footer_msg="Si considera que el problema persiste o requiere asistencia adicional, por favor comuníquese con nosotros indicando el número de su ticket."
        )
        try:
            from correos.models import ConfiguracionSMTP
            config = ConfiguracionSMTP.load()
            from_email = config.remitente_por_defecto or settings.DEFAULT_FROM_EMAIL
            
            msg = EmailMultiAlternatives(asunto, strip_tags(html_content), from_email, [correo_destino])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass
