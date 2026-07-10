from django.contrib import admin

from .models import Pma, InfraestructuraRed, RangoIP, SlaConfiguracion


class InfraestructuraRedInline(admin.TabularInline):
    model = InfraestructuraRed
    extra = 0
    fields = ('ip_direccion', 'estado', 'switch_ip', 'switch_port', 'rack', 'patch_panel')
    show_change_link = True


@admin.register(Pma)
class PmaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'edificio_piso', 'unidad', 'estado', 'descripcion')
    list_filter = ('estado', 'edificio_piso__edificio')
    search_fields = ('codigo', 'descripcion')
    autocomplete_fields = ['edificio_piso', 'unidad']


@admin.register(InfraestructuraRed)
class InfraestructuraRedAdmin(admin.ModelAdmin):
    list_display = ('ip_direccion', 'estado', 'pma', 'edificio', 'piso',
                    'unidad', 'rack', 'patch_panel', 'switch_ip', 'switch_port')
    list_filter = ('estado', 'institucion', 'edificio', 'piso')
    search_fields = ('ip_direccion', 'mac', 'sector', 'rack', 'patch_panel')
    autocomplete_fields = ['pma', 'vlan', 'institucion', 'edificio', 'piso', 'unidad']
    list_editable = ('estado',)


@admin.register(RangoIP)
class RangoIPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'piso', 'unidad', 'ubicacion', 'pma', 'rack',
                    'rango', 'dato', 'estado')
    list_filter = ('piso', 'estado', 'piso__edificio')
    search_fields = ('ip', 'unidad', 'ubicacion', 'pma', 'rack', 'comentario')
    autocomplete_fields = ['piso']
    list_editable = ('estado',)


@admin.register(SlaConfiguracion)
class SlaConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'horas_objetivo', 'alerta_porcentaje', 'activo')
    list_filter = ('activo',)
    list_editable = ('horas_objetivo', 'alerta_porcentaje', 'activo')
