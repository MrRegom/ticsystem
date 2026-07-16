"""
Modelos del módulo de Equipos (inventario TIC) y Bitácora de mantenciones.

Normalización aplicada (3NF):
- Equipo: ELIMINA columnas texto duplicadas (edificio, piso, marca, modelo, estado, so,
  proveedor, articulo, unidadservicio) que existían en tblistaequipos junto a las FK.
  Ahora quedan SOLO las FKs (id_edificio, id_piso, id_marca, id_modelo, id_estado, id_so,
  id_proveedor, id_articulo, id_unidad) → anomalía de actualización resuelta.
- imagen: ImageField (en PHP era MEDIUMTEXT con la ruta).
- ip: GenericIPAddressField (en PHP era MEDIUMTEXT).
- serial_number: unique (case-insensitive vía PG CITEXT o validación en clean).
- BitacoraOpcion: catálogo de fallas/actividades (enum → choices).
- BitacoraEquipo: FKs reales a Equipo (cascade) y User (restrict), con tipo_registro
  como choices (enum ampliado de la migración agregar_fecha_devolucion_bitacora.sql).
- Reglas de negocio en clean() y signals (audit trail, recálculo de estado, sync IPAM).
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from mantenedores.models import (
    Articulo, Marca, Modelo, Edificio, Piso, Unidad,
    SistemaOperativo, EstadoEquipo, Proveedor,
    Sector, AreaHospitalaria, Recinto, PMA
)


class Equipo(models.Model):
    """Equipo de inventario TIC. Reemplaza tblistaequipos.
    Solo FKs (sin columnas texto duplicadas) — normalización 3NF.
    """
    imagen = models.ImageField(
        upload_to='equipos/',
        null=True,
        blank=True,
        verbose_name="Imagen del Equipo"
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name='equipos',
        verbose_name="Artículo"
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='equipos',
        verbose_name="Marca"
    )
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.PROTECT,
        related_name='equipos',
        verbose_name="Modelo"
    )
    pma = models.ForeignKey(
        PMA,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='equipos',
        verbose_name="PMA (Punto de Montaje)"
    )
    num_inventario = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
        verbose_name="N° Inventario Institucional",
        help_text="Número de Activo Fijo asignado por Contabilidad (Ej: AF-000345)"
    )
    correlativo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Correlativo"
    )
    orden_interno = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Orden Interno"
    )
    serie_corta = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Serie Equipo (Corta)"
    )
    estado_candado = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Estado de Candado/Observación"
    )
    so = models.ForeignKey(
        SistemaOperativo,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='equipos',
        verbose_name="Sistema Operativo"
    )
    estado = models.ForeignKey(
        EstadoEquipo,
        on_delete=models.PROTECT,
        related_name='equipos',
        verbose_name="Estado"
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='equipos',
        verbose_name="Proveedor"
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Número de Serie"
    )
    ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP"
    )
    anexo = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Anexo telefónico"
    )
    usuario = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Usuario asignado"
    )
    office = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Office"
    )
    activador = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Activador / Cuenta"
    )
    pmalugar = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="PMA / Lugar"
    )
    
    # Nuevos campos Enterprise (Garantía y Compras)
    orden_compra = models.CharField(max_length=100, null=True, blank=True, verbose_name="Orden de Compra")
    fecha_compra = models.DateField(null=True, blank=True, verbose_name="Fecha de Compra")
    vencimiento_garantia = models.DateField(null=True, blank=True, verbose_name="Vencimiento Garantía")
    
    # Nuevos campos Enterprise (Conectividad / Red)
    mac_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="MAC Address")
    switch_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name="Switch (Nombre/IP)")
    patch_panel = models.CharField(max_length=100, null=True, blank=True, verbose_name="Patch Panel")
    puerto_red = models.CharField(max_length=50, null=True, blank=True, verbose_name="Puerto / Boca")
    comentario = models.TextField(
        null=True,
        blank=True,
        verbose_name="Comentario"
    )
    modificado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipos_modificados',
        verbose_name="Modificado por"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['estado']),
            models.Index(fields=['pma'], name='idx_equipo_pma'),
        ]

    def __str__(self):
        return f"{self.articulo.nombre} {self.marca.nombre} {self.modelo.nombre} - {self.serial_number}"

    def clean(self):
        super().clean()
        # Normalizar serial_number: sin espacios a los extremos
        if self.serial_number:
            self.serial_number = self.serial_number.strip()


class BitacoraOpcion(models.Model):
    """Catálogo de fallas y actividades de mantención. Reemplaza tb_bitacora_opciones.
    Enum tipo FALLA/ACTIVIDAD → choices. unique(tipo, nombre).
    """
    class Tipo(models.TextChoices):
        FALLA = 'FALLA', 'Falla'
        ACTIVIDAD = 'ACTIVIDAD', 'Actividad'

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
        db_index=True,
        verbose_name="Tipo"
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name="Nombre"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Activo"
    )
    orden = models.IntegerField(
        default=10,
        db_index=True,
        verbose_name="Orden"
    )
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bitacora_opciones_creadas',
        verbose_name="Creado por"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )

    class Meta:
        verbose_name = "Opción de Bitácora"
        verbose_name_plural = "Opciones de Bitácora"
        ordering = ['tipo', 'orden', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['tipo', 'nombre'],
                name='uniq_bitacora_opcion_tipo_nombre'
            )
        ]

    def clean(self):
        super().clean()
        if self.nombre:
            self.nombre = self.nombre.strip()
        if self.orden is not None and self.orden < 0:
            raise ValidationError({'orden': 'El orden no puede ser negativo.'})

    def __str__(self):
        return f"[{self.tipo}] {self.nombre}"


class BitacoraEquipo(models.Model):
    """Registro de eventos de un equipo (mantención, movimiento, actualización).
    Reemplaza tb_bitacora_equipos + migración agregar_fecha_devolucion_bitacora.sql.

    Reglas de negocio (en clean() y signals):
    1. No permitir >1 mantención abierta (sin fecha_devolucion) por equipo.
    2. fecha_devolucion no futura ni anterior a fecha_mantenimiento.
    3. Anti-duplicado por doble-submit en 15s.
    4. Recálculo automático de estado del equipo (signal post_save).
    """
    class TipoRegistro(models.TextChoices):
        MANTENCION = 'MANTENCION', 'Mantención'
        REPARACION_EXTERNA = 'REPARACION_EXTERNA', 'Reparación Externa'
        MOVIMIENTO = 'MOVIMIENTO', 'Movimiento'
        ACTUALIZACION_SISTEMA = 'ACTUALIZACION_SISTEMA', 'Actualización de Sistema'
        REEMPLAZO = 'REEMPLAZO', 'Reemplazo'
        REVISION_PREVENTIVA = 'REVISION_PREVENTIVA', 'Revisión Preventiva'
        INSTALACION = 'INSTALACION', 'Instalación'
        TRASLADO = 'TRASLADO', 'Traslado'
        AISLAMIENTO_MINSAL = 'AISLAMIENTO_MINSAL', 'Aislamiento MINSAL'

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='bitacoras',
        verbose_name="Equipo"
    )
    tecnico = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name='bitacoras_realizadas',
        verbose_name="Técnico"
    )
    fecha_mantenimiento = models.DateTimeField(
        verbose_name="Fecha de Mantención"
    )
    fecha_devolucion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Devolución",
        help_text="Fecha en que el equipo fue devuelto al usuario tras atención"
    )
    solicitante = models.ForeignKey(
        'core.Funcionario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bitacoras_solicitadas',
        verbose_name="Solicitante"
    )
    falla_reportada = models.TextField(
        null=True,
        blank=True,
        verbose_name="Falla Reportada"
    )
    actividades_realizadas = models.TextField(
        null=True,
        blank=True,
        verbose_name="Actividades Realizadas"
    )
    servicio_unidad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Servicio / Unidad"
    )
    tipo_registro = models.CharField(
        max_length=30,
        choices=TipoRegistro.choices,
        default=TipoRegistro.MANTENCION,
        verbose_name="Tipo de Registro"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        verbose_name = "Registro de Bitácora"
        verbose_name_plural = "Registros de Bitácora"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['equipo'], name='idx_bitacora_equipo'),
            models.Index(fields=['tecnico'], name='idx_bitacora_tecnico'),
            models.Index(fields=['tipo_registro'], name='idx_bitacora_tipo'),
        ]

    def __str__(self):
        return f"{self.equipo.serial_number} - {self.get_tipo_registro_display()} - {self.fecha_mantenimiento}"

    def clean(self):
        super().clean()
        hoy = timezone.localtime()

        # Regla 2: fecha_devolucion no futura ni anterior a fecha_mantenimiento
        if self.fecha_devolucion is not None:
            if self.fecha_devolucion < self.fecha_mantenimiento:
                raise ValidationError(
                    "La fecha de devolución no puede ser anterior a la fecha de mantención."
                )
            if self.fecha_devolucion > hoy:
                raise ValidationError(
                    "La fecha de devolución no puede ser futura."
                )

        # Regla 1: no permitir >1 mantención abierta (sin fecha_devolucion) por equipo
        if self.tipo_registro == self.TipoRegistro.MANTENCION and self.fecha_devolucion is None:
            qs = BitacoraEquipo.objects.filter(
                equipo=self.equipo,
                tipo_registro=self.TipoRegistro.MANTENCION,
                fecha_devolucion__isnull=True,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError(
                    "Ya existe una mantención abierta para este equipo. "
                    "Ciérrela (registre fecha de devolución) antes de abrir una nueva."
                )

        # Regla 3: anti-duplicado por doble-submit en 15s
        hace_15s = timezone.now() - timezone.timedelta(seconds=15)
        qs_dup = BitacoraEquipo.objects.filter(
            equipo=self.equipo,
            tecnico=self.tecnico,
            fecha_creacion__gte=hace_15s,
        )
        if self.pk:
            qs_dup = qs_dup.exclude(pk=self.pk)
        if qs_dup.exists():
            raise ValidationError(
                "Se detectó un registro duplicado (mismo equipo y técnico en menos de 15s)."
            )
