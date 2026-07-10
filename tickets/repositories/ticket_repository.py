from django.db import transaction
from django.db.models import Q

from tickets.models import Ticket, TicketBitacora


class TicketRepository:

    @staticmethod
    def get_by_id(ticket_id: int) -> Ticket:
        try:
            return Ticket.objects.select_related(
                'edificio', 'piso', 'unidad', 'equipo', 'tecnico', 'prioridad', 'categoria',
            ).get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def save(ticket: Ticket) -> Ticket:
        ticket.save()
        return ticket

    @staticmethod
    @transaction.atomic
    def delete(ticket: Ticket) -> None:
        ticket.delete()

    @classmethod
    def _apply_search(cls, queryset, search_value: str):
        if search_value:
            queryset = queryset.filter(
                Q(solicitante_nombre__icontains=search_value) |
                Q(solicitante_rut__icontains=search_value) |
                Q(solicitante_correo__icontains=search_value) |
                Q(descripcion__icontains=search_value) |
                Q(estado__icontains=search_value) |
                Q(edificio__nombre__icontains=search_value) |
                Q(unidad__nombre__icontains=search_value) |
                Q(equipo__serial_number__icontains=search_value) |
                Q(prioridad__nivel__icontains=search_value) |
                Q(categoria__nombre__icontains=search_value) |
                Q(tecnico__username__icontains=search_value)
            )
        return queryset

    @classmethod
    def get_paginated_list(cls, start: int, length: int, search_value: str,
                           order_column: str, order_dir: str):
        queryset = Ticket.objects.select_related(
            'edificio', 'piso', 'unidad', 'equipo', 'tecnico', 'prioridad', 'categoria',
        ).all()
        queryset = cls._apply_search(queryset, search_value)

        order_mapping = {
            'id': 'id',
            'solicitante_nombre': 'solicitante_nombre',
            'edificio': 'edificio__nombre',
            'piso': 'piso__nombre',
            'unidad': 'unidad__nombre',
            'equipo': 'equipo__serial_number',
            'estado': 'estado',
            'prioridad': 'prioridad__nivel',
            'categoria': 'categoria__nombre',
            'tecnico': 'tecnico__username',
            'fecha_hora': 'fecha_hora',
        }
        column_to_order = order_mapping.get(order_column, '-fecha_hora')
        if order_dir == 'desc' and not column_to_order.startswith('-'):
            column_to_order = f'-{column_to_order}'
        elif order_dir == 'asc' and column_to_order.startswith('-'):
            column_to_order = column_to_order[1:]

        queryset = queryset.order_by(column_to_order)
        end = start + length
        return queryset[start:end]

    @classmethod
    def count_total(cls) -> int:
        return Ticket.objects.count()

    @classmethod
    def count_filtered(cls, search_value: str) -> int:
        queryset = Ticket.objects.all()
        queryset = cls._apply_search(queryset, search_value)
        return queryset.count()
