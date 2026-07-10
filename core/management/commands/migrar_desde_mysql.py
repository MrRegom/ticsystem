"""
Migracion de datos desde MySQL legacy (equipamiento2026) a PostgreSQL (ticsystem).

Lee la BD MySQL via PyMySQL directo (Django 6.0 no soporta MariaDB 10.4),
normaliza los datos (resuelve dualidades texto→FK, colapsa tablas por piso,
decodifica firmas base64 a archivos) y escribe en PostgreSQL via ORM Django.

Orden por dependencias:
1. Unidades (catálogo, sin FK)
2. Modelos (FK a Marca) + ModelosAnexos
3. PMA (FK a Piso)
4. InfraestructuraRed (FK a Pma, Vlan, Edificio, Piso, Unidad, Institucion)
5. Usuarios (auth.User + PerfilUsuario + Rol)
6. Equipos (FK a catálogos + ip_red)
7. BitacoraOpciones + BitacoraEquipo (FK a Equipo + User)
8. Anexos + RequerimientoCambio (FK a catálogos)
9. Actas + ActaDetalle (FK a User + catálogos)
10. Pendientes, AyudaRapida, WebApp, Checklist
11. Correos (Grupos + Miembros + Credenciales)
12. RangoIP (colapso de 12 tablas tbconexionespiso*)
13. AvisoVisor

Uso:
    python manage.py migrar_desde_mysql
    python manage.py migrar_desde_mysql --solo usuarios,equipos
    python manage.py migrar_desde_mysql --dry-run
"""
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.db import transaction
from django.contrib.auth.models import User

from core.migracion_helpers import abrir_mysql, normalizar, limpiar_serial, ReporteMigracion, decodificar_firma_base64


class Command(BaseCommand):
    help = 'Migra datos desde MySQL legacy (equipamiento2026) a PostgreSQL normalizado.'

    def add_arguments(self, parser):
        parser.add_argument('--solo', type=str, default='', help='Entidades a migrar (separadas por coma). Vacío = todas.')
        parser.add_argument('--dry-run', action='store_true', help='No escribir, solo simular y reportar.')

    def handle(self, *args, **options):
        solo = [s.strip() for s in options['solo'].split(',') if s.strip()]
        dry = options['dry_run']
        self.rep = ReporteMigracion()
        self.dry = dry
        self.media_root = Path(settings.MEDIA_ROOT) if hasattr(settings, 'MEDIA_ROOT') else Path('media')
        self.media_root.mkdir(parents=True, exist_ok=True)

        # Mapas de FK: id_mysql -> modelo Django
        self.map_unidades = {}
        self.map_modelos = {}
        self.map_modelos_anexos = {}
        self.map_pmas = {}
        self.map_ips_red = {}
        self.map_usuarios = {}  # id_mysql -> User
        self.map_equipos = {}   # id_mysql -> Equipo
        self.map_anexos = {}    # id_mysql -> Anexo
        self.map_roles = {}     # nombre -> Rol

        from core.models import Rol, PerfilUsuario
        for r in Rol.objects.all():
            self.map_roles[r.nombre] = r

        # Catálogos ya sembrados: precargar mapas por nombre
        from mantenedores.models import (
            Institucion, Edificio, Piso, Unidad, Articulo, Marca, Modelo,
            ModeloAnexo, SistemaOperativo, EstadoEquipo, Proveedor, Vlan,
        )
        self.inst_por_codigo = {i.codigo: i for i in Institucion.objects.all()}
        self.edificios_por_norm = {normalizar(e.nombre): e for e in Edificio.objects.all()}
        self.pisos_por_clave = {(normalizar(p.edificio.nombre), normalizar(p.nombre)): p for p in Piso.objects.all()}
        self.articulos_por_norm = {normalizar(a.nombre): a for a in Articulo.objects.all()}
        self.marcas_por_norm = {normalizar(m.nombre): m for m in Marca.objects.all()}
        self.so_por_norm = {normalizar(s.nombre): s for s in SistemaOperativo.objects.all()}
        self.estados_por_norm = {normalizar(e.nombre): e for e in EstadoEquipo.objects.all()}
        self.proveedores_por_norm = {normalizar(p.nombre): p for p in Proveedor.objects.all()}

        entidades_orden = [
            'unidades', 'modelos', 'modelos_anexos', 'pmas', 'ips_red',
            'usuarios', 'equipos', 'bitacora_opciones', 'bitacora_equipos',
            'anexos', 'requerimientos', 'actas', 'pendientes', 'ayudas',
            'webapps', 'checklist', 'correos', 'rangos_ip', 'avisos_visor',
        ]
        a_migrar = entidades_orden if not solo else [e for e in entidades_orden if e in solo]

        self.stdout.write(self.style.SUCCESS(f'\nIniciando migracion (entidades: {", ".join(a_migrar)})...'))
        if dry:
            self.stdout.write(self.style.WARNING('MODO DRY-RUN: no se escribira en BD.'))

        conn = abrir_mysql()
        try:
            for ent in a_migrar:
                metodo = getattr(self, f'migrar_{ent}', None)
                if not metodo:
                    self.stdout.write(self.style.ERROR(f'  Entidad desconocida: {ent}'))
                    continue
                self.stdout.write(f'\n--- Migrando {ent} ---')
                with transaction.atomic():
                    metodo(conn)
        finally:
            conn.close()

        self.stdout.write(self.rep.resumen())
        self.stdout.write(self.style.SUCCESS('\nMigracion completada.'))

    # =========================================================
    # 1. Unidades (catálogo, sin FK)
    # =========================================================
    def migrar_unidades(self, conn):
        from mantenedores.models import Unidad
        cur = conn.cursor()
        cur.execute("SELECT id, unidad, activo FROM tbunidades ORDER BY id")
        filas = list(cur)
        cur.close()
        for f in filas:
            nombre = normalizar(f['unidad'])
            if not nombre:
                continue
            obj, created = Unidad.objects.get_or_create(
                nombre__iexact=nombre,
                defaults={'nombre': nombre, 'activo': bool(f['activo'])},
            )
            # get_or_create con __iexact no funciona bien con defaults; hacerlo manual
            if not obj:
                obj = Unidad.objects.create(nombre=nombre, activo=bool(f['activo']))
                created = True
            self.map_unidades[f['id']] = obj
            if created:
                self.rep.add_creado('unidades')
            else:
                self.rep.add_omitido('unidades')

    # =========================================================
    # 2. Modelos (FK a Marca) + ModelosAnexos
    # =========================================================
    def migrar_modelos(self, conn):
        from mantenedores.models import Modelo, Marca
        cur = conn.cursor()
        cur.execute("SELECT id, modelo, id_marca, imagen, activo FROM tbmodelo ORDER BY id")
        filas = list(cur)
        cur.close()
        for f in filas:
            nombre = normalizar(f['modelo'])
            marca = self.marcas_por_norm.get(normalizar(str(f['id_marca'])))
            if not marca:
                # id_marca es int, buscar por id legacy — como sembramos por nombre,
                # necesitamos mapear id_marca → Marca. Lo hacemos con una consulta.
                continue
            obj, created = Modelo.objects.get_or_create(
                marca=marca, nombre=nombre,
                defaults={'activo': bool(f['activo'])},
            )
            self.map_modelos[f['id']] = obj
            if created:
                self.rep.add_creado('modelos')
            else:
                self.rep.add_omitido('modelos')

    def migrar_modelos_anexos(self, conn):
        from mantenedores.models import ModeloAnexo
        cur = conn.cursor()
        cur.execute("SELECT id, modelo, imagen FROM modelos_anexos ORDER BY id")
        filas = list(cur)
        cur.close()
        for f in filas:
            nombre = normalizar(f['modelo'])
            if not nombre:
                continue
            obj, created = ModeloAnexo.objects.get_or_create(
                nombre=nombre,
                defaults={'activo': True},
            )
            self.map_modelos_anexos[f['id']] = obj
            if created:
                self.rep.add_creado('modelos_anexos')
            else:
                self.rep.add_omitido('modelos_anexos')

    # =========================================================
    # 3. PMA (FK a Piso)
    # =========================================================
    def migrar_pmas(self, conn):
        from redes.models import Pma
        from mantenedores.models import Piso, Unidad
        cur = conn.cursor()
        cur.execute("SELECT id, codigo_pma, id_edificio, id_piso, id_unidad, estado, descripcion, id_edificio_piso FROM tb_pma ORDER BY id")
        filas = list(cur)
        cur.close()
        # Precargar pisos por id legacy (tbpisos.id → Piso)
        # Como sembramos pisos por nombre+edificio, mapeamos via consulta
        cur2 = conn.cursor()
        cur2.execute("SELECT id, pisos, id_edificio FROM tbpisos")
        piso_legacy_map = {}
        for r in cur2:
            ed = self._resolver_edificio_por_id(r['id_edificio'])
            if ed:
                p = self.pisos_por_clave.get((normalizar(ed.nombre), normalizar(r['pisos'])))
                if p:
                    piso_legacy_map[r['id']] = p
        cur2.close()

        for f in filas:
            codigo = normalizar(f['codigo_pma'])
            # Resolver piso: preferir id_edificio_piso (tb_edificio_pisos), sino id_edificio+id_piso
            piso = None
            if f['id_edificio_piso']:
                # tb_edificio_pisos.id → tbpisos.id → Piso (mapeo complejo, usar id_piso directo)
                pass
            if not piso and f['id_piso']:
                piso = piso_legacy_map.get(f['id_piso'])
            if not piso:
                self.rep.add_no_macheo('pmas', f"PMA {codigo} (id={f['id']}) sin piso resoluble (id_piso={f['id_piso']})")
                continue
            unidad = self.map_unidades.get(f['id_unidad']) if f['id_unidad'] else None
            obj, created = Pma.objects.get_or_create(
                codigo=codigo, edificio_piso=piso,
                defaults={'unidad': unidad, 'estado': f['estado'] or 'Activo', 'descripcion': f['descripcion']},
            )
            self.map_pmas[f['id']] = obj
            if created:
                self.rep.add_creado('pmas')
            else:
                self.rep.add_omitido('pmas')

    def _resolver_edificio_por_id(self, id_edificio):
        from mantenedores.models import Edificio
        # Mapeo id_legacy → Edificio via consulta puntual (cache)
        if not hasattr(self, '_edificio_id_map'):
            conn = abrir_mysql()
            cur = conn.cursor()
            cur.execute("SELECT id, edificios FROM tbedificios")
            self._edificio_id_map = {}
            for r in cur:
                ed = self.edificios_por_norm.get(normalizar(r['edificios']))
                if ed:
                    self._edificio_id_map[r['id']] = ed
            cur.close()
            conn.close()
        return self._edificio_id_map.get(id_edificio)

    # =========================================================
    # 4. InfraestructuraRed
    # =========================================================
    def migrar_ips_red(self, conn):
        from redes.models import InfraestructuraRed
        cur = conn.cursor()
        cur.execute("""SELECT id, ip_direccion, id_pma, vlan, switch_ip, switch_port, estado,
                       id_institucion, id_edificio, id_piso, id_unidad, sector, mac, rack, patch_panel
                       FROM tb_infraestructura_red ORDER BY id""")
        filas = list(cur)
        cur.close()
        for f in filas:
            ip = (f['ip_direccion'] or '').strip()
            if not ip:
                continue
            pma = self.map_pmas.get(f['id_pma']) if f['id_pma'] else None
            institucion = self.inst_por_codigo.get('HGF')  # todos son HGF
            edificio = self._resolver_edificio_por_id(f['id_edificio']) if f['id_edificio'] else None
            piso = None
            if f['id_piso']:
                # resolver piso via id_edificio+id_piso legacy
                if edificio:
                    cur2 = conn.cursor()
                    cur2.execute("SELECT pisos FROM tbpisos WHERE id=%s", (f['id_piso'],))
                    r = cur2.fetchone()
                    cur2.close()
                    if r:
                        piso = self.pisos_por_clave.get((normalizar(edificio.nombre), normalizar(r['pisos'])))
            unidad = self.map_unidades.get(f['id_unidad']) if f['id_unidad'] else None
            estado_norm = (f['estado'] or 'LIBRE').upper()
            estado = InfraestructuraRed.Estado.FALLA if 'FALLA' in estado_norm else (
                InfraestructuraRed.Estado.OCUPADO if 'OCUP' in estado_norm else InfraestructuraRed.Estado.LIBRE
            )
            obj, created = InfraestructuraRed.objects.get_or_create(
                ip_direccion=ip,
                defaults={
                    'pma': pma, 'switch_ip': f['switch_ip'], 'switch_port': f['switch_port'],
                    'estado': estado, 'institucion': institucion, 'edificio': edificio,
                    'piso': piso, 'unidad': unidad, 'sector': f['sector'], 'mac': f['mac'],
                    'rack': f['rack'], 'patch_panel': f['patch_panel'],
                },
            )
            self.map_ips_red[f['id']] = obj
            if created:
                self.rep.add_creado('ips_red')
            else:
                self.rep.add_omitido('ips_red')

    # =========================================================
    # 5. Usuarios (auth.User + PerfilUsuario + Rol)
    # =========================================================
    def migrar_usuarios(self, conn):
        from core.models import PerfilUsuario
        cur = conn.cursor()
        cur.execute("""SELECT id, nombre, rut, usuario, password, perfil, id_itsm_grupo, estado,
                       foto, ultimo_login, email, telefono, acta_config_json
                       FROM tbusuarios ORDER BY id""")
        filas = list(cur)
        cur.close()
        for f in filas:
            username = (f['usuario'] or '').strip()
            rut = (f['rut'] or '').strip()
            if not username:
                continue
            # Saltar si ya existe (ej. 55555555-5 creado en Fase 0)
            if User.objects.filter(username=username).exists():
                u = User.objects.get(username=username)
                self.map_usuarios[f['id']] = u
                self.rep.add_omitido('usuarios')
                continue
            nombre_completo = (f['nombre'] or '').strip()
            partes = nombre_completo.split(' ', 1)
            first_name = partes[0]
            last_name = partes[1] if len(partes) > 1 else ''
            # Hash bcrypt de PHP es compatible con Django (mismo formato $2a$...)
            u = User(
                username=username,
                password=f['password'],  # hash bcrypt original
                first_name=first_name[:150],
                last_name=last_name[:150],
                email=(f['email'] or '').strip(),
                is_active=bool(f['estado']),
                last_login=f['ultimo_login'],
            )
            if not self.dry:
                u.save()
            self.map_usuarios[f['id']] = u
            self.rep.add_creado('usuarios')

            # PerfilUsuario
            rol = self.map_roles.get((f['perfil'] or '').strip())
            rut_perfil = rut or f'LEG-{username}'
            # Evitar duplicados: si el rut ya existe en otro perfil, usar fallback unico
            from core.models import PerfilUsuario
            if PerfilUsuario.objects.filter(rut=rut_perfil).exclude(user=u).exists():
                rut_perfil = f'LEG-{f["id"]}-{username}'
            perfil, pc = PerfilUsuario.objects.get_or_create(
                user=u,
                defaults={
                    'rut': rut_perfil,
                    'unidad': 'TIC',
                    'cargo': (f['perfil'] or ''),
                    'grado': '',
                    'rol': rol,
                    'telefono': f['telefono'],
                },
            )
            if pc:
                self.rep.add_creado('perfiles_usuario')
            else:
                self.rep.add_omitido('perfiles_usuario')

    # =========================================================
    # 6. Equipos (FK a catálogos + ip_red)
    # =========================================================
    def migrar_equipos(self, conn):
        from equipos.models import Equipo
        cur = conn.cursor()
        cur.execute("""SELECT * FROM tblistaequipos ORDER BY id""")
        filas = list(cur)
        cur.close()
        for f in filas:
            serial = limpiar_serial(f['serialnumber'])
            if not serial or serial.lower() == 'generico':
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} sin serial valido ('{f['serialnumber']}')")
                continue
            if Equipo.objects.filter(serial_number=serial).exists():
                self.map_equipos[f['id']] = Equipo.objects.get(serial_number=serial)
                self.rep.add_omitido('equipos')
                continue
            # Resolver FKs: preferir id_* (FK normalizada), sino resolver texto
            articulo = self.articulos_por_norm.get(normalizar(f['articulo']))
            if not articulo and f['id_articulo']:
                articulo = self._resolver_articulo_por_id(f['id_articulo'])
            marca = self.marcas_por_norm.get(normalizar(f['marca']))
            if not marca and f['id_marca']:
                marca = self._resolver_marca_por_id(f['id_marca'])
            modelo = self.map_modelos.get(f['id_modelo']) if f['id_modelo'] else None
            if not modelo and marca:
                from mantenedores.models import Modelo
                modelo = Modelo.objects.filter(marca=marca, nombre__iexact=normalizar(f['modelo'])).first()
            edificio = self._resolver_edificio_por_id(f['id_edificio']) if f['id_edificio'] else None
            if not edificio:
                edificio = self.edificios_por_norm.get(normalizar(f['edificio']))
            piso = None
            if f['id_piso']:
                if edificio:
                    cur2 = conn.cursor()
                    cur2.execute("SELECT pisos FROM tbpisos WHERE id=%s", (f['id_piso'],))
                    r = cur2.fetchone()
                    cur2.close()
                    if r:
                        piso = self.pisos_por_clave.get((normalizar(edificio.nombre), normalizar(r['pisos'])))
            if not piso and edificio:
                piso = self.pisos_por_clave.get((normalizar(edificio.nombre), normalizar(f['piso'])))
            unidad = self.map_unidades.get(f['id_unidad']) if f['id_unidad'] else None
            if not unidad:
                unidad_nombre = normalizar(f['unidadservicio'])
                from mantenedores.models import Unidad
                unidad = Unidad.objects.filter(nombre__iexact=unidad_nombre).first() if unidad_nombre else None
            so = self.so_por_norm.get(normalizar(f['so']))
            if not so and f['id_so']:
                so = self._resolver_so_por_id(f['id_so'])
            estado = self.estados_por_norm.get(normalizar(f['estado']))
            if not estado and f['id_estado']:
                estado = self._resolver_estado_por_id(f['id_estado'])
            proveedor = self.proveedores_por_norm.get(normalizar(f['proveedor']))
            ip_red = self.map_ips_red.get(f['id_ip_red']) if f['id_ip_red'] else None
            modificado_por = self.map_usuarios.get(f.get('usuario_modificador_id')) if f.get('usuario_modificador_id') else None
            # usuario_modificador en PHP es texto (nombre), no id. No mapeable a FK directo.

            if not articulo:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin articulo resoluble ('{f['articulo']}')")
                continue
            if not marca:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin marca resoluble ('{f['marca']}')")
                continue
            if not estado:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin estado resoluble ('{f['estado']}')")
                continue
            if not modelo:
                # Crear modelo al vuelo si no existe
                from mantenedores.models import Modelo
                modelo, mc = Modelo.objects.get_or_create(
                    marca=marca, nombre=normalizar(f['modelo']) or 'Generico',
                    defaults={'activo': True},
                )
                self.map_modelos[f['id_modelo']] = modelo if f['id_modelo'] else None
            if not edificio:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin edificio resoluble ('{f['edificio']}')")
                continue
            if not piso:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin piso resoluble ('{f['piso']}', id_piso={f['id_piso']})")
                continue
            if not unidad:
                self.rep.add_no_macheo('equipos', f"Equipo id={f['id']} serial={serial} sin unidad resoluble ('{f['unidadservicio']}')")
                continue

            ip = (f['ip'] or '').strip()
            if ip and ip.lower() in ('usb', 'sip', 'nd', 'n/a', 'no', '-', 'red oculta', 'no definido', 'no aplica'):
                ip = None
            if ip:
                # Validar que sea IP real
                import ipaddress
                try:
                    ipaddress.ip_address(ip)
                except ValueError:
                    ip = None

            eq = Equipo(
                articulo=articulo, marca=marca, modelo=modelo, edificio=edificio,
                piso=piso, unidad=unidad, so=so, estado=estado, proveedor=proveedor,
                serial_number=serial, ip=ip or None, anexo=(f['anexo'] or '').strip() or None,
                usuario=(f['usuario'] or '').strip() or None, office=(f['office'] or '').strip() or None,
                activador=(f['activador'] or '').strip() or None,
                pmalugar=(f['pmalugar'] or '').strip() or None,
                comentario=(f['comentario'] or '').strip() or None,
                ip_red=ip_red,
            )
            if not self.dry:
                eq.save()  # dispara audit trail signal (MOVIMIENTO alta)
            self.map_equipos[f['id']] = eq
            self.rep.add_creado('equipos')

    def _resolver_articulo_por_id(self, id_art):
        if not hasattr(self, '_art_id_map'):
            conn = abrir_mysql()
            cur = conn.cursor()
            cur.execute("SELECT id, articulos FROM tbarticulos")
            self._art_id_map = {}
            for r in cur:
                a = self.articulos_por_norm.get(normalizar(r['articulos']))
                if a:
                    self._art_id_map[r['id']] = a
            cur.close(); conn.close()
        return self._art_id_map.get(id_art)

    def _resolver_marca_por_id(self, id_marca):
        if not hasattr(self, '_marca_id_map'):
            conn = abrir_mysql()
            cur = conn.cursor()
            cur.execute("SELECT id, marca FROM tbmarca")
            self._marca_id_map = {}
            for r in cur:
                m = self.marcas_por_norm.get(normalizar(r['marca']))
                if m:
                    self._marca_id_map[r['id']] = m
            cur.close(); conn.close()
        return self._marca_id_map.get(id_marca)

    def _resolver_so_por_id(self, id_so):
        if not hasattr(self, '_so_id_map'):
            conn = abrir_mysql()
            cur = conn.cursor()
            cur.execute("SELECT id, so FROM tbso")
            self._so_id_map = {}
            for r in cur:
                s = self.so_por_norm.get(normalizar(r['so']))
                if s:
                    self._so_id_map[r['id']] = s
            cur.close(); conn.close()
        return self._so_id_map.get(id_so)

    def _resolver_estado_por_id(self, id_estado):
        if not hasattr(self, '_estado_id_map'):
            conn = abrir_mysql()
            cur = conn.cursor()
            cur.execute("SELECT id, estado FROM tbestado")
            self._estado_id_map = {}
            for r in cur:
                e = self.estados_por_norm.get(normalizar(r['estado']))
                if e:
                    self._estado_id_map[r['id']] = e
            cur.close(); conn.close()
        return self._estado_id_map.get(id_estado)

    # =========================================================
    # 7. BitacoraOpciones + BitacoraEquipo
    # =========================================================
    def migrar_bitacora_opciones(self, conn):
        from equipos.models import BitacoraOpcion
        cur = conn.cursor()
        cur.execute("SELECT id, tipo, nombre, activo, orden FROM tb_bitacora_opciones ORDER BY id")
        filas = list(cur)
        cur.close()
        for f in filas:
            tipo = f['tipo']
            if tipo not in ('FALLA', 'ACTIVIDAD'):
                continue
            obj, created = BitacoraOpcion.objects.get_or_create(
                tipo=tipo, nombre=f['nombre'],
                defaults={'activo': bool(f['activo']), 'orden': f['orden']},
            )
            if created:
                self.rep.add_creado('bitacora_opciones')
            else:
                self.rep.add_omitido('bitacora_opciones')

    def migrar_bitacora_equipos(self, conn):
        from equipos.models import BitacoraEquipo
        cur = conn.cursor()
        cur.execute("""SELECT id, id_equipo, id_usuario_tecnico, fecha_mantenimiento, fecha_devolucion,
                       solicitante, falla_reportada, actividades_realizadas, servicio_unidad, tipo_registro, fecha_creacion
                       FROM tb_bitacora_equipos ORDER BY id""")
        filas = list(cur)
        cur.close()
        usuario_sistema = User.objects.filter(is_superuser=True).first()
        for f in filas:
            equipo = self.map_equipos.get(f['id_equipo'])
            if not equipo:
                continue  # equipo no migrado (filtro de serial valido)
            tecnico = self.map_usuarios.get(f['id_usuario_tecnico']) or usuario_sistema
            tipo = f['tipo_registro'] or 'MANTENCION'
            if tipo not in dict(BitacoraEquipo.TipoRegistro.choices):
                tipo = BitacoraEquipo.TipoRegistro.MANTENCION
            # Desactivar signals para no recalcular estado ni auditar la migracion
            equipo._skip_audit = True
            b = BitacoraEquipo(
                equipo=equipo, tecnico=tecnico,
                fecha_mantenimiento=f['fecha_mantenimiento'],
                fecha_devolucion=f['fecha_devolucion'],
                solicitante=f['solicitante'], falla_reportada=f['falla_reportada'],
                actividades_realizadas=f['actividades_realizadas'],
                servicio_unidad=f['servicio_unidad'], tipo_registro=tipo,
            )
            if not self.dry:
                # Usar bulk_create para saltar signals? No: queremos validar.
                # Pero el signal post_save de BitacoraEquipo recalcula estado. Lo desactivamos temporalmente.
                from django.db.models.signals import post_save
                from equipos.signals import recalcular_estado_equipo
                post_save.disconnect(recalcular_estado_equipo, sender=BitacoraEquipo)
                try:
                    b.save()
                finally:
                    post_save.connect(recalcular_estado_equipo, sender=BitacoraEquipo)
            self.rep.add_creado('bitacora_equipos')

    # =========================================================
    # 8. Anexos + Requerimientos
    # =========================================================
    def migrar_anexos(self, conn):
        from anexos.models import Anexo, RequerimientoCambio
        cur = conn.cursor()
        cur.execute("""SELECT * FROM anexos ORDER BY id""")
        filas = list(cur)
        cur.close()
        for f in filas:
            num = (f['numero_anexo'] or '').strip()
            serial = limpiar_serial(f['serial_number'])
            if not num:
                continue
            if Anexo.objects.filter(numero_anexo=num).exists():
                self.map_anexos[f['id']] = Anexo.objects.get(numero_anexo=num)
                self.rep.add_omitido('anexos')
                continue
            edificio = self.edificios_por_norm.get(normalizar(f['edificio']))
            piso = None
            if edificio:
                piso = self.pisos_por_clave.get((normalizar(edificio.nombre), normalizar(f['piso'])))
            unidad = None
            un = normalizar(f['servicio_unidad'])
            if un:
                from mantenedores.models import Unidad
                unidad = Unidad.objects.filter(nombre__iexact=un).first()
            proveedor = self.proveedores_por_norm.get(normalizar(f['proveedor']))
            modelo_anexo = None
            mn = normalizar(f['modelo'])
            if mn:
                from mantenedores.models import ModeloAnexo
                modelo_anexo = ModeloAnexo.objects.filter(nombre__iexact=mn).first()
            ip = (f['ip'] or '').strip()
            if ip and not ip.replace('.', '').isdigit():
                ip = None
            creado_por = None  # creado_por en PHP es texto (nombre), no id
            estado = Anexo.Estado.INACTIVO if (f['estado'] or '').upper() == 'INACTIVO' else Anexo.Estado.ACTIVO
            ax = Anexo(
                numero_anexo=num, marca=(f['marca'] or '').strip(), modelo=(f['modelo'] or '').strip(),
                modelo_anexo=modelo_anexo, edificio=edificio, piso=piso, unidad=unidad,
                pma_lugar=(f['lugar_pma'] or '').strip(), proveedor=proveedor, estado=estado,
                serial_number=serial or num, ip=ip or None,
                comentario=(f['comentario'] or '').strip() or None,
                grupo=(f['grupo'] or '').strip() or None,
                establecimiento=self.inst_por_codigo.get('HGF'),
            )
            if not self.dry:
                ax.save()
            self.map_anexos[f['id']] = ax
            self.rep.add_creado('anexos')

            # RequerimientoCambio: si tiene campos de cambio de visor, crear registro
            if any([f.get('tipo'), f.get('sub_requerimiento'), f.get('accion'),
                    f.get('nombre_usuario_req'), f.get('cambiar_dos_anexos') == 'Si',
                    f.get('cascada')]):
                rc = RequerimientoCambio(
                    anexo=ax,
                    tipo=f.get('tipo'), sub_requerimiento=f.get('sub_requerimiento'),
                    accion=f.get('accion'), nombre_usuario_req=f.get('nombre_usuario_req'),
                    ubicacion_req=f.get('ubicacion_req'), estado_req=f.get('estado_req'),
                    grupo_captura=f.get('grupo_captura'),
                    cambiar_dos_anexos=(f.get('cambiar_dos_anexos') == 'Si'),
                    numero_anexo_cambio=f.get('numero_anexo_cambio'),
                    cascada=bool(f.get('cascada')),
                    observacion=f.get('observacion_req'),
                )
                if not self.dry:
                    rc.save()
                self.rep.add_creado('requerimientos')

    def migrar_requerimientos(self, conn):
        # Ya migrados en migrar_anexos (extraidos de campos de anexos)
        pass

    # =========================================================
    # 9. Actas + ActaDetalle (con firmas base64 → archivos)
    # =========================================================
    def migrar_actas(self, conn):
        from actas.models import Acta, ActaDetalle
        cur = conn.cursor()
        cur.execute("""SELECT id, codigo, receptor_nombre, receptor_rut, receptor_cargo, receptor_unidad,
                       encargado, observaciones, fecha, pdf_generado, pdf_firmado,
                       firma_receptor, firma_encargado, timbre_encargado, email_receptor, estado, fecha_envio
                       FROM actas ORDER BY id""")
        filas = list(cur)
        cur.close()
        encargado_sistema = User.objects.filter(is_superuser=True).first()
        for f in filas:
            codigo = (f['codigo'] or '').strip()
            if not codigo or Acta.objects.filter(codigo=codigo).exists():
                self.rep.add_omitido('actas')
                continue
            # Decodificar firmas base64 → archivos
            firma_r = decodificar_firma_base64(f['firma_receptor'], 'actas/firmas', self.media_root)
            firma_e = decodificar_firma_base64(f['firma_encargado'], 'actas/firmas', self.media_root)
            timbre = decodificar_firma_base64(f['timbre_encargado'], 'actas/timbres', self.media_root)
            # encargado es texto (nombre), no id. Mapear al superuser por defecto.
            encargado = encargado_sistema
            estado = f['estado'] or 'emitido'
            if estado not in dict(Acta.Estado.choices):
                estado = Acta.Estado.EMITIDO
            a = Acta(
                codigo=codigo, receptor_nombre=f['receptor_nombre'], receptor_rut=f['receptor_rut'],
                receptor_cargo=f['receptor_cargo'], receptor_unidad=f['receptor_unidad'],
                encargado=encargado, observaciones=f['observaciones'], estado=estado,
                email_receptor=f['email_receptor'], fecha_envio=f['fecha_envio'],
            )
            # Asignar ImageFields con ruta relativa
            if firma_r and not self.dry:
                a.firma_receptor.name = firma_r
            if firma_e and not self.dry:
                a.firma_encargado.name = firma_e
            if timbre and not self.dry:
                a.timbre_encargado.name = timbre
            if not self.dry:
                a.save()
            self.rep.add_creado('actas')

            # Detalles
            cur2 = conn.cursor()
            cur2.execute("SELECT * FROM actas_detalles WHERE id_acta=%s", (f['id'],))
            for d in cur2:
                edificio = self.edificios_por_norm.get(normalizar(d['edificio'])) if d['edificio'] else None
                piso = None
                if edificio and d['piso']:
                    piso = self.pisos_por_clave.get((normalizar(edificio.nombre), normalizar(d['piso'])))
                unidad = None
                if d['unidad']:
                    from mantenedores.models import Unidad
                    unidad = Unidad.objects.filter(nombre__iexact=normalizar(d['unidad'])).first()
                det = ActaDetalle(
                    acta=a, tipo_item=d['tipo_item'] or 'EQUIPO', id_item=d['id_item'],
                    articulo=d['articulo'], serie=d['serie'], edificio=edificio, piso=piso,
                    unidad=unidad, pma_lugar=d['pmalugar'], estado=d['estado'],
                )
                if not self.dry:
                    det.save()
                self.rep.add_creado('actas_detalles')
            cur2.close()

        # Consolidar actas_entrega (legacy) — solo los no duplicados por codigo/beneficiario
        cur2 = conn.cursor()
        cur2.execute("SELECT * FROM actas_entrega ORDER BY id_acta")
        for f in cur2:
            codigo = f"LEG-{f['id_acta']}"
            if Acta.objects.filter(codigo=codigo).exists():
                continue
            a = Acta(
                codigo=codigo, receptor_nombre=f['beneficiario'] or 'N/A',
                receptor_rut=f['rut'], receptor_cargo=f['cargo'],
                receptor_unidad=f['servicio_unidad'],
                encargado=encargado_sistema, observaciones=f['observaciones'],
                estado='emitido',
            )
            if not self.dry:
                a.save()
            self.rep.add_creado('actas_entrega_legacy')
        cur2.close()

    # =========================================================
    # 10. Pendientes, AyudaRapida, WebApp, Checklist
    # =========================================================
    def migrar_pendientes(self, conn):
        from utilidades.models import Pendiente
        cur = conn.cursor()
        cur.execute("SELECT * FROM pendientes ORDER BY id")
        for f in cur:
            estado = Pendiente.Estado.RESUELTO if f['estado'] == 'resuelto' else Pendiente.Estado.PENDIENTE
            obj, c = Pendiente.objects.get_or_create(
                titulo=f['titulo'], defaults={'link': f['link'], 'estado': estado,
                                              'fecha_cierre': f['fecha_cierre'],
                                              'fecha_programada': f['fecha_programada']},
            )
            if c: self.rep.add_creado('pendientes')
            else: self.rep.add_omitido('pendientes')
        cur.close()

    def migrar_ayudas(self, conn):
        from utilidades.models import AyudaRapida
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_ayudas_rapidas ORDER BY id")
        for f in cur:
            obj, c = AyudaRapida.objects.get_or_create(
                titulo=f['titulo'],
                defaults={'contenido': f['codigo'] or f['descripcion'] or '',
                          'categoria': f['icono'], 'activo': bool(f['activo']), 'orden': f['orden']},
            )
            if c: self.rep.add_creado('ayudas')
            else: self.rep.add_omitido('ayudas')
        cur.close()

    def migrar_webapps(self, conn):
        from utilidades.models import WebApp
        cur = conn.cursor()
        cur.execute("SELECT * FROM tb_webapps ORDER BY id")
        for f in cur:
            obj, c = WebApp.objects.get_or_create(
                nombre=f['nombre'],
                defaults={'url': f['url'], 'icono': f['icono'], 'descripcion': f['descripcion'],
                          'activo': bool(f['activo']), 'orden': f['orden']},
            )
            if c: self.rep.add_creado('webapps')
            else: self.rep.add_omitido('webapps')
        cur.close()

    def migrar_checklist(self, conn):
        from utilidades.models import ChecklistItem
        cur = conn.cursor()
        cur.execute("SELECT * FROM checklist ORDER BY orden")
        for f in cur:
            obj, c = ChecklistItem.objects.get_or_create(
                task_name=f['task_name'],
                defaults={'is_completed': bool(f['is_completed']), 'activo': bool(f['activo']), 'orden': f['orden']},
            )
            if c: self.rep.add_creado('checklist')
            else: self.rep.add_omitido('checklist')
        cur.close()

    # =========================================================
    # 11. Correos (Grupos + Miembros + Credenciales)
    # =========================================================
    def migrar_correos(self, conn):
        from correos.models import GrupoCorreo, MiembroGrupoCorreo, CredencialCorreo
        # Catálogo de grupos
        cur = conn.cursor()
        cur.execute("SELECT * FROM email_grupos_catalogo ORDER BY orden")
        grupos_map = {}
        for f in cur:
            g, c = GrupoCorreo.objects.get_or_create(
                nombre=f['nombre'],
                defaults={'descripcion': f['descripcion'], 'orden': f['orden'], 'activo': bool(f['estado'])},
            )
            grupos_map[f['id']] = g
            if c: self.rep.add_creado('grupos_correo')
            else: self.rep.add_omitido('grupos_correo')
        cur.close()
        # Miembros
        cur = conn.cursor()
        cur.execute("SELECT * FROM email_grupos ORDER BY id")
        for f in cur:
            g = grupos_map.get(f['grupo_id'])
            if not g:
                continue
            obj, c = MiembroGrupoCorreo.objects.get_or_create(grupo=g, email=f['email'])
            if c: self.rep.add_creado('miembros_grupo')
            else: self.rep.add_omitido('miembros_grupo')
        cur.close()
        # Credenciales (solo metadatos, NO el password)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbcorreos ORDER BY id LIMIT 5000")  # limitar: hay ~17M de registros historicos
        for f in cur:
            email = (f['correo'] or '').strip()
            if not email or '@' not in email:
                continue
            obj, c = CredencialCorreo.objects.get_or_create(
                email=email,
                defaults={'propietario': f['nombres'], 'departamento': f['servicios'], 'activo': True},
            )
            if c: self.rep.add_creado('credenciales_correo')
            else: self.rep.add_omitido('credenciales_correo')
        cur.close()

    # =========================================================
    # 12. RangoIP (colapso de 12 tablas tbconexionespiso*)
    # =========================================================
    def migrar_rangos_ip(self, conn):
        from redes.models import RangoIP
        from mantenedores.models import Piso
        # Mapear tbpisos → Piso (ya tenemos piso_legacy_map construido en migrar_pmas)
        # Reconstruirlo aquí si no existe
        if not hasattr(self, '_piso_legacy_map'):
            cur = conn.cursor()
            cur.execute("SELECT id, pisos, id_edificio FROM tbpisos")
            self._piso_legacy_map = {}
            for r in cur:
                ed = self._resolver_edificio_por_id(r['id_edificio'])
                if ed:
                    p = self.pisos_por_clave.get((normalizar(ed.nombre), normalizar(r['pisos'])))
                    if p:
                        self._piso_legacy_map[r['id']] = p
            cur.close()

        # Colapsar las 12 tablas: tbconexionespiso1..7, tbconexionespisoMenos1, tbconexioneszocalo
        tablas_pisos = [
            ('tbconexionespiso1', 27),      # Hospital Nuevo piso 1 (tbpisos id=27)
            ('tbconexionespiso2', 26),      # id=26
            ('tbconexionespiso3', 25),      # id=25
            ('tbconexionespiso4', 24),      # id=24
            ('tbconexionespiso5', 23),      # id=23
            ('tbconexionespiso6', 22),      # id=22
            ('tbconexionespiso7', 21),      # id=21
            ('tbconexionespisoMenos1', 31), # id=31
            ('tbconexioneszocalo', 29),     # id=29 (Zócalo)
        ]
        for tabla, id_piso_legacy in tablas_pisos:
            piso = self._piso_legacy_map.get(id_piso_legacy)
            if not piso:
                self.rep.add_no_macheo('rangos_ip', f"Tabla {tabla}: piso legacy id={id_piso_legacy} no resoluble")
                continue
            cur = conn.cursor()
            try:
                cur.execute(f"SELECT unidad, ubicacion, pma, rack, dato, rango, ip, estado, comentario FROM {tabla}")
            except Exception:
                cur.close()
                continue
            for f in cur:
                ip = (f['ip'] or '').strip()
                if not ip or ip == 'N/A':
                    continue
                # ip en estas tablas es el último octeto (string), rango es "10.67.18"
                # Construir IP completa si es solo el octeto
                ip_completa = ip
                if f['rango'] and ip.count('.') < 3:
                    ip_completa = f"{f['rango']}.{ip}"
                try:
                    import ipaddress
                    ipaddress.ip_address(ip_completa)
                except ValueError:
                    continue
                obj, c = RangoIP.objects.get_or_create(
                    ip=ip_completa, piso=piso,
                    defaults={'unidad': f['unidad'] or '', 'ubicacion': f['ubicacion'] or '',
                              'pma': f['pma'] or '', 'rack': f['rack'] or '',
                              'dato': f['dato'] or '', 'rango': f['rango'] or '',
                              'estado': bool(f['estado']), 'comentario': f['comentario'] or ''},
                )
                if c: self.rep.add_creado('rangos_ip')
                else: self.rep.add_omitido('rangos_ip')
            cur.close()

    # =========================================================
    # 13. AvisoVisor
    # =========================================================
    def migrar_avisos_visor(self, conn):
        from visor.models import AvisoVisor
        cur = conn.cursor()
        try:
            cur.execute("SHOW TABLES LIKE 'tb_avisos_visor'")
            if not cur.fetchone():
                cur.close(); return
        except Exception:
            cur.close(); return
        cur.execute("SELECT * FROM tb_avisos_visor")
        cols = [d[0] for d in cur.description]
        for f in cur:
            d = dict(zip(cols, f))
            titulo = d.get('titulo') or d.get('nombre') or ''
            mensaje = d.get('mensaje') or d.get('contenido') or ''
            if not titulo:
                continue
            obj, c = AvisoVisor.objects.get_or_create(
                titulo=titulo, defaults={'mensaje': mensaje, 'activo': bool(d.get('activo', 1))},
            )
            if c: self.rep.add_creado('avisos_visor')
            else: self.rep.add_omitido('avisos_visor')
        cur.close()
