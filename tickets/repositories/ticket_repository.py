from django.db.models import Q
from tickets.models import Ticket

class TicketRepository:
    """
    Capa de Acceso a Datos (Repository) para el módulo de Tickets.
    Aísla las consultas complejas (ORM) de la capa de Servicios.
    """

    @staticmethod
    def get_ticket_by_id(ticket_id: int):
        return Ticket.objects.select_related(
            'solicitante', 'responsable', 'activo', 'activo__pma',
            'prioridad', 'categoria'
        ).filter(id=ticket_id).first()

    @staticmethod
    def get_all_active_tickets():
        """Obtiene tickets abiertos para el tablero Kanban."""
        return Ticket.objects.exclude(
            estado__in=[Ticket.Estado.CERRADO, Ticket.Estado.CANCELADO]
        ).select_related(
            'solicitante', 'responsable', 'activo', 'activo__pma',
            'prioridad', 'categoria'
        ).order_by('-fecha_creacion')

    @staticmethod
    def get_tickets_by_activo(equipo_id: int):
        return Ticket.objects.filter(activo_id=equipo_id).order_by('-fecha_creacion')

    @staticmethod
    def get_latest_correlativo() -> str:
        latest = Ticket.objects.order_by('-id').first()
        return latest.correlativo if latest else None
