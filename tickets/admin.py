from django.contrib import admin
from .models import Ticket, TicketHistorial, ArchivoAdjunto, Prioridad, Categoria

@admin.register(Prioridad)
class PrioridadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sla_horas', 'color_hex')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('correlativo', 'estado', 'prioridad', 'categoria', 'solicitante', 'responsable', 'fecha_creacion')
    list_filter = ('estado', 'prioridad', 'categoria')
    search_fields = ('correlativo', 'descripcion', 'solicitante__username')

@admin.register(TicketHistorial)
class TicketHistorialAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'usuario', 'accion', 'fecha')
    search_fields = ('ticket__correlativo', 'accion')

@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'subido_por', 'fecha_subida')
