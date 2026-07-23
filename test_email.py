import os, sys, django
sys.path.append('/var/www/ticsystem')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
from django.core.mail import EmailMessage
try:
    EmailMessage('Prueba directa desde servidor', 'Hola', 'ticsystem@servirec.cl', ['reinaldo.gomez@redsalud.gob.cl']).send(fail_silently=False)
    print('EXITO')
except Exception as e:
    print('ERROR:', str(e))
