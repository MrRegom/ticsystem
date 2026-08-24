import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from equipos.models import Equipo
import sys

eq = Equipo.objects.first()
if eq:
    data = {
        'edificio': eq.pma.recinto.piso.edificio.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.piso and eq.pma.recinto.piso.edificio else None,
        'unidad': eq.pma.recinto.unidad.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.unidad else None,
        'piso': eq.pma.recinto.piso.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.piso else None,
        'pma': eq.pma.nombre if eq.pma else None,
        'num_inventario': eq.num_inventario,
        'serial': eq.serial_number
    }
    with open('/app/test_eq.json', 'w') as f:
        json.dump(data, f)
