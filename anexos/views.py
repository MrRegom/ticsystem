"""Vistas del módulo Anexos. Sigue el patrón de equipos.views."""
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error


class AnexosDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'anexos/anexos.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from mantenedores.models import (
            ModeloAnexo, Edificio, Piso, Unidad, Proveedor, Institucion, Marca, Recinto, PMA
        )
        ctx['marcas'] = list(Marca.objects.filter(activo=True).values('id', 'nombre'))
        ctx['modelos_anexos'] = list(ModeloAnexo.objects.filter(activo=True).values('id', 'nombre', 'marca__id'))
        ctx['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        ctx['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id'))
        ctx['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))
        ctx['recintos'] = list(Recinto.objects.filter(activo=True).values('id', 'nombre', 'piso_id', 'unidad_id'))
        ctx['pmas'] = list(PMA.objects.filter(activo=True).values('id', 'nombre', 'recinto_id'))
        ctx['proveedores'] = list(Proveedor.objects.filter(activo=True).values('id', 'nombre'))
        ctx['instituciones'] = list(Institucion.objects.filter(activo=True).values('id', 'nombre', 'codigo'))
        return ctx


class AnexoListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        from anexos.services.anexo_service import AnexoService
        r = AnexoService.obtener_anexos_para_datatable(
            dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )
        return JsonResponse({'draw': dt['draw'], **r})


class AnexoActionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from anexos.services.anexo_service import AnexoService
            a = AnexoService.crear_anexo(data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.CREAR,
                tabla='Anexo', registro_id=a.id,
                detalles=f"Anexo creado: {a.numero_anexo} ({a.marca} {a.modelo})",
                ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Anexo registrado con éxito.', 'data': {'id': a.id}})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            aid = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        if not aid:
            return JsonResponse({'success': False, 'message': 'ID requerido.'}, status=400)
        try:
            from anexos.services.anexo_service import AnexoService
            a = AnexoService.actualizar_anexo(aid, data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.MODIFICAR,
                tabla='Anexo', registro_id=a.id,
                detalles=f"Anexo modificado: {a.numero_anexo}", ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Anexo actualizado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            aid = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from anexos.services.anexo_service import AnexoService
            a = AnexoService.obtener_anexo_por_id(aid)
            if not a:
                return JsonResponse({'success': False, 'message': 'No existe.'}, status=400)
            num = a.numero_anexo
            AnexoService.eliminar_anexo(aid)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.ELIMINAR,
                tabla='Anexo', registro_id=aid,
                detalles=f"Anexo eliminado: {num}", ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Anexo eliminado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class AnexoDetailView(LoginRequiredMixin, View):
    def get(self, request, anexo_id, *args, **kwargs):
        from anexos.services.anexo_service import AnexoService
        a = AnexoService.obtener_anexo_por_id(anexo_id)
        if not a:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)
        return JsonResponse({'success': True, 'data': {
            'id': a.id, 'numero_anexo': a.numero_anexo, 'marca': a.marca, 'modelo': a.modelo,
            'modelo_anexo': a.modelo_anexo_id, 'edificio': a.edificio_id, 'piso': a.piso_id,
            'unidad': a.unidad_id, 'pma_lugar': a.pma_lugar, 'proveedor': a.proveedor_id,
            'estado': a.estado, 'serial_number': a.serial_number,
            'ip': str(a.ip) if a.ip else '', 'comentario': a.comentario or '',
            'grupo': a.grupo or '', 'establecimiento': a.establecimiento_id,
        }})
