import os
import django
import pandas as pd
import math

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from equipos.models import Equipo
from mantenedores.models import Articulo, Marca, Modelo, EstadoEquipo, PMA

def load():
    print("Borrando equipos actuales...")
    Equipo.objects.all().delete()
    
    file_path = r'c:\proyectos\ticsystem\doccs\Entrega equipos Marga_Marga PISOS.xlsx'
    print(f"Leyendo Excel: {file_path}")
    df = pd.read_excel(file_path, sheet_name='DATOS PISO 1 AA')
    
    # Tomar solo los primeros 10
    df = df.head(10)
    
    # Valores por defecto para FKs obligatorios
    articulo, _ = Articulo.objects.get_or_create(nombre='Computador de Escritorio AIO')
    marca, _ = Marca.objects.get_or_create(nombre='Lenovo')
    modelo, _ = Modelo.objects.get_or_create(nombre='Desconocido', marca=marca)
    estado, _ = EstadoEquipo.objects.get_or_create(nombre='Operativo', color_hex='#10b981')
    
    col_pma = df.columns[0] # N° PMA
    
    for idx, row in df.iterrows():
        pma_val = str(row[col_pma]) if not pd.isna(row[col_pma]) else ''
        pma_obj = None
        if pma_val:
            pma_obj, _ = PMA.objects.get_or_create(nombre=pma_val)
            
        ip = str(row['IP']) if not pd.isna(row['IP']) else None
        
        # Ojo con nan o NAT en numeros de orden
        orden = row['ORDEN INTERNO']
        orden = int(orden) if not pd.isna(orden) else None
        
        serial = str(row['SERIE']) if not pd.isna(row['SERIE']) else f'SN-DUMMY-{idx}'
        serie_corta = str(row['SERIE EQUIPO']) if not pd.isna(row['SERIE EQUIPO']) else ''
        candado = str(row['CANDADO']) if not pd.isna(row['CANDADO']) else ''
        correlativo = str(row['CORRELATIVO']) if not pd.isna(row['CORRELATIVO']) else ''
        lugar = str(row['NOMBRE DE RECINTO']) if not pd.isna(row['NOMBRE DE RECINTO']) else ''
        
        print(f"Creando equipo {idx+1}: {serial}")
        
        Equipo.objects.create(
            articulo=articulo,
            marca=marca,
            modelo=modelo,
            estado=estado,
            pma=pma_obj,
            serial_number=serial,
            serie_corta=serie_corta,
            ip=ip,
            orden_interno=orden,
            estado_candado=candado,
            correlativo=correlativo,
            pmalugar=lugar
        )
        
    print("¡Proceso finalizado! Se agregaron 10 equipos.")

if __name__ == '__main__':
    load()
