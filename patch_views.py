import os
import re

def patch_views(file_path, replacements):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add import
    if 'PermisoRequeridoMixin' not in content:
        content = re.sub(
            r'(from django\.contrib\.auth\.mixins import LoginRequiredMixin)',
            r'\1\nfrom core.mixins import PermisoRequeridoMixin',
            content
        )

    for class_name, permission in replacements.items():
        # Replace class inheritance
        pattern = r'(class ' + class_name + r'\s*\()LoginRequiredMixin'
        replacement = r'\1PermisoRequeridoMixin, LoginRequiredMixin'
        content = re.sub(pattern, replacement, content)
        
        # Add permiso_requerido variable
        pattern_body = r'(class ' + class_name + r'\s*\([^)]+\):)\s*'
        replacement_body = r'\1\n    permiso_requerido = ' + repr(permission) + r'\n    '
        content = re.sub(pattern_body, replacement_body, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


# core/views.py
patch_views('c:/proyectos/ticsystem/core/views.py', {
    'UsuariosDashboardView': 'VER_USUARIOS',
    'UsuarioListView': 'VER_USUARIOS',
    'UsuarioActionView': 'GESTIONAR_USUARIOS',
    'UsuarioCrearAPIView': 'GESTIONAR_USUARIOS',
    'UsuarioEditarAPIView': 'GESTIONAR_USUARIOS',
    'RolesDashboardView': 'GESTIONAR_ROLES',
    'RolesDetailAPIView': 'GESTIONAR_ROLES',
    'RolesAPIView': 'GESTIONAR_ROLES',
})

# tickets/views.py
patch_views('c:/proyectos/ticsystem/tickets/views.py', {
    'TicketsDashboardView': 'VER_TICKETS',
    'TicketActionView': 'VER_TICKETS',
    'TicketDetailApiView': 'VER_TICKETS',
    'TicketAssignApiView': 'GESTIONAR_TICKETS',
    'TicketTakeApiView': 'VER_TICKETS',
    'TicketSyncApiView': 'VER_TICKETS',
})

# equipos/views.py
patch_views('c:/proyectos/ticsystem/equipos/views.py', {
    'EquiposDashboardView': 'VER_EQUIPOS',
    'EquipoListView': 'VER_EQUIPOS',
    'EquipoActionView': 'GESTIONAR_EQUIPOS',
    'EquipoDetailView': 'GESTIONAR_EQUIPOS',
    'EquipoDetailReadView': 'VER_EQUIPOS',
    'EquipoHistorialView': 'VER_EQUIPOS',
    'EquipoBitacoraView': 'VER_EQUIPOS',
    'BitacoraRegistroView': 'GESTIONAR_EQUIPOS',
    'EquiposPanelControlView': 'GESTIONAR_EQUIPOS',
})

# mantenedores/views.py
patch_views('c:/proyectos/ticsystem/mantenedores/views.py', {
    'MantenedoresDashboardView': 'VER_MANTENEDORES',
    'MantenedorListView': 'VER_MANTENEDORES',
    'MantenedorActionView': 'GESTIONAR_MANTENEDORES',
    'MantenedorDetailView': 'GESTIONAR_MANTENEDORES',
})

# redes/views.py
patch_views('c:/proyectos/ticsystem/redes/views.py', {
    'RedesDashboardView': 'VER_MANTENEDORES',
    'IpListView': 'VER_MANTENEDORES',
    'IpActionView': 'GESTIONAR_MANTENEDORES',
    'IpDetailView': 'GESTIONAR_MANTENEDORES',
})

# reportes/views.py
patch_views('c:/proyectos/ticsystem/reportes/views.py', {
    'DashboardReportesView': 'VER_REPORTES',
    'ExportarTicketsView': 'VER_REPORTES',
    'ExportarActivosView': 'VER_REPORTES',
})

# actas/views.py
patch_views('c:/proyectos/ticsystem/actas/views.py', {
    'ActasDashboardView': 'VER_ACTAS',
    'ActaListView': 'VER_ACTAS',
    'ActaActionView': 'GESTIONAR_ACTAS',
})

# anexos/views.py
patch_views('c:/proyectos/ticsystem/anexos/views.py', {
    'AnexosDashboardView': 'VER_ANEXOS',
    'AnexoListView': 'VER_ANEXOS',
    'AnexoActionView': 'GESTIONAR_ANEXOS',
})

print("Vistas parcheadas con PermisoRequeridoMixin correctamente.")
