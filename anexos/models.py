"""
Modelos del módulo de Anexos Telefónicos IP.

Normalización aplicada (3NF):
- Anexo: ELIMINA los ~10 campos de "cambio de visor" (nombre_usuario_req, ubicacion_req,
  estado_req, grupo_captura, cascada, cambiar_dos_anexos, numero_anexo_cambio,
  sub_requerimiento, accion, observacion_req) que estaban incrustados en cada fila
  de `anexos` (anomalía 2NF: un anexo podía tener un requerimiento de cambio asociado,
  pero se modelaba como campos 1:1 en la misma tabla). Ahora esos campos van a una
  tabla separada RequerimientoCambio con relación 1:N (un anexo puede tener varios
  requerimientos de cambio a lo largo del tiempo).
- estado: enum('Activo','Inactivo') → choices + BooleanField `activo` (consistencia
  con el resto de catálogos que usan `activo`).
- modelo_anexo: FK a ModeloAnexo (catálogo separado de teléfonos, no a Modelo de
  equipos que es dominio distinto).
- edificio, piso, unidad: FKs reales (en PHP eran varchar sin FK ni siquiera index).
- establecimiento: FK a Institucion (en PHP era varchar).
- ip: GenericIPAddressField (en PHP era varchar(45)).
- foto: ImageField (en PHP era varchar con ruta).
- serial_number: unique.
- marca/modelo texto se conservan como campos libres además del FK a ModeloAnexo
  (los anexos Cisco tienen marca/modelo que no siempre matchea el catálogo).
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mantenedores.models import (
    ModeloAnexo, Edificio, Piso, Unidad, Institucion, Proveedor, PMA
)


class Anexo(models.Model):
    """Anexo telefónico IP. Reemplaza tabla `anexos` del esquema PHP."""
    class Estado(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        INACTIVO = 'Inactivo', 'Inactivo'

    numero_anexo = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name="Número de Anexo"
    )
    marca = models.CharField(
        max_length=50,
        verbose_name="Marca (texto)"
    )
    modelo = models.CharField(
        max_length=50,
        verbose_name="Modelo (texto)"
    )
    modelo_anexo = models.ForeignKey(
        ModeloAnexo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Modelo (catálogo)"
    )
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Edificio"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Piso"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Unidad / Servicio"
    )
    pma = models.ForeignKey(
        PMA,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="PMA (Punto de Montaje)"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Proveedor"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        db_index=True,
        verbose_name="Estado"
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="Número de Serie"
    )
    numero_inventario = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="N° Inventario"
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP"
    )
    comentario = models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentario"
    )
    foto = models.ImageField(
        upload_to='anexos/',
        null=True,
        blank=True,
        verbose_name="Foto"
    )
    grupo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Grupo"
    )
    establecimiento = models.ForeignKey(
        Institucion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='anexos',
        verbose_name="Establecimiento"
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anexos_creados',
        verbose_name="Creado por"
    )
    actualizado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anexos_actualizados',
        verbose_name="Actualizado por"
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )

    class Meta:
        verbose_name = "Anexo"
        verbose_name_plural = "Anexos"
        ordering = ['numero_anexo']
        indexes = [
            models.Index(fields=['numero_anexo'], name='idx_anexo_numero'),
            models.Index(fields=['estado'], name='idx_anexo_estado'),
            models.Index(fields=['edificio'], name='idx_anexo_edificio'),
        ]

    def clean(self):
        super().clean()
        if self.serial_number:
            self.serial_number = self.serial_number.strip()

    def __str__(self):
        return f"Anexo {self.numero_anexo} - {self.marca} {self.modelo}"


class RequerimientoCambio(models.Model):
    """Requerimiento de cambio de visor para un anexo.
    Normaliza 2NF: extrae los ~10 campos de "cambio de visor" que estaban incrustados
    en cada fila de `anexos` (nombre_usuario_req, ubicacion_req, estado_req,
    grupo_captura, cascada, cambiar_dos_anexos, numero_anexo_cambio, sub_requerimiento,
    accion, observacion_req) a una tabla 1:N separada.
    Un anexo puede tener varios requerimientos de cambio a lo largo del tiempo.
    """
    anexo = models.ForeignKey(
        Anexo,
        on_delete=models.CASCADE,
        related_name='requerimientos',
        verbose_name="Anexo"
    )
    tipo = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Tipo"
    )
    sub_requerimiento = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Sub Requerimiento"
    )
    accion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Acción"
    )
    nombre_usuario_req = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Nombre Usuario Requerimiento"
    )
    ubicacion_req = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Ubicación Requerimiento"
    )
    estado_req = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Estado Requerimiento"
    )
    grupo_captura = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Grupo Captura"
    )
    cambiar_dos_anexos = models.BooleanField(
        default=False,
        verbose_name="Cambiar dos anexos"
    )
    numero_anexo_cambio = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Número de anexo a cambiar"
    )
    cascada = models.BooleanField(
        default=False,
        verbose_name="Cascada"
    )
    observacion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observación"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha del requerimiento"
    )

    class Meta:
        verbose_name = "Requerimiento de Cambio"
        verbose_name_plural = "Requerimientos de Cambio"
        ordering = ['-fecha']

    def __str__(self):
        return f"Req cambio anexo {self.anexo.numero_anexo} - {self.accion or self.tipo or 'N/A'}"
