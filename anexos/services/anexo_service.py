"""Servicio de Anexos: lógica de negocio para anexos telefónicos IP."""
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from core.utils import normalizar_nombre

from anexos.models import Anexo, RequerimientoCambio
from anexos.repositories.anexo_repository import AnexoRepository


class AnexoService:

    @staticmethod
    def obtener_anexo_por_id(anexo_id): return AnexoRepository.get_by_id(anexo_id)

    @staticmethod
    def crear_anexo(datos, usuario):
        numero = (datos.get('numero_anexo') or '').strip()
        if not numero:
            raise ValidationError("El número de anexo es obligatorio.")
        if Anexo.objects.filter(numero_anexo__iexact=numero).exists():
            raise ValidationError(f"Ya existe el anexo '{numero}'.")
        serial = (datos.get('serial_number') or '').strip() or numero
        if Anexo.objects.filter(serial_number__iexact=serial).exists():
            raise ValidationError(f"Ya existe un anexo con serial '{serial}'.")

        anexo = Anexo(
            numero_anexo=numero,
            marca=normalizar_nombre(datos.get('marca')),
            modelo=normalizar_nombre(datos.get('modelo')),
            modelo_anexo_id=datos.get('modelo_anexo') or None,
            edificio_id=datos.get('edificio') or None,
            piso_id=datos.get('piso') or None,
            unidad_id=datos.get('unidad') or None,
            pma_lugar=normalizar_nombre(datos.get('pma_lugar')),
            proveedor_id=datos.get('proveedor') or None,
            estado=datos.get('estado') or Anexo.Estado.ACTIVO,
            serial_number=serial,
            ip=datos.get('ip') or None,
            comentario=(datos.get('comentario') or '').strip() or None,
            grupo=(datos.get('grupo') or '').strip() or None,
            establecimiento_id=datos.get('establecimiento') or None,
            creado_por=usuario,
        )
        anexo.full_clean()
        AnexoRepository.save(anexo)
        return anexo

    @staticmethod
    def actualizar_anexo(anexo_id, datos, usuario):
        anexo = AnexoRepository.get_by_id(anexo_id)
        if not anexo:
            raise ValidationError("El anexo no existe.")
        numero = (datos.get('numero_anexo') or '').strip()
        if Anexo.objects.filter(numero_anexo__iexact=numero).exclude(pk=anexo_id).exists():
            raise ValidationError(f"Otro anexo ya usa el número '{numero}'.")
        serial = (datos.get('serial_number') or '').strip() or numero
        if Anexo.objects.filter(serial_number__iexact=serial).exclude(pk=anexo_id).exists():
            raise ValidationError(f"Ya existe un anexo con serial '{serial}'.")

        anexo.numero_anexo = numero
        anexo.marca = normalizar_nombre(datos.get('marca'))
        anexo.modelo = normalizar_nombre(datos.get('modelo'))
        anexo.modelo_anexo_id = datos.get('modelo_anexo') or None
        anexo.edificio_id = datos.get('edificio') or None
        anexo.piso_id = datos.get('piso') or None
        anexo.unidad_id = datos.get('unidad') or None
        anexo.pma_lugar = normalizar_nombre(datos.get('pma_lugar'))
        anexo.proveedor_id = datos.get('proveedor') or None
        anexo.estado = datos.get('estado') or Anexo.Estado.ACTIVO
        anexo.serial_number = serial
        anexo.ip = datos.get('ip') or None
        anexo.comentario = (datos.get('comentario') or '').strip() or None
        anexo.grupo = (datos.get('grupo') or '').strip() or None
        anexo.establecimiento_id = datos.get('establecimiento') or None
        anexo.actualizado_por = usuario
        anexo.full_clean()
        AnexoRepository.save(anexo)
        return anexo

    @staticmethod
    def eliminar_anexo(anexo_id):
        anexo = AnexoRepository.get_by_id(anexo_id)
        if not anexo:
            raise ValidationError("El anexo no existe.")
        try:
            AnexoRepository.delete(anexo)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar el anexo '{anexo.numero_anexo}' porque está siendo usado por otros registros."
            )

    @classmethod
    def obtener_anexos_para_datatable(cls, start, length, search_value,
                                      order_column_index, order_dir, columns_data):
        order_name = 'numero_anexo'
        if 0 <= order_column_index < len(columns_data):
            order_name = columns_data[order_column_index].get('data', 'numero_anexo')
        records = AnexoRepository.get_paginated_list(start, length, search_value, order_name, order_dir)
        total = AnexoRepository.count_total()
        filtered = AnexoRepository.count_filtered(search_value)
        data = []
        for a in records:
            data.append({
                'id': a.id,
                'numero_anexo': a.numero_anexo,
                'marca': a.marca,
                'modelo': a.modelo,
                'modelo_anexo_id': a.modelo_anexo.id if a.modelo_anexo else '',
                'modelo_anexo_nombre': a.modelo_anexo.nombre if a.modelo_anexo else '',
                'modelo_img': a.modelo_anexo.imagen.url if a.modelo_anexo and a.modelo_anexo.imagen else '',
                'edificio_id': a.edificio.id if a.edificio else '',
                'edificio_nombre': a.edificio.nombre if a.edificio else '',
                'piso_id': a.piso.id if a.piso else '',
                'piso_nombre': a.piso.nombre if a.piso else '',
                'unidad_id': a.unidad.id if a.unidad else '',
                'unidad_nombre': a.unidad.nombre if a.unidad else '',
                'estado': a.estado,
                'serial_number': a.serial_number,
                'ip': str(a.ip) if a.ip else '',
                'pma_lugar': a.pma_lugar or '',
                'grupo': a.grupo or '',
                'observacion': a.observacion if hasattr(a, 'observacion') else getattr(a, 'comentario', ''),
            })
        return {'recordsTotal': total, 'recordsFiltered': filtered, 'data': data}
