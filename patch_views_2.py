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

# correos/views.py
patch_views('c:/proyectos/ticsystem/correos/views.py', {
    'ConfiguracionSMTPDashboardView': 'GESTIONAR_ROLES',
    'ConfiguracionSMTPAPIView': 'GESTIONAR_ROLES',
    'TestSMTPAPIView': 'GESTIONAR_ROLES',
})

# sla/views.py
patch_views('c:/proyectos/ticsystem/sla/views.py', {
    'SlaConfigView': 'GESTIONAR_ROLES',
    'SlaMatrixApiView': 'GESTIONAR_ROLES',
    'PrioridadListApiView': 'GESTIONAR_ROLES',
    'PrioridadApiView': 'GESTIONAR_ROLES',
})

print("Vistas adicionales parcheadas.")
