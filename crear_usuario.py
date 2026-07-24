import os, sys, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticsystem.settings")
django.setup()

from django.contrib.auth.models import User
from core.models import PerfilUsuario, Rol
from tickets.models import GrupoResolutor

# 1. Crear usuario super administrador
rut = '17944996-k'
email = 'christian.balladares.v@redsalud.gob.cl'
nombres = 'Christian Alcione Rodolfo'
apellidos = 'Balladares Vinet'

user, created = User.objects.get_or_create(username=rut, defaults={
    'email': email,
    'first_name': nombres[:30],
    'last_name': apellidos[:30],
    'is_staff': True,
    'is_superuser': True,
    'is_active': True
})
user.set_password(rut)
user.save()

# Obtener rol super admin
rol_super_admin = Rol.objects.filter(nombre__icontains='Super').first()

# Actualizar perfil
perfil, _ = PerfilUsuario.objects.get_or_create(user=user, defaults={'rut': rut})
perfil.rut = rut
perfil.nombres = nombres
perfil.apellidos = apellidos
perfil.cargo = 'Desarrollador'
perfil.rol = rol_super_admin
perfil.save()

print(f"Usuario {nombres} {apellidos} ({rut}) creado exitosamente como Super Administrador. Clave: {rut}")

# 2. Crear grupos resolutores basicos
grupos = [
    ("Soporte Software", "Atención de incidentes y requerimientos de software y sistemas informáticos."),
    ("Soporte Hardware", "Mantenimiento y reparación de equipos físicos e impresoras."),
    ("Sistemas Médicos", "Soporte de sistemas clínicos, HIS, LIS y equipos médicos digitalizados."),
    ("Infraestructura y Redes", "Soporte a servidores, conectividad, redes y telefonía."),
    ("Mesa de Ayuda (Derivación)", "Primer nivel de atención, filtro y derivación de tickets.")
]

for nombre, desc in grupos:
    g, c = GrupoResolutor.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
    if c:
        print(f"Grupo resolutor '{nombre}' creado.")

print("Listo!")
