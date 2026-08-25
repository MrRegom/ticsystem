"""
Views del módulo de Configuración del Sistema.
Expone la gestión de la Matriz SLA y las Prioridades.

Arquitectura:
- SlaConfigView: Renderiza el dashboard de configuración.
- SlaMatrixApiView: API CRUD para las celdas de la Matriz SLA.
- PrioridadApiView: API CRUD para las Prioridades del helpdesk.
"""
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisoRequeridoMixin
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from tickets.models import Prioridad, Ticket
from sla.models import SLAMatrix


class SlaConfigView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    permiso_requerido = 'GESTIONAR_ROLES'
    """Vista principal del módulo de Configuración."""
    template_name = 'sla/configuracion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Prioridades para los selects del modal
        prioridades = list(
            Prioridad.objects.all().values('id', 'nombre', 'color_hex', 'sla_horas')
        )
        context['prioridades'] = prioridades

        # Construir la matriz SLA para el render visual
        # Formato: {impacto: {urgencia: celda_data}}
        matriz = {}
        for impacto_val, impacto_label in Ticket.Impacto.choices:
            matriz[impacto_val] = {}
            for urgencia_val, urgencia_label in Ticket.Urgencia.choices:
                try:
                    sla = SLAMatrix.objects.select_related('prioridad').get(
                        impacto=impacto_val, urgencia=urgencia_val
                    )
                    matriz[impacto_val][urgencia_val] = {
                        'id': sla.id,
                        'prioridad_id': sla.prioridad_id,
                        'prioridad_nombre': sla.prioridad.nombre,
                        'prioridad_color': sla.prioridad.color_hex,
                        'tiempo_respuesta_minutos': sla.tiempo_respuesta_minutos,
                        'tiempo_resolucion_horas': sla.tiempo_resolucion_horas,
                    }
                except SLAMatrix.DoesNotExist:
                    matriz[impacto_val][urgencia_val] = None

        context['matriz_sla'] = matriz
        context['impactos'] = Ticket.Impacto.choices
        context['urgencias'] = Ticket.Urgencia.choices

        # Serializar datos para JavaScript
        context['matriz_json'] = json.dumps(matriz, cls=DjangoJSONEncoder)
        context['impactos_json'] = json.dumps([
            {'val': v, 'label': l} for v, l in Ticket.Impacto.choices
        ])
        context['urgencias_json'] = json.dumps([
            {'val': v, 'label': l} for v, l in Ticket.Urgencia.choices
        ])

        return context


class SlaMatrixApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ROLES'
    """API JSON para editar celdas de la Matriz SLA."""

    def put(self, request, *args, **kwargs):
        """Actualizar una celda específica de la matriz."""
        try:
            data = json.loads(request.body)
            sla_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not sla_id:
            return JsonResponse({'success': False, 'message': 'ID de celda SLA requerido.'}, status=400)

        try:
            sla = SLAMatrix.objects.get(id=sla_id)
            sla.prioridad_id = data.get('prioridad_id', sla.prioridad_id)
            sla.tiempo_respuesta_minutos = int(data.get('tiempo_respuesta_minutos', sla.tiempo_respuesta_minutos))
            sla.tiempo_resolucion_horas = int(data.get('tiempo_resolucion_horas', sla.tiempo_resolucion_horas))
            sla.save()
            return JsonResponse({'success': True, 'message': 'SLA actualizado correctamente.'})
        except SLAMatrix.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Celda SLA no encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class PrioridadListApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ROLES'
    """API JSON para listar Prioridades."""

    def get(self, request, *args, **kwargs):
        prioridades = list(Prioridad.objects.all().values('id', 'nombre', 'sla_horas', 'color_hex').order_by('sla_horas'))
        return JsonResponse({'success': True, 'data': prioridades})


class PrioridadApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'GESTIONAR_ROLES'
    """API JSON CRUD para Prioridades."""

    def post(self, request, *args, **kwargs):
        """Crear nueva prioridad."""
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        nombre = (data.get('nombre') or '').strip()
        sla_horas = data.get('sla_horas')
        color_hex = (data.get('color_hex') or '#333333').strip()

        if not nombre:
            return JsonResponse({'success': False, 'message': 'El nombre es obligatorio.'}, status=400)
        if not sla_horas:
            return JsonResponse({'success': False, 'message': 'El SLA en horas es obligatorio.'}, status=400)

        try:
            p = Prioridad.objects.create(nombre=nombre, sla_horas=int(sla_horas), color_hex=color_hex)
            return JsonResponse({'success': True, 'message': 'Prioridad creada.', 'data': {'id': p.id, 'nombre': p.nombre}})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe una prioridad con ese nombre.'}, status=400)

    def put(self, request, *args, **kwargs):
        """Actualizar prioridad existente."""
        try:
            data = json.loads(request.body)
            prio_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            p = Prioridad.objects.get(id=prio_id)
            p.nombre = (data.get('nombre') or p.nombre).strip()
            p.sla_horas = int(data.get('sla_horas', p.sla_horas))
            p.color_hex = (data.get('color_hex') or p.color_hex).strip()
            p.save()
            return JsonResponse({'success': True, 'message': 'Prioridad actualizada correctamente.'})
        except Prioridad.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Prioridad no encontrada.'}, status=404)

    def delete(self, request, *args, **kwargs):
        """Eliminar prioridad."""
        try:
            data = json.loads(request.body)
            prio_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            p = Prioridad.objects.get(id=prio_id)
            p.delete()
            return JsonResponse({'success': True, 'message': 'Prioridad eliminada.'})
        except Prioridad.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Prioridad no encontrada.'}, status=404)
        except models.ProtectedError:
            return JsonResponse({'success': False, 'message': 'No se puede eliminar porque esta prioridad está en uso en la Matriz SLA o en tickets.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'}, status=500)
