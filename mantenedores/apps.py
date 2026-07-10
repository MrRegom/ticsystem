from django.apps import AppConfig


class MantenedoresConfig(AppConfig):
    name = 'mantenedores'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Mantenedores'

    def ready(self):
        pass
