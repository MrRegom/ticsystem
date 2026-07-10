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


class ActasDashboardView(LoginRequiredMixin, TemplateView):
    """Vista del módulo de Actas de Entrega."""
    template_name = 'actas/actas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from mantenedores.models import Edificio, Piso, Unidad
        context['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        context['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id', 'edificio__nombre'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))
        context['encargados'] = list(User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name'))
        return context


class ActaListView(LoginRequiredMixin, View):
    """API Server-Side para DataTables de Actas."""

    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        from actas.services.acta_service import ActaService
        result = ActaService.obtener_actas_para_datatable(
            dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )
        return JsonResponse({
            'draw': dt['draw'],
            'recordsTotal': result['recordsTotal'],
            'recordsFiltered': result['recordsFiltered'],
            'data': result['data'],
        })


class ActaActionView(LoginRequiredMixin, View):
    """API JSON para acciones CRUD de actas."""

    def post(self, request, *args, **kwargs):
        """Crear nueva acta."""
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from actas.services.acta_service import ActaService
            acta = ActaService.crear_acta(data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='Acta',
                registro_id=acta.id,
                detalles=f"Acta creada: {acta.codigo} - {acta.receptor_nombre}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Acta registrada con éxito.',
                'data': {'id': acta.id, 'codigo': acta.codigo},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        """Actualizar acta existente."""
        try:
            data = json.loads(request.body)
            acta_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not acta_id:
            return JsonResponse({'success': False, 'message': 'ID de acta requerido.'}, status=400)

        try:
            from actas.services.acta_service import ActaService
            acta = ActaService.actualizar_acta(acta_id, data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.MODIFICAR,
                tabla='Acta',
                registro_id=acta.id,
                detalles=f"Acta modificada: {acta.codigo}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Acta actualizada con éxito.',
                'data': {'id': acta.id, 'codigo': acta.codigo},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        """Eliminar acta."""
        try:
            data = json.loads(request.body)
            acta_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not acta_id:
            return JsonResponse({'success': False, 'message': 'ID de acta requerido.'}, status=400)

        try:
            from actas.services.acta_service import ActaService
            acta = ActaService.obtener_acta_por_id(acta_id)
            if not acta:
                return JsonResponse({'success': False, 'message': 'El acta no existe.'}, status=400)
            codigo = acta.codigo
            ActaService.eliminar_acta(acta_id)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.ELIMINAR,
                tabla='Acta',
                registro_id=acta_id,
                detalles=f"Acta eliminada: {codigo}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({'success': True, 'message': 'Acta eliminada con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class ActaDetailView(LoginRequiredMixin, View):
    """API JSON para obtener detalle de un acta (para modal de edición)."""

    def get(self, request, acta_id, *args, **kwargs):
        from actas.services.acta_service import ActaService
        acta = ActaService.obtener_acta_por_id(acta_id)
        if not acta:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)
        detalles = []
        for d in acta.detalles.all():
            detalles.append({
                'id': d.id,
                'tipo_item': d.tipo_item,
                'id_item': d.id_item,
                'articulo': d.articulo or '',
                'serie': d.serie or '',
                'edificio': d.edificio_id,
                'piso': d.piso_id,
                'unidad': d.unidad_id,
                'pma_lugar': d.pma_lugar or '',
                'estado': d.estado or '',
            })
        return JsonResponse({
            'success': True,
            'data': {
                'id': acta.id,
                'codigo': acta.codigo,
                'receptor_nombre': acta.receptor_nombre,
                'receptor_rut': acta.receptor_rut or '',
                'receptor_cargo': acta.receptor_cargo or '',
                'receptor_unidad': acta.receptor_unidad or '',
                'encargado': acta.encargado_id,
                'observaciones': acta.observaciones or '',
                'email_receptor': acta.email_receptor or '',
                'estado': acta.estado,
                'detalles': detalles,
            }
        })
