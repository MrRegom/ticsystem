from django.utils import timezone
from django.db.models import Q, Count
from datetime import datetime, timedelta
from core.models import LogAuditoria

class AuditoriaService:
    @staticmethod
    def obtener_resumen_hoy():
        hoy = timezone.now().date()
        logs_hoy = LogAuditoria.objects.filter(fecha_registro__date=hoy)
        
        return {
            'total_movimientos': logs_hoy.count(),
            'total_logins': logs_hoy.filter(accion__startswith='LOGIN').count(),
            'total_creaciones': logs_hoy.filter(accion='CREAR').count(),
            'total_eliminaciones': logs_hoy.filter(accion='ELIMINAR').count(),
        }

    @staticmethod
    def obtener_logs_paginados(start, length, search, modulo, accion, usuario, fecha_inicio, fecha_fin):
        qs = LogAuditoria.objects.all()
        
        # Filtros de búsqueda (Global)
        if search:
            qs = qs.filter(
                Q(usuario__icontains=search) |
                Q(detalles__icontains=search) |
                Q(tabla__icontains=search)
            )
            
        # Filtros Custom
        if modulo:
            qs = qs.filter(tabla__iexact=modulo)
        if accion:
            qs = qs.filter(accion__iexact=accion)
        if usuario:
            qs = qs.filter(usuario__icontains=usuario)
            
        if fecha_inicio:
            try:
                dt_ini = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                qs = qs.filter(fecha_registro__gte=dt_ini)
            except ValueError:
                pass
                
        if fecha_fin:
            try:
                dt_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
                dt_fin = dt_fin + timedelta(days=1)
                qs = qs.filter(fecha_registro__lt=dt_fin)
            except ValueError:
                pass

        total_records = LogAuditoria.objects.count()
        filtered_records = qs.count()
        
        # Ordenación descendente
        qs = qs.order_by('-fecha_registro')
        
        # Paginación
        if length > 0:
            qs = qs[start:start + length]
            
        # Formatear datos para DataTable
        data = []
        for log in qs:
            data.append({
                'id': log.id,
                'fecha': log.fecha_registro.strftime('%d/%m/%Y %H:%M:%S'),
                'usuario': log.usuario or 'Sistema',
                'accion': log.get_accion_display() if hasattr(log, 'get_accion_display') and log.get_accion_display() else log.accion,
                'modulo': log.tabla,
                'detalles': log.detalles,
                'ip': log.ip_address or 'Desconocida'
            })
            
        return data, total_records, filtered_records
