import os, sys, django
sys.path.append('/var/www/ticsystem')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
from correos.models import ConfiguracionSMTP
config = ConfiguracionSMTP.load()
config.host = 'mail.servirec.cl'
config.puerto = 465
config.usuario = 'ticsystem@servirec.cl'
config.password = 'Servirec2026..'
config.use_tls = False
config.remitente_por_defecto = 'ticsystem@servirec.cl'
config.save()
print('Configuracion SMTP actualizada con exito en Produccion.')
