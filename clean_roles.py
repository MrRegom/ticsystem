import os
from core.models import Rol, PerfilUsuario

def clean_roles():
    print("Iniciando limpieza de roles...")
    
    # Obtener el rol principal técnico (crearlo si no existe)
    rol_tecnico_nivel_2, created = Rol.objects.get_or_create(
        nombre="Técnico de Soporte Nivel 2",
        defaults={
            'descripcion': "Técnico en terreno que resuelve incidentes",
            'activo': True
        }
    )
    # Asignarle permisos base
    permisos_tecnico = rol_tecnico_nivel_2.permisos or {}
    permisos_tecnico.update({
        'VER_INICIO': True,
        'VER_TICKETS': True,
        'GESTIONAR_TICKETS': True,
        'RECIBIR_TICKETS': True
    })
    rol_tecnico_nivel_2.permisos = permisos_tecnico
    rol_tecnico_nivel_2.save()
    print(f"Rol '{rol_tecnico_nivel_2.nombre}' preparado.")

    # Reasignar perfiles de los roles antiguos al nuevo rol
    roles_a_unificar = ["Tecnico", "Nivel 2", "Técnico Terreno", "T\u00e9cnico Terreno", "Tcnico Terreno"]
    perfiles = PerfilUsuario.objects.filter(rol__nombre__in=roles_a_unificar)
    count = perfiles.update(rol=rol_tecnico_nivel_2)
    print(f"{count} perfiles reasignados a '{rol_tecnico_nivel_2.nombre}'.")

    # Eliminar roles antiguos vacíos
    roles_viejos = Rol.objects.filter(nombre__in=roles_a_unificar)
    for r in roles_viejos:
        if r.usuarios.count() == 0:
            print(f"Eliminando rol vacío: {r.nombre}")
            r.delete()
        else:
            print(f"ATENCIÓN: El rol {r.nombre} aún tiene {r.usuarios.count()} usuarios (no debería pasar).")

    # Configurar Mesa de Ayuda (Despachadores)
    roles_mesa_ayuda = Rol.objects.filter(nombre__in=['Mesa de Ayuda', 'Operador de Mesa de Ayuda'])
    for r in roles_mesa_ayuda:
        permisos = r.permisos or {}
        permisos['DESPACHAR_TICKETS'] = True
        # Me aseguro de quitar RECIBIR_TICKETS si lo tenían (los despachadores no reciben)
        if 'RECIBIR_TICKETS' in permisos:
            del permisos['RECIBIR_TICKETS']
        r.permisos = permisos
        r.save()
        print(f"Rol '{r.nombre}' configurado como Despachador.")

    # Configurar Super Administrador
    super_admin = Rol.objects.filter(nombre='Super Administrador').first()
    if super_admin:
        permisos = super_admin.permisos or {}
        permisos['DESPACHAR_TICKETS'] = True
        permisos['RECIBIR_TICKETS'] = True
        super_admin.permisos = permisos
        super_admin.save()
        print(f"Rol '{super_admin.nombre}' configurado con todos los permisos.")

    # A cualquier otro rol que tenga GESTIONAR_TICKETS (ej. Soporte Equipamiento) también le damos RECIBIR_TICKETS
    # si no es Mesa de Ayuda.
    otros_roles = Rol.objects.exclude(id__in=[rol_tecnico_nivel_2.id, super_admin.id if super_admin else 0] + [x.id for x in roles_mesa_ayuda])
    for r in otros_roles:
        if r.permisos.get('GESTIONAR_TICKETS') or r.permisos.get('VER_TICKETS'):
            permisos = r.permisos or {}
            permisos['RECIBIR_TICKETS'] = True
            r.permisos = permisos
            r.save()
            print(f"Rol '{r.nombre}' configurado para recibir tickets.")

    print("Limpieza finalizada.")

clean_roles()