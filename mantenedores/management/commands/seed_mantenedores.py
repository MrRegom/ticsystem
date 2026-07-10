"""
Semilla inicial de catálogos básicos para ticsystem.

Crea la institución HGF, los edificios principales y pisos asociados, más los
catálogos mínimos (artículos, estados, SO, marcas, proveedores) necesarios para
operar desde el inicio. La migración completa de datos desde MySQL se hace en
la Fase 5 (migrar_desde_mysql).

Es idempotente: usa get_or_create en cada registro.

Fuente: equipamiento/basedatos2/equipamiento2026.sql (tablas tb_*, tbpisos, tbedificios).

Uso:
    python manage.py seed_mantenedores
"""
from django.core.management.base import BaseCommand
from mantenedores.models import (
    Institucion, Edificio, Piso, Unidad, Articulo, Marca,
    SistemaOperativo, EstadoEquipo, Proveedor,
)


class Command(BaseCommand):
    help = 'Crea catálogos básicos: institución HGF, edificios, pisos, artículos, estados, SO, marcas, proveedores.'

    def handle(self, *args, **options):
        # --- Institución ---
        hgf, created = Institucion.objects.get_or_create(
            codigo='HGF',
            defaults={'nombre': 'HOSPITAL DR. GUSTAVO FRICKE', 'activo': True}
        )
        self._log('Institución', hgf.codigo, created)

        # --- Edificios (de tbedificios) ---
        edificios_data = [
            ('CAE',), ('HOSPITAL NUEVO',), ('HOSPITAL ANTIGUO',),
            ('ARCHIVOS CLÍNICOS',), ('CASA JOVEN',), ('CASONA',),
            ('HOSPITAL DIURNO ADULTO',), ('HOSPITAL DIURNO INFANTO-JUVENIL',),
            ('CONTAINERS',),
        ]
        edificio_map = {}
        for nombre, in edificios_data:
            ed, c = Edificio.objects.get_or_create(
                nombre=nombre,
                institucion=hgf,
                defaults={'activo': True}
            )
            edificio_map[nombre] = ed
            self._log('Edificio', ed.nombre, c)

        # --- Pisos por edificio (de tbpisos) ---
        pisos_data = [
            ('HOSPITAL NUEVO', ['8', '7', '6', '5', '4', '3', '2', '1', 'Zócalo', '-1']),
            ('CAE', ['1', '2', '3']),
            ('CASA JOVEN', ['1', '2']),
            ('CONTAINERS', ['1', '2', '3']),
            ('ARCHIVOS CLÍNICOS', ['1']),
            ('HOSPITAL ANTIGUO', ['-1', '1', '2']),
            ('CASONA', ['1', '2', '3']),
            ('HOSPITAL DIURNO ADULTO', ['1', '2']),
            ('HOSPITAL DIURNO INFANTO-JUVENIL', ['1', '2']),
        ]
        for ed_nombre, pisos in pisos_data:
            ed = edificio_map.get(ed_nombre)
            if not ed:
                continue
            for p in pisos:
                _, c = Piso.objects.get_or_create(
                    nombre=p, edificio=ed, defaults={'activo': True}
                )
                if c:
                    self._log('Piso', f'{ed_nombre} - {p}', c)

        # --- Artículos (de tbarticulos) ---
        articulos = [
            'Notebook', 'All in One', 'Impresora', 'Etiquetadora', 'Desktop',
            'TELEVISOR', 'SOPORTE TV', 'Control Remoto TV', 'Tablet',
            'Lector de Código', 'Modulo Registro',
        ]
        for nombre in articulos:
            _, c = Articulo.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            if c:
                self._log('Artículo', nombre, c)

        # --- Estados de equipo (de tbestado) ---
        estados = [
            ('Funcional', '#28a745'),
            ('Mantenimiento', '#ffc107'),
            ('Desuso', '#6c757d'),
            ('No Funcional', '#dc3545'),
            ('En Equipamiento', '#17a2b8'),
        ]
        for nombre, color in estados:
            _, c = EstadoEquipo.objects.get_or_create(
                nombre=nombre, defaults={'color_hex': color, 'activo': True}
            )
            if c:
                self._log('Estado', nombre, c)

        # --- Sistemas Operativos (de tbso) ---
        sos = ['Win 11', 'Win 10', 'Win 7', 'Win xp', 'WIN 8', 'Linux', 'macOS', 'NO DEFINIDO']
        for nombre in sos:
            _, c = SistemaOperativo.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            if c:
                self._log('SO', nombre, c)

        # --- Marcas (de tbmarca) ---
        marcas = [
            'Asus', 'HP', 'Lenovo', 'Olidata', 'Cisco', 'Zebra', 'MSI',
            'Fusion 5', 'ECS', 'Brother', 'Kyocera ECOSYS', 'Toshiba',
            'Honeywell', 'DELL', 'TSC', 'OKI', 'Ricoh', 'LG', 'DINON',
            'ergotron', 'Samsung', 'HID', 'Ozxen', 'Siderall', 'INTEL',
            'Spektra', 'Generico', 'AOC', 'Epson', 'Canon', 'Alcatel',
            'Apple', 'digitalPersona',
        ]
        for nombre in marcas:
            _, c = Marca.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            if c:
                self._log('Marca', nombre, c)

        # --- Proveedores (de tbproveedores) ---
        proveedores = [
            'Telefónica', 'HGF', 'Upgrade', 'Minsal', 'Tecnofax', 'Loginteg',
            'Sonda', 'Intesis', 'Donado', 'Grifols', 'SSVQ',
        ]
        for nombre in proveedores:
            _, c = Proveedor.objects.get_or_create(nombre=nombre, defaults={'activo': True})
            if c:
                self._log('Proveedor', nombre, c)

        self.stdout.write(self.style.SUCCESS('\nSemilla de mantenedores completada.'))

    def _log(self, entidad, nombre, created):
        if created:
            self.stdout.write(self.style.SUCCESS(f'+ {entidad}: {nombre}'))
        else:
            self.stdout.write(f'  {entidad} omitido (ya existe): {nombre}')
