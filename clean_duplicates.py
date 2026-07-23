import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticsystem.settings')
django.setup()

from core.models import Rol
from tickets.models import GrupoResolutor, Ticket

print("--- LIMPIANDO DUPLICADOS EN GRUPO RESOLUTOR ---")
try:
    grupo_bueno = GrupoResolutor.objects.get(nombre='Mesa de Ayuda', is_system=True)
    grupos_malos = GrupoResolutor.objects.filter(nombre__iexact='mesa de ayuda').exclude(id=grupo_bueno.id)
    
    for g_malo in grupos_malos:
        # Reasignar miembros
        for miembro in g_malo.miembros.all():
            grupo_bueno.miembros.add(miembro)
        
        # Reasignar tickets
        tickets_afectados = Ticket.objects.filter(grupo_resolutor=g_malo)
        count = tickets_afectados.count()
        tickets_afectados.update(grupo_resolutor=grupo_bueno)
        
        print(f"Grupo '{g_malo.nombre}' eliminado. {count} tickets reasignados a '{grupo_bueno.nombre}'.")
        g_malo.delete()
except Exception as e:
    print("Error en GrupoResolutor:", e)


print("\n--- LIMPIANDO ROLES INVENTADOS POR SETUP_ROLES ---")
roles_a_borrar = ['Técnicos Terreno', 'Soporte Equipamiento y Hardware']
for r_nombre in roles_a_borrar:
    try:
        rol = Rol.objects.get(nombre=r_nombre, is_system=False)
        count_usuarios = rol.usuarios.count()
        if count_usuarios == 0:
            rol.delete()
            print(f"Rol '{r_nombre}' eliminado.")
        else:
            print(f"ATENCION: Rol '{r_nombre}' tiene {count_usuarios} usuarios. No se eliminó.")
    except Rol.DoesNotExist:
        print(f"Rol '{r_nombre}' no existe o ya fue eliminado.")
    except Rol.MultipleObjectsReturned:
        print(f"Rol '{r_nombre}' duplicado.")
        
print("Hecho.")
