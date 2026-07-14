from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from tickets.models import Ticket

class ReportesRepository:
    """
    Se encarga de interactuar con el ORM de forma pesada y óptima
    para extraer datos puros sin lógica de presentación.
    """
    
    @staticmethod
    def obtener_cumplimiento_sla():
        """Retorna el número de tickets vencidos vs en tiempo."""
        total = Ticket.objects.exclude(estado=Ticket.Estado.CANCELADO).count()
        if total == 0:
            return {'a_tiempo': 0, 'vencidos': 0}
            
        vencidos_count = 0
        a_tiempo_count = 0
        
        # Como is_sla_vencido es una property dinámica en python y no un campo DB,
        # lo ideal sería tenerlo en DB para reportes masivos.
        # Por ahora, iteramos en memoria si son pocos, o usamos un queryset básico.
        # En Enterprise real, se usaría F() expressions sobre fecha_vencimiento_sla vs ahora.
        tickets = Ticket.objects.exclude(estado=Ticket.Estado.CANCELADO)
        ahora = timezone.now()
        
        # Vencidos: no resueltos y fecha_vencimiento < ahora, O resueltos y fecha_cierre > fecha_vencimiento
        vencidos = Ticket.objects.filter(
            Q(estado__in=[Ticket.Estado.NUEVO, Ticket.Estado.ASIGNADO, Ticket.Estado.EN_PROCESO, Ticket.Estado.PENDIENTE_USUARIO, Ticket.Estado.PENDIENTE_PROVEEDOR, Ticket.Estado.ESPERA_APROBACION, Ticket.Estado.ESCALADO], fecha_vencimiento_sla__lt=ahora) |
            Q(estado__in=[Ticket.Estado.RESUELTO, Ticket.Estado.CERRADO], fecha_cierre__gt=models.F('fecha_vencimiento_sla'))
        ).count()
        
        a_tiempo = total - vencidos
        
        return {'a_tiempo': a_tiempo, 'vencidos': vencidos}

    @staticmethod
    def obtener_carga_por_categoria():
        """Retorna la cantidad de tickets por categoría."""
        return Ticket.objects.values('categoria__nombre').annotate(
            total=Count('id')
        ).order_by('-total')[:10]

    @staticmethod
    def obtener_tendencia_mensual():
        """Tickets creados en los últimos 6 meses."""
        seis_meses_atras = timezone.now() - relativedelta(months=6)
        return Ticket.objects.filter(fecha_creacion__gte=seis_meses_atras)\
            .annotate(mes=TruncMonth('fecha_creacion'))\
            .values('mes')\
            .annotate(total=Count('id'))\
            .order_by('mes')

    @staticmethod
    def obtener_top_equipos_criticos():
        """Top 5 activos con más fallas históricas."""
        return Ticket.objects.filter(activo__isnull=False)\
            .values('activo__id', 'activo__articulo__nombre', 'activo__marca__nombre', 'activo__serial_number')\
            .annotate(total_fallas=Count('id'))\
            .order_by('-total_fallas')[:5]
