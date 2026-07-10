from django.apps import AppConfig


class ActasConfig(AppConfig):
    name = 'actas'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Actas de Entrega'

    def ready(self):
        pass
