import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from equipos.models import Equipo

eq = Equipo.objects.first()
if eq:
    print('ID:', eq.id)
    print('Num Inv:', eq.num_inventario)
    print('Serial:', eq.serial_number)
    print('IP:', eq.ip)
    if eq.pma:
        print('PMA Nombre:', eq.pma.nombre)
        if eq.pma.recinto:
            print('Recinto Nombre:', eq.pma.recinto.nombre)
            if eq.pma.recinto.piso:
                print('Piso Nombre:', eq.pma.recinto.piso.nombre)
                if eq.pma.recinto.piso.edificio:
                    print('Edificio Nombre:', eq.pma.recinto.piso.edificio.nombre)
                else:
                    print('Edificio: None')
            else:
                print('Piso: None')
        else:
            print('Recinto: None')
    else:
        print('PMA: None')
