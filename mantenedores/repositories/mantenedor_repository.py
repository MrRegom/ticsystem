"""
MantenedorRepository
====================
Capa de acceso a datos para los catálogos del sistema.

Principios aplicados (django-patterns skill):
  - Custom QuerySet patterns con select_related / prefetch_related para evitar N+1.
  - Mapas declarativos por modelo (evitar if/elif creciente).
  - Transacciones atómicas en operaciones de escritura.
  - Separación estricta de responsabilidades: este módulo SOLO toca la BD.
"""
from django.db import transaction
from django.db.models import Q


# ─── Mapas de configuración por modelo ──────────────────────────────────────

# Relaciones ForeignKey/OneToOne a cargar con select_related (evita N+1 en listas)
SELECT_RELATED_MAP: dict = {
    'Edificio'        : ['institucion'],
    'Piso'            : ['edificio', 'edificio__institucion'],
    'Modelo'          : ['marca'],
    'Sector'          : ['piso', 'piso__edificio'],
    'Unidad'          : ['area_hospitalaria'],
    'Recinto'         : ['piso', 'sector', 'unidad', 'piso__edificio'],
    'PMA'             : ['recinto', 'recinto__piso', 'recinto__unidad',
                         'recinto__piso__edificio'],
    'Funcionario'     : ['unidad'],
}

# Campos de búsqueda por modelo (se combinarán con OR)
SEARCH_FIELDS_MAP: dict = {
    'BitacoraOpcion'  : ['nombre', 'tipo'],
    'Edificio'        : ['nombre', 'institucion__nombre'],
    'Piso'            : ['nombre', 'alias', 'edificio__nombre'],
    'Modelo'          : ['nombre', 'marca__nombre'],
    'Sector'          : ['nombre', 'piso__nombre'],
    'Unidad'          : ['nombre', 'area_hospitalaria__nombre'],
    'Recinto'         : ['nombre', 'piso__nombre', 'sector__nombre', 'unidad__nombre'],
    'PMA'             : ['nombre', 'recinto__nombre', 'recinto__piso__nombre', 'recinto__unidad__nombre', 'recinto__piso__edificio__nombre'],
    'Funcionario'     : ['rut', 'nombres', 'apellidos', 'correo', 'cargo__nombre', 'unidad__nombre'],
}

# Columnas de ordenamiento por modelo (data-key DataTables → campo ORM)
ORDER_MAP: dict = {
    'BitacoraOpcion'  : {'tipo': 'tipo', 'nombre': 'nombre', 'orden': 'orden'},
    'Edificio'        : {'nombre': 'nombre', 'institucion': 'institucion__nombre'},
    'Piso'            : {'nombre': 'nombre', 'alias': 'alias', 'edificio': 'edificio__nombre'},
    'Modelo'          : {'nombre': 'nombre', 'marca': 'marca__nombre'},
    'Sector'          : {'nombre': 'nombre', 'piso': 'piso__nombre'},
    'Unidad'          : {'nombre': 'nombre', 'area_hospitalaria': 'area_hospitalaria__nombre'},
    'Recinto'         : {'nombre': 'nombre', 'piso': 'piso__nombre',
                         'sector': 'sector__nombre', 'unidad': 'unidad__nombre'},
    'PMA'             : {'nombre': 'nombre', 'recinto': 'recinto__nombre', 'recinto__piso': 'recinto__piso__nombre', 'recinto__unidad': 'recinto__unidad__nombre'},
    'Funcionario'     : {'nombres': 'nombres', 'rut': 'rut', 'correo': 'correo', 'cargo': 'cargo__nombre', 'unidad': 'unidad__nombre'},
}


class MantenedorRepository:
    """
    Repositorio genérico para todos los catálogos del sistema.

    Métodos de lectura:
        get_by_id          → instancia individual con relaciones precargadas
        get_paginated_list → lista paginada, filtrada y ordenada para DataTables
        count_total        → total de registros sin filtrar
        count_filtered     → total de registros filtrados por búsqueda

    Métodos de escritura (transaccionales):
        save               → INSERT o UPDATE
        delete             → DELETE
    """

    # ── Lectura ─────────────────────────────────────────────────────────────

    @staticmethod
    def get_by_id(model_class, item_id):
        """Retorna una instancia con relaciones optimizadas, o None si no existe."""
        related = SELECT_RELATED_MAP.get(model_class.__name__, [])
        try:
            qs = model_class.objects
            if related:
                qs = qs.select_related(*related)
            return qs.get(pk=item_id)
        except model_class.DoesNotExist:
            return None

    @classmethod
    def _build_search_q(cls, model_class, search_value: str) -> Q:
        """Construye expresión Q para filtrado full-text sobre los campos configurados."""
        fields = SEARCH_FIELDS_MAP.get(model_class.__name__, ['nombre'])
        q = Q()
        for field in fields:
            q |= Q(**{f'{field}__icontains': search_value})
        return q

    @classmethod
    def _apply_search(cls, qs, search_value: str, model_class):
        """Aplica filtro de búsqueda al QuerySet dado."""
        if search_value:
            qs = qs.filter(cls._build_search_q(model_class, search_value))
        return qs

    @classmethod
    def get_paginated_list(cls, model_class, start: int, length: int,
                           search_value: str, order_column: str, order_dir: str):
        """
        Retorna una lista paginada, ordenada y filtrada para DataTables server-side.

        Evita N+1 mediante select_related configurable por modelo.
        """
        related = SELECT_RELATED_MAP.get(model_class.__name__, [])
        qs = model_class.objects.all()
        if related:
            qs = qs.select_related(*related)

        qs = cls._apply_search(qs, search_value, model_class)

        # Ordenamiento seguro: mapeamos el nombre de columna DataTables al campo ORM real
        mapping = ORDER_MAP.get(model_class.__name__, {'nombre': 'nombre'})
        default_sort = 'nombres' if model_class.__name__ == 'Funcionario' else 'nombre'
        orm_col = mapping.get(order_column, default_sort)
        if order_dir == 'desc' and not orm_col.startswith('-'):
            orm_col = f'-{orm_col}'
        elif order_dir == 'asc' and orm_col.startswith('-'):
            orm_col = orm_col[1:]

        return list(qs.order_by(orm_col)[start:start + length])

    @classmethod
    def count_total(cls, model_class) -> int:
        """Total de registros sin filtrar (recordsTotal para DataTables)."""
        return model_class.objects.count()

    @classmethod
    def count_filtered(cls, model_class, search_value: str) -> int:
        """Total de registros filtrados (recordsFiltered para DataTables)."""
        qs = model_class.objects.all()
        return cls._apply_search(qs, search_value, model_class).count()

    # ── Escritura ────────────────────────────────────────────────────────────

    @staticmethod
    @transaction.atomic
    def save(instance):
        """Persiste la instancia (INSERT o UPDATE). Transacción atómica."""
        instance.save()
        return instance

    @staticmethod
    @transaction.atomic
    def delete(instance):
        """Elimina la instancia. Transacción atómica."""
        instance.delete()
