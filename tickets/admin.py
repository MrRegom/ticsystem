from django.contrib import admin

from .models import Ticket, TicketBitacora, Prioridad, Categoria


class TicketBitacoraInline(admin.TabularInline):
    model = TicketBitacora
    extra = 0
    fields = ('usuario', 'tipo_nota', 'nota', 'fecha_registro')
    readonly_fields = ('fecha_registro',)
    show_change_link = True


@admin.register(Prioridad)
class PrioridadAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'sla_respuesta_minutos', 'sla_resolucion_horas', 'color_hex')
    list_editable = ('sla_respuesta_minutos', 'sla_resolucion_horas', 'color_hex')
    search_fields = ('nivel',)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    list_filter = ('activo',)
    list_editable = ('activo',)
    search_fields = ('nombre',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'solicitante_nombre', 'estado', 'prioridad', 'categoria',
                    'tecnico', 'edificio', 'fecha_hora', 'fecha_cierre')
    list_filter = ('estado', 'prioridad', 'categoria', 'tecnico')
    search_fields = ('solicitante_nombre', 'solicitante_rut', 'solicitante_correo',
                     'descripcion', 'piso')
    autocomplete_fields = ['edificio', 'unidad', 'equipo', 'tecnico',
                           'prioridad', 'categoria']
    inlines = [TicketBitacoraInline]
    date_hierarchy = 'fecha_hora'


@admin.register(TicketBitacora)
class TicketBitacoraAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'usuario', 'tipo_nota', 'fecha_registro')
    list_filter = ('tipo_nota',)
    search_fields = ('nota', 'ticket__solicitante_nombre')
    autocomplete_fields = ['ticket', 'usuario']
