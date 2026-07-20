import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Rol
from core.services.rol_service import PERMISOS_DISPONIBLES

# 1. Asegurar roles clave y sus permisos exactos
todosp = [p['id'] for p in PERMISOS_DISPONIBLES]
permisos_admin = {p: True for p in todosp}

# Super Administrador
rol_superadmin, _ = Rol.objects.get_or_create(
    nombre='Super Administrador', 
    defaults={
        'descripcion': 'Acceso total a todos los módulos y configuración', 
        'icono': 'fas fa-shield-alt'
    }
)
rol_superadmin.permisos = permisos_admin
rol_superadmin.save()

# Técnico Nivel 2
rol_tecnico, _ = Rol.objects.get_or_create(
    nombre='Técnico Nivel 2', 
    defaults={
        'descripcion': 'Técnico que va a terreno a resolver incidentes y tickets', 
        'icono': 'fas fa-tools'
    }
)
rol_tecnico.permisos = {
    'VER_INICIO': True, 
    'VER_TICKETS': True, 
    'RECIBIR_TICKETS': True, 
    'VER_EQUIPOS': True
}
rol_tecnico.save()

# Operador de Mesa de Ayuda (Asignador)
rol_operador, _ = Rol.objects.get_or_create(
    nombre='Operador de Mesa de Ayuda', 
    defaults={
        'descripcion': 'Recibe tickets nuevos y los asigna a técnicos o grupos', 
        'icono': 'fas fa-headset'
    }
)
rol_operador.permisos = {
    'VER_INICIO': True, 
    'VER_TICKETS': True, 
    'DESPACHAR_TICKETS': True, 
    'GESTIONAR_TICKETS': True,
    'VER_EQUIPOS': True,
    'VER_MANTENEDORES': True
}
rol_operador.save()

# 2. Reasignar usuarios de roles a borrar hacia los nuevos roles oficiales
def migrar_usuarios(nombre_origen, rol_destino):
    try:
        rol_or = Rol.objects.get(nombre=nombre_origen)
        count = 0
        for usuario in list(rol_or.usuarios.all()):
            if hasattr(usuario, 'perfil') and usuario.perfil:
                usuario.perfil.rol = rol_destino
                usuario.perfil.save()
                count += 1
        rol_or.delete()
        print(f"Rol '{nombre_origen}' eliminado. {count} usuarios migrados a '{rol_destino.nombre}'.")
    except Rol.DoesNotExist:
        pass

# Ejecutar migración y limpieza
migrar_usuarios('Mesa de Ayuda', rol_operador)
migrar_usuarios('TEST ROL', rol_operador)
migrar_usuarios('Técnico de Soporte Nivel 2', rol_tecnico)
migrar_usuarios('Técnicos Terreno', rol_tecnico)

print("\n--- ROLES ACTUALES ---")
for r in Rol.objects.all():
    print(f"- {r.nombre} ({r.usuarios.count()} usuarios)")
