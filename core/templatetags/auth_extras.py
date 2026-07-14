from django import template

register = template.Library()

@register.filter(name='has_permiso')
def has_permiso(user, permiso_nombre):
    """
    Verifica si el usuario actual tiene el permiso indicado en su perfil/rol.
    Si el usuario es superuser de Django, también se le permite todo por defecto
    o podemos forzar que se revise el rol. Para mantenerlo seguro, si es superuser de django:
    """
    if not user.is_authenticated:
        return False
        
    if user.is_superuser:
        return True
        
    if not hasattr(user, 'perfil') or not user.perfil.rol:
        return False
        
    return user.perfil.rol.tiene_permiso(permiso_nombre)
