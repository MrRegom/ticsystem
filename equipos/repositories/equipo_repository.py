"""
Repositorio de datos para el modelo Equipo.
Única capa autorizada para consultas complejas / acceso directo a datos.
Sigue el patrón de core.repositories.usuario_repository.
"""
from django.db import transaction
from django.db.models import Q

from equipos.models import Equipo, BitacoraEquipo, BitacoraOpcion


class EquipoRepository:
    """Repositorio para Equipo y bitácoras asociadas."""

    @staticmethod
    def get_by_id(equipo_id: int) -> Equipo:
        try:
            return Equipo.objects.select_related(
                'articulo', 'marca', 'modelo', 'pma', 'pma__recinto', 'pma__recinto__piso', 
                'pma__recinto__unidad', 'pma__recinto__piso__edificio',
                'so', 'estado', 'proveedor'
            ).get(pk=equipo_id)
        except Equipo.DoesNotExist:
            return None

    @staticmethod
    def get_by_serial(serial: str) -> Equipo:
        try:
            return Equipo.objects.get(serial_number__iexact=serial)
        except Equipo.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def save(equipo: Equipo) -> Equipo:
        equipo.save()
        return equipo

    @staticmethod
    @transaction.atomic
    def delete(equipo: Equipo) -> None:
        equipo.delete()

    @classmethod
    def _apply_search_and_filters(cls, queryset, search_value: str):
        if search_value:
            queryset = queryset.filter(
                Q(serial_number__icontains=search_value) |
                Q(correlativo__icontains=search_value) |
                Q(ip__icontains=search_value) |
                Q(articulo__nombre__icontains=search_value) |
                Q(marca__nombre__icontains=search_value) |
                Q(modelo__nombre__icontains=search_value) |
                Q(pma__recinto__piso__edificio__nombre__icontains=search_value) |
                Q(pma__recinto__piso__nombre__icontains=search_value) |
                Q(pma__recinto__unidad__nombre__icontains=search_value) |
                Q(estado__nombre__icontains=search_value) |
                Q(so__nombre__icontains=search_value)
            )
        return queryset

    @classmethod
    def get_paginated_list(cls, start: int, length: int, search_value: str,
                           order_column: str, order_dir: str):
        queryset = Equipo.objects.select_related(
            'articulo', 'marca', 'modelo', 'pma', 'pma__recinto', 'pma__recinto__piso', 
            'pma__recinto__unidad', 'pma__recinto__piso__edificio',
            'so', 'estado', 'proveedor'
        ).all()
        queryset = cls._apply_search_and_filters(queryset, search_value)

        order_mapping = {
            'serial_number': 'serial_number',
            'articulo': 'articulo__nombre',
            'marca': 'marca__nombre',
            'modelo': 'modelo__nombre',
            'edificio': 'pma__recinto__piso__edificio__nombre',
            'piso': 'pma__recinto__piso__nombre',
            'unidad': 'pma__recinto__unidad__nombre',
            'estado': 'estado__nombre',
            'so': 'so__nombre',
            'ip': 'ip',
            'fecha_creacion': 'fecha_creacion',
        }
        column_to_order = order_mapping.get(order_column, '-fecha_creacion')
        if order_dir == 'desc' and not column_to_order.startswith('-'):
            column_to_order = f'-{column_to_order}'
        elif order_dir == 'asc' and column_to_order.startswith('-'):
            column_to_order = column_to_order[1:]

        queryset = queryset.order_by(column_to_order)
        end = start + length
        return queryset[start:end]

    @classmethod
    def count_total(cls) -> int:
        return Equipo.objects.count()

    @classmethod
    def count_filtered(cls, search_value: str) -> int:
        queryset = Equipo.objects.all()
        queryset = cls._apply_search_and_filters(queryset, search_value)
        return queryset.count()
