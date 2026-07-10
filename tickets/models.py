"""
Modelos del módulo de Tickets de Terreno (despacho a terreno / Mesa de Ayuda).

Normalización aplicada (3NF):
- Ticket: consolida `tb_tickets_terreno` + `tickets` (legacy duplicada).
  FKs reales (en PHP ya tenía constraints a tbedificios, tbunidades, tblistaequipos,
  tbusuarios). estado enum → choices. Añade FK a Prioridad y Categoria.
- TicketBitacora: de tb_itsm_bitacora (esbozo vacío). Notas públicas/internas/sistema.
- Prioridad: de tb_itsm_prioridades (4 niveles con SLA).
- Categoria: de tb_itsm_categorias (4 categorías).
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mantenedores.models import Edificio, Piso, Unidad
from equipos.models import Equipo


class Prioridad(models.Model):
    """Nivel de prioridad de un ticket. Reemplaza tb_itsm_prioridades."""
    nivel = models.CharField(
        max_length=100,
        verbose_name="Nivel"
    )
    sla_respuesta_minutos = models.IntegerField(
        verbose_name="SLA respuesta (minutos)",
        help_text="Tiempo esperado para tomar el caso"
    )
    sla_resolucion_horas = models.IntegerField(
        verbose_name="SLA resolución (horas)",
        help_text="Tiempo esperado para solucionar"
    )
    color_hex = models.CharField(
        max_length=20,
        default='#333333',
        verbose_name="Color (hex)"
    )

    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"
        ordering = ['id']

    def __str__(self):
        return self.nivel


class Categoria(models.Model):
    """Categoría de un ticket. Reemplaza tb_itsm_categorias."""
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Ticket(models.Model):
    """Ticket de terreno / despacho. Reemplaza tb_tickets_terreno + consolida `tickets` legacy."""
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_TERRENO = 'EN_TERRENO', 'En Terreno'
        RESUELTO = 'RESUELTO', 'Resuelto'

    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha y Hora"
    )
    solicitante_nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre del Solicitante"
    )
    solicitante_rut = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="RUT del Solicitante"
    )
    solicitante_correo = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Correo del Solicitante"
    )
    solicitante_anexo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Anexo del Solicitante"
    )
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name="Edificio"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Piso"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name="Unidad"
    )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name="Equipo"
    )
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    tecnico = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_asignados',
        verbose_name="Técnico asignado"
    )
    grupo_asignado = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Grupo asignado"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
        verbose_name="Estado"
    )
    prioridad = models.ForeignKey(
        Prioridad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name="Prioridad"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets',
        verbose_name="Categoría"
    )
    fecha_cierre = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Cierre"
    )
    fecha_toma = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Toma",
        help_text="El segundo exacto en que el técnico asume"
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['estado'], name='idx_ticket_estado'),
            models.Index(fields=['tecnico'], name='idx_ticket_tecnico'),
            models.Index(fields=['prioridad'], name='idx_ticket_prioridad'),
        ]

    def clean(self):
        super().clean()
        if self.fecha_cierre and self.fecha_hora and self.fecha_cierre < self.fecha_hora:
            raise ValidationError({'fecha_cierre': 'La fecha de cierre no puede ser anterior a la creación del ticket.'})
        if self.fecha_toma and self.fecha_hora and self.fecha_toma < self.fecha_hora:
            raise ValidationError({'fecha_toma': 'La fecha de toma no puede ser anterior a la creación del ticket.'})

    def __str__(self):
        return f"Ticket #{self.pk} - {self.solicitante_nombre} ({self.estado})"


class TicketBitacora(models.Model):
    """Nota/comentario de un ticket. Reemplaza tb_itsm_bitacora (esbozo vacío)."""
    class TipoNota(models.TextChoices):
        PUBLICA = 'PUBLICA', 'Pública'
        INTERNA = 'INTERNA', 'Interna'
        SISTEMA = 'SISTEMA', 'Sistema'

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='notas',
        verbose_name="Ticket"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notas_tickets',
        verbose_name="Usuario"
    )
    nota = models.TextField(
        verbose_name="Nota"
    )
    tipo_nota = models.CharField(
        max_length=20,
        choices=TipoNota.choices,
        default=TipoNota.INTERNA,
        verbose_name="Tipo de nota"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Nota de Ticket"
        verbose_name_plural = "Notas de Tickets"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.ticket} - {self.tipo_nota} - {self.fecha_registro}"
