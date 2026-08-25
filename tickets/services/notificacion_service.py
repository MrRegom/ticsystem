from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags

class NotificacionService:
    @staticmethod
    def _build_html_email(titulo, nombre_usuario, mensaje_principal, detalles_lista, footer_msg, nombre_sistema='TicSystem Mesa de Ayuda', pie_correo='Mesa de Ayuda - Plataforma Tecnológica'):
        detalles_html = ""
        for key, val in detalles_lista:
            detalles_html += f"<tr><td style='padding: 6px 0;'><strong style='color:#002855;'>{key}:</strong> <span style='color:#334155;'>{val}</span></td></tr>"
            
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
        </head>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 30px 10px;">
            <table width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f1f5f9">
                <tr>
                    <td align="center">
                        <table width="600" border="0" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;">
                            <tr>
                                <td align="center" style="background-color: #002855; color: #ffffff; padding: 24px; border-bottom: 4px solid #3b82f6;">
                                    <h2 style="margin: 0; font-size: 24px; font-weight: 600;">{nombre_sistema}</h2>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 32px;">
                                    <h3 style="color: #0f172a; margin-top: 0; font-size: 20px;">{titulo}</h3>
                                    <p style="font-size: 16px; line-height: 1.6; color: #1e293b;">Estimado(a) <strong>{nombre_usuario}</strong>,</p>
                                    <p style="font-size: 16px; line-height: 1.6; color: #1e293b;">{mensaje_principal}</p>
                                    
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
                            <tr>
                                <td align="center" style="background-color: #f8fafc; color: #64748b; padding: 20px; font-size: 13px; border-top: 1px solid #e2e8f0;">
                                    Este es un correo generado automáticamente. Por favor no responda a este mensaje.<br>
                                    <strong style="color: #002855;">{pie_correo}</strong>
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
    def generar_html_ticket(ticket, tipo, comentario=""):
        """Genera el HTML dinámico inyectando los datos del ticket."""
        solicitante_nombre = "Usuario"
        if ticket.solicitante:
            if hasattr(ticket.solicitante, 'nombres'):
                solicitante_nombre = f"{ticket.solicitante.nombres} {ticket.solicitante.apellidos}".strip()
            elif hasattr(ticket.solicitante, 'get_full_name'):
                solicitante_nombre = ticket.solicitante.get_full_name() or ticket.solicitante.username
        
        titulo_email = ""
        mensaje_principal = ""
        footer_msg = "Puede revisar el estado detallado ingresando a la plataforma."
        
        detalles_lista = [
            ("Código", ticket.correlativo),
            ("Usuario Notificador", solicitante_nombre),
        ]
        
        # Añadir ubicación y equipo si existen
        if ticket.activo:
            detalles_lista.append(("Equipo Afectado", ticket.activo.nombre))
        
        detalles_lista.append(("Motivo Original (Problema Reportado)", ticket.descripcion))
        
        if tipo == 'CREACION':
            titulo_email = "Registro de Nuevo Ticket"
            mensaje_principal = f"Se ha registrado exitosamente su solicitud en nuestra plataforma. Nuestro equipo de soporte técnico la atenderá a la brevedad."
            
        elif tipo == 'RESOLUCION':
            titulo_email = "Resolución de Ticket"
            mensaje_principal = f"Nos complace informarle que su solicitud ha sido analizada y marcada como <strong>RESUELTA</strong>."
            if comentario:
                detalles_lista.append(("Solución Aplicada / Resolución", comentario))
            footer_msg = "Si considera que el inconveniente persiste, por favor responda a este correo o reabra el ticket a través de la plataforma."
            
        elif tipo == 'ESCALADO':
            titulo_email = "Reasignación / Escalamiento de Ticket"
            mensaje_principal = f"Su ticket ha requerido la intervención de otros especialistas y ha sido <strong>REASIGNADO</strong> para asegurar una correcta solución."
            if comentario:
                detalles_lista.append(("Motivo del Escalamiento", comentario))
                
        elif tipo == 'ESPERA_APROBACION' or tipo == 'PENDIENTE':
            titulo_email = "Ticket en Espera"
            mensaje_principal = f"Su ticket se encuentra temporalmente en <strong>ESPERA</strong> debido a que requiere acciones administrativas o técnicas adicionales (ej. aprobación o adquisición de insumos)."
            if comentario:
                detalles_lista.append(("Detalle de la Espera", comentario))

        # Leer branding personalizado desde la configuración SMTP
        try:
            from correos.models import ConfiguracionSMTP
            smtp = ConfiguracionSMTP.load()
            nombre_sistema = smtp.nombre_sistema or 'TicSystem Mesa de Ayuda'
            pie_correo = smtp.pie_correo or 'Mesa de Ayuda - Plataforma Tecnológica'
        except Exception:
            nombre_sistema = 'TicSystem Mesa de Ayuda'
            pie_correo = 'Mesa de Ayuda - Plataforma Tecnológica'

        return NotificacionService._build_html_email(
            titulo=titulo_email,
            nombre_usuario=solicitante_nombre,
            mensaje_principal=mensaje_principal,
            detalles_lista=detalles_lista,
            footer_msg=footer_msg,
            nombre_sistema=nombre_sistema,
            pie_correo=pie_correo
        )

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
    def _encolar_correo(ticket, tipo: str, destinatario: str, asunto: str) -> None:
        """
        Método central de encolamiento.

        Lógica:
        1. Si no hay SMTP configurado → registra CorreoLog(SIN_SMTP) y retorna.
           Nunca se encola en Celery. El correo queda como registro histórico.
        2. Si hay SMTP → crea CorreoLog(PENDIENTE) y encola la tarea en Celery.
           El worker intentará el envío hasta 3 veces en background.
        """
        from correos.models import CorreoLog, ConfiguracionSMTP
        from correos.tasks import enviar_correo_task

        # Detectar si SMTP está configurado y activo
        smtp_activo = False
        try:
            smtp = ConfiguracionSMTP.load()
            smtp_activo = bool(smtp.host)
        except Exception:
            smtp_activo = False

        # Crear el registro de log (trazabilidad siempre)
        log = CorreoLog.objects.create(
            ticket=ticket,
            tipo=tipo,
            destinatario=destinatario,
            asunto=asunto,
            estado=CorreoLog.Estado.PENDIENTE if smtp_activo else CorreoLog.Estado.SIN_SMTP,
        )

        if not smtp_activo:
            # Sin SMTP: no se encola nada. El log queda como evidencia.
            return

        # Encolar en Celery — la vista ya respondió al usuario antes de esto
        try:
            enviar_correo_task.delay(log.id)
        except Exception as e:
            # Si Redis no está disponible, el correo queda PENDIENTE en BD.
            # El admin puede reenviarlo manualmente desde el panel.
            import logging
            logging.getLogger('correos').error(
                f"[Celery] No se pudo encolar correo log_id={log.id}: {e}"
            )

    @staticmethod
    def notificar_creacion(ticket):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (
            ticket.solicitante.correo if ticket.solicitante else None
        )
        if not correo_destino:
            return

        asunto = f"[Mesa de Ayuda] Ticket Creado: {ticket.correlativo}"
        NotificacionService._encolar_correo(
            ticket=ticket,
            tipo='CREACION',
            destinatario=correo_destino,
            asunto=asunto,
        )

    @staticmethod
    def notificar_resolucion(ticket, comentario):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (
            ticket.solicitante.correo if ticket.solicitante else None
        )
        if not correo_destino:
            return

        asunto = f"[Mesa de Ayuda] Ticket Resuelto: {ticket.correlativo}"
        NotificacionService._encolar_correo(
            ticket=ticket,
            tipo='RESOLUCION',
            destinatario=correo_destino,
            asunto=asunto,
        )
    @staticmethod
    def notificar_escalamiento(ticket, comentario=""):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (
            ticket.solicitante.correo if ticket.solicitante else None
        )
        if not correo_destino:
            return

        asunto = f"[Mesa de Ayuda] Ticket Escalamiento: {ticket.correlativo}"
        NotificacionService._encolar_correo(
            ticket=ticket,
            tipo='ESCALADO',
            destinatario=correo_destino,
            asunto=asunto,
        )

    @staticmethod
    def notificar_espera(ticket, comentario=""):
        correo_destino = ticket.correo_contacto if ticket.correo_contacto else (
            ticket.solicitante.correo if ticket.solicitante else None
        )
        if not correo_destino:
            return

        asunto = f"[Mesa de Ayuda] Ticket en Espera: {ticket.correlativo}"
        NotificacionService._encolar_correo(
            ticket=ticket,
            tipo='ESPERA_APROBACION',
            destinatario=correo_destino,
            asunto=asunto,
        )
