from django.contrib import admin
from django.utils.html import mark_safe

from .models import Equipo, BitacoraOpcion, BitacoraEquipo


class BitacoraEquipoInline(admin.TabularInline):
    model = BitacoraEquipo
    extra = 0
    readonly_fields = ('fecha_creacion', 'tecnico', 'tipo_registro', 'fecha_mantenimiento',
                       'fecha_devolucion', 'solicitante', 'falla_reportada',
                       'actividades_realizadas', 'servicio_unidad')
    can_delete = False
    show_change_link = True
    ordering = ('-fecha_creacion',)
    verbose_name = "Registro de bitácora"
    verbose_name_plural = "Historial de bitácora"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'articulo', 'marca', 'modelo', 'pma', 'estado', 'ip', 'fecha_modificacion')
    list_filter = ('estado', 'articulo', 'marca', 'so')
    search_fields = ('serial_number', 'usuario', 'ip', 'pmalugar', 'comentario', 'anexo')
    autocomplete_fields = ['articulo', 'marca', 'modelo', 'so', 'estado', 'proveedor']
    readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'imagen_preview')
    inlines = [BitacoraEquipoInline]
    date_hierarchy = 'fecha_creacion'

    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height:100px;">')
        return '—'
    imagen_preview.short_description = 'Vista previa'


@admin.register(BitacoraOpcion)
class BitacoraOpcionAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'nombre', 'activo', 'orden', 'fecha_creacion')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre',)
    list_editable = ('orden', 'activo')


@admin.register(BitacoraEquipo)
class BitacoraEquipoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'tipo_registro', 'tecnico', 'fecha_mantenimiento',
                    'fecha_devolucion', 'solicitante', 'fecha_creacion')
    list_filter = ('tipo_registro', 'fecha_mantenimiento', 'tecnico')
    search_fields = ('equipo__serial_number', 'solicitante', 'falla_reportada',
                     'actividades_realizadas', 'servicio_unidad')
    autocomplete_fields = ['equipo', 'tecnico']
    date_hierarchy = 'fecha_mantenimiento'
