"""
Tareas Celery del módulo de Correos.

Arquitectura de reintentos (Enterprise Dead-Letter):
- Máximo 3 intentos con backoff exponencial: 60s → 300s → definitivo.
- Tras 3 fallos: estado = FALLIDO. Nunca más se reintenta automáticamente.
- Estado SIN_SMTP: la tarea detecta esto como salvaguarda y aborta sin error.
- Todo reenvío posterior es acción MANUAL del administrador en el panel.
"""
from celery import shared_task
from django.utils import timezone
import logging

logger = logging.getLogger('correos.tasks')

# Número máximo de reintentos antes de marcar como FALLIDO definitivo
MAX_REINTENTOS = 3


@shared_task(
    bind=True,
    max_retries=MAX_REINTENTOS,
    default_retry_delay=60,   # 1 minuto entre reintentos
    time_limit=60,
    name='correos.tasks.enviar_correo_task'
)
def enviar_correo_task(self, correo_log_id: int) -> dict:
    """
    Tarea Celery: intenta enviar un correo registrado en CorreoLog.
    
    Args:
        correo_log_id: ID del registro CorreoLog a procesar.
    
    Returns:
        dict con resultado del intento.
    """
    from correos.models import CorreoLog
    from correos.models import ConfiguracionSMTP
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings

    try:
        log = CorreoLog.objects.get(id=correo_log_id)
    except CorreoLog.DoesNotExist:
        logger.error(f"[Celery] CorreoLog id={correo_log_id} no encontrado. Tarea abortada.")
        return {'ok': False, 'error': 'CorreoLog no encontrado'}

    # Salvaguarda crítica: si por algún motivo llegó aquí un SIN_SMTP, abortar.
    if log.estado == CorreoLog.Estado.SIN_SMTP:
        logger.warning(f"[Celery] Correo id={correo_log_id} tiene estado SIN_SMTP. Abortando.")
        return {'ok': False, 'error': 'Estado SIN_SMTP, no se procesa'}

    # Si ya fue enviado exitosamente (tarea duplicada), ignorar.
    if log.estado == CorreoLog.Estado.ENVIADO:
        return {'ok': True, 'info': 'Ya enviado previamente'}

    # Verificar que SMTP esté activo ahora (puede haber cambiado desde que se encoló)
    try:
        smtp_config = ConfiguracionSMTP.load()
        if not smtp_config.host or not smtp_config.activo:
            # El SMTP se desconfiguró después de encolar. Marcar como FALLIDO definitivo.
            log.estado = CorreoLog.Estado.FALLIDO
            log.error_detalle = 'SMTP desconfigurado o inactivo al momento del envío.'
            log.fecha_ultimo_intento = timezone.now()
            log.save(update_fields=['estado', 'error_detalle', 'fecha_ultimo_intento'])
            logger.warning(f"[Celery] Correo id={correo_log_id} fallido: SMTP inactivo al procesar.")
            return {'ok': False, 'error': 'SMTP inactivo'}
    except Exception as e:
        logger.error(f"[Celery] Error cargando ConfiguracionSMTP: {e}")

    # Actualizar contador de intentos
    log.intentos += 1
    log.fecha_ultimo_intento = timezone.now()
    log.save(update_fields=['intentos', 'fecha_ultimo_intento'])

    try:
        from_email = smtp_config.remitente_por_defecto or settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(
            subject=log.asunto,
            body=log.asunto,          # Texto plano (fallback)
            from_email=from_email,
            to=[log.destinatario],
        )
        # El HTML se guarda en el campo cuerpo_html si lo implementamos;
        # por ahora usamos el asunto como body de emergencia.
        msg.send(fail_silently=False)

        # Éxito
        log.estado = CorreoLog.Estado.ENVIADO
        log.error_detalle = ''
        log.save(update_fields=['estado', 'error_detalle'])
        logger.info(f"[Celery] Correo id={correo_log_id} enviado exitosamente a {log.destinatario}.")
        return {'ok': True, 'destinatario': log.destinatario}

    except Exception as exc:
        error_str = str(exc)
        logger.warning(f"[Celery] Intento {log.intentos}/{MAX_REINTENTOS} fallido para correo id={correo_log_id}: {error_str}")

        if log.intentos >= MAX_REINTENTOS:
            # Dead-letter: máximos reintentos alcanzados, falla definitiva
            log.estado = CorreoLog.Estado.FALLIDO
            log.error_detalle = f"Fallo definitivo tras {MAX_REINTENTOS} intentos. Último error: {error_str}"
            log.save(update_fields=['estado', 'error_detalle'])
            logger.error(f"[Celery] Correo id={correo_log_id} marcado FALLIDO definitivo.")
            return {'ok': False, 'error': error_str}
        else:
            # Reintento con backoff: 60s primer reintento, 300s segundo
            delay = 60 if log.intentos == 1 else 300
            log.error_detalle = f"Intento {log.intentos}: {error_str}"
            log.save(update_fields=['error_detalle'])
            raise self.retry(exc=exc, countdown=delay)
