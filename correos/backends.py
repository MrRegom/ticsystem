from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)

class DynamicSMTPEmailBackend(EmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        try:
            from correos.models import ConfiguracionSMTP
            config = ConfiguracionSMTP.load()
            
            kwargs['host'] = config.host
            kwargs['port'] = config.puerto
            kwargs['username'] = config.usuario
            kwargs['password'] = config.password
            
            if config.puerto == 465:
                kwargs['use_ssl'] = True
                kwargs['use_tls'] = False
            else:
                kwargs['use_ssl'] = False
                kwargs['use_tls'] = config.use_tls

            # Set a hard timeout to prevent Gunicorn worker death
            kwargs.setdefault('timeout', 5)

            # Set default from email globally if not overridden
            from django.conf import settings
            if config.remitente_por_defecto:
                settings.DEFAULT_FROM_EMAIL = config.remitente_por_defecto

        except Exception as e:
            logger.error(f"Error cargando ConfiguracionSMTP dinámica: {e}")
            pass
            
        super().__init__(fail_silently=fail_silently, **kwargs)
