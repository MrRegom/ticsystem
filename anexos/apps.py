from django.apps import AppConfig


class AnexosConfig(AppConfig):
    name = 'anexos'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Anexos Telefónicos'

    def ready(self):
        pass
