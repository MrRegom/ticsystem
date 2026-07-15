from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q, F

from equipos.models import Equipo, BitacoraEquipo
from anexos.models import Anexo
from actas.models import Acta
from redes.models import InfraestructuraRed
from mantenedores.models import EstadoEquipo


def obtener_kpis_generales():
    hoy = timezone.now()
    hace_90 = hoy - timedelta(days=90)
    hace_30 = hoy - timedelta(days=30)
    hace_7 = hoy - timedelta(days=7)

    # ============================================================
    # 1. Equipos
    # ============================================================
    equipos_total = Equipo.objects.count()
    estados_qs = Equipo.objects.values('estado__nombre').annotate(n=Count('id'))
    estados_nombres = {e['estado__nombre']: e['n'] for e in estados_qs}

    equipos_funcional = estados_nombres.get('Funcional', 0)
    equipos_desuso = estados_nombres.get('Desuso', 0)
    equipos_mantenimiento = estados_nombres.get('Mantenimiento', 0)

    # ============================================================
    # 2. Top artículos
    # ============================================================
    top_articulos = list(
        Equipo.objects.values('articulo__nombre')
        .annotate(n=Count('id'))
        .order_by('-n')[:5]
    )

    # ============================================================
    # 3. Anexos
    # ============================================================
    anexos_total = Anexo.objects.count()
    anexos_activos = Anexo.objects.filter(estado=Anexo.Estado.ACTIVO).count()
    anexos_inactivos = anexos_total - anexos_activos

    # ============================================================
    # 4. IPAM
    # ============================================================
    ips_total = InfraestructuraRed.objects.count()
    ips_libres = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.LIBRE).count()
    ips_ocupadas = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.OCUPADO).count()
    ips_falla = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.FALLA).count()

    # ============================================================
    # 5. Actas
    # ============================================================
    actas_total = Acta.objects.count()
    actas_emitidas = Acta.objects.filter(estado=Acta.Estado.EMITIDO).count()
    actas_borrador = Acta.objects.filter(estado=Acta.Estado.BORRADOR).count()
    actas_enviadas = Acta.objects.filter(estado=Acta.Estado.ENVIADO).count()

    # ============================================================
    # 6. Bitácora (general)
    # ============================================================
    bitacoras_30d = BitacoraEquipo.objects.filter(fecha_creacion__gte=hace_30).count()
    bitacoras_7d = BitacoraEquipo.objects.filter(fecha_creacion__gte=hace_7).count()
    mantenciones_abiertas = BitacoraEquipo.objects.filter(
        tipo_registro=BitacoraEquipo.TipoRegistro.MANTENCION,
        fecha_devolucion__isnull=True,
    ).count()

    # ============================================================
    # 7. Meta operativa de mantención
    # ============================================================
    MANT_TIPOS = [
        BitacoraEquipo.TipoRegistro.MANTENCION,
        BitacoraEquipo.TipoRegistro.REPARACION_EXTERNA,
    ]

    mant_total = BitacoraEquipo.objects.filter(tipo_registro__in=MANT_TIPOS).count()
    mant_cerradas = BitacoraEquipo.objects.filter(
        tipo_registro__in=MANT_TIPOS, fecha_devolucion__isnull=False
    ).count()
    mant_abiertas = BitacoraEquipo.objects.filter(
        tipo_registro__in=MANT_TIPOS, fecha_devolucion__isnull=True
    ).count()

    mant_cerradas_72h = BitacoraEquipo.objects.filter(
        tipo_registro__in=MANT_TIPOS,
        fecha_devolucion__isnull=False,
        fecha_mantenimiento__gte=F('fecha_devolucion') - timedelta(days=3),
    ).count()

    mant_abiertas_vencidas = BitacoraEquipo.objects.filter(
        tipo_registro__in=MANT_TIPOS,
        fecha_devolucion__isnull=True,
        fecha_mantenimiento__lt=(hoy - timedelta(days=3)).date(),
    ).count()

    cumplimiento_pct = round((mant_cerradas_72h / mant_cerradas * 100)) if mant_cerradas > 0 else 0

    # Tiempo promedio de cierre (días)
    tiempo_promedio = None
    cerradas = BitacoraEquipo.objects.filter(
        tipo_registro__in=MANT_TIPOS,
        fecha_devolucion__isnull=False,
    ).values_list('fecha_mantenimiento', 'fecha_devolucion')
    if cerradas:
        total_dias = sum((dev - mant).days for mant, dev in cerradas)
        avg_dias = total_dias / len(cerradas)
        dias = int(avg_dias)
        horas = int((avg_dias - dias) * 24)
        tiempo_promedio = f"{dias} d {horas} h"

    # ============================================================
    # 8. Métricas operativas útiles
    # ============================================================
    equipos_sin_ip = Equipo.objects.filter(Q(ip__isnull=True) | Q(ip='')).count()
    equipos_sin_usuario = Equipo.objects.filter(Q(usuario__isnull=True) | Q(usuario='')).count()
    equipos_sin_pma = Equipo.objects.filter(Q(pmalugar__isnull=True) | Q(pmalugar='')).count()

    # ============================================================
    # 9. Índice de salud operativa (0-100)
    # ============================================================
    pct_sin_usr = (equipos_sin_usuario / equipos_total * 100) if equipos_total else 0
    pct_sin_pma = (equipos_sin_pma / equipos_total * 100) if equipos_total else 0
    pct_mant_venc = (mant_abiertas_vencidas / max(mant_total, 1) * 100)
    pct_sin_ip = (equipos_sin_ip / equipos_total * 100) if equipos_total else 0

    indice_salud = max(0, min(100, round(
        100 - pct_sin_usr * 0.25 - pct_sin_pma * 0.25 - pct_mant_venc * 0.30 - pct_sin_ip * 0.20
    )))

    # ============================================================
    # 10. Actividad reciente (últimos equipos modificados)
    # ============================================================
    actividad_reciente = list(Equipo.objects.select_related(
        'articulo', 'pma', 'modificado_por'
    ).order_by('-fecha_modificacion')[:8].values(
        'serial_number', 'articulo__nombre', 'pma__nombre',
        'modificado_por__first_name', 'modificado_por__last_name', 'fecha_modificacion'
    ))

    # ============================================================
    # 11. Últimos anexos
    # ============================================================
    ultimos_anexos = list(Anexo.objects.select_related(
        'unidad', 'edificio', 'piso'
    ).order_by('-creado_en')[:6].values(
        'numero_anexo', 'unidad__nombre', 'ip', 'edificio__nombre', 'piso__nombre',
        'pma__nombre', 'estado'
    ))

    # ============================================================
    # 12. Mapa de calor: bitácora por unidad (últimos 90 días)
    # ============================================================
    bitacoras_90d = BitacoraEquipo.objects.filter(
        fecha_creacion__gte=hace_90,
        equipo__pma__recinto__unidad__isnull=False,
    ).select_related('equipo__pma__recinto__unidad').values('equipo__pma__recinto__unidad__nombre').annotate(
        total=Count('id'),
        mantenciones=Count('id', filter=Q(
            tipo_registro__in=[BitacoraEquipo.TipoRegistro.MANTENCION,
                               BitacoraEquipo.TipoRegistro.REPARACION_EXTERNA]
        )),
        actualizaciones=Count('id', filter=Q(
            tipo_registro=BitacoraEquipo.TipoRegistro.ACTUALIZACION_SISTEMA
        )),
        abiertas=Count('id', filter=Q(
            fecha_devolucion__isnull=True,
            tipo_registro=BitacoraEquipo.TipoRegistro.MANTENCION,
        )),
    ).order_by('-total')[:12]

    mapa_calor = list(bitacoras_90d)

    # ============================================================
    # 13. Últimas actas (5) + receptor_nombre
    # ============================================================
    ultimas_actas = list(Acta.objects.order_by('-fecha')[:5].values(
        'codigo', 'receptor_nombre', 'estado', 'fecha'
    ))

    # ============================================================
    # 14. Últimos equipos ingresados (5)
    # ============================================================
    ultimos_equipos = list(Equipo.objects.order_by('-fecha_creacion')[:5].values(
        'serial_number', 'articulo__nombre', 'marca__nombre', 'estado__nombre'
    ))

    # ============================================================
    # 15. Recomendaciones (placeholder)
    # ============================================================
    recomendaciones = []

    return {
        # KPIs básicos
        'equipos_total': equipos_total,
        'equipos_funcional': equipos_funcional,
        'equipos_mantenimiento': equipos_mantenimiento,
        'equipos_desuso': equipos_desuso,
        'equipos_no_funcional': estados_nombres.get('No Funcional', 0),
        'equipos_en_equipamiento': estados_nombres.get('En Equipamiento', 0),
        'estados_nombres': estados_nombres,
        'top_articulos': top_articulos,
        'anexos_total': anexos_total,
        'anexos_activos': anexos_activos,
        'anexos_inactivos': anexos_inactivos,
        'ips_total': ips_total,
        'ips_libres': ips_libres,
        'ips_ocupadas': ips_ocupadas,
        'ips_falla': ips_falla,
        'actas_total': actas_total,
        'actas_emitidas': actas_emitidas,
        'actas_borrador': actas_borrador,
        'actas_enviadas': actas_enviadas,
        'bitacoras_30d': bitacoras_30d,
        'bitacoras_7d': bitacoras_7d,
        'mantenciones_abiertas': mantenciones_abiertas,

        # Meta operativa
        'mant_total': mant_total,
        'mant_cerradas': mant_cerradas,
        'mant_abiertas': mant_abiertas,
        'mant_cerradas_72h': mant_cerradas_72h,
        'mant_abiertas_vencidas': mant_abiertas_vencidas,
        'cumplimiento_pct': cumplimiento_pct,
        'tiempo_promedio': tiempo_promedio,

        # Métricas operativas
        'equipos_sin_ip': equipos_sin_ip,
        'equipos_sin_usuario': equipos_sin_usuario,
        'equipos_sin_pma': equipos_sin_pma,

        # Índice de salud
        'indice_salud': indice_salud,

        # Listas
        'actividad_reciente': actividad_reciente,
        'ultimos_anexos': ultimos_anexos,
        'mapa_calor': mapa_calor,
        'ultimas_actas': ultimas_actas,
        'ultimos_equipos': ultimos_equipos,
        'recomendaciones': recomendaciones,
    }

