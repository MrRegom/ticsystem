from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from core.utils import normalizar_nombre, normalizar_codigo

from actas.models import Acta, ActaDetalle
from actas.repositories.acta_repository import ActaRepository


class ActaService:

    @staticmethod
    def obtener_acta_por_id(acta_id: int) -> Acta:
        return ActaRepository.get_by_id(acta_id)

    @staticmethod
    def crear_acta(datos: dict, usuario) -> Acta:
        codigo = normalizar_codigo(datos.get('codigo'))
        if not codigo:
            raise ValidationError("El código es obligatorio.")
        receptor_nombre = normalizar_nombre(datos.get('receptor_nombre'))
        if not receptor_nombre:
            raise ValidationError("El nombre del receptor es obligatorio.")
        if not datos.get('encargado'):
            raise ValidationError("El encargado es obligatorio.")

        acta = Acta(
            codigo=codigo,
            receptor_nombre=receptor_nombre,
            receptor_rut=(datos.get('receptor_rut') or '').strip() or None,
            receptor_cargo=normalizar_nombre(datos.get('receptor_cargo')) or None,
            receptor_unidad=normalizar_nombre(datos.get('receptor_unidad')) or None,
            encargado_id=datos.get('encargado') or None,
            observaciones=(datos.get('observaciones') or '').strip() or None,
            email_receptor=(datos.get('email_receptor') or '').strip() or None,
            estado=datos.get('estado', Acta.Estado.EMITIDO),
        )
        acta.full_clean()
        ActaRepository.save(acta)

        detalles = datos.get('detalles', [])
        if detalles:
            for d in detalles:
                ActaDetalle.objects.create(
                    acta=acta,
                    tipo_item=d.get('tipo_item', ActaDetalle.TipoItem.EQUIPO),
                    id_item=d.get('id_item', 0),
                    articulo=normalizar_nombre(d.get('articulo')) or None,
                    serie=(d.get('serie') or '').strip() or None,
                    edificio_id=d.get('edificio') or None,
                    piso_id=d.get('piso') or None,
                    unidad_id=d.get('unidad') or None,
                    pma_lugar=normalizar_nombre(d.get('pma_lugar')) or None,
                    estado=(d.get('estado') or '').strip() or None,
                )

        return acta

    @staticmethod
    def actualizar_acta(acta_id: int, datos: dict, usuario) -> Acta:
        acta = ActaRepository.get_by_id(acta_id)
        if not acta:
            raise ValidationError("El acta no existe.")

        codigo = normalizar_codigo(datos.get('codigo'))
        if not codigo:
            raise ValidationError("El código es obligatorio.")
        receptor_nombre = normalizar_nombre(datos.get('receptor_nombre'))
        if not receptor_nombre:
            raise ValidationError("El nombre del receptor es obligatorio.")

        acta.codigo = codigo
        acta.receptor_nombre = receptor_nombre
        acta.receptor_rut = (datos.get('receptor_rut') or '').strip() or None
        acta.receptor_cargo = normalizar_nombre(datos.get('receptor_cargo')) or None
        acta.receptor_unidad = normalizar_nombre(datos.get('receptor_unidad')) or None
        acta.encargado_id = datos.get('encargado') or acta.encargado_id
        acta.observaciones = (datos.get('observaciones') or '').strip() or None
        acta.email_receptor = (datos.get('email_receptor') or '').strip() or None
        acta.estado = datos.get('estado', acta.estado)

        acta.full_clean()
        ActaRepository.save(acta)

        detalles = datos.get('detalles')
        if detalles is not None:
            acta.detalles.all().delete()
            for d in detalles:
                ActaDetalle.objects.create(
                    acta=acta,
                    tipo_item=d.get('tipo_item', ActaDetalle.TipoItem.EQUIPO),
                    id_item=d.get('id_item', 0),
                    articulo=normalizar_nombre(d.get('articulo')) or None,
                    serie=(d.get('serie') or '').strip() or None,
                    edificio_id=d.get('edificio') or None,
                    piso_id=d.get('piso') or None,
                    unidad_id=d.get('unidad') or None,
                    pma_lugar=normalizar_nombre(d.get('pma_lugar')) or None,
                    estado=(d.get('estado') or '').strip() or None,
                )

        return acta

    @staticmethod
    def eliminar_acta(acta_id: int) -> None:
        acta = ActaRepository.get_by_id(acta_id)
        if not acta:
            raise ValidationError("El acta no existe.")
        try:
            ActaRepository.delete(acta)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar el acta '{acta.codigo}' porque tiene detalles asociados."
            )

    @classmethod
    def obtener_actas_para_datatable(cls, start: int, length: int, search_value: str,
                                     order_column_index: int, order_dir: str,
                                     columns_data: list) -> dict:
        order_column_name = '-fecha'
        if 0 <= order_column_index < len(columns_data):
            order_column_name = columns_data[order_column_index].get('data', '-fecha')

        records = ActaRepository.get_paginated_list(
            start=start, length=length, search_value=search_value,
            order_column=order_column_name, order_dir=order_dir,
        )
        total_records = ActaRepository.count_total()
        filtered_records = ActaRepository.count_filtered(search_value)

        data = []
        for a in records:
            data.append({
                'id': a.id,
                'codigo': a.codigo,
                'receptor': a.receptor_nombre,
                'receptor_rut': a.receptor_rut or '',
                'estado': a.estado,
                'fecha': a.fecha.strftime('%d/%m/%Y %H:%M') if a.fecha else '',
                'encargado': a.encargado.get_full_name() or a.encargado.username if a.encargado else '',
                'email_receptor': a.email_receptor or '',
                'observaciones': a.observaciones or '',
                'pdf_url': a.pdf_generado.url if a.pdf_generado else '',
            })

        return {
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
