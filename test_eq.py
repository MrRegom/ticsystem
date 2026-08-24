import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from equipos.models import Equipo
for eq in Equipo.objects.all():
    print(eq.id, "|", eq.edificio, "|", eq.unidad, "|", eq.pma, "|", eq.piso, "|", eq.num_inventario, "|", eq.serial_number, "|", eq.ip)
