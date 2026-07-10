import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error
from mantenedores.models import (
    Institucion, Edificio, Piso, Sector, AreaHospitalaria, Unidad, Recinto, PMA,
    Articulo, Marca, Modelo, ModeloAnexo, SistemaOperativo, EstadoEquipo, Proveedor,
)
from equipos.models import BitacoraOpcion


MODELOS_INFO = [
    # --- Infraestructura Técnica ---
    {'key': 'articulo',          'label': 'Artículos',             'icon': 'tag',           'fields': ['nombre'],                              'grupo': 'tecnico'},
    {'key': 'fallas_bitacora',   'label': 'Fallas Bitácora',       'icon': 'clipboard-list','fields': ['tipo', 'nombre', 'orden'],              'grupo': 'tecnico'},
    {'key': 'marca',             'label': 'Marcas',                'icon': 'trademark',     'fields': ['nombre'],                              'grupo': 'tecnico'},
    {'key': 'modelo',            'label': 'Modelos',               'icon': 'microchip',     'fields': ['nombre', 'marca'],                     'grupo': 'tecnico'},
    {'key': 'modeloanexo',       'label': 'Modelos de Anexos',     'icon': 'phone',         'fields': ['nombre'],                              'grupo': 'tecnico'},
    {'key': 'proveedor',         'label': 'Proveedores',           'icon': 'truck',         'fields': ['nombre'],                              'grupo': 'tecnico'},
    {'key': 'sistemaoperativo',  'label': 'Sistemas Operativos',   'icon': 'desktop',       'fields': ['nombre'],                              'grupo': 'tecnico'},
    # --- Infraestructura Física ---
    {'key': 'institucion',       'label': 'Instituciones',         'icon': 'university',    'fields': ['nombre', 'codigo'],                    'grupo': 'fisica'},
    {'key': 'edificio',          'label': 'Edificios',             'icon': 'building',      'fields': ['nombre', 'institucion'],               'grupo': 'fisica'},
    {'key': 'piso',              'label': 'Pisos',                 'icon': 'layer-group',   'fields': ['nombre', 'alias', 'edificio'],         'grupo': 'fisica'},
    {'key': 'sector',            'label': 'Sectores',              'icon': 'map-marker-alt','fields': ['nombre', 'piso'],                      'grupo': 'fisica'},
    # --- Infraestructura Hospitalaria ---
    {'key': 'area_hospitalaria', 'label': 'Áreas Hospitalarias',    'icon': 'hospital',      'fields': ['nombre'],                              'grupo': 'hospitalaria'},
    {'key': 'unidad',            'label': 'Unidades / Servicios',  'icon': 'sitemap',       'fields': ['nombre', 'area_hospitalaria'],          'grupo': 'hospitalaria'},
    {'key': 'recinto',           'label': 'Recintos',              'icon': 'door-open',     'fields': ['nombre', 'piso', 'sector', 'unidad'],  'grupo': 'hospitalaria'},
    {'key': 'pma',               'label': 'PMAs',                  'icon': 'plug',          'fields': ['nombre', 'recinto'],                   'grupo': 'hospitalaria'},
]


class MantenedoresDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'mantenedores/mantenedores.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['modelos'] = MODELOS_INFO
        # Listas para selects del formulario modal
        ctx['instituciones'] = list(Institucion.objects.filter(activo=True).values('id', 'nombre'))
        ctx['edificios'] = list(
            Edificio.objects.filter(activo=True)
            .select_related('institucion')
            .values('id', 'nombre', 'institucion__nombre', 'institucion_id')
        )
        ctx['pisos'] = list(
            Piso.objects.filter(activo=True)
            .select_related('edificio')
            .values('id', 'nombre', 'alias', 'edificio__nombre', 'edificio_id')
        )
        ctx['sectores'] = list(
            Sector.objects.filter(activo=True)
            .select_related('piso', 'piso__edificio')
            .values('id', 'nombre', 'piso_id', 'piso__nombre', 'piso__edificio__nombre')
        )
        ctx['areas'] = list(AreaHospitalaria.objects.filter(activo=True).values('id', 'nombre'))
        ctx['unidades'] = list(
            Unidad.objects.filter(activo=True)
            .select_related('area_hospitalaria')
            .values('id', 'nombre', 'area_hospitalaria__nombre', 'area_hospitalaria_id')
        )
        ctx['recintos'] = list(
            Recinto.objects.filter(activo=True)
            .select_related('unidad', 'piso')
            .values('id', 'nombre', 'unidad__nombre', 'piso__nombre')
        )
        ctx['marcas'] = list(Marca.objects.filter(activo=True).values('id', 'nombre'))
        return ctx


class MantenedorListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        modelo = request.POST.get('modelo', '')
        from mantenedores.services.mantenedor_service import MantenedorService
        r = MantenedorService.obtener_items_para_datatable(
            modelo, dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )
        return JsonResponse({'draw': dt['draw'], **r})


class MantenedorActionView(LoginRequiredMixin, View):
    def _get_modelo(self, data):
        return (data.get('modelo') or '').strip().lower()

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from mantenedores.services.mantenedor_service import MantenedorService
            item = MantenedorService.crear_item(self._get_modelo(data), data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.CREAR,
                tabla=self._get_modelo(data).capitalize(), registro_id=item.id,
                detalles=f"{self._get_modelo(data).capitalize()} creado: {item.nombre}",
                ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Registro creado con éxito.', 'data': {'id': item.id}})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        if not item_id:
            return JsonResponse({'success': False, 'message': 'ID requerido.'}, status=400)
        try:
            from mantenedores.services.mantenedor_service import MantenedorService
            item = MantenedorService.actualizar_item(self._get_modelo(data), item_id, data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.MODIFICAR,
                tabla=self._get_modelo(data).capitalize(), registro_id=item.id,
                detalles=f"{self._get_modelo(data).capitalize()} modificado: {item.nombre}",
                ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Registro actualizado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item_id = int(data.get('id', 0))
            modelo = (data.get('modelo') or '').strip().lower()
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from mantenedores.services.mantenedor_service import MantenedorService
            item = MantenedorService.obtener_item_por_id(modelo, item_id)
            if not item:
                return JsonResponse({'success': False, 'message': 'No existe.'}, status=400)
            nombre = item.nombre
            MantenedorService.eliminar_item(modelo, item_id)
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.ELIMINAR,
                tabla=modelo.capitalize(), registro_id=item_id,
                detalles=f"{modelo.capitalize()} eliminado: {nombre}",
                ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'Registro eliminado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class MantenedorDetailView(LoginRequiredMixin, View):
    def get(self, request, item_id, *args, **kwargs):
        modelo = request.GET.get('modelo', '')
        from mantenedores.services.mantenedor_service import MantenedorService
        item = MantenedorService.obtener_item_por_id(modelo, item_id)
        if not item:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)
        data = {'id': item.id, 'nombre': item.nombre, 'activo': item.activo}
        # Campos adicionales por tipo de entidad
        if modelo == 'edificio':
            data['institucion'] = item.institucion_id
        elif modelo == 'institucion':
            data['codigo'] = item.codigo
        elif modelo == 'estados':
            data['color_hex'] = item.color_hex
        elif modelo == 'fallas_bitacora':
            data['tipo'] = item.tipo
            data['orden'] = item.orden
        elif modelo == 'modelo':
            data['marca'] = item.marca_id
        elif modelo == 'piso':
            data['alias'] = item.alias or ''
            data['edificio'] = item.edificio_id
        elif modelo == 'proveedor':
            data['contacto'] = item.contacto or ''
            data['telefono'] = item.telefono or ''
            data['email'] = item.email or ''
            data['direccion'] = item.direccion or ''
        # --- Nuevas entidades jerárquicas ---
        elif modelo == 'sector':
            data['piso'] = item.piso_id
        elif modelo == 'unidad':
            data['area_hospitalaria'] = item.area_hospitalaria_id
        elif modelo == 'recinto':
            data['piso'] = item.piso_id
            data['sector'] = item.sector_id
            data['unidad'] = item.unidad_id
        elif modelo == 'pma':
            data['recinto'] = item.recinto_id
        return JsonResponse({'success': True, 'data': data})
