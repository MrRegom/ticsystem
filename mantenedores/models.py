"""
Modelos de catálogos / mantenedores del sistema TIC.

Normalización aplicada (3NF):
- Unificación de collation (PostgreSQL utf8).
- Eliminación de MEDIUMTEXT: uso de CharField con longitudes apropiadas.
- FKs reales con on_delete explícito (la BD PHP no tenía constraints en id_edificio de tbpisos, etc.).
- unique constraints donde correspondía (marca, so, estado, artículo, modelo por marca).
- Campos de auditoría unificados: fecha_creacion / fecha_actualizacion.
- Estado como BooleanField `activo` (consistencia, en vez de mezclar int 0/1, enum, varchar).
- Piso consolide tb_edificio_pisos (que tenía filas duplicadas y alias sueltos).
"""
import re
from django.db import models
from django.core.exceptions import ValidationError


class TimestampedActivo(models.Model):
    """Base abstracta con campos de auditoría y activo comunes a todos los catálogos."""
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
        abstract = True


class Institucion(TimestampedActivo):
    """Institución / sede hospitalaria (ej. HGF). Reemplaza tb_instituciones."""
    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código"
    )
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre"
    )

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Edificio(TimestampedActivo):
    """Edificio físico dentro de una institución. Reemplaza tbedificios.
    Añade FK a Institucion (la tabla PHP no la tenía, pero tb_infraestructura_red sí).
    """
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre del Edificio"
    )
    institucion = models.ForeignKey(
        Institucion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='edificios',
        verbose_name="Institución"
    )

    class Meta:
        verbose_name = "Edificio"
        verbose_name_plural = "Edificios"
        ordering = ['nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['nombre', 'institucion'],
                name='uniq_edificio_nombre_institucion'
            )
        ]

    def __str__(self):
        return self.nombre


class Piso(TimestampedActivo):
    """Piso físico dentro de un edificio. Reemplaza tbpisos + tb_edificio_pisos.
    Colapsa la dualidad: tbpisos tenía (pisos, id_edificio) y tb_edificio_pisos
    tenía (id_edificio, id_piso, alias_piso) con filas duplicadas.
    Aquí: un solo modelo con FK a Edificio, alias opcional, unique(edificio, nombre).
    """
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre del Piso"
    )
    alias = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Alias del Piso"
    )
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.CASCADE,
        related_name='pisos',
        verbose_name="Edificio"
    )

    class Meta:
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"
        ordering = ['edificio__nombre', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['edificio', 'nombre'],
                name='uniq_piso_edificio_nombre'
            )
        ]

    def __str__(self):
        return f"{self.edificio.nombre} - Piso {self.nombre}"


class Sector(TimestampedActivo):
    """Sector geográfico o de ala (ej. NORTE, SUR, A, AU, EP)."""
    nombre = models.CharField(
        max_length=50,
        verbose_name="Nombre del Sector"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='sectores',
        verbose_name="Piso"
    )

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class AreaHospitalaria(TimestampedActivo):
    """Área Hospitalaria (ej. APOYO CLINICO ATENCION DIRECTA)."""
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Área"
    )

    class Meta:
        verbose_name = "Área Hospitalaria"
        verbose_name_plural = "Áreas Hospitalarias"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Unidad(TimestampedActivo):
    """Unidad / Servicio hospitalario. Reemplaza tbunidades."""
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre de la Unidad"
    )
    area_hospitalaria = models.ForeignKey(
        AreaHospitalaria,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='unidades',
        verbose_name="Área Hospitalaria"
    )

    class Meta:
        verbose_name = "Unidad / Servicio"
        verbose_name_plural = "Unidades / Servicios"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Recinto(TimestampedActivo):
    """Recinto o sala específica (ej. Sala Informes, Oficina Modular)."""
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del Recinto"
    )
    piso = models.ForeignKey(
        Piso,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='recintos',
        verbose_name="Piso"
    )
    sector = models.ForeignKey(
        Sector,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='recintos',
        verbose_name="Sector"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='recintos',
        verbose_name="Unidad / Servicio"
    )

    class Meta:
        verbose_name = "Recinto"
        verbose_name_plural = "Recintos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class PMA(TimestampedActivo):
    """Punto de Montaje/Acceso (PMA) físico (ej. J-1-24)."""
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código PMA"
    )
    recinto = models.ForeignKey(
        Recinto,
        on_delete=models.CASCADE,
        related_name='pmas',
        verbose_name="Recinto"
    )

    class Meta:
        verbose_name = "PMA"
        verbose_name_plural = "PMAs"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre



class Articulo(TimestampedActivo):
    """Tipo de artículo / categoría de equipo. Reemplaza tbarticulos.
    Ej: Notebook, All in One, Impresora, Etiquetadora, Desktop, Tablet, etc.
    """
    nombre = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre del Artículo"
    )

    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Marca(TimestampedActivo):
    """Marca de equipo. Reemplaza tbmarca."""
    nombre = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre de la Marca"
    )

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Modelo(TimestampedActivo):
    """Modelo de equipo. Reemplaza tbmodelo.
    FK a Marca, imagen como ImageField (no varchar con ruta).
    unique(marca, nombre) — en la BD PHP era uniq_modelo(id_marca, modelo).
    """
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del Modelo"
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='modelos',
        verbose_name="Marca"
    )
    imagen = models.ImageField(
        upload_to='modelos/',
        null=True,
        blank=True,
        verbose_name="Imagen del Modelo"
    )

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"
        ordering = ['marca__nombre', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['marca', 'nombre'],
                name='uniq_modelo_marca_nombre'
            )
        ]

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class ModeloAnexo(TimestampedActivo):
    """Modelo de anexo telefónico IP (catálogo separado de Modelo de equipos).
    Reemplaza modelos_anexos. Dominio distinto: teléfonos Cisco CP-xxxx.
    """
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre del Modelo"
    )
    imagen = models.ImageField(
        upload_to='modelos_anexos/',
        null=True,
        blank=True,
        verbose_name="Imagen del Modelo"
    )

    class Meta:
        verbose_name = "Modelo de Anexo"
        verbose_name_plural = "Modelos de Anexos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class SistemaOperativo(TimestampedActivo):
    """Sistema operativo. Reemplaza tbso."""
    nombre = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre del SO"
    )

    class Meta:
        verbose_name = "Sistema Operativo"
        verbose_name_plural = "Sistemas Operativos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class EstadoEquipo(TimestampedActivo):
    """Estado de un equipo. Reemplaza tbestado.
    Añade color_hex para badges visuales (en PHP estaba hardcoded en vistas).
    """
    nombre = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre del Estado"
    )
    color_hex = models.CharField(
        max_length=20,
        default='#17a2b8',
        verbose_name="Color (hex) para badges"
    )

    class Meta:
        verbose_name = "Estado de Equipo"
        verbose_name_plural = "Estados de Equipos"
        ordering = ['nombre']

    def clean(self):
        super().clean()
        if self.color_hex and not self.color_hex.startswith('#'):
            self.color_hex = f'#{self.color_hex}'
        if self.color_hex and not re.match(r'^#[0-9A-Fa-f]{3,8}$', self.color_hex):
            raise ValidationError({'color_hex': 'Debe ser un color hex válido (ej: #17a2b8).'})

    def __str__(self):
        return self.nombre


class Proveedor(TimestampedActivo):
    """Proveedor / proveedor de servicio. Reemplaza tbproveedores."""
    nombre = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nombre del Proveedor"
    )
    contacto = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="Persona de Contacto"
    )
    telefono = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="Teléfono"
    )
    email = models.EmailField(
        max_length=120,
        null=True, blank=True,
        verbose_name="Correo Electrónico"
    )
    direccion = models.CharField(
        max_length=255,
        null=True, blank=True,
        verbose_name="Dirección"
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Vlan(TimestampedActivo):
    """VLAN de red. Reemplaza tb_vlan (esquema básico)."""
    nombre = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre de la VLAN"
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )

    class Meta:
        verbose_name = "VLAN"
        verbose_name_plural = "VLANs"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
