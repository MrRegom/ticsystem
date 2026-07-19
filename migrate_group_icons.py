import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from tickets.models import GrupoResolutor

grupos = GrupoResolutor.objects.filter(icono__startswith='ms-Icon')
updated = grupos.update(icono='fas fa-users')
print(f"Grupos resolutores actualizados: {updated}")
