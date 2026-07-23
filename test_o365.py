import os, sys, django
sys.path.append('/var/www/ticsystem')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
from correos.models import ConfiguracionSMTP
config = ConfiguracionSMTP.load()
config.host = 'smtp.office365.com'
config.puerto = 587
config.usuario = 'informativos.hgf@appminsal.cl'
config.password = 'inhgf0304$'
config.remitente_por_defecto = 'informativos.hgf@appminsal.cl'
config.use_tls = True
config.save()

from django.core.mail import EmailMessage
try:
    EmailMessage('Prueba Office365 HGF', 'Hola Reinaldo, esto salió por Office365', 'informativos.hgf@appminsal.cl', ['reinaldo.gomez@redsalud.gob.cl']).send(fail_silently=False)
    print('EXITO')
except Exception as e:
    print('ERROR:', str(e))
