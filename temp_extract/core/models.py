from django.db import models
from django.contrib.auth.models import User


class LogAuditoria(models.Model):
    class Accion(models.TextChoices):
        CREAR = 'CREAR', 'Creación'
        MODIFICAR = 'MODIFICAR', 'Modificación'
        ELIMINAR = 'ELIMINAR', 'Eliminación'
        LOGIN_EXITOSO = 'LOGIN_OK', 'Inicio Sesión Exitoso'
        LOGIN_FALLIDO = 'LOGIN_FAIL', 'Inicio Sesión Fallido'
        LOGOUT = 'LOGOUT', 'Cierre de Sesión'

    usuario = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Usuario"
    )
    accion = models.CharField(
        max_length=10,
        choices=Accion.choices,
        verbose_name="Acción"
    )
    tabla = models.CharField(
        max_length=100,
        verbose_name="Tabla/Objeto"
    )
    registro_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="ID de Registro"
    )
    detalles = models.TextField(
        verbose_name="Detalles de la Operación"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Dirección IP"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.fecha_registro} - {self.usuario} - {self.get_accion_display()} ({self.tabla})"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name="Usuario Django"
    )
    unidad = models.CharField(
        max_length=100,
        verbose_name="Unidad / Servicio"
    )
    cargo = models.CharField(
        max_length=100,
        verbose_name="Cargo"
    )
    grado = models.CharField(
        max_length=20,
        verbose_name="Grado"
    )
    rut = models.CharField(
        max_length=12,
        unique=True,
        db_index=True,
        verbose_name="RUT del Funcionario"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut}) - {self.cargo} - Grado {self.grado}"
