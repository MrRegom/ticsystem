import os
import dj_database_url
from .base import *

DEBUG = True

# Clave secreta de desarrollo (en produccion se exige DJANGO_SECRET_KEY via env)
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-dev-key-123456789'
)

ALLOWED_HOSTS = ['*']

# Base de datos: PostgreSQL local por defecto (via DATABASE_URL en .env).
# Si no hay DATABASE_URL definida, cae a SQLite para entornos minimos/tests.
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Nota: La migracion de datos MySQL→PG (Fase 5) se hace con PyMySQL directo
# (no via ORM de Django) porque Django 6.0 exige MariaDB 10.6+ y XAMPP trae 10.4.32.
# El management command 'migrar_desde_mysql' abre su propia conexion pymysql.

# Logs para desarrollo en consola
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
