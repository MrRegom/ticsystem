"""
Modelos del módulo Enterprise Helpdesk (Gestión de Incidentes).

Normalización (3NF) y Clean Architecture:
- El Ticket NO duplica datos de ubicación (Edificio, Piso, Unidad, PMA).
- Todo se infiere a través de la relación ForeignKey con 'Equipo' (el Activo).
- Implementación de patrón de auditoría inmutable (TicketHistorial).
"""
from django.db import models
from django.contrib.auth.models import User
from equipos.models import Equipo


class Prioridad(models.Model):
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    sla_horas = models.IntegerField(verbose_name="SLA Resolución (horas)")
    color_hex = models.CharField(max_length=20, default='#333333', verbose_name="Color Hex")

    class Meta:
        verbose_name = "Prioridad"
        verbose_name_plural = "Prioridades"

    def __str__(self):
        return self.nombre


class GrupoResolutor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Grupo")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    icono = models.CharField(max_length=50, null=True, blank=True, default="ms-Icon--Group", verbose_name="Icono Fluent UI")
    # Los usuarios que pertenecen a este grupo
    miembros = models.ManyToManyField(User, related_name='grupos_resolutores', blank=True, verbose_name="Técnicos Miembros")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    is_system = models.BooleanField(default=False, verbose_name="Grupo de Sistema (No borrable)")

    class Meta:
        verbose_name = "Grupo Resolutor"
        verbose_name_plural = "Grupos Resolutores"

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    grupo_resolutor = models.ForeignKey(GrupoResolutor, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Grupo de Resolución Asignado")
    activa = models.BooleanField(default=True, verbose_name="Activa")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Ticket(models.Model):
    class Estado(models.TextChoices):
        NUEVO = 'NUEVO', 'Nuevo'
        ASIGNADO = 'ASIGNADO', 'Asignado'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        ESPERA_APROBACION = 'ESPERA_APROBACION', 'En Espera de Aprobación'
        PENDIENTE_USUARIO = 'PENDIENTE_USUARIO', 'Pendiente Usuario'
        PENDIENTE_PROVEEDOR = 'PENDIENTE_PROVEEDOR', 'Pendiente Proveedor'
        ESCALADO = 'ESCALADO', 'Escalado'
        RESUELTO = 'RESUELTO', 'Resuelto'
        CERRADO = 'CERRADO', 'Cerrado'
        CANCELADO = 'CANCELADO', 'Cancelado'
        
    class Tipo(models.TextChoices):
        INCIDENTE = 'INCIDENTE', 'Incidente (Falla/Interrupción)'
        REQUERIMIENTO = 'REQUERIMIENTO', 'Requerimiento (Solicitud)'

    class Impacto(models.IntegerChoices):
        HOSPITAL = 1, 'Hospital / Alta Críticidad'
        SERVICIO = 2, 'Servicio / Área'
        PACIENTE = 3, 'Paciente / Usuario Único'
        BAJO = 4, 'Bajo / Sin Impacto Clínico'

    class Urgencia(models.IntegerChoices):
        ALTA = 1, 'Alta / Detiene Operación'
        MEDIA = 2, 'Media / Operación Degradada'
        BAJA = 3, 'Baja / Operación Normal'

    correlativo = models.CharField(max_length=20, unique=True, verbose_name="N° Ticket")
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.INCIDENTE, verbose_name="Tipo")
    estado = models.CharField(max_length=30, choices=Estado.choices, default=Estado.NUEVO, verbose_name="Estado")
    
    impacto = models.IntegerField(choices=Impacto.choices, default=Impacto.BAJO, verbose_name="Impacto")
    urgencia = models.IntegerField(choices=Urgencia.choices, default=Urgencia.BAJA, verbose_name="Urgencia")
    
    prioridad = models.ForeignKey(Prioridad, on_delete=models.PROTECT, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    
    # Enrutamiento ITIL
    grupo_resolutor = models.ForeignKey(GrupoResolutor, on_delete=models.PROTECT, null=True, blank=True, related_name='tickets_asignados', verbose_name="Grupo Resolutor")
    responsable = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='tickets_asignados', verbose_name="Técnico Responsable")
    
    # El Operador de Mesa de Ayuda que tomó la llamada
    creador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tickets_creados', null=True, blank=True, verbose_name="Creador (Operador)")
    # El Funcionario que reporta el problema (para el cual es el ticket)
    solicitante = models.ForeignKey('core.Funcionario', on_delete=models.PROTECT, related_name='tickets_solicitados', verbose_name="Solicitante")
    
    activo = models.ForeignKey(Equipo, on_delete=models.PROTECT, related_name='tickets', null=True, blank=True, verbose_name="Activo / Equipo")
    
    anexo_contacto = models.CharField(max_length=50, null=True, blank=True, verbose_name="Anexo/Teléfono de Contacto")
    correo_contacto = models.EmailField(max_length=150, null=True, blank=True, verbose_name="Correo de Contacto")
    
    descripcion = models.TextField(verbose_name="Descripción del Problema")
    diagnostico = models.TextField(null=True, blank=True, verbose_name="Diagnóstico Técnico")
    solucion = models.TextField(null=True, blank=True, verbose_name="Solución Aplicada")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_asignacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Asignación")
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre")
    
    # Campos para SLA
    fecha_vencimiento_sla = models.DateTimeField(null=True, blank=True, verbose_name="Vencimiento SLA Resolución")

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.correlativo} - {self.get_estado_display()}"

    @property
    def en_pausa_sla(self):
        """
        Determina si el cronómetro SLA está pausado.
        En ITIL, el reloj se detiene cuando el ticket depende de factores externos
        (Pendiente de Usuario o Proveedor).
        """
        return self.estado in [
            self.Estado.PENDIENTE_USUARIO,
            self.Estado.PENDIENTE_PROVEEDOR,
            self.Estado.ESPERA_APROBACION
        ]

    @property
    def is_sla_vencido(self):
        """
        Retorna True si la fecha actual es mayor a la fecha de vencimiento.
        Si está cerrado/resuelto, se compara con la fecha de cierre.
        """
        if not self.fecha_vencimiento_sla:
            return False
            
        from django.utils import timezone
        
        if self.estado in [self.Estado.RESUELTO, self.Estado.CERRADO]:
            # Verificar si se venció ANTES de resolverlo
            if self.fecha_cierre and self.fecha_cierre > self.fecha_vencimiento_sla:
                return True
            return False
            
        return timezone.now() > self.fecha_vencimiento_sla

    @property
    def porcentaje_tiempo_transcurrido(self):
        """
        Calcula un porcentaje aproximado para pintar el semáforo.
        > 90% = Rojo
        > 75% = Amarillo
        < 75% = Verde
        """
        if not self.fecha_vencimiento_sla:
            return 0
            
        if self.estado in [self.Estado.RESUELTO, self.Estado.CERRADO]:
            return 0
            
        from django.utils import timezone
        ahora = timezone.now()
        
        total = (self.fecha_vencimiento_sla - self.fecha_creacion).total_seconds()
        transcurrido = (ahora - self.fecha_creacion).total_seconds()
        
        if total <= 0:
            return 100
            
        pct = (transcurrido / total) * 100
        return min(max(pct, 0), 100) # Clamp entre 0 y 100


class TicketHistorial(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    accion = models.CharField(max_length=255, verbose_name="Acción (ej. Cambio de Estado)")
    valor_anterior = models.TextField(null=True, blank=True)
    valor_nuevo = models.TextField(null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de Ticket"
        ordering = ['-fecha']


class ArchivoAdjunto(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='tickets/adjuntos/')
    subido_por = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo Adjunto"
