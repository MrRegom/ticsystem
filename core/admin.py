from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from core.models import LogAuditoria, PerfilUsuario


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha_registro', 'usuario', 'accion', 'tabla', 'registro_id', 'ip_address')
    list_filter = ('accion', 'fecha_registro')
    search_fields = ('usuario', 'tabla', 'registro_id', 'detalles')
    date_hierarchy = 'fecha_registro'
    readonly_fields = ('usuario', 'accion', 'tabla', 'registro_id', 'detalles', 'ip_address', 'fecha_registro')
    ordering = ('-fecha_registro',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil TIC'
    fk_name = 'user'


class UserAdmin(DjangoUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
