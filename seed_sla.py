import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticsystem.settings')
django.setup()

from tickets.models import Prioridad, Ticket
from sla.models import SLAMatrix

# 1. Crear Prioridades Base si no existen
p_critica, _ = Prioridad.objects.get_or_create(nombre="Crítica", defaults={"sla_horas": 4, "color_hex": "#e11d48"})
p_alta, _ = Prioridad.objects.get_or_create(nombre="Alta", defaults={"sla_horas": 8, "color_hex": "#ea580c"})
p_media, _ = Prioridad.objects.get_or_create(nombre="Media", defaults={"sla_horas": 24, "color_hex": "#eab308"})
p_baja, _ = Prioridad.objects.get_or_create(nombre="Baja", defaults={"sla_horas": 72, "color_hex": "#3b82f6"})

print("Prioridades listas.")

# 2. Poblacion de la matriz (Basado en mejores prácticas ITIL)
# Impactos: 4 (Hosp), 3 (Area), 2 (User), 1 (Bajo)
# Urgencias: 4 (Alta), 3 (Media), 2 (Baja)

configuracion = [
    # Impacto Hospital (4)
    (4, 4, p_critica, 15, 2), # Alta urgencia
    (4, 3, p_critica, 30, 4), # Media urgencia
    (4, 2, p_alta, 60, 8),    # Baja urgencia
    
    # Impacto Servicio/Area (3)
    (3, 4, p_critica, 30, 4),
    (3, 3, p_alta, 60, 8),
    (3, 2, p_media, 120, 24),
    
    # Impacto Usuario (2)
    (2, 4, p_alta, 60, 8),
    (2, 3, p_media, 120, 24),
    (2, 2, p_baja, 240, 48),
    
    # Impacto Bajo (1)
    (1, 4, p_media, 120, 24),
    (1, 3, p_baja, 240, 48),
    (1, 2, p_baja, 480, 72)
]

for imp, urg, prio, t_resp, t_res in configuracion:
    obj, created = SLAMatrix.objects.update_or_create(
        impacto=imp,
        urgencia=urg,
        defaults={
            'prioridad': prio,
            'tiempo_respuesta_minutos': t_resp,
            'tiempo_resolucion_horas': t_res
        }
    )
    
print("Matriz SLA pre-configurada con éxito.")
