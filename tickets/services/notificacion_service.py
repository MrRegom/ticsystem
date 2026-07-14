from django.core.mail import send_mail
from django.conf import settings

class NotificacionService:
    @staticmethod
    def notificar_creacion(ticket):
        if not ticket.solicitante or not ticket.solicitante.correo:
            return
            
        asunto = f"[Mesa de Ayuda] Ticket Creado: {ticket.correlativo}"
        mensaje = f"""Estimado(a) {ticket.solicitante.nombre_completo},

Se ha registrado exitosamente su requerimiento/incidente en nuestro sistema.

Detalles del Ticket:
- Número: {ticket.correlativo}
- Descripción: {ticket.descripcion}
- Categoría: {ticket.categoria.nombre if ticket.categoria else 'N/A'}
- Prioridad Asignada: {ticket.prioridad.nombre if ticket.prioridad else 'N/A'}

Nuestro equipo técnico lo revisará a la brevedad.

Atentamente,
Unidad de Tecnologías de la Información
Hospital
"""
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [ticket.solicitante.correo],
                fail_silently=True,
            )
        except Exception as e:
            # En producción se debería loguear este error
            pass

    @staticmethod
    def notificar_resolucion(ticket, comentario):
        if not ticket.solicitante or not ticket.solicitante.correo:
            return
            
        asunto = f"[Mesa de Ayuda] Ticket Resuelto: {ticket.correlativo}"
        mensaje = f"""Estimado(a) {ticket.solicitante.nombre_completo},

Su ticket ha sido resuelto por nuestro equipo.

Detalles de la Resolución:
- Número: {ticket.correlativo}
- Técnico: {ticket.responsable.get_full_name() if ticket.responsable else 'Soporte TI'}
- Comentario de Cierre: {comentario}

Si considera que el problema persiste, por favor comuníquese nuevamente.

Atentamente,
Unidad de Tecnologías de la Información
Hospital
"""
        try:
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [ticket.solicitante.correo],
                fail_silently=True,
            )
        except Exception as e:
            pass
