from django.db import transaction
from django.db.models import Q, Prefetch

from actas.models import Acta, ActaDetalle


class ActaRepository:

    @staticmethod
    def get_by_id(acta_id: int) -> Acta:
        try:
            return Acta.objects.select_related(
                'encargado',
            ).prefetch_related(
                Prefetch('detalles', queryset=ActaDetalle.objects.select_related('edificio', 'piso', 'unidad'))
            ).get(pk=acta_id)
        except Acta.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def save(acta: Acta) -> Acta:
        acta.save()
        return acta

    @staticmethod
    @transaction.atomic
    def delete(acta: Acta) -> None:
        acta.delete()

    @classmethod
    def _apply_search_and_filters(cls, queryset, search_value: str):
        if search_value:
            queryset = queryset.filter(
                Q(codigo__icontains=search_value) |
                Q(receptor_nombre__icontains=search_value) |
                Q(estado__icontains=search_value) |
                Q(encargado__username__icontains=search_value) |
                Q(encargado__first_name__icontains=search_value) |
                Q(encargado__last_name__icontains=search_value) |
                Q(receptor_rut__icontains=search_value) |
                Q(receptor_cargo__icontains=search_value) |
                Q(receptor_unidad__icontains=search_value)
            )
        return queryset

    @classmethod
    def get_paginated_list(cls, start: int, length: int, search_value: str,
                           order_column: str, order_dir: str):
        queryset = Acta.objects.select_related(
            'encargado',
        ).all()
        queryset = cls._apply_search_and_filters(queryset, search_value)

        order_mapping = {
            'codigo': 'codigo',
            'receptor': 'receptor_nombre',
            'estado': 'estado',
            'fecha': 'fecha',
            'encargado': 'encargado__username',
        }
        column_to_order = order_mapping.get(order_column, '-fecha')
        if order_dir == 'desc' and not column_to_order.startswith('-'):
            column_to_order = f'-{column_to_order}'
        elif order_dir == 'asc' and column_to_order.startswith('-'):
            column_to_order = column_to_order[1:]

        queryset = queryset.order_by(column_to_order)
        end = start + length
        return queryset[start:end]

    @classmethod
    def count_total(cls) -> int:
        return Acta.objects.count()

    @classmethod
    def count_filtered(cls, search_value: str) -> int:
        queryset = Acta.objects.all()
        queryset = cls._apply_search_and_filters(queryset, search_value)
        return queryset.count()
