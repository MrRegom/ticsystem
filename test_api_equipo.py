import os
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
import django
django.setup()

from equipos.services.equipo_service import EquipoService

try:
    r = EquipoService.obtener_equipos_para_datatable(0, 3, "", 0, "desc", [])
    print("TOTAL:", r["recordsTotal"])
    if r["data"]:
        print("KEYS:", list(r["data"][0].keys()))
        print("MUESTRA:", r["data"][0])
    else:
        print("SIN DATOS")
except Exception as e:
    print("ERROR:", e)
