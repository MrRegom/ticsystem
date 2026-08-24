"""
Configuración de la aplicación Celery para TicSystem.
Celery actúa como el orquestador de tareas asíncronas (envío de correos, reportes, etc.)
El broker es Redis y los resultados se guardan en PostgreSQL via django-celery-results.
"""
import os
from celery import Celery

# Establecer el módulo de settings por defecto de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crear la instancia de la aplicación Celery
app = Celery('ticsystem')

# Cargar configuración desde Django settings usando el namespace 'CELERY'
# Todas las variables de configuración de Celery deben tener el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscovery de tareas en todos los módulos tasks.py de las apps instaladas
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Tarea de diagnóstico para verificar que Celery está funcionando."""
    print(f'Request: {self.request!r}')
