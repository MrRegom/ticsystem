from django.contrib import admin

from .models import Acta, ActaDetalle


class ActaDetalleInline(admin.TabularInline):
    model = ActaDetalle
    extra = 1
    fields = ('tipo_item', 'id_item', 'articulo', 'serie', 'edificio',
              'piso', 'unidad', 'pma_lugar', 'estado')
    autocomplete_fields = ['edificio', 'piso', 'unidad']
    show_change_link = True


@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'receptor_nombre', 'receptor_rut', 'encargado',
                    'estado', 'fecha', 'fecha_envio')
    list_filter = ('estado', 'fecha', 'encargado')
    search_fields = ('codigo', 'receptor_nombre', 'receptor_rut',
                     'receptor_unidad', 'observaciones', 'email_receptor')
    autocomplete_fields = ['encargado']
    readonly_fields = ('fecha', 'fecha_envio', 'firma_receptor_preview',
                       'firma_encargado_preview', 'timbre_encargado_preview')
    inlines = [ActaDetalleInline]
    date_hierarchy = 'fecha'

    def firma_receptor_preview(self, obj):
        if obj.firma_receptor:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.firma_receptor.url}" style="max-height:80px;">')
        return '—'
    firma_receptor_preview.short_description = 'Firma receptor'

    def firma_encargado_preview(self, obj):
        if obj.firma_encargado:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.firma_encargado.url}" style="max-height:80px;">')
        return '—'
    firma_encargado_preview.short_description = 'Firma encargado'

    def timbre_encargado_preview(self, obj):
        if obj.timbre_encargado:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.timbre_encargado.url}" style="max-height:80px;">')
        return '—'
    timbre_encargado_preview.short_description = 'Timbre encargado'


@admin.register(ActaDetalle)
class ActaDetalleAdmin(admin.ModelAdmin):
    list_display = ('acta', 'tipo_item', 'id_item', 'articulo', 'serie')
    list_filter = ('tipo_item',)
    search_fields = ('acta__codigo', 'articulo', 'serie')
    autocomplete_fields = ['acta', 'edificio', 'piso', 'unidad']
