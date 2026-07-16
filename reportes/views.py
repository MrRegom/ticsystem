from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import GraficosService
import json

class DashboardReportesView(LoginRequiredMixin, TemplateView):
    template_name = 'reportes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Inyectamos los JSON directo al template para que Chart.js los consuma
        context['sla_data'] = json.dumps(GraficosService.get_sla_data())
        context['categoria_data'] = json.dumps(GraficosService.get_categoria_data())
        context['tendencia_data'] = json.dumps(GraficosService.get_tendencia_mensual_data())
        
        # El Top de equipos se renderiza en HTML nativo
        context['top_equipos'] = GraficosService.get_top_equipos_data()
        
        return context

class ExportarTicketsView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        from .services import ExportadorCSVService
        return ExportadorCSVService.exportar_tickets()

class ExportarActivosView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        from .services import ExportadorCSVService
        return ExportadorCSVService.exportar_activos()
