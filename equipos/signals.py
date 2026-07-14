"""
Signals del módulo Equipos.

Implementan las reglas de negocio que en PHP estaban embebidas en los modelos:

1. Audit trail automático al editar/crear equipo (listaEquipos.modelo.php:497-606):
   - pre_save: captura estado anterior y calcula diff de campos.
   - post_save: si es creación → BitacoraEquipo MOVIMIENTO "Alta de equipo".
                 si es edición con cambios → BitacoraEquipo ACTUALIZACION_SISTEMA
                 con "Campos actualizados: X, Y, Z".

2. Recálculo automático de estado del equipo (bitacora.modelo.php:39-91):
   - post_save de BitacoraEquipo:
     * Si tipo=MANTENCION y fecha_devolucion is None → estado = "Mantenimiento".
     * Si fecha_devolucion is not None → estado = "Funcional".

3. Sync IPAM al guardar equipo (listaEquipos.modelo.php:758-788):
   - post_save de Equipo: si tiene ip, marcar InfraestructuraRed(ip=...) como OCUPADO.
   (Se conecta a redes.signals desde la app redes para evitar import circular.)
"""
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Equipo, BitacoraEquipo, BitacoraOpcion


# Mapeo de campos a etiquetas legibles para el audit trail
CAMPOS_AUDITABLES = {
    'articulo': 'Artículo',
    'marca': 'Marca',
    'modelo': 'Modelo',
    'pma': 'PMA',
    'so': 'Sistema Operativo',
    'estado': 'Estado',
    'proveedor': 'Proveedor',
    'serial_number': 'Número de Serie',
    'ip': 'IP',
    'usuario': 'Usuario',
    'office': 'Office',
    'activador': 'Activador',
    'pmalugar': 'PMA/Lugar',
    'comentario': 'Comentario',
    'anexo': 'Anexo',
    'imagen': 'Imagen',
}


def _valor_campo(equipo, campo):
    """Devuelve representación en texto del valor de un campo FK o plano."""
    val = getattr(equipo, campo, None)
    if val is None:
        return '(vacio)'
    # Si es FK, mostrar str del relacionado
    if hasattr(val, 'pk') and val.pk is None:
        return '(vacio)'
    if hasattr(val, '__str__') and not isinstance(val, (str, int, float)):
        return str(val)
    return str(val) if val != '' else '(vacio)'


@receiver(pre_save, sender=Equipo)
def capturar_estado_anterior(sender, instance, **kwargs):
    """Guarda en el instance el estado anterior para comparar en post_save."""
    if instance.pk:
        try:
            original = Equipo.objects.get(pk=instance.pk)
            instance._estado_anterior = original
        except Equipo.DoesNotExist:
            instance._estado_anterior = None
    else:
        instance._estado_anterior = None


@receiver(post_save, sender=Equipo)
def audit_trail_equipo(sender, instance, created, **kwargs):
    """Crea BitacoraEquipo automático al crear/editar un equipo."""
    # Evitar recursión: si el save viene de un signal de recálculo, no auditar
    if getattr(instance, '_skip_audit', False):
        return

    tecnico = instance.modificado_por

    if created:
        # Alta de equipo → MOVIMIENTO
        nombre_tec = tecnico.get_full_name() or tecnico.username if tecnico else 'Sistema'
        BitacoraEquipo.objects.create(
            equipo=instance,
            tecnico=tecnico or _usuario_sistema(),
            fecha_mantenimiento=timezone_localdate(),
            solicitante=None,
            falla_reportada='Alta de equipo en inventario',
            actividades_realizadas=f'Creación de equipo por: {nombre_tec}',
            servicio_unidad=instance.pma.recinto.unidad.nombre if instance.pma and instance.pma.recinto and getattr(instance.pma.recinto, 'unidad', None) else '',
            tipo_registro=BitacoraEquipo.TipoRegistro.MOVIMIENTO,
        )
        return

    # Edición: comparar con estado anterior
    original = getattr(instance, '_estado_anterior', None)
    if original is None:
        return
        
    # Si el usuario explicitó que es una corrección, no registramos el movimiento en bitácora
    motivo_edicion = getattr(instance, '_motivo_edicion_pma', None)
    if motivo_edicion == 'CORRECCION':
        return

    cambios = []
    for campo, etiqueta in CAMPOS_AUDITABLES.items():
        val_nuevo = _valor_campo(instance, campo)
        val_antiguo = _valor_campo(original, campo)
        if val_nuevo != val_antiguo:
            cambios.append(f"{etiqueta} [{val_antiguo} -> {val_nuevo}]")

    if cambios:
        nombre_tec = tecnico.get_full_name() or tecnico.username if tecnico else 'Sistema'
        BitacoraEquipo.objects.create(
            equipo=instance,
            tecnico=tecnico or _usuario_sistema(),
            fecha_mantenimiento=timezone_localdate(),
            solicitante=None,
            falla_reportada='Actualización',
            actividades_realizadas=(
                f'Actualizacion por: {nombre_tec}. '
                f'Campos actualizados: {", ".join(cambios)}'
            ),
            servicio_unidad=instance.pma.recinto.unidad.nombre if instance.pma and instance.pma.recinto and getattr(instance.pma.recinto, 'unidad', None) else '',
            tipo_registro=BitacoraEquipo.TipoRegistro.ACTUALIZACION_SISTEMA,
        )


@receiver(post_save, sender=BitacoraEquipo)
def recalcular_estado_equipo(sender, instance, created, **kwargs):
    """Recalcula el estado del equipo según la bitácora (bitacora.modelo.php:39-91).
    - MANTENCION abierta (sin fecha_devolucion) → estado 'Mantenimiento'.
    - MANTENCION cerrada (con fecha_devolucion) → estado 'Funcional'.
    No aplica para ACTUALIZACION_SISTEMA/MOVIMIENTO (esos no cambian estado).
    """
    if instance.tipo_registro != BitacoraEquipo.TipoRegistro.MANTENCION:
        return

    from mantenedores.models import EstadoEquipo
    equipo = instance.equipo

    if instance.fecha_devolucion is None:
        # Mantención abierta → Mantenimiento
        estado_mant = EstadoEquipo.objects.filter(nombre='Mantenimiento').first()
        if estado_mant and equipo.estado_id != estado_mant.pk:
            equipo._skip_audit = True
            equipo.estado = estado_mant
            equipo.save(update_fields=['estado', 'fecha_modificacion'])
            equipo._skip_audit = False
    else:
        # Mantención cerrada → Funcional
        estado_func = EstadoEquipo.objects.filter(nombre='Funcional').first()
        if estado_func and equipo.estado_id != estado_func.pk:
            equipo._skip_audit = True
            equipo.estado = estado_func
            equipo.save(update_fields=['estado', 'fecha_modificacion'])
            equipo._skip_audit = False


def _usuario_sistema():
    """Devuelve un usuario 'sistema' para bitácoras automáticas.
    Crea uno si no existe (superuser admin). Usa el primer superuser.
    """
    u = User.objects.filter(is_superuser=True).first()
    if u:
        return u
    # Fallback: primer usuario activo
    return User.objects.first()


def timezone_localdate():
    """Import local para evitar circular imports."""
    from django.utils import timezone
    return timezone.localdate()
