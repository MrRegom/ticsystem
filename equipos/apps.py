from django.apps import AppConfig


class EquiposConfig(AppConfig):
    name = 'equipos'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Equipos'

    def ready(self):
        # Importar signals para activar audit trail y recálculo de estado
        from . import signals  # noqa: F401
