"""Vistas del módulo Redes / IPAM."""
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q, Count, ProtectedError
from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, normalizar_nombre, extract_validation_error


class RedesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'redes/redes.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from redes.models import InfraestructuraRed
        from mantenedores.models import Institucion, Edificio, Piso, Unidad, Vlan
        ctx['instituciones'] = list(Institucion.objects.filter(activo=True).values('id', 'nombre'))
        ctx['edificios'] = list(Edificio.objects.filter(activo=True).values('id', 'nombre'))
        ctx['pisos'] = list(Piso.objects.filter(activo=True).select_related('edificio').values('id', 'nombre', 'edificio__id'))
        ctx['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))
        ctx['vlans'] = list(Vlan.objects.filter(activo=True).values('id', 'nombre'))
        # KPIs IPAM
        ctx['ips_total'] = InfraestructuraRed.objects.count()
        ctx['ips_libres'] = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.LIBRE).count()
        ctx['ips_ocupadas'] = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.OCUPADO).count()
        ctx['ips_falla'] = InfraestructuraRed.objects.filter(estado=InfraestructuraRed.Estado.FALLA).count()
        return ctx


class IpListView(LoginRequiredMixin, View):
    """API DataTables server-side para IPs de red (IPAM)."""
    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)

        from redes.models import InfraestructuraRed
        search_val = dt['search_value']
        qs = InfraestructuraRed.objects.select_related('pma', 'vlan', 'institucion', 'edificio', 'piso', 'unidad').all()
        if search_val:
            qs = qs.filter(
                Q(ip_direccion__icontains=search_val) | Q(mac__icontains=search_val) |
                Q(rack__icontains=search_val) | Q(patch_panel__icontains=search_val) |
                Q(sector__icontains=search_val) | Q(switch_ip__icontains=search_val) |
                Q(pma__codigo__icontains=search_val) | Q(edificio__nombre__icontains=search_val)
            )
        order_map = {
            'ip_direccion': 'ip_direccion', 'estado': 'estado', 'pma': 'pma__codigo',
            'edificio': 'edificio__nombre', 'piso': 'piso__nombre', 'vlan': 'vlan__nombre',
            'rack': 'rack', 'switch_ip': 'switch_ip', 'switch_port': 'switch_port',
        }
        cols = dt['columns_data']
        order_name = '-ip_direccion'
        if 0 <= dt['order_column_index'] < len(cols):
            order_name = cols[dt['order_column_index']].get('data', '-ip_direccion')
        col = order_map.get(order_name, '-ip_direccion')
        if dt['order_dir'] == 'desc' and not col.startswith('-'):
            col = f'-{col}'
        qs = qs.order_by(col)
        total = InfraestructuraRed.objects.count()
        filtered = qs.count()
        data = []
        for ip in qs[dt['start']:dt['start'] + dt['length']]:
            data.append({
                'id': ip.id, 'ip_direccion': str(ip.ip_direccion),
                'estado': ip.estado, 'pma': ip.pma.codigo if ip.pma else '',
                'vlan': ip.vlan.nombre if ip.vlan else '',
                'edificio': ip.edificio.nombre if ip.edificio else '',
                'piso': ip.piso.nombre if ip.piso else '',
                'unidad': ip.unidad.nombre if ip.unidad else '',
                'rack': ip.rack or '', 'patch_panel': ip.patch_panel or '',
                'switch_ip': str(ip.switch_ip) if ip.switch_ip else '',
                'switch_port': ip.switch_port or '', 'mac': ip.mac or '',
            })
        return JsonResponse({'draw': dt['draw'], 'recordsTotal': total, 'recordsFiltered': filtered, 'data': data})


class IpActionView(LoginRequiredMixin, View):
    """CRUD JSON para IPs de red."""
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from redes.models import InfraestructuraRed
            import ipaddress
            ip_val = data.get('ip_direccion', '').strip()
            if not ip_val:
                return JsonResponse({'success': False, 'message': 'IP requerida.'}, status=400)
            try:
                ipaddress.ip_address(ip_val)
            except ValueError:
                return JsonResponse({'success': False, 'message': 'IP inválida.'}, status=400)
            if InfraestructuraRed.objects.filter(ip_direccion=ip_val).exists():
                return JsonResponse({'success': False, 'message': 'Ya existe esa IP.'}, status=400)
            ip = InfraestructuraRed(
                ip_direccion=ip_val, pma_id=data.get('pma') or None,
                vlan_id=data.get('vlan') or None, switch_ip=data.get('switch_ip') or None,
                switch_port=data.get('switch_port') or None,
                estado=data.get('estado', 'LIBRE'),
                institucion_id=data.get('institucion') or None,
                edificio_id=data.get('edificio') or None, piso_id=data.get('piso') or None,
                unidad_id=data.get('unidad') or None, sector=normalizar_nombre(data.get('sector')) or None,
                mac=(data.get('mac') or '').strip().upper() or None,
                rack=normalizar_nombre(data.get('rack')) or None,
                patch_panel=normalizar_nombre(data.get('patch_panel')) or None,
            )
            ip.full_clean()
            ip.save()
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.CREAR,
                tabla='InfraestructuraRed', registro_id=ip.id,
                detalles=f"IP creada: {ip.ip_direccion}", ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'IP registrada con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ip_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from redes.models import InfraestructuraRed
            ip = InfraestructuraRed.objects.get(pk=ip_id)
            ip.pma_id = data.get('pma') or None
            ip.vlan_id = data.get('vlan') or None
            ip.switch_ip = data.get('switch_ip') or None
            ip.switch_port = data.get('switch_port') or None
            ip.estado = data.get('estado', ip.estado)
            ip.institucion_id = data.get('institucion') or None
            ip.edificio_id = data.get('edificio') or None
            ip.piso_id = data.get('piso') or None
            ip.unidad_id = data.get('unidad') or None
            ip.sector = normalizar_nombre(data.get('sector')) or None
            ip.mac = (data.get('mac') or '').strip().upper() or None
            ip.rack = normalizar_nombre(data.get('rack')) or None
            ip.patch_panel = normalizar_nombre(data.get('patch_panel')) or None
            ip.full_clean()
            ip.save()
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.MODIFICAR,
                tabla='InfraestructuraRed', registro_id=ip.id,
                detalles=f"IP modificada: {ip.ip_direccion}", ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'IP actualizada con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ip_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)
        try:
            from redes.models import InfraestructuraRed
            ip = InfraestructuraRed.objects.get(pk=ip_id)
            ip_str = str(ip.ip_direccion)
            ip.delete()
            AuditoriaService.registrar_accion(
                usuario=request.user.username, accion=LogAuditoria.Accion.ELIMINAR,
                tabla='InfraestructuraRed', registro_id=ip_id,
                detalles=f"IP eliminada: {ip_str}", ip_address=get_client_ip(request))
            return JsonResponse({'success': True, 'message': 'IP eliminada con éxito.'})
        except ProtectedError:
            return JsonResponse({'success': False, 'message': f"No se puede eliminar la IP {ip_str} porque está siendo usada por otros registros."}, status=400)
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un registro con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class IpDetailView(LoginRequiredMixin, View):
    def get(self, request, ip_id, *args, **kwargs):
        from redes.models import InfraestructuraRed
        try:
            ip = InfraestructuraRed.objects.get(pk=ip_id)
        except InfraestructuraRed.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'No encontrada.'}, status=404)
        return JsonResponse({'success': True, 'data': {
            'id': ip.id, 'ip_direccion': str(ip.ip_direccion), 'estado': ip.estado,
            'pma': ip.pma_id, 'vlan': ip.vlan_id, 'switch_ip': str(ip.switch_ip) if ip.switch_ip else '',
            'switch_port': ip.switch_port or '', 'institucion': ip.institucion_id,
            'edificio': ip.edificio_id, 'piso': ip.piso_id, 'unidad': ip.unidad_id,
            'sector': ip.sector or '', 'mac': ip.mac or '', 'rack': ip.rack or '',
            'patch_panel': ip.patch_panel or '',
        }})
