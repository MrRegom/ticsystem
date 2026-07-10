"""
Semilla inicial de roles y permisos para ticsystem.

Crea los 6 roles por defecto del sistema TIC del Hospital Dr. Gustavo Fricke,
con sus 19 permisos booleanos cada uno. Es idempotente: si un rol ya existe
por nombre, se omite (no se sobrescribe).

Fuente: equipamiento/docs/sql_roles_permisos_v4.sql

Uso:
    python manage.py seed_roles
"""
from django.core.management.base import BaseCommand
from core.models import Rol


PERMISOS_POR_ROL = {
    'Administrador': {
        'descripcion': 'Control total del sistema',
        'orden': 1,
        'permisos': {
            'admin_total': True, 'gestionar_roles': True, 'gestionar_usuarios': True,
            'usuarios_crear': True, 'usuarios_editar': True, 'usuarios_eliminar': True,
            'equipos_crear': True, 'equipos_editar': True, 'equipos_eliminar': True,
            'anexos_crear': True, 'anexos_editar': True, 'anexos_eliminar': True,
            'actas_crear': True, 'actas_eliminar': True,
            'gestionar_mantenedores': True, 'mantenedores_crear': True, 'mantenedores_editar': True,
            'eliminar_registros': True, 'gestionar_modulos_autogestion': True,
        },
    },
    'Especial': {
        'descripcion': 'Gestion avanzada sin eliminaciones',
        'orden': 2,
        'permisos': {
            'admin_total': False, 'gestionar_roles': False, 'gestionar_usuarios': False,
            'usuarios_crear': False, 'usuarios_editar': False, 'usuarios_eliminar': False,
            'equipos_crear': True, 'equipos_editar': True, 'equipos_eliminar': False,
            'anexos_crear': True, 'anexos_editar': True, 'anexos_eliminar': False,
            'actas_crear': True, 'actas_eliminar': False,
            'gestionar_mantenedores': True, 'mantenedores_crear': True, 'mantenedores_editar': True,
            'eliminar_registros': False, 'gestionar_modulos_autogestion': True,
        },
    },
    'MesaAyuda': {
        'descripcion': 'Operacion diaria sin permisos de eliminacion',
        'orden': 3,
        'permisos': {
            'admin_total': False, 'gestionar_roles': False, 'gestionar_usuarios': False,
            'usuarios_crear': False, 'usuarios_editar': False, 'usuarios_eliminar': False,
            'equipos_crear': True, 'equipos_editar': True, 'equipos_eliminar': False,
            'anexos_crear': True, 'anexos_editar': True, 'anexos_eliminar': False,
            'actas_crear': True, 'actas_eliminar': False,
            'gestionar_mantenedores': False, 'mantenedores_crear': False, 'mantenedores_editar': False,
            'eliminar_registros': False, 'gestionar_modulos_autogestion': False,
        },
    },
    'Tecnico': {
        'descripcion': 'Operacion tecnica',
        'orden': 4,
        'permisos': {
            'admin_total': False, 'gestionar_roles': False, 'gestionar_usuarios': False,
            'usuarios_crear': False, 'usuarios_editar': False, 'usuarios_eliminar': False,
            'equipos_crear': True, 'equipos_editar': True, 'equipos_eliminar': False,
            'anexos_crear': True, 'anexos_editar': True, 'anexos_eliminar': False,
            'actas_crear': True, 'actas_eliminar': False,
            'gestionar_mantenedores': False, 'mantenedores_crear': False, 'mantenedores_editar': False,
            'eliminar_registros': False, 'gestionar_modulos_autogestion': False,
        },
    },
    'Vendedor': {
        'descripcion': 'Perfil comercial',
        'orden': 5,
        'permisos': {
            'admin_total': False, 'gestionar_roles': False, 'gestionar_usuarios': False,
            'usuarios_crear': False, 'usuarios_editar': False, 'usuarios_eliminar': False,
            'equipos_crear': False, 'equipos_editar': False, 'equipos_eliminar': False,
            'anexos_crear': False, 'anexos_editar': False, 'anexos_eliminar': False,
            'actas_crear': True, 'actas_eliminar': False,
            'gestionar_mantenedores': False, 'mantenedores_crear': False, 'mantenedores_editar': False,
            'eliminar_registros': False, 'gestionar_modulos_autogestion': False,
        },
    },
    'Consulta': {
        'descripcion': 'Sin permisos de modificacion',
        'orden': 6,
        'permisos': {
            'admin_total': False, 'gestionar_roles': False, 'gestionar_usuarios': False,
            'usuarios_crear': False, 'usuarios_editar': False, 'usuarios_eliminar': False,
            'equipos_crear': False, 'equipos_editar': False, 'equipos_eliminar': False,
            'anexos_crear': False, 'anexos_editar': False, 'anexos_eliminar': False,
            'actas_crear': False, 'actas_eliminar': False,
            'gestionar_mantenedores': False, 'mantenedores_crear': False, 'mantenedores_editar': False,
            'eliminar_registros': False, 'gestionar_modulos_autogestion': False,
        },
    },
}


class Command(BaseCommand):
    help = 'Crea los 6 roles por defecto del sistema TIC con sus 19 permisos booleanos.'

    def handle(self, *args, **options):
        creados = 0
        omitidos = 0
        for nombre, datos in PERMISOS_POR_ROL.items():
            _, created = Rol.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': datos['descripcion'],
                    'permisos': datos['permisos'],
                    'activo': True,
                    'orden': datos['orden'],
                    'creado_por': 'seed_roles',
                    'actualizado_por': 'seed_roles',
                },
            )
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'Rol creado: {nombre}'))
            else:
                omitidos += 1
                self.stdout.write(f'Rol omitido (ya existe): {nombre}')

        self.stdout.write(
            self.style.SUCCESS(f'\nResumen: {creados} creados, {omitidos} omitidos.')
        )
