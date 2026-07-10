from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
        db_index=True,
        verbose_name="Usuario"
    )
    accion = models.CharField(
        max_length=10,
        choices=Accion.choices,
        db_index=True,
        verbose_name="Acción"
    )
    tabla = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Tabla/Objeto"
    )
    registro_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
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
        db_index=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Log de Auditoría"
        verbose_name_plural = "Logs de Auditoría"
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['tabla', 'registro_id'], name='idx_log_tabla_reg'),
            models.Index(fields=['ip_address'], name='idx_log_ip'),
        ]

    def __str__(self):
        return f"{self.fecha_registro} - {self.usuario} - {self.get_accion_display()} ({self.tabla})"


class Rol(models.Model):
    """Rol de usuario (RBAC). Reemplaza al campo texto `perfil` de tbusuarios (PHP).
    Los permisos se almacenan como JSON (19 permisos booleanos) y se consultan
    via helpers en core.services.rol_service o mixins de autorizacion.
    """
    nombre = models.CharField(
        max_length=80,
        unique=True,
        db_index=True,
        verbose_name="Nombre del Rol"
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )
    permisos = models.JSONField(
        default=dict,
        verbose_name="Permisos (JSON)",
        help_text="Diccionario de 19 permisos booleanos"
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
    creado_por = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="Creado por"
    )
    actualizado_por = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="Actualizado por"
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
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    def tiene_permiso(self, permiso):
        """Devuelve True si el rol tiene el permiso indicado (bool True)."""
        return bool(self.permisos.get(permiso, False))


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
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="RUT del Funcionario"
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name="Rol TIC"
    )
    telefono = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Teléfono"
    )
    foto = models.ImageField(
        upload_to='usuarios/fotos/',
        null=True,
        blank=True,
        verbose_name="Foto"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ['-fecha_registro']

    def clean(self):
        super().clean()
        if self.rut:
            self.rut = self.rut.strip().upper()

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.rut}) - {self.cargo} - Grado {self.grado}"
