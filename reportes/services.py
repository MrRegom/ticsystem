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
            'ID Ticket', 'Asunto', 'Estado', 'Prioridad', 'Categoría',
            'Equipo Asociado', 'Serie Equipo', 'Servicio / Unidad',
            'Creador', 'Técnico Asignado', 'Fecha Creación', 'Fecha Cierre'
        ])
        
        # Evitar N+1 queries con select_related
        tickets = Ticket.objects.select_related(
            'estado', 'prioridad', 'categoria', 'equipo', 
            'equipo__id_unidad', 'creador', 'tecnico_asignado'
        ).all().order_by('-id')
        
        for t in tickets:
            writer.writerow([
                f"T-{t.id:04d}",
                t.asunto,
                t.estado.nombre if t.estado else '',
                t.prioridad.nombre if t.prioridad else '',
                t.categoria.nombre if t.categoria else '',
                t.equipo.id_articulo.nombre if t.equipo and t.equipo.id_articulo else 'Sin Equipo',
                t.equipo.serial_number if t.equipo else '',
                t.equipo.id_unidad.nombre if t.equipo and t.equipo.id_unidad else '',
                t.creador.get_full_name() or t.creador.username if t.creador else '',
                t.tecnico_asignado.get_full_name() or t.tecnico_asignado.username if t.tecnico_asignado else 'Sin Asignar',
                t.fecha_creacion.strftime('%Y-%m-%d %H:%M') if t.fecha_creacion else '',
                t.fecha_cierre.strftime('%Y-%m-%d %H:%M') if t.fecha_cierre else ''
            ])
            
        return response

    @classmethod
    def exportar_activos(cls):
        response = cls._crear_respuesta_csv('Inventario_Activos_Enterprise')
        writer = csv.writer(response, delimiter=';')
        
        writer.writerow([
            'ID', 'Número de Serie', 'Artículo', 'Marca', 'Modelo',
            'Estado', 'Unidad / Servicio', 'Ubicación Física',
            'IP', 'Sistema Operativo', 'Fecha de Compra'
        ])
        
        equipos = Equipo.objects.select_related(
            'id_articulo', 'id_marca', 'id_modelo', 'id_estado',
            'id_unidad', 'id_edificio', 'id_piso', 'id_so'
        ).all().order_by('id')
        
        for e in equipos:
            ubicacion = f"{e.id_edificio.nombre if e.id_edificio else ''} - {e.id_piso.nombre if e.id_piso else ''}".strip(' -')
            
            writer.writerow([
                e.id,
                e.serial_number,
                e.id_articulo.nombre if e.id_articulo else '',
                e.id_marca.nombre if e.id_marca else '',
                e.id_modelo.nombre if e.id_modelo else '',
                e.id_estado.nombre if e.id_estado else '',
                e.id_unidad.nombre if e.id_unidad else '',
                ubicacion,
                e.ip or '',
                e.id_so.nombre if e.id_so else '',
                e.fecha_compra.strftime('%Y-%m-%d') if e.fecha_compra else ''
            ])
            
        return response
