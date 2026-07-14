from django.db import models

class CategoriaConocimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    
    class Meta:
        verbose_name = "Categoría de Conocimiento"
        verbose_name_plural = "Categorías de Conocimiento"
        ordering = ['nombre']
        
    def __str__(self):
        return self.nombre


class ArticuloConocimiento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título / Síntoma Breve")
    sintomas = models.TextField(verbose_name="Síntomas Detallados")
    solucion = models.TextField(verbose_name="Solución o Procedimiento")
    categoria = models.ForeignKey(CategoriaConocimiento, on_delete=models.SET_NULL, null=True, blank=True, related_name='articulos')
    
    # KEDB: Known Error Database fields
    es_error_conocido = models.BooleanField(default=True, verbose_name="Es Error Conocido")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Artículo de Conocimiento"
        verbose_name_plural = "Artículos de Conocimiento"
        ordering = ['-actualizado_en']
        
    def __str__(self):
        return self.titulo
