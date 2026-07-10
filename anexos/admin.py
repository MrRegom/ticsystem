from django.contrib import admin

from .models import Anexo, RequerimientoCambio


class RequerimientoCambioInline(admin.TabularInline):
    model = RequerimientoCambio
    extra = 0
    fields = ('tipo', 'sub_requerimiento', 'accion', 'nombre_usuario_req',
              'ubicacion_req', 'estado_req', 'cambiar_dos_anexos',
              'numero_anexo_cambio', 'cascada', 'observacion', 'fecha')
    readonly_fields = ('fecha',)
    show_change_link = True


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ('numero_anexo', 'marca', 'modelo', 'edificio', 'piso',
                    'unidad', 'estado', 'ip', 'serial_number')
    list_filter = ('estado', 'marca', 'edificio', 'establecimiento')
    search_fields = ('numero_anexo', 'serial_number', 'ip', 'pma_lugar',
                     'comentario', 'grupo')
    autocomplete_fields = ['modelo_anexo', 'edificio', 'piso', 'unidad',
                           'proveedor', 'establecimiento']
    inlines = [RequerimientoCambioInline]
    date_hierarchy = 'creado_en'


@admin.register(RequerimientoCambio)
class RequerimientoCambioAdmin(admin.ModelAdmin):
    list_display = ('anexo', 'tipo', 'accion', 'nombre_usuario_req',
                    'cambiar_dos_anexos', 'cascada', 'fecha')
    list_filter = ('tipo', 'cambiar_dos_anexos', 'cascada')
    search_fields = ('anexo__numero_anexo', 'nombre_usuario_req', 'accion', 'observacion')
    autocomplete_fields = ['anexo']
    date_hierarchy = 'fecha'
