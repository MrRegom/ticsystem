from .repositories import ReportesRepository
import csv
from django.http import HttpResponse
from tickets.models import Ticket
from equipos.models import Equipo

class GraficosService:
    """
    Toma los datos crudos del Repositorio y los adapta a las estructuras
    requeridas por Chart.js (labels, datasets, backgroundColors).
    """
    
    # Paleta Corporativa (Enterprise Glassmorphism)
    COLORS = {
        'success': '#10b981', # Verde
        'danger': '#ef4444',  # Rojo
        'warning': '#f59e0b', # Naranja
        'primary': '#3b82f6', # Azul
        'info': '#0ea5e9',    # Celeste
        'purple': '#8b5cf6',
        'pink': '#ec4899',
    }

    @classmethod
    def get_sla_data(cls):
        data = ReportesRepository.obtener_cumplimiento_sla()
        return {
            'labels': ['En Tiempo', 'Vencidos'],
            'datasets': [{
                'data': [data['a_tiempo'], data['vencidos']],
                'backgroundColor': [cls.COLORS['success'], cls.COLORS['danger']],
                'hoverOffset': 4
            }]
        }

    @classmethod
    def get_categoria_data(cls):
        qs = ReportesRepository.obtener_carga_por_categoria()
        labels = [item['categoria__nombre'] if item['categoria__nombre'] else 'Sin Categoría' for item in qs]
        data = [item['total'] for item in qs]
        
        # Generar gradiente de colores (usamos la paleta)
        bg_colors = [list(cls.COLORS.values())[i % len(cls.COLORS)] for i in range(len(labels))]
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Volumen de Requerimientos',
                'data': data,
                'backgroundColor': bg_colors,
                'borderRadius': 6,
            }]
        }

    @classmethod
    def get_tendencia_mensual_data(cls):
        qs = ReportesRepository.obtener_tendencia_mensual()
        labels = []
        data = []
        
        meses_espanol = {
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        }
        
        for item in qs:
            mes_num = item['mes'].month if item['mes'] else 1
            labels.append(f"{meses_espanol.get(mes_num, '')} {item['mes'].year if item['mes'] else ''}")
            data.append(item['total'])
            
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Tickets Creados',
                'data': data,
                'borderColor': cls.COLORS['primary'],
                'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                'borderWidth': 3,
                'fill': True,
                'tension': 0.4 # Curvas suaves (Spline)
            }]
        }

    @classmethod
    def get_top_equipos_data(cls):
        qs = ReportesRepository.obtener_top_equipos_criticos()
        equipos = []
        for item in qs:
            articulo = item['activo__articulo__nombre'] or 'Desconocido'
            marca = item['activo__marca__nombre'] or ''
            serie = item['activo__serial_number'] or 'S/N'
            
            equipos.append({
                'nombre': f"{articulo} {marca}",
                'serie': serie,
                'fallas': item['total_fallas']
            })
        return equipos

class ExportadorCSVService:
    """
    Motor universal de exportación a CSV UTF-8 con BOM.
    Compatible de forma nativa con Microsoft Excel sin librerías de terceros.
    """
    
    @staticmethod
    def _crear_respuesta_csv(filename):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        # Insertar BOM (Byte Order Mark) para que Excel reconozca automáticamente UTF-8
        response.write('\ufeff')
        return response

    @classmethod
    def exportar_tickets(cls):
        response = cls._crear_respuesta_csv('Historial_Tickets_Enterprise')
        writer = csv.writer(response, delimiter=';') # Excel en español prefiere punto y coma
        
        # Cabeceras
        writer.writerow([
            'N° Ticket', 'Descripción', 'Estado', 'Prioridad', 'Categoría',
            'Equipo Asociado', 'Serie Equipo', 'Ubicación / PMA',
            'Creador', 'Técnico Responsable', 'Fecha Creación', 'Fecha Cierre'
        ])
        
        # Evitar N+1 queries con select_related
        tickets = Ticket.objects.select_related(
            'prioridad', 'categoria', 'activo', 
            'activo__pma', 'creador', 'responsable'
        ).all().order_by('-id')
        
        for t in tickets:
            writer.writerow([
                t.correlativo,
                t.descripcion.replace('\n', ' ').replace('\r', '') if t.descripcion else '',
                t.get_estado_display() if hasattr(t, 'get_estado_display') else t.estado,
                t.prioridad.nombre if t.prioridad else '',
                t.categoria.nombre if t.categoria else '',
                t.activo.articulo.nombre if t.activo and t.activo.articulo else 'Sin Equipo',
                t.activo.serial_number if t.activo else '',
                t.activo.pma.nombre if t.activo and t.activo.pma else '',
                t.creador.get_full_name() or t.creador.username if t.creador else '',
                t.responsable.get_full_name() or t.responsable.username if t.responsable else 'Sin Asignar',
                t.fecha_creacion.strftime('%Y-%m-%d %H:%M') if t.fecha_creacion else '',
                t.fecha_cierre.strftime('%Y-%m-%d %H:%M') if t.fecha_cierre else ''
            ])
            
        return response

    @classmethod
    def exportar_activos(cls):
        response = cls._crear_respuesta_csv('Inventario_Activos_Enterprise')
        writer = csv.writer(response, delimiter=';')
        
        writer.writerow([
            'N° Inventario', 'Número de Serie', 'Artículo', 'Marca', 'Modelo',
            'Estado', 'PMA (Ubicación)', 'IP', 'Sistema Operativo'
        ])
        
        equipos = Equipo.objects.select_related(
            'articulo', 'marca', 'modelo', 'estado',
            'pma', 'so'
        ).all().order_by('id')
        
        for e in equipos:
            writer.writerow([
                e.num_inventario or '',
                e.serial_number or '',
                e.articulo.nombre if e.articulo else '',
                e.marca.nombre if e.marca else '',
                e.modelo.nombre if e.modelo else '',
                e.estado.nombre if e.estado else '',
                e.pma.nombre if e.pma else '',
                e.ip or '',
                e.so.nombre if e.so else ''
            ])
            
        return response
