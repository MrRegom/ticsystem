"""
Modelos del módulo de Redes / IPAM (gestión de infraestructura de red).

Normalización aplicada (3NF):
- Pma: ELIMINA id_edificio e id_piso redundantes (dependencia transitiva) que
  duplicaban la info ya contenida en id_edificio_piso. Ahora solo FK a Piso
  (que ya contiene edificio+piso). En PHP tb_pma tenía los 3 campos.
- InfraestructuraRed: AÑADE FK real a pma (en PHP era solo índice sin constraint).
  AÑADE FK a Vlan. ip_direccion unique. estado como choices.
- RangoIP: COLAPSA 12 tablas (tbconexionespiso1..7, Menos1, zocalo, tbconexiones1/2/3)
  en un solo modelo con FK a Piso. El valor del piso (antes en el NOMBRE de la
  tabla) ahora es un campo. Anomalía 1NF resuelta.
- SlaConfiguracion: config de SLA de mantenciones.
"""
from django.db import models
from django.core.exceptions import ValidationError

from mantenedores.models import Piso, Unidad, Edificio, Institucion, Vlan


class Pma(models.Model):
    """Punto de Ingeniería Real (rack de red). Reemplaza tb_pma.
    Elimina id_edificio + id_piso redundantes (ya están en edificio_piso → Piso).
    """
    codigo = models.CharField(
        max_length=50,
        verbose_name="Código PMA"
    )
    edificio_piso = models.ForeignKey(
        Piso,
        on_delete=models.PROTECT,
        related_name='pmas',
        verbose_name="Edificio / Piso"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pmas',
        verbose_name="Unidad"
    )
    estado = models.CharField(
        max_length=20,
        default='Activo',
        verbose_name="Estado"
    )
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name="Descripción"
    )

    class Meta:
        verbose_name = "PMA"
        verbose_name_plural = "PMAs"
        ordering = ['codigo', 'edificio_piso']
        constraints = [
            models.UniqueConstraint(
                fields=['codigo', 'edificio_piso'],
                name='uniq_pma_codigo_piso'
            )
        ]

    def __str__(self):
        return f"{self.codigo} ({self.edificio_piso})"


class InfraestructuraRed(models.Model):
    """IP de red (IPAM). Reemplaza tb_infraestructura_red.
    Añade FK real a pma (en PHP era solo índice). Añade FK a Vlan.
    """
    class Estado(models.TextChoices):
        LIBRE = 'LIBRE', 'Libre'
        OCUPADO = 'OCUPADO', 'Ocupado'
        FALLA = 'FALLA', 'Falla'

    ip_direccion = models.GenericIPAddressField(
        unique=True,
        db_index=True,
        verbose_name="Dirección IP"
    )
    pma = models.ForeignKey(
        Pma,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips',
        verbose_name="PMA"
    )
    vlan = models.ForeignKey(
        Vlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips',
        verbose_name="VLAN"
    )
    switch_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP del Switch"
    )
    switch_port = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Puerto del Switch"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.LIBRE,
        db_index=True,
        verbose_name="Estado"
    )
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='ips_red',
        verbose_name="Institución"
    )
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips_red',
        verbose_name="Edificio"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips_red',
        verbose_name="Piso"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ips_red',
        verbose_name="Unidad"
    )
    sector = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Sector"
    )
    mac = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="MAC"
    )
    rack = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Rack"
    )
    patch_panel = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Patch Panel"
    )

    class Meta:
        verbose_name = "IP de Red"
        verbose_name_plural = "IPs de Red (IPAM)"
        ordering = ['ip_direccion']
        indexes = [
            models.Index(fields=['estado'], name='idx_ipred_estado'),
            models.Index(fields=['pma'], name='idx_ipred_pma'),
        ]

    def clean(self):
        super().clean()
        if self.mac:
            self.mac = self.mac.strip().upper()
        if self.switch_port:
            self.switch_port = self.switch_port.strip()

    def __str__(self):
        return f"{self.ip_direccion} ({self.estado})"


class RangoIP(models.Model):
    """Rango de IP por piso. COLAPSA 12 tablas del esquema PHP:
    tbconexionespiso1, tbconexionespiso2, ..., tbconexionespiso7,
    tbconexionespisoMenos1, tbconexioneszocalo, tbconexiones1, tbconexiones2, tbconexiones3.

    Anomalía 1NF resuelta: el valor del piso estaba en el NOMBRE de la tabla
    (una tabla por piso). Ahora es un campo `piso` (FK) en una sola tabla.

    Campos de tbconexionespiso*: unidad, ubicacion, pma, rack, dato, rango, ip, estado(int), comentario.
    Campos de tbconexiones1/2/3: nombre, vlan, red, mascara, gateway, pass, visibilidad, tipo.
    (las 1/2/3 son VLANs/SSIDs, no rangos por piso — se mapean a Vlan o un modelo aparte).
    Aquí modelamos solo las tbconexionespiso* (rangos por piso). Las tbconexiones1/2/3
    son SSIDs WiFi / VLANes y van al modelo Vlan.
    """
    piso = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        related_name='rangos_ip',
        verbose_name="Piso"
    )
    unidad = models.CharField(
        max_length=200,
        verbose_name="Unidad"
    )
    ubicacion = models.CharField(
        max_length=200,
        verbose_name="Ubicación"
    )
    pma = models.CharField(
        max_length=100,
        verbose_name="PMA"
    )
    rack = models.CharField(
        max_length=100,
        verbose_name="Rack"
    )
    dato = models.CharField(
        max_length=100,
        verbose_name="Dato (último octeto)"
    )
    rango = models.CharField(
        max_length=50,
        verbose_name="Rango (3 primeros octetos)"
    )
    ip = models.GenericIPAddressField(
        verbose_name="IP completa"
    )
    estado = models.BooleanField(
        default=False,
        verbose_name="Estado (ocupado)"
    )
    comentario = models.TextField(
        default='',
        verbose_name="Comentario"
    )

    class Meta:
        verbose_name = "Rango de IP"
        verbose_name_plural = "Rangos de IP por Piso"
        ordering = ['piso', 'rango', 'ip']
        indexes = [
            models.Index(fields=['piso'], name='idx_rangoip_piso'),
            models.Index(fields=['ip'], name='idx_rangoip_ip'),
        ]

    def __str__(self):
        return f"{self.piso} - {self.ip} ({self.unidad})"


class SlaConfiguracion(models.Model):
    """Configuración de SLA para mantenciones. Reemplaza tb_sla_configuracion."""
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre"
    )
    horas_objetivo = models.IntegerField(
        default=48,
        verbose_name="Horas objetivo"
    )
    alerta_porcentaje = models.IntegerField(
        default=80,
        verbose_name="% alerta"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Activo"
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
        verbose_name = "Configuración SLA"
        verbose_name_plural = "Configuraciones SLA"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.horas_objetivo}h, alerta {self.alerta_porcentaje}%)"
