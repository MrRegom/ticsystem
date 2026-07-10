from django.contrib import admin

from .models import AyudaRapida, WebApp, ChecklistItem, Pendiente


@admin.register(AyudaRapida)
class AyudaRapidaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'activo', 'orden', 'fecha_actualizacion')
    list_filter = ('activo', 'categoria')
    search_fields = ('titulo', 'contenido')
    list_editable = ('orden', 'activo')


@admin.register(WebApp)
class WebAppAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'url', 'icono', 'activo', 'orden')
    list_filter = ('activo',)
    search_fields = ('nombre', 'url', 'descripcion')
    list_editable = ('orden', 'activo')


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'is_completed', 'activo', 'orden')
    list_filter = ('activo', 'is_completed')
    search_fields = ('task_name',)
    list_editable = ('is_completed', 'orden', 'activo')


@admin.register(Pendiente)
class PendienteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'estado', 'fecha_creacion', 'fecha_programada', 'fecha_cierre')
    list_filter = ('estado',)
    search_fields = ('titulo',)
    list_editable = ('estado',)
    date_hierarchy = 'fecha_creacion'
