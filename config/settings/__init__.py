import os
from dotenv import load_dotenv

# Cargar variables de entorno antes de importar settings
# Esto es necesario si se levanta el servidor usando WSGI directamente en producción
load_dotenv()

django_env = os.environ.get('DJANGO_ENV', 'local').lower()

if django_env == 'production':
    from .production import *
elif django_env == 'development':
    from .development import *
elif django_env == 'testing':
    from .testing import *
else:
    from .local import *
