from .repositories import ReportesRepository

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
