from core.models import Rol

# Lista de permisos disponibles en el sistema y su descripción.
PERMISOS_DISPONIBLES = [
    {'id': 'VER_INICIO', 'nombre': 'Acceso a Inicio', 'modulo': 'Dashboard'},
    {'id': 'VER_USUARIOS', 'nombre': 'Ver Usuarios', 'modulo': 'Usuarios'},
    {'id': 'GESTIONAR_USUARIOS', 'nombre': 'Gestionar Usuarios', 'modulo': 'Usuarios'},
    {'id': 'VER_EQUIPOS', 'nombre': 'Ver Equipos', 'modulo': 'Equipos'},
    {'id': 'GESTIONAR_EQUIPOS', 'nombre': 'Gestionar Equipos', 'modulo': 'Equipos'},
    {'id': 'VER_MANTENEDORES', 'nombre': 'Ver Mantenedores', 'modulo': 'Mantenedores'},
    {'id': 'GESTIONAR_MANTENEDORES', 'nombre': 'Gestionar Mantenedores', 'modulo': 'Mantenedores'},
    {'id': 'VER_TICKETS', 'nombre': 'Ver Tickets', 'modulo': 'Tickets'},
    {'id': 'GESTIONAR_TICKETS', 'nombre': 'Gestionar Tickets', 'modulo': 'Tickets'},
    {'id': 'VER_REPORTES', 'nombre': 'Ver Reportes', 'modulo': 'Reportes'},
    {'id': 'VER_ACTAS', 'nombre': 'Ver Actas', 'modulo': 'Actas'},
    {'id': 'GESTIONAR_ACTAS', 'nombre': 'Gestionar Actas', 'modulo': 'Actas'},
    {'id': 'VER_ANEXOS', 'nombre': 'Ver Anexos', 'modulo': 'Anexos'},
    {'id': 'GESTIONAR_ANEXOS', 'nombre': 'Gestionar Anexos', 'modulo': 'Anexos'},
    {'id': 'GESTIONAR_ROLES', 'nombre': 'Gestionar Roles y Perfiles', 'modulo': 'Sistema'},
]

class RolService:
    @staticmethod
    def obtener_permisos_disponibles():
        return PERMISOS_DISPONIBLES

    @staticmethod
    def validar_permiso(user, permiso_id):
        if user.is_superuser:
            return True
        if not hasattr(user, 'perfil') or not user.perfil.rol:
            return False
        return user.perfil.rol.tiene_permiso(permiso_id)

    @staticmethod
    def actualizar_permisos_rol(rol_id, permisos_dict):
        """
        Recibe el ID del rol y un diccionario con las llaves de los permisos que estaran en True.
        Los demás se ponen en False o no se incluyen.
        """
        try:
            rol = Rol.objects.get(id=rol_id)
            rol.permisos = permisos_dict
            rol.save()
            return True
        except Rol.DoesNotExist:
            return False
