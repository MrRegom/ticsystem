from django.contrib import admin

from .models import AvisoVisor


@admin.register(AvisoVisor)
class AvisoVisorAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'activo', 'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('activo',)
    search_fields = ('titulo', 'mensaje')
    list_editable = ('activo',)
