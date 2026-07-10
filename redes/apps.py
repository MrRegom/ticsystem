from django.apps import AppConfig


class RedesConfig(AppConfig):
    name = 'redes'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = 'Redes / IPAM'

    def ready(self):
        from . import signals  # noqa: F401
