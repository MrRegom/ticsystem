from django.contrib import admin

from mantenedores.models import (
    Institucion, Edificio, Piso, Unidad, Articulo, Marca, Modelo,
    ModeloAnexo, SistemaOperativo, EstadoEquipo, Proveedor, Vlan,
)


class PisoInline(admin.TabularInline):
    model = Piso
    extra = 1
    show_change_link = True


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('codigo', 'nombre')


@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'institucion', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'institucion')
    search_fields = ('nombre',)
    inlines = [PisoInline]


@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'alias', 'edificio', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'edificio__institucion', 'edificio')
    search_fields = ('nombre', 'alias', 'edificio__nombre')
    autocomplete_fields = ['edificio']


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


class ModeloInline(admin.TabularInline):
    model = Modelo
    extra = 1
    show_change_link = True


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'marca')
    search_fields = ('nombre', 'marca__nombre')
    autocomplete_fields = ['marca']
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.imagen.url}" style="max-height:80px;">')
        return '—'
    imagen_preview.short_description = 'Vista previa'


@admin.register(ModeloAnexo)
class ModeloAnexoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(SistemaOperativo)
class SistemaOperativoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(EstadoEquipo)
class EstadoEquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color_hex', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)


@admin.register(Vlan)
class VlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
