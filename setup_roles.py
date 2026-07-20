import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from core.models import Rol

# Permisos Base (todos los roles los tendrán)
PERMISOS_BASE = {
    'VER_INICIO': True
}

# 1. Super Administrador (Ve TODO)
admin_permisos = {
    'VER_INICIO': True,
    'VER_USUARIOS': True,
    'GESTIONAR_USUARIOS': True,
    'VER_EQUIPOS': True,
    'GESTIONAR_EQUIPOS': True,
    'VER_MANTENEDORES': True,
    'GESTIONAR_MANTENEDORES': True,
    'VER_TICKETS': True,
    'GESTIONAR_TICKETS': True,
    'VER_REPORTES': True,
    'VER_ACTAS': True,
    'GESTIONAR_ACTAS': True,
    'VER_ANEXOS': True,
    'GESTIONAR_ANEXOS': True,
    'GESTIONAR_ROLES': True,
}

rol_admin, created = Rol.objects.get_or_create(nombre='Super Administrador')
rol_admin.permisos = admin_permisos
rol_admin.descripcion = 'Acceso total a todos los módulos y configuración'
rol_admin.save()
print(f"Rol '{rol_admin.nombre}' configurado.")

# 2. Mesa de Ayuda (Crea tickets y deriva)
mesa_ayuda_permisos = {
    'VER_INICIO': True,
    'VER_TICKETS': True,
    'GESTIONAR_TICKETS': True,  # Puede derivar, crear, etc.
}
rol_mesa, created = Rol.objects.get_or_create(nombre='Mesa de Ayuda')
rol_mesa.permisos = mesa_ayuda_permisos
rol_mesa.descripcion = 'Atención de Nivel 1, creación y derivación de tickets'
rol_mesa.save()
print(f"Rol '{rol_mesa.nombre}' configurado.")


# 3. Técnicos Terreno (Solo tickets, Nivel 2, Grupos resolutores genéricos)
tecnico_permisos = {
    'VER_INICIO': True,
    'VER_TICKETS': True,
    'GESTIONAR_TICKETS': True, # Porque necesitan responder y cerrar tickets
}
rol_tecnico, created = Rol.objects.get_or_create(nombre='Técnicos Terreno')
rol_tecnico.permisos = tecnico_permisos
rol_tecnico.descripcion = 'Atención de Nivel 2 en terreno'
rol_tecnico.save()
print(f"Rol '{rol_tecnico.nombre}' configurado.")


# 4. Soporte Equipamiento y Hardware (Tickets + Equipos)
equipamiento_permisos = {
    'VER_INICIO': True,
    'VER_TICKETS': True,
    'GESTIONAR_TICKETS': True,
    'VER_EQUIPOS': True,
    'GESTIONAR_EQUIPOS': True, # Para mover la bitácora e inventario
}
rol_equip, created = Rol.objects.get_or_create(nombre='Soporte Equipamiento y Hardware')
rol_equip.permisos = equipamiento_permisos
rol_equip.descripcion = 'Técnicos con acceso al inventario de Equipos TIC'
rol_equip.save()
print(f"Rol '{rol_equip.nombre}' configurado.")
print("Roles configurados exitosamente en la base de datos.")

# ---------------------------------------------
# Grupos del Sistema (SPOC)
# ---------------------------------------------
from tickets.models import GrupoResolutor

grupo_mesa, created = GrupoResolutor.objects.get_or_create(
    nombre="Mesa de Ayuda",
    defaults={
        'descripcion': "Grupo principal (SPOC) para recepción y derivación de incidentes",
        'icono': 'ms-Icon--Headset',
        'is_system': True
    }
)
if not created and not grupo_mesa.is_system:
    grupo_mesa.is_system = True
    grupo_mesa.save()

print(f"Grupo de Sistema '{grupo_mesa.nombre}' configurado exitosamente.")
