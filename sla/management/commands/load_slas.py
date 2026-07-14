from django.core.management.base import BaseCommand
from tickets.models import Prioridad, Ticket
from sla.models import SLAMatrix

class Command(BaseCommand):
    help = 'Carga las prioridades y la matriz de SLA por defecto'

    def handle(self, *args, **kwargs):
        # 1. Crear Prioridades Base (ITIL)
        prio_critica, _ = Prioridad.objects.get_or_create(
            nombre="Crítica", defaults={"sla_horas": 4, "color_hex": "#ef4444"}
        )
        prio_alta, _ = Prioridad.objects.get_or_create(
            nombre="Alta", defaults={"sla_horas": 8, "color_hex": "#f97316"}
        )
        prio_media, _ = Prioridad.objects.get_or_create(
            nombre="Media", defaults={"sla_horas": 24, "color_hex": "#eab308"}
        )
        prio_baja, _ = Prioridad.objects.get_or_create(
            nombre="Baja", defaults={"sla_horas": 72, "color_hex": "#3b82f6"}
        )

        # 2. Construir Matriz SLA (Impacto x Urgencia)
        # Impacto: 1(HOSPITAL), 2(SERVICIO), 3(PACIENTE), 4(BAJO)
        # Urgencia: 1(ALTA), 2(MEDIA), 3(BAJA)
        
        matrices = [
            # Alta Urgencia
            (1, 1, prio_critica, 2, 4),    # Hosp + Alta
            (2, 1, prio_critica, 2, 4),    # Serv + Alta
            (3, 1, prio_alta, 4, 8),       # Paci + Alta
            (4, 1, prio_media, 8, 24),     # Bajo + Alta

            # Media Urgencia
            (1, 2, prio_alta, 4, 8),       # Hosp + Media
            (2, 2, prio_alta, 4, 8),       # Serv + Media
            (3, 2, prio_media, 8, 24),     # Paci + Media
            (4, 2, prio_baja, 12, 72),     # Bajo + Media

            # Baja Urgencia
            (1, 3, prio_media, 8, 24),     # Hosp + Baja
            (2, 3, prio_media, 8, 24),     # Serv + Baja
            (3, 3, prio_baja, 12, 72),     # Paci + Baja
            (4, 3, prio_baja, 12, 72),     # Bajo + Baja
        ]

        for imp, urg, prio, t_resp, t_res in matrices:
            SLAMatrix.objects.update_or_create(
                impacto=imp, urgencia=urg,
                defaults={
                    'prioridad': prio,
                    'tiempo_respuesta_minutos': t_resp * 60, # guardamos en mins
                    'tiempo_resolucion_horas': t_res
                }
            )

        self.stdout.write(self.style.SUCCESS('¡Matriz SLA y Prioridades inicializadas correctamente!'))
