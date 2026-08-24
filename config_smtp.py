import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from correos.models import ConfiguracionSMTP

obj = ConfiguracionSMTP.load()
obj.host = 'mail.servirec.cl'
obj.puerto = 465
obj.usuario = 'ticsystem@servirec.cl'
obj.password = 'Servirec2026..'
obj.remitente_por_defecto = 'ticsystem@servirec.cl'
obj.save()
print('SMTP configurado en producción con cPanel')
