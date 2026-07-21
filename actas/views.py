import json

from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisoRequeridoMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

import os
import base64
from django.core.files.base import ContentFile
from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error
from actas.utils.pdf_generator import generar_pdf_acta


class ActasDashboardView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    permiso_requerido = 'VER_ACTAS'
    """Vista del módulo de Actas de Entrega."""
    template_name = 'actas/actas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from mantenedores.models import Edificio, Piso, Unidad, Cargo
        context['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        context['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id', 'edificio__nombre'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))
        context['cargos'] = list(Cargo.objects.filter(activo=True).values('id', 'nombre'))
        context['encargados'] = list(User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name'))
        return context


class ActaListView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'VER_ACTAS'
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


class ActaActionView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ACTAS'
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


class ActaGenerateView(LoginRequiredMixin, View):
    """API para generar un Acta con PDF y firmas desde el UI."""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from actas.services.acta_service import ActaService
            
            # Generar un código único (ej: ACT-20260714-1)
            from django.utils import timezone
            import time
            from actas.models import Acta
            # Podríamos buscar el último y sumarle 1, pero usaremos timestamp corto por simplicidad
            codigo = f"ACT-{timezone.now().strftime('%Y%m%d')}-{int(time.time() * 1000) % 10000}"
            data['codigo'] = codigo

            # 1. Crear el Acta en DB
            acta = ActaService.crear_acta(data, usuario=request.user)
            
            # 2. Procesar y guardar firmas en Base64
            firma_rec_b64 = data.get('firma_receptor_b64')
            firma_tic_b64 = data.get('firma_tic_b64')
            
            if firma_rec_b64 and ',' in firma_rec_b64:
                format, imgstr = firma_rec_b64.split(';base64,')
                ext = format.split('/')[-1]
                acta.firma_receptor.save(f"firma_rec_{acta.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)
                
            if firma_tic_b64 and ',' in firma_tic_b64:
                format, imgstr = firma_tic_b64.split(';base64,')
                ext = format.split('/')[-1]
                acta.firma_encargado.save(f"firma_tic_{acta.id}.{ext}", ContentFile(base64.b64decode(imgstr)), save=False)
            
            acta.save()

            # 3. Generar el PDF
            rutas_firmas = {}
            if acta.firma_receptor: rutas_firmas['receptor'] = acta.firma_receptor.path
            if acta.firma_encargado: rutas_firmas['tic'] = acta.firma_encargado.path
            
            pdf_buffer = generar_pdf_acta(acta, firmas_paths=rutas_firmas, datos_ui_detalles=data.get('detalles', []))
            
            # 4. Guardar el PDF en el modelo
            pdf_filename = f"Acta_{acta.codigo}.pdf"
            acta.pdf_generado.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)

            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='Acta',
                registro_id=acta.id,
                detalles=f"Acta generada con PDF: {acta.codigo}",
                ip_address=get_client_ip(request),
            )

            return JsonResponse({
                'success': True,
                'message': 'Acta generada exitosamente.',
                'pdf_url': acta.pdf_generado.url
            })
            
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'}, status=500)
