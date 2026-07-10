"""
Signals del módulo Redes (IPAM sync).

Implementa la regla de sync IPAM (listaEquipos.modelo.php:758-788):
al guardar/editar un Equipo con IP, marcar la InfraestructuraRed(ip=...) como OCUPADO.
Al quitar la IP de un Equipo, la IP queda LIBRE (si existe en IPAM).

Se conecta al post_save de Equipo desde aquí para evitar import circular
(equipos.signals no debe importar redes.models).
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from equipos.models import Equipo


@receiver(post_save, sender=Equipo)
def sync_ipam_on_equipo_save(sender, instance, **kwargs):
    """Marca la IP del equipo como OCUPADO en IPAM si existe."""
    if not instance.ip:
        return
    try:
        from .models import InfraestructuraRed
    except ImportError:
        return
    InfraestructuraRed.objects.filter(ip_direccion=instance.ip).update(
        estado=InfraestructuraRed.Estado.OCUPADO
    )


@receiver(post_delete, sender=Equipo)
def liberar_ip_on_equipo_delete(sender, instance, **kwargs):
    """Libera la IP en IPAM al eliminar un equipo."""
    if not instance.ip:
        return
    try:
        from .models import InfraestructuraRed
    except ImportError:
        return
    InfraestructuraRed.objects.filter(ip_direccion=instance.ip).update(
        estado=InfraestructuraRed.Estado.LIBRE
    )
