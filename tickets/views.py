import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error


class TicketsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tickets/tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from mantenedores.models import Edificio, Piso, Unidad
        from tickets.models import Prioridad, Categoria
        from equipos.models import Equipo
        context['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        context['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))
        context['prioridades'] = list(Prioridad.objects.all().values('id', 'nivel', 'color_hex'))
        context['categorias'] = list(Categoria.objects.filter(activo=True).values('id', 'nombre'))
        context['tecnicos'] = list(User.objects.filter(is_active=True).values('id', 'username'))
        context['equipos'] = list(Equipo.objects.values('id', 'serial_number'))
        return context


class TicketListView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        from tickets.services.ticket_service import TicketService
        result = TicketService.obtener_tickets_para_datatable(
            dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )
        return JsonResponse({
            'draw': dt['draw'],
            'recordsTotal': result['recordsTotal'],
            'recordsFiltered': result['recordsFiltered'],
            'data': result['data'],
        })


class TicketActionView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from tickets.services.ticket_service import TicketService
            ticket = TicketService.crear_ticket(data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='Ticket',
                registro_id=ticket.id,
                detalles=f"Ticket creado: #{ticket.id} - {ticket.solicitante_nombre}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Ticket registrado con éxito.',
                'data': {'id': ticket.id},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ticket_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not ticket_id:
            return JsonResponse({'success': False, 'message': 'ID de ticket requerido.'}, status=400)

        try:
            from tickets.services.ticket_service import TicketService
            ticket = TicketService.actualizar_ticket(ticket_id, data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.MODIFICAR,
                tabla='Ticket',
                registro_id=ticket.id,
                detalles=f"Ticket modificado: #{ticket.id} - {ticket.solicitante_nombre}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Ticket actualizado con éxito.',
                'data': {'id': ticket.id},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ticket_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not ticket_id:
            return JsonResponse({'success': False, 'message': 'ID de ticket requerido.'}, status=400)

        try:
            from tickets.services.ticket_service import TicketService
            ticket = TicketService.obtener_ticket_por_id(ticket_id)
            if not ticket:
                return JsonResponse({'success': False, 'message': 'El ticket no existe.'}, status=400)
            solic = ticket.solicitante_nombre
            TicketService.eliminar_ticket(ticket_id)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.ELIMINAR,
                tabla='Ticket',
                registro_id=ticket_id,
                detalles=f"Ticket eliminado: #{ticket_id} - {solic}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({'success': True, 'message': 'Ticket eliminado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketDetailView(LoginRequiredMixin, View):

    def get(self, request, ticket_id, *args, **kwargs):
        from tickets.services.ticket_service import TicketService
        ticket = TicketService.obtener_ticket_por_id(ticket_id)
        if not ticket:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)

        notas = []
        for n in ticket.notas.all().select_related('usuario')[:50]:
            notas.append({
                'id': n.id,
                'usuario': n.usuario.username if n.usuario else '',
                'nota': n.nota,
                'tipo_nota': n.tipo_nota,
                'fecha_registro': n.fecha_registro.strftime('%d/%m/%Y %H:%M') if n.fecha_registro else '',
            })

        return JsonResponse({
            'success': True,
            'data': {
                'id': ticket.id,
                'solicitante_nombre': ticket.solicitante_nombre,
                'solicitante_rut': ticket.solicitante_rut or '',
                'solicitante_correo': ticket.solicitante_correo or '',
                'solicitante_anexo': ticket.solicitante_anexo or '',
                'edificio': ticket.edificio_id,
                'piso': ticket.piso_id,
                'unidad': ticket.unidad_id,
                'equipo': ticket.equipo_id,
                'descripcion': ticket.descripcion,
                'tecnico': ticket.tecnico_id,
                'prioridad': ticket.prioridad_id,
                'categoria': ticket.categoria_id,
                'estado': ticket.estado,
                'fecha_hora': ticket.fecha_hora.strftime('%d/%m/%Y %H:%M') if ticket.fecha_hora else '',
                'notas': notas,
            }
        })
