"""
Modelos del módulo de Utilidades TIC (autogestión).

Normalización aplicada (3NF):
- AyudaRapida: de tb_ayudas_rapidas (snippets/comandos Windows).
- WebApp: de tb_webapps (accesos directos a sistemas hospitalarios).
- ChecklistItem: de `checklist` (¡sin PK autogenerada en PHP!). Añade PK + reordena.
- Pendiente: de `pendientes` (tareas del visor TV). estado enum → choices.
"""
from django.db import models


class AyudaRapida(models.Model):
    """Snippet/comando de soporte rápido. Reemplaza tb_ayudas_rapidas."""
    titulo = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Título"
    )
    contenido = models.TextField(
        verbose_name="Contenido"
    )
    categoria = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Categoría"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Activo"
    )
    orden = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name="Orden"
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
        verbose_name = "Ayuda Rápida"
        verbose_name_plural = "Ayudas Rápidas"
        ordering = ['orden', 'titulo']

    def __str__(self):
        return self.titulo


class WebApp(models.Model):
    """Acceso directo a sistema hospitalario. Reemplaza tb_webapps."""
    nombre = models.CharField(
        max_length=180,
        unique=True,
        verbose_name="Nombre"
    )
    url = models.URLField(
        verbose_name="URL"
    )
    icono = models.CharField(
        max_length=100,
        default='bi bi-link-45deg',
        verbose_name="Icono (clase Bootstrap Icons)"
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Activo"
    )
    orden = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name="Orden"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )

    class Meta:
        verbose_name = "Web App / Acceso"
        verbose_name_plural = "Web Apps / Accesos"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class ChecklistItem(models.Model):
    """Ítem de checklist de preparación de equipos. Reemplaza `checklist`.
    AÑADE PK autogenerada (en PHP `id` era int sin AUTO_INCREMENT, era un ordinal fijo).
    """
    task_name = models.CharField(
        max_length=255,
        verbose_name="Tarea"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Completado"
    )
    activo = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Activo"
    )
    orden = models.IntegerField(
        default=0,
        db_index=True,
        verbose_name="Orden"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )

    class Meta:
        verbose_name = "Ítem de Checklist"
        verbose_name_plural = "Ítems de Checklist"
        ordering = ['orden', 'id']

    def __str__(self):
        return self.task_name


class Pendiente(models.Model):
    """Tarea pendiente del visor TV. Reemplaza `pendientes`."""
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        RESUELTO = 'resuelto', 'Resuelto'

    titulo = models.CharField(
        max_length=255,
        verbose_name="Título"
    )
    link = models.CharField(
        max_length=255,
        default='#',
        verbose_name="Link"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
        db_index=True,
        verbose_name="Estado"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    fecha_cierre = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de Cierre"
    )
    fecha_programada = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha Programada"
    )

    class Meta:
        verbose_name = "Pendiente"
        verbose_name_plural = "Pendientes"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
