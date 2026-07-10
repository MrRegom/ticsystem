"""
Vistas del módulo Equipos.

Siguen el patrón Clean Architecture de core.views:
- EquiposDashboardView: renderiza el template con la tabla.
- EquipoListView: API JSON server-side para DataTables.
- EquipoActionView: API JSON CRUD (crear/actualizar/eliminar).

Las vistas solo enrutamiento + validación inicial. La lógica está en
equipos.services.equipo_service.
"""
import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error


class EquiposDashboardView(LoginRequiredMixin, TemplateView):
    """Vista del módulo de Equipos (inventario TIC)."""
    template_name = 'equipos/equipos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Catálogos para los selects de los modales
        from mantenedores.models import (
            Articulo, Marca, Modelo, Edificio, Piso, Sector, Unidad, AreaHospitalaria, Recinto, PMA,
            SistemaOperativo, EstadoEquipo, Proveedor,
        )
        context['articulos'] = list(Articulo.objects.filter(activo=True).values('id', 'nombre'))
        context['marcas'] = list(Marca.objects.filter(activo=True).values('id', 'nombre'))
        context['modelos'] = list(Modelo.objects.filter(activo=True).values('id', 'nombre', 'marca_id'))
        context['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        context['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id', 'edificio__nombre'))
        context['sectores'] = list(Sector.objects.filter(activo=True).select_related('piso').values('id', 'nombre', 'piso_id', 'piso__nombre'))
        context['areas'] = list(AreaHospitalaria.objects.filter(activo=True).values('id', 'nombre'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).select_related('area_hospitalaria').values('id', 'nombre', 'area_hospitalaria_id', 'area_hospitalaria__nombre'))
        context['recintos'] = list(Recinto.objects.filter(activo=True).select_related('piso', 'sector', 'unidad').values('id', 'nombre', 'piso_id', 'sector_id', 'unidad_id'))
        context['pmas'] = list(PMA.objects.filter(activo=True).select_related('recinto').values('id', 'nombre', 'recinto_id'))
        context['sos'] = list(SistemaOperativo.objects.filter(activo=True).values('id', 'nombre'))
        context['estados'] = list(EstadoEquipo.objects.filter(activo=True).values('id', 'nombre', 'color_hex'))
        context['proveedores'] = list(Proveedor.objects.filter(activo=True).values('id', 'nombre'))
        
        # KPIs iniciales
        from equipos.models import Equipo
        total = Equipo.objects.count()
        operativos = Equipo.objects.filter(estado__nombre__icontains='inventario').count() + Equipo.objects.filter(estado__nombre__icontains='funcional').count()
        mantenimiento = Equipo.objects.filter(estado__nombre__icontains='mantenimiento').count()
        
        context['kpi'] = {
            'total': total,
            'operativos': operativos,
            'mantenimiento': mantenimiento
        }
        
        return context


class EquipoListView(LoginRequiredMixin, View):
    """API Server-Side para DataTables de Equipos."""

    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        from equipos.services.equipo_service import EquipoService
        result = EquipoService.obtener_equipos_para_datatable(
            dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )
        return JsonResponse({
            'draw': dt['draw'],
            'recordsTotal': result['recordsTotal'],
            'recordsFiltered': result['recordsFiltered'],
            'data': result['data'],
        })


class EquipoActionView(LoginRequiredMixin, View):
    """API JSON para acciones CRUD de equipos."""

    def post(self, request, *args, **kwargs):
        """Crear nuevo equipo."""
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from equipos.services.equipo_service import EquipoService
            equipo = EquipoService.crear_equipo(data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='Equipo',
                registro_id=equipo.id,
                detalles=f"Equipo creado: {equipo.serial_number} ({equipo.articulo} {equipo.marca})",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Equipo registrado con éxito.',
                'data': {'id': equipo.id, 'serial_number': equipo.serial_number},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        """Actualizar equipo existente."""
        try:
            data = json.loads(request.body)
            equipo_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not equipo_id:
            return JsonResponse({'success': False, 'message': 'ID de equipo requerido.'}, status=400)

        try:
            from equipos.services.equipo_service import EquipoService
            equipo = EquipoService.actualizar_equipo(equipo_id, data, usuario=request.user)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.MODIFICAR,
                tabla='Equipo',
                registro_id=equipo.id,
                detalles=f"Equipo modificado: {equipo.serial_number}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({
                'success': True,
                'message': 'Equipo actualizado con éxito.',
                'data': {'id': equipo.id, 'serial_number': equipo.serial_number},
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        """Eliminar equipo."""
        try:
            data = json.loads(request.body)
            equipo_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not equipo_id:
            return JsonResponse({'success': False, 'message': 'ID de equipo requerido.'}, status=400)

        try:
            from equipos.services.equipo_service import EquipoService
            equipo = EquipoService.obtener_equipo_por_id(equipo_id)
            if not equipo:
                return JsonResponse({'success': False, 'message': 'El equipo no existe.'}, status=400)
            serial = equipo.serial_number
            EquipoService.eliminar_equipo(equipo_id)
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.ELIMINAR,
                tabla='Equipo',
                registro_id=equipo_id,
                detalles=f"Equipo eliminado: {serial}",
                ip_address=get_client_ip(request),
            )
            return JsonResponse({'success': True, 'message': 'Equipo eliminado con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class EquipoDetailView(LoginRequiredMixin, View):
    """API JSON para obtener detalle de un equipo (para modal de edición)."""

    def get(self, request, equipo_id, *args, **kwargs):
        from equipos.services.equipo_service import EquipoService, _resolver_imagen_equipo
        equipo = EquipoService.obtener_equipo_por_id(equipo_id)
        if not equipo:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)
        img_url = _resolver_imagen_equipo(equipo)
        return JsonResponse({
            'success': True,
            'data': {
                'id': equipo.id,
                'serial_number': equipo.serial_number,
                'articulo': equipo.articulo_id,
                'articulo_nombre': str(equipo.articulo) if equipo.articulo else '',
                'marca': equipo.marca_id,
                'marca_nombre': str(equipo.marca) if equipo.marca else '',
                'modelo': equipo.modelo_id,
                'modelo_nombre': str(equipo.modelo) if equipo.modelo else '',
                'pma': equipo.pma_id,
                
                
                'so': equipo.so_id,
                'estado': equipo.estado_id,
                'proveedor': equipo.proveedor_id,
                'ip': str(equipo.ip) if equipo.ip else '',
                'anexo': equipo.anexo or '',
                'usuario': equipo.usuario or '',
                'office': equipo.office or '',
                'activador': equipo.activador or '',
                'pmalugar': equipo.pmalugar or '',
                'comentario': equipo.comentario or '',
                'imagen': img_url,
            }
        })


class EquipoDetailReadView(LoginRequiredMixin, View):
    """API JSON con detalle completo read-only de un equipo."""

    def get(self, request, equipo_id, *args, **kwargs):
        from equipos.services.equipo_service import EquipoService, _resolver_imagen_equipo
        e = EquipoService.obtener_equipo_por_id(equipo_id)
        if not e:
            return JsonResponse({'success': False, 'message': 'No encontrado.'}, status=404)
        img_url = _resolver_imagen_equipo(e)
        return JsonResponse({'success': True, 'data': {
            'serial_number': e.serial_number,
            'articulo': str(e.articulo) if e.articulo else '',
            'marca': str(e.marca) if e.marca else '',
            'modelo': str(e.modelo) if e.modelo else '',
            'pma': str(e.pma) if e.pma else '',
            
            
            'so': str(e.so) if e.so else '',
            'estado': str(e.estado) if e.estado else '',
            'proveedor': str(e.proveedor) if e.proveedor else '',
            'ip': str(e.ip) if e.ip else '',
            'anexo': e.anexo or '',
            'usuario': e.usuario or '',
            'office': e.office or '',
            'activador': e.activador or '',
            'pmalugar': e.pmalugar or '',
            'comentario': e.comentario or '',
            'imagen': img_url,
            'fecha_creacion': e.fecha_creacion.strftime('%d/%m/%Y %H:%M') if e.fecha_creacion else '',
            'fecha_modificacion': e.fecha_modificacion.strftime('%d/%m/%Y %H:%M') if e.fecha_modificacion else '',
            'usuario_modificador': e.modificado_por.get_full_name() or e.modificado_por.username if e.modificado_por else '',
        }})


class EquipoHistorialView(LoginRequiredMixin, View):
    """API JSON: historial de auditoría de un equipo."""

    def get(self, request, equipo_id, *args, **kwargs):
        from core.models import LogAuditoria
        logs = LogAuditoria.objects.filter(
            tabla='Equipo', registro_id=equipo_id
        ).order_by('-fecha_registro')[:50]
        data = []
        for log in logs:
            data.append({
                'usuario': log.usuario,
                'accion': log.accion,
                'detalles': log.detalles or '',
                'fecha': log.fecha_registro.strftime('%d/%m/%Y %H:%M') if log.fecha_registro else '',
                'ip': log.ip_address or '',
            })
        return JsonResponse({'success': True, 'data': data})


class EquipoBitacoraView(LoginRequiredMixin, View):
    """API JSON: bitácora de mantención de un equipo."""

    def get(self, request, equipo_id, *args, **kwargs):
        from equipos.models import BitacoraEquipo
        bitacoras = BitacoraEquipo.objects.filter(
            equipo_id=equipo_id
        ).select_related('tecnico').order_by('-fecha_creacion')[:50]
        data = []
        for b in bitacoras:
            data.append(self._serialize(b))
        return JsonResponse({'success': True, 'data': data})

    def post(self, request, equipo_id, *args, **kwargs):
        from equipos.models import BitacoraEquipo, Equipo
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'JSON inválido.'}, status=400)

        equipo = Equipo.objects.filter(id=equipo_id).first()
        if not equipo:
            return JsonResponse({'success': False, 'message': 'Equipo no encontrado.'}, status=404)

        fecha_mtto = body.get('fecha_mantenimiento')
        if not fecha_mtto:
            return JsonResponse({'success': False, 'message': 'Fecha de mantención requerida.'}, status=400)

        try:
            fecha_mtto = datetime.strptime(fecha_mtto, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Formato de fecha inválido (YYYY-MM-DD).'}, status=400)

        fecha_dev = body.get('fecha_devolucion')
        if fecha_dev:
            try:
                fecha_dev = datetime.strptime(fecha_dev, '%Y-%m-%d').date()
            except ValueError:
                fecha_dev = None

        registro = BitacoraEquipo(
            equipo=equipo,
            tecnico=request.user,
            tipo_registro=body.get('tipo_registro', BitacoraEquipo.TipoRegistro.MANTENCION),
            fecha_mantenimiento=fecha_mtto,
            fecha_devolucion=fecha_dev,
            solicitante=body.get('solicitante', '')[:150] or None,
            falla_reportada=body.get('falla_reportada', '') or None,
            actividades_realizadas=body.get('actividades_realizadas', '') or None,
            servicio_unidad=body.get('servicio_unidad', '')[:100] or None,
        )

        try:
            registro.full_clean()
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)

        registro.save()

        AuditoriaService.registrar_accion(
            usuario=request.user.username,
            accion=LogAuditoria.Accion.CREAR,
            tabla='BitacoraEquipo',
            registro_id=registro.id,
            detalles=f"Nuevo registro de bitácora: {registro.get_tipo_registro_display()} para equipo {equipo.serial_number}",
            ip_address=get_client_ip(request),
        )

        return JsonResponse({'success': True, 'message': 'Registro de bitácora creado.', 'data': self._serialize(registro)})

    @staticmethod
    def _serialize(b):
        return {
            'id': b.id,
            'tecnico': b.tecnico.username if b.tecnico else '',
            'tipo_registro': b.tipo_registro,
            'tipo_registro_display': b.get_tipo_registro_display(),
            'fecha_mantenimiento': b.fecha_mantenimiento.strftime('%d/%m/%Y') if b.fecha_mantenimiento else '',
            'fecha_mantenimiento_iso': b.fecha_mantenimiento.isoformat() if b.fecha_mantenimiento else '',
            'fecha_devolucion': b.fecha_devolucion.strftime('%d/%m/%Y') if b.fecha_devolucion else '',
            'fecha_devolucion_iso': b.fecha_devolucion.isoformat() if b.fecha_devolucion else '',
            'solicitante': b.solicitante or '',
            'falla_reportada': b.falla_reportada or '',
            'actividades_realizadas': b.actividades_realizadas or '',
            'servicio_unidad': b.servicio_unidad or '',
            'fecha_creacion': b.fecha_creacion.strftime('%d/%m/%Y %H:%M') if b.fecha_creacion else '',
        }


class BitacoraRegistroView(LoginRequiredMixin, View):
    """API JSON: actualizar/eliminar un registro individual de bitácora."""

    def put(self, request, bitacora_id, *args, **kwargs):
        from equipos.models import BitacoraEquipo
        registro = BitacoraEquipo.objects.filter(id=bitacora_id).first()
        if not registro:
            return JsonResponse({'success': False, 'message': 'Registro no encontrado.'}, status=404)

        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'JSON inválido.'}, status=400)

        fecha_dev = body.get('fecha_devolucion')
        if fecha_dev:
            try:
                fecha_dev = datetime.strptime(fecha_dev, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Formato de fecha inválido (YYYY-MM-DD).'}, status=400)
            registro.fecha_devolucion = fecha_dev
        elif 'fecha_devolucion' in body and not fecha_dev:
            registro.fecha_devolucion = None

        if 'solicitante' in body:
            registro.solicitante = body['solicitante'][:150] or None
        if 'falla_reportada' in body:
            registro.falla_reportada = body['falla_reportada'] or None
        if 'actividades_realizadas' in body:
            registro.actividades_realizadas = body['actividades_realizadas'] or None
        if 'servicio_unidad' in body:
            registro.servicio_unidad = body['servicio_unidad'][:100] or None
        if 'tipo_registro' in body:
            registro.tipo_registro = body['tipo_registro']

        try:
            registro.full_clean()
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)

        registro.save()

        AuditoriaService.registrar_accion(
            usuario=request.user.username,
            accion=LogAuditoria.Accion.MODIFICAR,
            tabla='BitacoraEquipo',
            registro_id=registro.id,
            detalles=f"Registro de bitácora actualizado: {registro.get_tipo_registro_display()}",
            ip_address=get_client_ip(request),
        )

        return JsonResponse({'success': True, 'message': 'Registro actualizado.', 'data': EquipoBitacoraView._serialize(registro)})

    def delete(self, request, bitacora_id, *args, **kwargs):
        from equipos.models import BitacoraEquipo
        registro = BitacoraEquipo.objects.filter(id=bitacora_id).first()
        if not registro:
            return JsonResponse({'success': False, 'message': 'Registro no encontrado.'}, status=404)

        equipo_serial = registro.equipo.serial_number
        tipo = registro.get_tipo_registro_display()
        registro.delete()

        AuditoriaService.registrar_accion(
            usuario=request.user.username,
            accion=LogAuditoria.Accion.ELIMINAR,
            tabla='BitacoraEquipo',
            registro_id=bitacora_id,
            detalles=f"Registro de bitácora eliminado: {tipo} de equipo {equipo_serial}",
            ip_address=get_client_ip(request),
        )

        return JsonResponse({'success': True, 'message': 'Registro eliminado.'})


class ModelosPorMarcaView(LoginRequiredMixin, View):
    """API JSON: devuelve los modelos asociados a una marca (select dependiente)."""

    def get(self, request, marca_id, *args, **kwargs):
        from mantenedores.models import Modelo
        from equipos.services.equipo_service import _resolver_imagen_modelo
        modelos_qs = Modelo.objects.filter(marca_id=marca_id, activo=True).order_by('nombre')
        data = []
        for m in modelos_qs:
            data.append({
                'id': m.id,
                'nombre': m.nombre,
                'imagen_url': _resolver_imagen_modelo(m),
            })
        return JsonResponse({'success': True, 'data': data})


class EquipoCheckView(LoginRequiredMixin, View):
    """API JSON: verifica en tiempo real si serial o IP ya existen."""

    def get(self, request, *args, **kwargs):
        from equipos.models import Equipo
        serial = request.GET.get('serial', '').strip()
        ip = request.GET.get('ip', '').strip()
        exclude_id = request.GET.get('exclude_id')
        result = {}

        if serial:
            qs = Equipo.objects.filter(serial_number__iexact=serial)
            if exclude_id:
                qs = qs.exclude(pk=exclude_id)
            if qs.exists():
                eq = qs.first()
                result['serial'] = {
                    'exists': True,
                    'message': f"Ya existe un equipo con ese serial.",
                    'equipo': f"{eq.articulo.nombre if eq.articulo else ''} {eq.marca.nombre if eq.marca else ''} {eq.modelo.nombre if eq.modelo else ''}",
                    'ubicacion': f"{eq.pma.recinto.sector.piso.edificio.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.sector and eq.pma.recinto.sector.piso else ''} Piso {eq.pma.recinto.sector.piso.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.sector and eq.pma.recinto.sector.piso else ''}",
                }
            else:
                result['serial'] = {'exists': False}

        if ip:
            import ipaddress as ipmod
            try:
                ipmod.ip_address(ip)
            except ValueError:
                result['ip'] = {'exists': False, 'invalid': True, 'message': 'Dirección IP no válida.'}
                return JsonResponse(result)
            qs = Equipo.objects.filter(ip=ip)
            if exclude_id:
                qs = qs.exclude(pk=exclude_id)
            if qs.exists():
                eq = qs.first()
                result['ip'] = {
                    'exists': True,
                    'message': f"La IP {ip} ya está asignada.",
                    'equipo': f"Serial: {eq.serial_number} - {eq.articulo.nombre if eq.articulo else ''} {eq.marca.nombre if eq.marca else ''}",
                    'ubicacion': f"{eq.pma.recinto.sector.piso.edificio.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.sector and eq.pma.recinto.sector.piso else ''} Piso {eq.pma.recinto.sector.piso.nombre if eq.pma and eq.pma.recinto and eq.pma.recinto.sector and eq.pma.recinto.sector.piso else ''}",
                }
            else:
                result['ip'] = {'exists': False}

        return JsonResponse(result)


class ImportarMargaMargaView(LoginRequiredMixin, View):
    """Vista para cargar el Excel de Marga Marga e invocar el servicio."""
    
    def get(self, request, *args, **kwargs):
        return render(request, 'equipos/importar.html')
        
    def post(self, request, *args, **kwargs):
        archivo = request.FILES.get('archivo_excel')
        if not archivo:
            messages.error(request, "Por favor seleccione un archivo Excel válido.")
            return redirect('equipos:importar_marga_marga')
            
        if not archivo.name.endswith('.xlsx'):
            messages.error(request, "El archivo debe tener extensión .xlsx")
            return redirect('equipos:importar_marga_marga')
            
        fs = FileSystemStorage()
        filename = fs.save(archivo.name, archivo)
        filepath = fs.path(filename)
        
        try:
            from equipos.services.importacion_marga_marga import MargaMargaImporterService
            total = MargaMargaImporterService.importar_excel(filepath)
            messages.success(request, f"¡Éxito! Se importaron/actualizaron {total} equipos desde el archivo.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error procesando el archivo: {str(e)}")
        finally:
            fs.delete(filename)
            
        return redirect('equipos:importar_marga_marga')
