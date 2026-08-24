import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from equipos.services.equipo_service import EquipoService

result = EquipoService.obtener_equipos_para_datatable(0, 1, "", 0, "desc", [])["data"]
print(json.dumps(result, indent=2))
