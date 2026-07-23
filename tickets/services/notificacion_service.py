from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

class NotificacionService:
    @staticmethod
    def _build_html_email(titulo, nombre_usuario, mensaje_principal, detalles_lista, footer_msg):
        detalles_html = "".join([f"<li style='margin-bottom: 8px;'><strong style='color:#002855;'>{k}:</strong> <span style='color:#334155;'>{v}</span></li>" for k, v in detalles_lista])
        return f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; color: #1e293b; margin: 0; padding: 30px 10px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div style="background-color: #002855; color: #ffffff; padding: 24px; text-align: center; border-bottom: 4px solid #3b82f6;">
                    <h2 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">TicSystem Mesa de Ayuda</h2>
                </div>
                <div style="padding: 32px;">
                    <h3 style="color: #0f172a; margin-top: 0; font-size: 20px;">{titulo}</h3>
                    <p style="font-size: 16px; line-height: 1.6;">Estimado(a) <strong>{nombre_usuario}</strong>,</p>
                    <p style="font-size: 16px; line-height: 1.6;">{mensaje_principal}</p>
                    
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 4px solid #3b82f6; border-radius: 4px; padding: 20px; margin: 24px 0;">
                        <ul style="list-style: none; padding: 0; margin: 0; font-size: 15px; line-height: 1.6;">
                            {detalles_html}
                        </ul>
                    </div>
                    
                    <p style="font-size: 15px; line-height: 1.6; color: #475569;">{footer_msg}</p>
                </div>
                <div style="background-color: #f8fafc; color: #64748b; text-align: center; padding: 20px; font-size: 13px; border-top: 1px solid #e2e8f0;">
                    Este es un correo generado automáticamente. Por favor no responda a este mensaje.<br>
                    <strong style="color: #002855; display: inline-block; margin-top: 8px;">Unidad de Tecnologías de la Información</strong>
                </div>
            </div>
        </body>
        </html>
        """

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
            msg = EmailMultiAlternatives(asunto, strip_tags(html_content), settings.DEFAULT_FROM_EMAIL, [correo_destino])
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
            msg = EmailMultiAlternatives(asunto, strip_tags(html_content), settings.DEFAULT_FROM_EMAIL, [correo_destino])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)
        except Exception:
            pass
