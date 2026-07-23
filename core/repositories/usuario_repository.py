from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from core.models import PerfilUsuario

class UsuarioRepository:
    """
    Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado.
    """

    @staticmethod
    def get_by_id(user_id: int) -> User:
        try:
            return User.objects.select_related('perfil').get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_username(username: str) -> User:
        try:
            return User.objects.select_related('perfil').get(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_by_rut(rut: str) -> User:
        try:
            perfil = PerfilUsuario.objects.select_related('user').get(rut=rut)
            return perfil.user
        except PerfilUsuario.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def save(user: User, perfil: PerfilUsuario) -> User:
        user.save()
        perfil.user = user
        perfil.save()
        return user

    @staticmethod
    @transaction.atomic
    def delete(user: User) -> None:
        user.delete()

    @classmethod
    def _apply_search_and_filters(cls, queryset, search_value: str):
        if search_value:
            queryset = queryset.filter(
                Q(username__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(perfil__unidad__icontains=search_value) |
                Q(perfil__cargo__icontains=search_value) |
                Q(perfil__grado__icontains=search_value)
            )
        return queryset

    @classmethod
    def get_paginated_list(cls, start: int, length: int, search_value: str, 
                            order_column: str, order_dir: str, status: str = 'active'):
        queryset = User.objects.select_related('perfil').prefetch_related('groups').all()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'disabled':
            queryset = queryset.filter(is_active=False)
            
        queryset = cls._apply_search_and_filters(queryset, search_value)

        # Mapeo seguro de columnas de ordenamiento
        order_mapping = {
            'rut': 'username',
            'username': 'username',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'unidad': 'perfil__unidad',
            'cargo': 'perfil__cargo',
            'grado': 'perfil__grado',
            'fecha_registro': 'perfil__fecha_registro'
        }

        column_to_order = order_mapping.get(order_column, 'perfil__fecha_registro')
        if order_dir == 'desc':
            column_to_order = f'-{column_to_order}'
        
        queryset = queryset.order_by(column_to_order)
        end = start + length
        return queryset[start:end]

    @classmethod
    def count_total(cls, status: str = 'active') -> int:
        queryset = User.objects.all()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'disabled':
            queryset = queryset.filter(is_active=False)
        return queryset.count()

    @classmethod
    def count_filtered(cls, search_value: str, status: str = 'active') -> int:
        queryset = User.objects.all()
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'disabled':
            queryset = queryset.filter(is_active=False)
            
        queryset = cls._apply_search_and_filters(queryset, search_value)
        return queryset.count()
