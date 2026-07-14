import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from core.models import Rol

for rol in Rol.objects.all():
    rol.nombre = rol.nombre.replace('TÃ©cnicos', 'Técnicos').replace('Ã©', 'é').replace('Ã³', 'ó').replace('Ã', 'í')
    if rol.descripcion:
        rol.descripcion = rol.descripcion.replace('TÃ©cnicos', 'Técnicos').replace('Ã©', 'é').replace('Ã³', 'ó').replace('Ã', 'í')
    rol.save()
print("Fix encoding local ok")
