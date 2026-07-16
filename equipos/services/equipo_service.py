"""
Servicio de Equipo: lógica de negocio para el inventario TIC.

Sigue el patrón de core.services.usuario_service. Valida, coordina y delega
al repositorio. Las reglas de audit trail y recálculo de estado están en
signals.py (se disparan automáticamente al guardar Equipo / BitacoraEquipo).
"""
import os
import re
import unicodedata
from functools import lru_cache

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError

from equipos.models import Equipo, BitacoraEquipo, BitacoraOpcion
from equipos.repositories.equipo_repository import EquipoRepository
from mantenedores.models import (
    Articulo, Marca, Modelo, Edificio, Piso, Unidad,
    SistemaOperativo, EstadoEquipo, Proveedor,
)


def _normalizar_nombre(nombre: str) -> str:
    """Normaliza un nombre de modelo al formato usado en PHP (vistas/img/modelos/)."""
    nombre = nombre.strip().upper()
    nombre = nombre.replace(' ', '')
    nfkd = unicodedata.normalize('NFKD', nombre)
    nombre = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    return re.sub(r'[^A-Z0-9\-]', '', nombre)


MODEL_IMAGE_CACHE: dict[str, str] = {}


def _resolver_imagen_equipo(equipo) -> str:
    """Resuelve la URL de la imagen para un equipo.

    Priodad:
    1. Si equipo.imagen existe (ImageField), usa su URL.
    2. Si no, busca la imagen del modelo asociado en media/modelos/.
    3. Si no hay modelo o no existe archivo, retorna ''.
    """
    if equipo.imagen and hasattr(equipo.imagen, 'url') and equipo.imagen.name:
        return equipo.imagen.url

    modelo = getattr(equipo, 'modelo', None)
    if not modelo:
        return ''

    # Check if the modelo has an image uploaded via the UI
    if hasattr(modelo, 'imagen') and modelo.imagen and hasattr(modelo.imagen, 'url') and modelo.imagen.name:
        return modelo.imagen.url

    cache_key = f'modelo_{modelo.id}'
    if cache_key in MODEL_IMAGE_CACHE:
        return MODEL_IMAGE_CACHE[cache_key]

    norm = _normalizar_nombre(modelo.nombre)
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL.rstrip('/')

    candidates = [
        (f'{norm}/{norm}.jpg',  'jpg'),
        (f'{norm}/{norm}.png',  'png'),
        (f'{norm}.jpg',         'jpg'),
        (f'{norm}.png',         'png'),
    ]

    for rel_path, _ext in candidates:
        abs_path = os.path.join(media_root, 'modelos', rel_path)
        if os.path.isfile(abs_path):
            url = f'{media_url}/modelos/{rel_path}'.replace('\\', '/')
            MODEL_IMAGE_CACHE[cache_key] = url
            return url

    MODEL_IMAGE_CACHE[cache_key] = ''
    
    # 3. Fallback: imagen por defecto del Articulo
    articulo = getattr(equipo, 'articulo', None)
    if articulo and hasattr(articulo, 'imagen') and articulo.imagen and articulo.imagen.name:
        return articulo.imagen.url
        
    return ''


def _resolver_imagen_modelo(modelo) -> str:
    """Resuelve la URL de la imagen para un modelo (sin equipo asociado)."""
    if not modelo:
        return ''
        
    if hasattr(modelo, 'imagen') and modelo.imagen and hasattr(modelo.imagen, 'url') and modelo.imagen.name:
        return modelo.imagen.url

    cache_key = f'modelo_{modelo.id}'
    if cache_key in MODEL_IMAGE_CACHE:
        return MODEL_IMAGE_CACHE[cache_key]
    norm = _normalizar_nombre(modelo.nombre)
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL.rstrip('/')
    candidates = [
        (f'{norm}/{norm}.jpg',  'jpg'),
        (f'{norm}/{norm}.png',  'png'),
        (f'{norm}.jpg',         'jpg'),
        (f'{norm}.png',         'png'),
    ]
    for rel_path, _ext in candidates:
        abs_path = os.path.join(media_root, 'modelos', rel_path)
        if os.path.isfile(abs_path):
            url = f'{media_url}/modelos/{rel_path}'.replace('\\', '/')
            MODEL_IMAGE_CACHE[cache_key] = url
            return url
    MODEL_IMAGE_CACHE[cache_key] = ''
    return ''


class EquipoService:
    """Servicio para operaciones CRUD y consultas de Equipos."""

    @staticmethod
    def obtener_equipo_por_id(equipo_id: int) -> Equipo:
        return EquipoRepository.get_by_id(equipo_id)

    @staticmethod
    def obtener_equipo_por_serial(serial: str) -> Equipo:
        return EquipoRepository.get_by_serial(serial)

    @staticmethod
    def crear_equipo(datos: dict, usuario) -> Equipo:
        """Crea un equipo validando FKs y unicidad de serial.
        Dispara el signal post_save que genera bitácora MOVIMIENTO automática.
        """
        serial = (datos.get('serial_number') or '').strip()
        if not serial:
            raise ValidationError("El número de serie es obligatorio.")
        if Equipo.objects.filter(serial_number__iexact=serial).exists():
            raise ValidationError(f"Ya existe un equipo con el serial '{serial}'.")

        # Validar IP única si viene
        ip = (datos.get('ip') or '').strip() or None
        if ip and Equipo.objects.filter(ip=ip).exists():
            raise ValidationError(f"La IP {ip} ya está asignada a otro equipo.")

        equipo = Equipo(
            articulo_id=datos.get('articulo_id') or None,
            marca_id=datos.get('marca_id') or None,
            modelo_id=datos.get('modelo_id') or None,
            pma_id=datos.get('pma_id') or None,
            so_id=datos.get('so_id') or None,
            estado_id=datos.get('estado_id') or None,
            proveedor_id=datos.get('proveedor_id') or None,
            serial_number=serial,
            ip=ip,
            office=(datos.get('office') or '').strip() or None,
            activador=(datos.get('activador') or '').strip() or None,
            pmalugar=(datos.get('pmalugar') or '').strip() or None,
            comentario=(datos.get('comentario') or '').strip() or None,
            correlativo=(datos.get('correlativo') or '').strip() or None,
            num_inventario=(datos.get('num_inventario') or '').strip() or None,
            mac_address=(datos.get('mac_address') or '').strip() or None,
            switch_ip=(datos.get('switch_ip') or '').strip() or None,
            patch_panel=(datos.get('patch_panel') or '').strip() or None,
            puerto_red=(datos.get('puerto_red') or '').strip() or None,
            orden_compra=(datos.get('orden_compra') or '').strip() or None,
            fecha_compra=datos.get('fecha_compra') or None,
            vencimiento_garantia=datos.get('vencimiento_garantia') or None,
            modificado_por=usuario,
        )
        equipo.full_clean()
        EquipoRepository.save(equipo)
        return equipo

    @staticmethod
    def actualizar_equipo(equipo_id: int, datos: dict, usuario) -> Equipo:
        equipo = EquipoRepository.get_by_id(equipo_id)
        if not equipo:
            raise ValidationError("El equipo no existe.")

        serial = (datos.get('serial_number') or '').strip()
        if not serial:
            raise ValidationError("El número de serie es obligatorio.")
        if Equipo.objects.filter(serial_number__iexact=serial).exclude(pk=equipo_id).exists():
            raise ValidationError(f"Otro equipo ya usa el serial '{serial}'.")

        ip = (datos.get('ip') or '').strip() or None
        if ip and Equipo.objects.filter(ip=ip).exclude(pk=equipo_id).exists():
            raise ValidationError(f"La IP {ip} ya está asignada a otro equipo.")

        equipo.articulo_id = datos.get('articulo_id') or None
        equipo.marca_id = datos.get('marca_id') or None
        equipo.modelo_id = datos.get('modelo_id') or None
        equipo.pma_id = datos.get('pma_id') or None
        equipo.so_id = datos.get('so_id') or None
        equipo.estado_id = datos.get('estado_id') or None
        equipo.proveedor_id = datos.get('proveedor_id') or None
        equipo.serial_number = serial
        equipo.ip = ip
        equipo.office = (datos.get('office') or '').strip() or None
        equipo.activador = (datos.get('activador') or '').strip() or None
        equipo.pmalugar = (datos.get('pmalugar') or '').strip() or None
        equipo.comentario = (datos.get('comentario') or '').strip() or None
        equipo.correlativo = (datos.get('correlativo') or '').strip() or None
        equipo.num_inventario = (datos.get('num_inventario') or '').strip() or None
        equipo.mac_address = (datos.get('mac_address') or '').strip() or None
        equipo.switch_ip = (datos.get('switch_ip') or '').strip() or None
        equipo.patch_panel = (datos.get('patch_panel') or '').strip() or None
        equipo.puerto_red = (datos.get('puerto_red') or '').strip() or None
        equipo.orden_compra = (datos.get('orden_compra') or '').strip() or None
        
        # Las fechas pueden venir vacías, si es string vacío se asigna None para DB
        f_compra = datos.get('fecha_compra')
        equipo.fecha_compra = f_compra if f_compra else None
        
        f_garantia = datos.get('vencimiento_garantia')
        equipo.vencimiento_garantia = f_garantia if f_garantia else None

        equipo.modificado_por = usuario
        
        # Volatile property para signals.py
        equipo._motivo_edicion_pma = datos.get('motivo_edicion_pma')

        equipo.full_clean()
        EquipoRepository.save(equipo)
        return equipo

    @staticmethod
    def eliminar_equipo(equipo_id: int) -> None:
        equipo = EquipoRepository.get_by_id(equipo_id)
        if not equipo:
            raise ValidationError("El equipo no existe.")
        try:
            EquipoRepository.delete(equipo)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar el equipo '{equipo.serial_number}' porque está siendo usado por otros registros."
            )

    @classmethod
    def obtener_equipos_para_datatable(cls, start: int, length: int, search_value: str,
                                       order_column_index: int, order_dir: str,
                                       columns_data: list, estado: str = '', unidad: str = '') -> dict:
        """Caso de uso para DataTables Server-side de Equipos."""
        order_column_name = '-fecha_creacion'
        if 0 <= order_column_index < len(columns_data):
            order_column_name = columns_data[order_column_index].get('data', '-fecha_creacion')

        records = EquipoRepository.get_paginated_list(
            start=start, length=length, search_value=search_value,
            order_column=order_column_name, order_dir=order_dir,
            estado=estado, unidad=unidad
        )
        total_records = EquipoRepository.count_total()
        filtered_records = EquipoRepository.count_filtered(search_value, estado=estado, unidad=unidad)

        data = []
        for e in records:
            img_url = _resolver_imagen_equipo(e)
            # Resolver navegación de relaciones jerárquicas con manejo seguro de nulos
            recinto = e.pma.recinto if e.pma else None
            piso = recinto.piso if recinto else None
            edificio = piso.edificio if piso else None
            unidad = recinto.unidad if recinto else None

            data.append({
                'id': e.id,
                'num_inventario': e.num_inventario or '',
                'serial_number': e.serial_number or e.correlativo or str(e.id),
                'articulo': e.articulo.nombre if e.articulo else '',
                'marca': e.marca.nombre if e.marca else '',
                'modelo': e.modelo.nombre if e.modelo else '',
                'edificio': edificio.nombre if edificio else '',
                'piso': piso.nombre if piso else '',
                'unidad': unidad.nombre if unidad else '',
                'so': e.so.nombre if e.so else '',
                'estado': e.estado.nombre if e.estado else '',
                'estado_color': e.estado.color_hex if e.estado else '#333',
                'ip': str(e.ip) if e.ip else '',
                'pma': e.pma.nombre if e.pma else '',
                'imagen': img_url,
                'fecha_creacion': e.fecha_creacion.strftime('%d/%m/%Y %H:%M') if e.fecha_creacion else '',
            })

        return {
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
