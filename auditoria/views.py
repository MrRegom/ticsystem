import json
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisoRequeridoMixin
from .services import AuditoriaService

class AuditoriaDashboardView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    """
    Vista principal del Dashboard de Auditoría y Trazabilidad.
    Requiere un permiso alto, asumiremos SUPERADMIN o equivalente.
    """
    permiso_requerido = 'SUPERADMIN'  # Solo usuarios con alto privilegio
    template_name = 'auditoria/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Resumen de tarjetas
        context['kpis'] = AuditoriaService.obtener_resumen_hoy()
        return context

class AuditoriaLogsAPIView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    """
    API para alimentar el DataTable dinámico. Server-side processing.
    """
    permiso_requerido = 'SUPERADMIN'
    
    def get(self, request, *args, **kwargs):
        # Parámetros de DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        # Parámetros custom (Filtros)
        modulo = request.GET.get('modulo', '')
        accion = request.GET.get('accion', '')
        usuario = request.GET.get('usuario', '')
        fecha_inicio = request.GET.get('fecha_inicio', '')
        fecha_fin = request.GET.get('fecha_fin', '')
        
        # Obtener datos paginados
        data, total_records, filtered_records = AuditoriaService.obtener_logs_paginados(
            start=start,
            length=length,
            search=search_value,
            modulo=modulo,
            accion=accion,
            usuario=usuario,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        return JsonResponse({
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        })
