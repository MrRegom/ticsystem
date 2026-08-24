from core.models import Rol
r, _ = Rol.objects.get_or_create(
    nombre="Coordinador de Soporte",
    defaults={
        "descripcion": "Puede crear tickets, asignar, resolver y cerrar. Acceso completo al módulo de Tickets.",
        "is_system": True,
        "icono": "fas fa-headset"
    }
)
r.permisos = {
    "VER_INICIO": True,
    "VER_TICKETS": True,
    "GESTIONAR_TICKETS": True,
    "RECIBIR_TICKETS": True,
    "DERIVAR_TICKETS": True
}
r.save()
print("Rol creado en PROD exitosamente.")
