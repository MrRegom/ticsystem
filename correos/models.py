"""
Modelos del módulo de Correos / Notificaciones.

Normalización aplicada (3NF):
- GrupoCorreo: de email_grupos_catalogo.
- MiembroGrupoCorreo: de email_grupos. ELIMINA el campo `grupo` (string) redundante
  que duplicaba el nombre del grupo ya referenciado por `grupo_id` (FK).
  Anomalía de actualización resuelta: ahora solo FK a GrupoCorreo.
- CredencialCorreo: de tbcorreos (credenciales SMTP). En producción estas creds
  deben ir en settings/env vars, no en BD. Se mantiene para registro de cuentas
  institucionales (metadatos), pero el password va en env vars.
"""
from django.db import models


class GrupoCorreo(models.Model):
    """Catálogo de grupos de correo (listas de distribución). Reemplaza email_grupos_catalogo."""
    nombre = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Nombre del Grupo"
    )
    descripcion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Descripción"
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden"
    )
    activo = models.BooleanField(
        default=True,
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
        verbose_name = "Grupo de Correo"
        verbose_name_plural = "Grupos de Correo"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class MiembroGrupoCorreo(models.Model):
    """Email miembro de un grupo de correo. Reemplaza email_grupos.
    Elimina `grupo` (string) redundante — ahora solo FK a GrupoCorreo (3NF).
    """
    grupo = models.ForeignKey(
        GrupoCorreo,
        on_delete=models.CASCADE,
        related_name='miembros',
        verbose_name="Grupo"
    )
    email = models.EmailField(
        verbose_name="Email"
    )

    class Meta:
        verbose_name = "Miembro de Grupo"
        verbose_name_plural = "Miembros de Grupos"
        ordering = ['email']
        constraints = [
            models.UniqueConstraint(
                fields=['grupo', 'email'],
                name='uniq_miembro_grupo_email'
            )
        ]

    def __str__(self):
        return f"{self.email} ({self.grupo.nombre})"


class CredencialCorreo(models.Model):
    """Registro de una cuenta de correo institucional. Reemplaza tbcorreos.
    El PASSWORD va en variables de entorno / gestor de secretos, NO en este modelo.
    Aquí solo metadatos (email, propietario, estado).
    """
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    propietario = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Propietario"
    )
    departamento = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Departamento"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )

    class Meta:
        verbose_name = "Credencial de Correo"
        verbose_name_plural = "Credenciales de Correo"
        ordering = ['email']

    def __str__(self):
        return self.email

class ConfiguracionSMTP(models.Model):
    """
    Configuración centralizada para el servidor SMTP (Singleton).
    Permite a los administradores cambiar credenciales desde la UI.
    """
    host = models.CharField(max_length=150, default='smtp.office365.com', verbose_name="Servidor SMTP (Host)")
    puerto = models.IntegerField(default=587, verbose_name="Puerto")
    usuario = models.CharField(max_length=150, verbose_name="Usuario / Email", blank=True, null=True)
    password = models.CharField(max_length=255, verbose_name="Contraseña", blank=True, null=True)
    use_tls = models.BooleanField(default=True, verbose_name="Usar TLS")
    remitente_por_defecto = models.EmailField(verbose_name="Remitente por Defecto (From)", blank=True, null=True)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración SMTP"
        verbose_name_plural = "Configuraciones SMTP"

    def __str__(self):
        return f"Configuración SMTP: {self.host}:{self.puerto}"

    @classmethod
    def load(cls):
        """Devuelve la única instancia de configuración o la crea si no existe (Patrón Singleton)"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj
