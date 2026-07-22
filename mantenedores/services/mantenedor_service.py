from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from core.utils import normalizar_nombre, normalizar_codigo

from mantenedores.models import (
    Edificio, Piso, Sector, Unidad, AreaHospitalaria, Recinto, PMA,
    Articulo, Marca, Modelo, ModeloAnexo, SistemaOperativo, EstadoEquipo,
    Proveedor, Institucion, Cargo
)
from equipos.models import BitacoraOpcion
from tickets.models import GrupoResolutor, Categoria
from mantenedores.repositories.mantenedor_repository import MantenedorRepository


MODEL_MAP = {
    'articulo': Articulo,
    'area_hospitalaria': AreaHospitalaria,
    'categoria': Categoria,
    'edificio': Edificio,
    'grupo_resolutor': GrupoResolutor,
    'institucion': Institucion,
    'estados': EstadoEquipo,
    'fallas_bitacora': BitacoraOpcion,
    'marca': Marca,
    'modelo': Modelo,
    'modeloanexo': ModeloAnexo,
    'piso': Piso,
    'pma': PMA,
    'proveedor': Proveedor,
    'recinto': Recinto,
    'sector': Sector,
    'sistemaoperativo': SistemaOperativo,
    'unidad': Unidad,
    'cargo': Cargo,
}


class MantenedorService:

    @staticmethod
    def _get_modelo_class(modelo_nombre):
        cls = MODEL_MAP.get(modelo_nombre.lower())
        if not cls:
            from core.models import Funcionario
            if modelo_nombre.lower() == 'funcionario':
                return Funcionario
            raise ValidationError(f"Modelo '{modelo_nombre}' no válido.")
        return cls

    @staticmethod
    def obtener_item_por_id(modelo_nombre, item_id):
        cls = MantenedorService._get_modelo_class(modelo_nombre)
        return MantenedorRepository.get_by_id(cls, item_id)

    @staticmethod
    def _validar_fk(field_name, value):
        """Valida que un valor de ForeignKey sea un entero positivo o vacío."""
        if not value:
            return None
        try:
            v = int(value)
            if v <= 0:
                raise ValueError
            return v
        except (ValueError, TypeError):
            raise ValidationError(
                f"El campo '{field_name}' no es válido. Debe seleccionar un valor de la lista."
            )

    @staticmethod
    def _validar_duplicado(cls, nombre, extra_filters=None, exclude_id=None):
        """Verifica duplicados antes de full_clean() para mensajes en español."""
        if not nombre:
            return
        qs = cls.objects.all()
        if exclude_id:
            qs = qs.exclude(pk=exclude_id)
        unique_fields = [f.name for f in cls._meta.fields if f.unique and f.name == 'nombre']
        if unique_fields and qs.filter(nombre__iexact=nombre).exists():
            raise ValidationError(f"Ya existe '{nombre}'.")
        constraints = cls._meta.constraints
        for constraint in constraints:
            if hasattr(constraint, 'fields') and 'nombre' in constraint.fields:
                filters = {}
                for f in constraint.fields:
                    if f == 'nombre':
                        filters['nombre__iexact'] = nombre
                    elif extra_filters and f in extra_filters:
                        filters[f] = extra_filters[f]
                if filters and qs.filter(**filters).exists():
                    raise ValidationError(f"Ya existe '{nombre}' en esta combinación.")

    @staticmethod
    def crear_item(modelo_nombre, datos, usuario, archivos=None):
        cls = MantenedorService._get_modelo_class(modelo_nombre)
        
        if modelo_nombre == 'funcionario':
            rut = datos.get('rut', '').strip().upper()
            nombres = datos.get('nombres', '').strip()
            apellidos = datos.get('apellidos', '').strip()
            if not rut or not nombres or not apellidos:
                raise ValidationError("RUT, Nombres y Apellidos son obligatorios.")
            
            if cls.objects.filter(rut=rut).exists():
                raise ValidationError(f"Ya existe un funcionario con el RUT '{rut}'.")
                
            kwargs = {
                'rut': rut,
                'nombres': nombres,
                'apellidos': apellidos,
                'correo': datos.get('correo', ''),
            }
            if datos.get('cargo'):
                kwargs['cargo_id'] = MantenedorService._validar_fk('cargo', datos.get('cargo'))
            if datos.get('unidad'):
                kwargs['unidad_id'] = MantenedorService._validar_fk('unidad', datos.get('unidad'))
                
            instance = cls(**kwargs)
            instance.full_clean()
            instance.save()
            return instance

        nombre = normalizar_nombre(datos.get('nombre'))
        # Para modelos de equipos y anexos, el nombre va en MAYÚSCULAS (ej: CP-7841)
        if modelo_nombre in ('modelo', 'modeloanexo'):
            nombre = nombre.upper() if nombre else nombre
        if not nombre:
            raise ValidationError("El nombre es obligatorio.")

        kwargs = {'nombre': nombre}

        # Mapa de campos adicionales (incluyendo nuevas entidades jerárquicas)
        extra_fields = {
            'edificio':          ['institucion'],
            'estados':           ['color_hex'],
            'fallas_bitacora':   ['tipo'],
            'institucion':       ['codigo'],
            'modelo':            ['marca'],
            'modeloanexo':       ['marca'],
            'piso':              ['alias', 'edificio'],
            'proveedor':         ['contacto', 'telefono', 'email', 'direccion', 'rut'],
            'sector':            ['piso'],
            'unidad':            ['area_hospitalaria'],
            'recinto':           ['piso', 'sector', 'unidad'],
            'pma':               ['recinto'],
            'grupo_resolutor':   ['descripcion', 'icono'],
        }
        # FKs de las nuevas entidades
        FK_FIELDS = {'edificio', 'marca', 'institucion', 'piso', 'sector', 'unidad', 'area_hospitalaria', 'recinto'}

        for f in extra_fields.get(modelo_nombre, []):
            v = datos.get(f)
            if f in FK_FIELDS:
                fk_val = MantenedorService._validar_fk(f, v)
                if fk_val is not None:
                    kwargs[f'{f}_id'] = fk_val
            elif f == 'color_hex' and v:
                kwargs[f] = v
            elif f == 'codigo' and v:
                kwargs[f] = normalizar_codigo(v)
            elif f in ('contacto', 'direccion') and v:
                kwargs[f] = normalizar_nombre(v)
            elif v is not None:
                kwargs[f] = v

        # Auto-calcular orden secuencial para fallas_bitacora
        if modelo_nombre == 'fallas_bitacora':
            ultimo = cls.objects.filter(tipo=datos.get('tipo', '')).order_by('-orden').first()
            kwargs['orden'] = (ultimo.orden + 1) if ultimo else 1

        instance = cls(**kwargs)
        extra = {}
        if modelo_nombre == 'edificio':
            extra['institucion'] = kwargs.get('institucion_id')
        elif modelo_nombre == 'piso':
            extra['edificio'] = kwargs.get('edificio_id')
        elif modelo_nombre == 'modelo':
            extra['marca'] = kwargs.get('marca_id')
        MantenedorService._validar_duplicado(cls, nombre, extra)

        if modelo_nombre in ('modelo', 'modeloanexo', 'articulo') and archivos and 'imagen' in archivos:
            instance.imagen = archivos['imagen']

        instance.full_clean()
        MantenedorRepository.save(instance)

        if modelo_nombre == 'grupo_resolutor' and 'miembros' in datos:
            miembros = datos.get('miembros')
            if isinstance(miembros, str):
                import json
                try:
                    miembros = json.loads(miembros)
                except:
                    pass
            if isinstance(miembros, list):
                instance.miembros.set(miembros)

        return instance

    @staticmethod
    def actualizar_item(modelo_nombre, item_id, datos, usuario, archivos=None):
        cls = MantenedorService._get_modelo_class(modelo_nombre)
        instance = MantenedorRepository.get_by_id(cls, item_id)
        if not instance:
            raise ValidationError("El registro no existe.")

        if modelo_nombre == 'funcionario':
            rut = datos.get('rut', '').strip().upper()
            if rut:
                if cls.objects.filter(rut=rut).exclude(id=item_id).exists():
                    raise ValidationError(f"Ya existe un funcionario con el RUT '{rut}'.")
                instance.rut = rut
            if 'nombres' in datos: instance.nombres = datos.get('nombres').strip()
            if 'apellidos' in datos: instance.apellidos = datos.get('apellidos').strip()
            if 'correo' in datos: instance.correo = datos.get('correo', '').strip()
            if 'cargo' in datos: 
                instance.cargo_id = MantenedorService._validar_fk('cargo', datos.get('cargo'))
            if 'unidad' in datos:
                instance.unidad_id = MantenedorService._validar_fk('unidad', datos.get('unidad'))
            
            instance.full_clean()
            instance.save()
            return instance

        if 'nombre' in datos:
            nombre = normalizar_nombre(datos.get('nombre'))
            # Para modelos de equipos y anexos, el nombre va en MAYÚSCULAS
            if modelo_nombre in ('modelo', 'modeloanexo'):
                nombre = nombre.upper() if nombre else nombre
            if not nombre:
                raise ValidationError("El nombre es obligatorio.")
            instance.nombre = nombre

        extra_fields = {
            'edificio':          ['institucion'],
            'estados':           ['color_hex'],
            'fallas_bitacora':   ['tipo'],
            'institucion':       ['codigo'],
            'modelo':            ['marca'],
            'modeloanexo':       ['marca'],
            'piso':              ['alias', 'edificio'],
            'proveedor':         ['contacto', 'telefono', 'email', 'direccion', 'rut'],
            'sector':            ['piso'],
            'unidad':            ['area_hospitalaria'],
            'recinto':           ['piso', 'sector', 'unidad'],
            'pma':               ['recinto'],
            'grupo_resolutor':   ['descripcion', 'icono'],
        }
        FK_FIELDS = {'edificio', 'marca', 'institucion', 'piso', 'sector', 'unidad', 'area_hospitalaria', 'recinto'}

        for f in extra_fields.get(modelo_nombre, []):
            if f in datos:
                v = datos.get(f)
                if f in FK_FIELDS:
                    fk_val = MantenedorService._validar_fk(f, v)
                    setattr(instance, f'{f}_id', fk_val)
                elif f == 'codigo' and v:
                    setattr(instance, f, normalizar_codigo(v))
                elif f in ('contacto', 'direccion') and v:
                    setattr(instance, f, normalizar_nombre(v))
                elif v is not None:
                    setattr(instance, f, v)

        activo = datos.get('activo')
        if activo is not None:
            instance.activo = bool(activo)

        extra = {}
        if modelo_nombre == 'edificio':
            extra['institucion'] = instance.institucion_id
        elif modelo_nombre == 'piso':
            extra['edificio'] = instance.edificio_id
        elif modelo_nombre in ('modelo', 'modeloanexo'):
            extra['marca'] = instance.marca_id
        MantenedorService._validar_duplicado(cls, instance.nombre, extra, exclude_id=item_id)
        
        if modelo_nombre in ('modelo', 'modeloanexo', 'articulo') and archivos and 'imagen' in archivos:
            instance.imagen = archivos['imagen']

        instance.full_clean()
        MantenedorRepository.save(instance)

        if modelo_nombre == 'grupo_resolutor' and 'miembros' in datos:
            miembros = datos.get('miembros')
            if isinstance(miembros, str):
                import json
                try:
                    miembros = json.loads(miembros)
                except:
                    pass
            if isinstance(miembros, list):
                instance.miembros.set(miembros)

        return instance

    @staticmethod
    def eliminar_item(modelo_nombre, item_id):
        cls = MantenedorService._get_modelo_class(modelo_nombre)
        instance = MantenedorRepository.get_by_id(cls, item_id)
        if not instance:
            raise ValidationError("El registro no existe.")
            
        if modelo_nombre == 'modelo' and instance.nombre.upper() in ('GENÉRICO', 'GENERICO'):
            raise ValidationError("No se puede eliminar el modelo Genérico porque actúa como valor por defecto del sistema.")
            
        if getattr(instance, 'is_system', False):
            raise ValidationError(f"No se puede eliminar <strong style='color:#dc3545'>{instance.nombre}</strong> porque es un registro protegido del sistema.")
            
        try:
            MantenedorRepository.delete(instance)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar <strong style='color:#dc3545'>{instance.nombre}</strong> porque está siendo usado por otros registros del sistema."
            )

    @classmethod
    def obtener_items_para_datatable(cls, modelo_nombre, start, length, search_value, order_col, order_dir, cols):
        cls_modelo = MantenedorService._get_modelo_class(modelo_nombre)

        order_name = 'nombre'
        if modelo_nombre == 'funcionario':
            order_name = 'nombres'
        if 0 <= order_col < len(cols):
            col_data = cols[order_col].get('data', 'nombre')
            if col_data != 'acciones':
                order_name = col_data
                if modelo_nombre == 'funcionario' and col_data == 'nombre':
                    order_name = 'nombres'

        records = MantenedorRepository.get_paginated_list(
            cls_modelo, start, length, search_value, order_name, order_dir,
        )
        total = MantenedorRepository.count_total(cls_modelo)
        filtered = MantenedorRepository.count_filtered(cls_modelo, search_value)

        data = []
        for idx, item in enumerate(records):
            if modelo_nombre == 'funcionario':
                unidad_str = item.unidad.nombre if item.unidad else ''
                cargo_str = item.cargo.nombre if item.cargo else ''
                row = {
                    'id': item.id,
                    'row_num': start + idx + 1,
                    'nombre': f"{item.nombres} {item.apellidos}",
                    'activo': True,
                    'rut': item.rut,
                    'nombres': item.nombres,
                    'apellidos': item.apellidos,
                    'correo': item.correo or '',
                    'cargo': cargo_str,
                    'unidad': unidad_str
                }
                data.append(row)
                continue

            row = {
                'id': item.id,
                'row_num': start + idx + 1,
                'nombre': item.nombre,
                'activo': item.activo,
            }
            # --- Entidades de infraestructura clásicas ---
            if modelo_nombre == 'edificio':
                row['institucion'] = item.institucion.nombre if item.institucion else ''
            elif modelo_nombre == 'institucion':
                row['codigo'] = item.codigo
            elif modelo_nombre == 'estados':
                row['color_hex'] = item.color_hex
            elif modelo_nombre == 'fallas_bitacora':
                row['tipo'] = item.tipo
            elif modelo_nombre == 'modelo':
                row['marca'] = item.marca.nombre if item.marca else ''
                row['imagen_url'] = item.imagen.url if item.imagen else ''
            elif modelo_nombre == 'modeloanexo':
                row['marca'] = item.marca.nombre if item.marca else ''
                row['imagen_url'] = item.imagen.url if item.imagen else ''
            elif modelo_nombre == 'piso':
                row['alias'] = item.alias or ''
                row['edificio'] = item.edificio.nombre if item.edificio else ''
            elif modelo_nombre == 'proveedor':
                row['contacto'] = item.contacto or ''
                row['rut'] = item.rut or ''
                row['telefono'] = item.telefono or ''
                row['email'] = item.email or ''
                row['direccion'] = item.direccion or ''
            # --- Nuevas entidades jerárquicas ---
            elif modelo_nombre == 'sector':
                row['piso'] = str(item.piso) if item.piso else ''
            elif modelo_nombre == 'unidad':
                row['area_hospitalaria'] = item.area_hospitalaria.nombre if item.area_hospitalaria else ''
            elif modelo_nombre == 'recinto':
                row['piso'] = str(item.piso) if item.piso else ''
                row['sector'] = item.sector.nombre if item.sector else ''
                row['unidad'] = item.unidad.nombre if item.unidad else ''
            elif modelo_nombre == 'pma':
                row['recinto'] = item.recinto.nombre if item.recinto else ''
                row['unidad'] = item.recinto.unidad.nombre if item.recinto and item.recinto.unidad else ''
                row['piso'] = str(item.recinto.piso) if item.recinto and item.recinto.piso else ''
            elif modelo_nombre == 'grupo_resolutor':
                row['miembros'] = [f"{u.first_name} {u.last_name}".strip() for u in item.miembros.all()]
            data.append(row)

        return {'recordsTotal': total, 'recordsFiltered': filtered, 'data': data}
