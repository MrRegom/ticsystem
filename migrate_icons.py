import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Rol

# Map old icons to new FontAwesome icons (using fas fa-user-circle as fallback)
roles = Rol.objects.filter(icono__startswith='ms-Icon')
for r in roles:
    r.icono = 'fas fa-user-circle'
    r.save()

print("Icons migrated to fas fa-user-circle successfully!")
