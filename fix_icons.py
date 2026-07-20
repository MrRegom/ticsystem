import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Rol
from tickets.models import GrupoResolutor

roles_mapping = {
    'Mesa de Ayuda': 'ms-Icon--Headset',
    'Operador de Mesa de Ayuda': 'ms-Icon--ContactInfo',
    'Soporte Equipamiento y Hardware': 'ms-Icon--Devices3',
    'Super Administrador': 'ms-Icon--Shield',
    'Técnico de Soporte Nivel 2': 'ms-Icon--Wrench',
    'Técnicos Terreno': 'ms-Icon--Build'
}

for rol_nombre, icon in roles_mapping.items():
    rol = Rol.objects.filter(nombre=rol_nombre).first()
    if rol:
        rol.icono = icon
        rol.save()
        print(f"Assigned {icon} to Rol '{rol_nombre}'")

grupos = GrupoResolutor.objects.all()
for g in grupos:
    if not g.icono:
        g.icono = 'ms-Icon--Group'
        g.save()
        print(f"Assigned ms-Icon--Group to Grupo '{g.nombre}'")

print("Done!")
