import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from equipos.models import Equipo

def clear():
    count, _ = Equipo.objects.all().delete()
    print(f"Se eliminaron {count} equipos exitosamente.")

if __name__ == '__main__':
    clear()
