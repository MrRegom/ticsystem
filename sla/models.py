"""
Modelos de SLA (Service Level Agreement).
Define los tiempos de resolución basados en matrices de prioridades.
"""
from django.db import models
from tickets.models import Prioridad, Ticket

class SLAMatrix(models.Model):
    """
    Matriz de SLA que cruza Impacto y Urgencia para derivar Prioridad y Tiempos.
    """
    impacto = models.IntegerField(choices=Ticket.Impacto.choices, verbose_name="Impacto")
    urgencia = models.IntegerField(choices=Ticket.Urgencia.choices, verbose_name="Urgencia")
    prioridad = models.ForeignKey(Prioridad, on_delete=models.PROTECT, verbose_name="Prioridad Resultante")
    
    tiempo_respuesta_minutos = models.IntegerField(default=15, verbose_name="SLA Primera Respuesta (min)")
    tiempo_resolucion_horas = models.IntegerField(default=24, verbose_name="SLA Resolución (horas)")

    class Meta:
        verbose_name = "Matriz SLA"
        verbose_name_plural = "Matrices SLA"
        unique_together = ('impacto', 'urgencia')

    def __str__(self):
        return f"{self.get_impacto_display()} + {self.get_urgencia_display()} -> {self.prioridad.nombre}"
