"""Repositorio de Anexos. Sigue el patrón de equipo_repository."""
from django.db import transaction
from django.db.models import Q

from anexos.models import Anexo, RequerimientoCambio


class AnexoRepository:

    @staticmethod
    def get_by_id(anexo_id: int) -> Anexo:
        try:
            return Anexo.objects.select_related(
                'modelo_anexo', 'edificio', 'piso', 'unidad', 'pma', 'proveedor', 'establecimiento',
            ).get(pk=anexo_id)
        except Anexo.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def save(anexo: Anexo) -> Anexo:
        anexo.save()
        return anexo

    @staticmethod
    @transaction.atomic
    def delete(anexo: Anexo) -> None:
        anexo.delete()

    @classmethod
    def _apply_search(cls, qs, search_value: str):
        if search_value:
            qs = qs.filter(
                Q(numero_anexo__icontains=search_value) |
                Q(serial_number__icontains=search_value) |
                Q(marca__icontains=search_value) |
                Q(modelo__icontains=search_value) |
                Q(ip__icontains=search_value) |
                Q(pma__nombre__icontains=search_value) |
                Q(comentario__icontains=search_value) |
                Q(grupo__icontains=search_value) |
                Q(edificio__nombre__icontains=search_value) |
                Q(piso__nombre__icontains=search_value) |
                Q(unidad__nombre__icontains=search_value)
            )
        return qs

    @classmethod
    def get_paginated_list(cls, start, length, search_value, order_column, order_dir):
        qs = Anexo.objects.select_related(
            'modelo_anexo', 'edificio', 'piso', 'unidad', 'pma', 'establecimiento',
        ).all()
        qs = cls._apply_search(qs, search_value)
        order_map = {
            'numero_anexo': 'numero_anexo', 'marca': 'marca', 'modelo': 'modelo',
            'edificio': 'edificio__nombre', 'piso': 'piso__nombre',
            'unidad': 'unidad__nombre', 'estado': 'estado', 'ip': 'ip',
            'serial_number': 'serial_number', 'pma_lugar': 'pma__nombre',
        }
        col = order_map.get(order_column, 'numero_anexo')
        if order_dir == 'desc' and not col.startswith('-'):
            col = f'-{col}'
        elif order_dir == 'asc' and col.startswith('-'):
            col = col[1:]
        return qs.order_by(col)[start:start + length]

    @classmethod
    def count_total(cls): return Anexo.objects.count()

    @classmethod
    def count_filtered(cls, search_value):
        return cls._apply_search(Anexo.objects.all(), search_value).count()
