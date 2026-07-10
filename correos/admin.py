from django.contrib import admin

from .models import GrupoCorreo, MiembroGrupoCorreo, CredencialCorreo


class MiembroGrupoCorreoInline(admin.TabularInline):
    model = MiembroGrupoCorreo
    extra = 1
    fields = ('email',)


@admin.register(GrupoCorreo)
class GrupoCorreoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'orden', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre', 'descripcion')
    list_editable = ('orden', 'activo')
    inlines = [MiembroGrupoCorreoInline]


@admin.register(MiembroGrupoCorreo)
class MiembroGrupoCorreoAdmin(admin.ModelAdmin):
    list_display = ('email', 'grupo')
    list_filter = ('grupo',)
    search_fields = ('email', 'grupo__nombre')
    autocomplete_fields = ['grupo']


@admin.register(CredencialCorreo)
class CredencialCorreoAdmin(admin.ModelAdmin):
    list_display = ('email', 'propietario', 'departamento', 'activo', 'fecha_creacion')
    list_filter = ('activo', 'departamento')
    search_fields = ('email', 'propietario', 'departamento')
    list_editable = ('activo',)
