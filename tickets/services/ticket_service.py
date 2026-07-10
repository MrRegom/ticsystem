from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from core.utils import normalizar_nombre

from tickets.models import Ticket, TicketBitacora
from tickets.repositories.ticket_repository import TicketRepository


class TicketService:

    @staticmethod
    def obtener_ticket_por_id(ticket_id: int) -> Ticket:
        return TicketRepository.get_by_id(ticket_id)

    @staticmethod
    def crear_ticket(datos: dict, usuario) -> Ticket:
        nombre = normalizar_nombre(datos.get('solicitante_nombre'))
        if not nombre:
            raise ValidationError("El nombre del solicitante es obligatorio.")
        descripcion = (datos.get('descripcion') or '').strip()
        if not descripcion:
            raise ValidationError("La descripción es obligatoria.")

        ticket = Ticket(
            solicitante_nombre=nombre,
            solicitante_rut=(datos.get('solicitante_rut') or '').strip() or None,
            solicitante_correo=(datos.get('solicitante_correo') or '').strip() or None,
            solicitante_anexo=(datos.get('solicitante_anexo') or '').strip() or None,
            edificio_id=datos.get('edificio') or None,
            piso_id=datos.get('piso') or None,
            unidad_id=datos.get('unidad') or None,
            equipo_id=datos.get('equipo') or None,
            descripcion=descripcion,
            tecnico_id=datos.get('tecnico') or None,
            prioridad_id=datos.get('prioridad') or None,
            categoria_id=datos.get('categoria') or None,
            estado=datos.get('estado') or Ticket.Estado.PENDIENTE,
        )
        ticket.full_clean()
        TicketRepository.save(ticket)
        return ticket

    @staticmethod
    def actualizar_ticket(ticket_id: int, datos: dict, usuario) -> Ticket:
        ticket = TicketRepository.get_by_id(ticket_id)
        if not ticket:
            raise ValidationError("El ticket no existe.")

        nombre = normalizar_nombre(datos.get('solicitante_nombre'))
        if not nombre:
            raise ValidationError("El nombre del solicitante es obligatorio.")
        descripcion = (datos.get('descripcion') or '').strip()
        if not descripcion:
            raise ValidationError("La descripción es obligatoria.")

        ticket.solicitante_nombre = nombre
        ticket.solicitante_rut = (datos.get('solicitante_rut') or '').strip() or None
        ticket.solicitante_correo = (datos.get('solicitante_correo') or '').strip() or None
        ticket.solicitante_anexo = (datos.get('solicitante_anexo') or '').strip() or None
        ticket.edificio_id = datos.get('edificio') or None
        ticket.piso_id = datos.get('piso') or None
        ticket.unidad_id = datos.get('unidad') or None
        ticket.equipo_id = datos.get('equipo') or None
        ticket.descripcion = descripcion
        ticket.tecnico_id = datos.get('tecnico') or None
        ticket.prioridad_id = datos.get('prioridad') or None
        ticket.categoria_id = datos.get('categoria') or None
        ticket.estado = datos.get('estado') or Ticket.Estado.PENDIENTE

        ticket.full_clean()
        TicketRepository.save(ticket)
        return ticket

    @staticmethod
    def eliminar_ticket(ticket_id: int) -> None:
        ticket = TicketRepository.get_by_id(ticket_id)
        if not ticket:
            raise ValidationError("El ticket no existe.")
        try:
            TicketRepository.delete(ticket)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar el ticket #{ticket.id} porque está siendo usado por otros registros."
            )

    @classmethod
    def obtener_tickets_para_datatable(cls, start: int, length: int, search_value: str,
                                       order_column_index: int, order_dir: str,
                                       columns_data: list) -> dict:
        order_column_name = '-fecha_hora'
        if 0 <= order_column_index < len(columns_data):
            order_column_name = columns_data[order_column_index].get('data', '-fecha_hora')

        records = TicketRepository.get_paginated_list(
            start=start, length=length, search_value=search_value,
            order_column=order_column_name, order_dir=order_dir,
        )
        total_records = TicketRepository.count_total()
        filtered_records = TicketRepository.count_filtered(search_value)

        data = []
        for t in records:
            data.append({
                'id': t.id,
                'solicitante_nombre': t.solicitante_nombre,
                'solicitante_rut': t.solicitante_rut or '',
                'edificio': t.edificio.nombre if t.edificio else '',
                'piso': t.piso.nombre if t.piso else '',
                'unidad': t.unidad.nombre if t.unidad else '',
                'equipo': str(t.equipo) if t.equipo else '',
                'estado': t.get_estado_display(),
                'prioridad': t.prioridad.nivel if t.prioridad else '',
                'prioridad_color': t.prioridad.color_hex if t.prioridad else '#333',
                'categoria': t.categoria.nombre if t.categoria else '',
                'tecnico': t.tecnico.username if t.tecnico else '',
                'fecha_hora': t.fecha_hora.strftime('%d/%m/%Y %H:%M') if t.fecha_hora else '',
            })

        return {
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data,
        }
