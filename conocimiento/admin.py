from django.contrib import admin
from .models import CategoriaConocimiento, ArticuloConocimiento

@admin.register(CategoriaConocimiento)
class CategoriaConocimientoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(ArticuloConocimiento)
class ArticuloConocimientoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'es_error_conocido', 'actualizado_en')
    list_filter = ('categoria', 'es_error_conocido')
    search_fields = ('titulo', 'sintomas', 'solucion')
