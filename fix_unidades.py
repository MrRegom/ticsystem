import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticsystem.settings')
django.setup()

from core.models import PerfilUsuario
from mantenedores.models import Unidad

unidades = {u.nombre.lower(): u.nombre for u in Unidad.objects.all()}
perfiles = PerfilUsuario.objects.all()
count = 0

for p in perfiles:
    if p.unidad and p.unidad.lower() in unidades and p.unidad != unidades[p.unidad.lower()]:
        p.unidad = unidades[p.unidad.lower()]
        p.save()
        count += 1

print(f"Arreglados {count} perfiles.")
