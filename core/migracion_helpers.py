"""
Helpers para la migracion de datos MySQL→PostgreSQL (Fase 5).

Funciones utilitarias usadas por el management command migrar_desde_mysql:
- Conexion PyMySQL al legacy.
- Resolucion texto→FK (normalizacion case-insensitive + limpieza).
- Decodificacion de firmas base64 → archivos ImageField.
- Logger con reporte de no-macheos.
"""
import base64
import os
import re
from pathlib import Path

import pymysql


def abrir_mysql():
    """Abre conexion PyMySQL a la BD legacy (XAMPP MariaDB)."""
    return pymysql.connect(
        host='localhost',
        user='root',
        db='equipamiento2026',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.SSDictCursor,
    )


def normalizar(texto):
    """Normaliza un texto para comparacion FK: strip, quita espacios dobles, upper."""
    if texto is None:
        return ''
    s = str(texto).strip()
    # Reparar caracteres con encoding roto (Z?calo -> Zócalo)
    s = s.replace('?calo', 'ócalo').replace('Recepci?n', 'Recepción')
    s = re.sub(r'\s+', ' ', s)
    return s


def limpiar_serial(serial):
    """Limpia un serial number: quita tabs/espacios internos accidentales."""
    if not serial:
        return ''
    return re.sub(r'\s+', '', str(serial).strip())


class ReporteMigracion:
    """Acumula conteos y no-macheos durante la migracion para reporte final."""
    def __init__(self):
        self.creados = {}
        self.omitidos = {}
        self.no_macheos = {}

    def add_creado(self, entidad, n=1):
        self.creados[entidad] = self.creados.get(entidad, 0) + n

    def add_omitido(self, entidad, n=1):
        self.omitidos[entidad] = self.omitidos.get(entidad, 0) + n

    def add_no_macheo(self, entidad, detalle):
        self.no_macheos.setdefault(entidad, []).append(detalle)

    def resumen(self):
        out = ['\n=== REPORTE DE MIGRACION ===']
        out.append('\n[Creados]')
        for k in sorted(self.creados):
            out.append(f'  {k:30} {self.creados[k]}')
        out.append('\n[Omitidos (ya existian / duplicados)]')
        for k in sorted(self.omitidos):
            out.append(f'  {k:30} {self.omitidos[k]}')
        if self.no_macheos:
            out.append('\n[NO-MACHEOS (revisar manualmente)]')
            for k in sorted(self.no_macheos):
                out.append(f'  {k}: {len(self.no_macheos[k])} casos')
                for d in self.no_macheos[k][:10]:
                    out.append(f'    - {d}')
                if len(self.no_macheos[k]) > 10:
                    out.append(f'    ... y {len(self.no_macheos[k]) - 10} mas')
        return '\n'.join(out)


def decodificar_firma_base64(data_uri, ruta_destino, media_root):
    """Decodifica una firma base64 (data:image/png;base64,...) a archivo PNG.
    Devuelve la ruta relativa para ImageField, o None si falla.
    """
    if not data_uri or not data_uri.startswith('data:image'):
        return None
    try:
        # Separar header del base64
        header, b64 = data_uri.split(',', 1)
        ext = 'png' if 'png' in header else 'jpg'
        # Asegurar directorio
        dir_dest = Path(media_root) / ruta_destino
        dir_dest.mkdir(parents=True, exist_ok=True)
        # Nombre unico basado en hash del contenido
        import hashlib
        nombre = hashlib.md5(b64.encode('ascii', errors='ignore')).hexdigest()[:16] + f'.{ext}'
        ruta = dir_dest / nombre
        if not ruta.exists():
            with open(ruta, 'wb') as f:
                f.write(base64.b64decode(b64))
        # Devolver ruta relativa para ImageField
        return f'{ruta_destino}/{nombre}'
    except Exception:
        return None
