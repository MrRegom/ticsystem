"""
Modelos del módulo Visor TV (pantalla pública de Mesa de Ayuda).

- AvisoVisor: de tb_avisos_visor (auto-creada en ajax/avisos-visor.ajax.php:6).
  Avisos de dirección mostrados en pantalla TV.
"""
from django.db import models


class AvisoVisor(models.Model):
    """Aviso para pantalla TV de Mesa de Ayuda. Reemplaza tb_avisos_visor."""
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título"
    )
    mensaje = models.TextField(
        verbose_name="Mensaje"
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
        verbose_name = "Aviso del Visor"
        verbose_name_plural = "Avisos del Visor"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
