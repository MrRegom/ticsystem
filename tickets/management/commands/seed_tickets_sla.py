"""
Semilla de catálogos de tickets (prioridades y categorías) + SLA de mantenciones.

Fuente: equipamiento/basedatos2/equipamiento2026.sql (tb_itsm_prioridades,
tb_itsm_categorias, tb_sla_configuracion).

Uso:
    python manage.py seed_tickets_sla
"""
from django.core.management.base import BaseCommand
from tickets.models import Prioridad, Categoria
from redes.models import SlaConfiguracion


class Command(BaseCommand):
    help = 'Crea prioridades, categorías de tickets y configuración SLA.'

    def handle(self, *args, **options):
        # --- Prioridades (de tb_itsm_prioridades) ---
        prioridades = [
            ('CRÍTICA (Pabellón/Urgencia/Vidas)', 15, 2, '#dc3545'),
            ('ALTA (Fallo de servicio importante)', 30, 8, '#fd7e14'),
            ('MEDIA (Un funcionario bloqueado)', 60, 24, '#ffc107'),
            ('BAJA (Requerimiento/Consulta)', 120, 72, '#17a2b8'),
        ]
        for nivel, sla_resp, sla_res, color in prioridades:
            _, c = Prioridad.objects.get_or_create(
                nivel=nivel,
                defaults={
                    'sla_respuesta_minutos': sla_resp,
                    'sla_resolucion_horas': sla_res,
                    'color_hex': color,
                }
            )
            self._log('Prioridad', nivel, c)

        # --- Categorías (de tb_itsm_categorias) ---
        categorias = [
            'Hardware (Equipos, Pantallas, Piezas)',
            'Software y Plataformas Clínicas',
            'Redes e Infraestructura',
            'Impresión y Escáneres',
        ]
        for nombre in categorias:
            _, c = Categoria.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            self._log('Categoría', nombre, c)

        # --- SLA (de tb_sla_configuracion) ---
        _, c = SlaConfiguracion.objects.get_or_create(
            nombre='Meta Operativa Mantencion',
            defaults={'horas_objetivo': 72, 'alerta_porcentaje': 80, 'activo': True}
        )
        self._log('SLA', 'Meta Operativa Mantencion', c)

        self.stdout.write(self.style.SUCCESS('\nSemilla tickets+SLA completada.'))

    def _log(self, entidad, nombre, created):
        if created:
            self.stdout.write(self.style.SUCCESS(f'+ {entidad}: {nombre}'))
        else:
            self.stdout.write(f'  {entidad} omitido (ya existe): {nombre}')
