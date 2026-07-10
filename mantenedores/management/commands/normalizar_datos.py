from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.utils import normalizar_nombre, normalizar_codigo
from mantenedores.models import (
    Institucion, Edificio, Piso, Unidad, Articulo, Marca, Modelo,
    ModeloAnexo, SistemaOperativo, EstadoEquipo, Proveedor,
)
from equipos.models import BitacoraOpcion
from anexos.models import Anexo
from tickets.models import Ticket
from actas.models import Acta, ActaDetalle
from core.models import PerfilUsuario
from redes.models import InfraestructuraRed


CAMBIOS = 0


def normalizar_qs(qs, campo, fn=normalizar_nombre, filtro=None):
    global CAMBIOS
    for obj in qs:
        valor = getattr(obj, campo)
        if not valor or not isinstance(valor, str):
            continue
        nuevo = fn(valor) if fn else valor
        if filtro and not filtro(valor):
            continue
        if nuevo == valor:
            continue
        setattr(obj, campo, nuevo)
        obj.save(update_fields=[campo])
        CAMBIOS += 1


class Command(BaseCommand):
    help = 'Normaliza nombres existentes a Title Case en toda la app'

    def handle(self, *args, **options):
        global CAMBIOS

        self.stdout.write('Normalizando mantenedores...')
        for cls in [Institucion, Edificio, Piso, Unidad, Articulo, Marca,
                     Modelo, ModeloAnexo, SistemaOperativo, EstadoEquipo, Proveedor]:
            normalizar_qs(cls.objects.all(), 'nombre')

        normalizar_qs(Piso.objects.all(), 'alias')
        normalizar_qs(Proveedor.objects.all(), 'contacto')
        normalizar_qs(Proveedor.objects.all(), 'direccion')
        normalizar_qs(Institucion.objects.all(), 'codigo', fn=normalizar_codigo)

        self.stdout.write('Normalizando BitacoraOpcion...')
        normalizar_qs(BitacoraOpcion.objects.all(), 'nombre')

        self.stdout.write('Normalizando Anexos...')
        normalizar_qs(Anexo.objects.all(), 'marca')
        normalizar_qs(Anexo.objects.all(), 'modelo')
        normalizar_qs(Anexo.objects.all(), 'pma_lugar')

        self.stdout.write('Normalizando Tickets...')
        normalizar_qs(Ticket.objects.all(), 'solicitante_nombre')

        self.stdout.write('Normalizando Actas...')
        normalizar_qs(Acta.objects.all(), 'codigo', fn=normalizar_codigo)
        normalizar_qs(Acta.objects.all(), 'receptor_nombre')
        normalizar_qs(Acta.objects.all(), 'receptor_cargo')
        normalizar_qs(Acta.objects.all(), 'receptor_unidad')
        normalizar_qs(ActaDetalle.objects.all(), 'articulo')
        normalizar_qs(ActaDetalle.objects.all(), 'pma_lugar')

        self.stdout.write('Normalizando Usuarios...')
        normalizar_qs(User.objects.all(), 'first_name')
        normalizar_qs(User.objects.all(), 'last_name')
        for p in PerfilUsuario.objects.all():
            for campo in ['unidad', 'cargo', 'grado']:
                valor = getattr(p, campo)
                if valor and isinstance(valor, str):
                    nuevo = normalizar_nombre(valor)
                    if nuevo != valor:
                        setattr(p, campo, nuevo)
                        p.save(update_fields=[campo])
                        CAMBIOS += 1

        self.stdout.write('Normalizando Redes (sector, rack, patch_panel)...')
        normalizar_qs(InfraestructuraRed.objects.all(), 'sector')
        normalizar_qs(InfraestructuraRed.objects.all(), 'rack')
        normalizar_qs(InfraestructuraRed.objects.all(), 'patch_panel')

        self.stdout.write(self.style.SUCCESS(f'Hecho. {CAMBIOS} registros actualizados.'))
