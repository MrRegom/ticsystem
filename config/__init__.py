# config package init.
# La migracion de datos MySQL/MariaDB→PostgreSQL (Fase 5) se hace con PyMySQL
# directo en el management command 'migrar_desde_mysql', sin pasar por el ORM de
# Django (Django 6.0 exige MariaDB 10.6+ y XAMPP trae 10.4.32).

# Cargar la app Celery al iniciar Django para que las tareas asíncronas
# estén disponibles automáticamente en todas las apps del proyecto.
from .celery import app as celery_app

__all__ = ('celery_app',)

