"""
Modelos del módulo de Actas de Entrega de Equipamiento.

Normalización aplicada (3NF):
- Acta: consolida `actas` + `actas_entrega` (legacy utf32/spanish2, duplicada).
  Firmas y timbres: ImageField (archivos en media/) en vez de base64 longtext en BD
  (anomalía 0NF: binarios en BD). Añade FK real a encargado (User).
- ActaDetalle: AÑADE FK real a acta (en PHP actas_detalles no tenía FK, solo id_acta
  sin constraint). tipo_item choices. FKs a edificio/piso/unidad.
  id_item es int (polimórfico: apunta a Equipo o Anexo según tipo_item).
"""
import re
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mantenedores.models import Edificio, Piso, Unidad


class Acta(models.Model):
    """Acta de entrega de equipamiento. Reemplaza `actas` + consolida `actas_entrega`."""
    class Estado(models.TextChoices):
        BORRADOR = 'borrador', 'Borrador'
        EMITIDO = 'emitido', 'Emitido'
        ENVIADO = 'enviado', 'Enviado'

    codigo = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="Código del Acta"
    )
    receptor_nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Receptor"
    )
    receptor_rut = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="RUT del Receptor"
    )
    receptor_cargo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Cargo del Receptor"
    )
    receptor_unidad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Unidad del Receptor"
    )
    encargado = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='actas_emitidas',
        verbose_name="Encargado TIC"
    )
    observaciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha del Acta"
    )
    pdf_generado = models.FileField(
        upload_to='actas/pdf/',
        null=True,
        blank=True,
        verbose_name="PDF generado"
    )
    pdf_firmado = models.FileField(
        upload_to='actas/firmadas/',
        null=True,
        blank=True,
        verbose_name="PDF firmado"
    )
    firma_receptor = models.ImageField(
        upload_to='actas/firmas/',
        null=True,
        blank=True,
        verbose_name="Firma del Receptor"
    )
    firma_encargado = models.ImageField(
        upload_to='actas/firmas/',
        null=True,
        blank=True,
        verbose_name="Firma del Encargado"
    )
    timbre_encargado = models.ImageField(
        upload_to='actas/timbres/',
        null=True,
        blank=True,
        verbose_name="Timbre del Encargado"
    )
    email_receptor = models.EmailField(
        null=True,
        blank=True,
        verbose_name="Email del Receptor"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.EMITIDO,
        db_index=True,
        verbose_name="Estado"
    )
    fecha_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Envío"
    )

    class Meta:
        verbose_name = "Acta de Entrega"
        verbose_name_plural = "Actas de Entrega"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['estado'], name='idx_acta_estado'),
            models.Index(fields=['fecha'], name='idx_acta_fecha'),
        ]

    def clean(self):
        super().clean()
        if self.codigo:
            self.codigo = self.codigo.strip().upper()
            if not re.match(r'^[A-Z0-9\-/]+$', self.codigo):
                raise ValidationError({'codigo': 'El código solo puede contener letras mayúsculas, números, guiones y slash.'})
        if self.fecha_envio and self.fecha_envio < self.fecha:
            raise ValidationError({'fecha_envio': 'La fecha de envío no puede ser anterior a la fecha del acta.'})

    def __str__(self):
        return f"{self.codigo} - {self.receptor_nombre}"


class ActaDetalle(models.Model):
    """Detalle de ítems de un acta. Reemplaza `actas_detalles`.
    Añade FK real a acta (en PHP no había constraint).
    """
    class TipoItem(models.TextChoices):
        EQUIPO = 'EQUIPO', 'Equipo'
        ANEXO = 'ANEXO', 'Anexo'

    acta = models.ForeignKey(
        Acta,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name="Acta"
    )
    tipo_item = models.CharField(
        max_length=20,
        choices=TipoItem.choices,
        verbose_name="Tipo de Ítem"
    )
    id_item = models.PositiveIntegerField(
        verbose_name="ID del Ítem",
        help_text="ID del Equipo o Anexo según tipo_item"
    )
    articulo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Artículo"
    )
    serie = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Número de Serie"
    )
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actas_detalles',
        verbose_name="Edificio"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actas_detalles',
        verbose_name="Piso"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actas_detalles',
        verbose_name="Unidad"
    )
    pma_lugar = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="PMA / Lugar"
    )
    estado = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Estado del ítem"
    )

    class Meta:
        verbose_name = "Detalle de Acta"
        verbose_name_plural = "Detalles de Acta"
        ordering = ['id']
        indexes = [
            models.Index(fields=['tipo_item', 'id_item'], name='idx_actadetalle_tipo_item'),
        ]

    def __str__(self):
        return f"{self.acta.codigo} - {self.tipo_item} #{self.id_item} ({self.articulo or ''})"
