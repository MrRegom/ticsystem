import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from equipos.models import Equipo
from tickets.models import Ticket, TicketHistorial, ArchivoAdjunto

print("Iniciando limpieza de datos transaccionales para Simulacro de Producción...")

# 1. Borrar Anexos de Tickets
count_anexos, _ = ArchivoAdjunto.objects.all().delete()
print(f"Borrados {count_anexos} anexos de tickets.")

# 2. (Saltamos Comentarios porque se integraron a Historial en este branch)

# 3. Borrar Historial
count_historial, _ = TicketHistorial.objects.all().delete()
print(f"Borrados {count_historial} registros de historial.")

# 4. Borrar Tickets
count_tickets, _ = Ticket.objects.all().delete()
print(f"Borrados {count_tickets} tickets.")

# 5. Borrar Equipos (Inventario)
count_equipos, _ = Equipo.objects.all().delete()
print(f"Borrados {count_equipos} equipos del inventario.")

print("¡Limpieza completada! La base de datos está lista para exportarse a Docker.")
