import json
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria
from core.utils import get_client_ip, parse_datatables_params, extract_validation_error


class CustomLoginView(View):
    """
    Vista para renderizar e iniciar sesión.
    Cumple con OWASP y responde solicitudes de sesión mediante AJAX.
    """
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'core/login.html')

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'El usuario y la contraseña son obligatorios.'}, status=400)

        # Autenticación desacoplada de Django auth standard
        # Normalizar el RUT ingresado (ej: quitar puntos y formatear guion)
        try:
            from core.services.usuario_service import UsuarioService
            username_normalized = UsuarioService.normalizar_rut(username)
        except Exception:
            username_normalized = username

        user = authenticate(request, username=username_normalized, password=password)
        ip_addr = get_client_ip(request)

        if user is not None:
            if user.is_active:
                login(request, user)
                AuditoriaService.registrar_accion(
                    usuario=username,
                    accion=LogAuditoria.Accion.LOGIN_EXITOSO,
                    tabla='User',
                    registro_id=user.id,
                    detalles='Inicio de sesión exitoso mediante AJAX',
                    ip_address=ip_addr
                )
                return JsonResponse({'success': True, 'redirect_url': redirect('dashboard').url})
            else:
                AuditoriaService.registrar_accion(
                    usuario=username,
                    accion=LogAuditoria.Accion.LOGIN_FALLIDO,
                    tabla='User',
                    registro_id=user.id,
                    detalles='Intento de ingreso con cuenta deshabilitada',
                    ip_address=ip_addr
                )
                return JsonResponse({'success': False, 'message': 'La cuenta está deshabilitada.'}, status=403)
        else:
            AuditoriaService.registrar_accion(
                usuario=username,
                accion=LogAuditoria.Accion.LOGIN_FALLIDO,
                tabla='User',
                registro_id=None,
                detalles=f'Intento fallido de inicio de sesión para el usuario: {username}',
                ip_address=ip_addr
            )
            return JsonResponse({'success': False, 'message': 'Credenciales incorrectas.'}, status=401)


class CustomLogoutView(View):
    """
    Cierre de sesión seguro.
    """
    def post(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anónimo'
        ip_addr = get_client_ip(request)
        logout(request)
        AuditoriaService.registrar_accion(
            usuario=username,
            accion=LogAuditoria.Accion.LOGOUT,
            tabla='User',
            registro_id=None,
            detalles='Cierre de sesión exitoso (POST)',
            ip_address=ip_addr
        )
        return JsonResponse({'success': True, 'redirect_url': reverse('login')})

    def get(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anónimo'
        ip_addr = get_client_ip(request)
        logout(request)
        AuditoriaService.registrar_accion(
            usuario=username,
            accion=LogAuditoria.Accion.LOGOUT,
            tabla='User',
            registro_id=None,
            detalles='Cierre de sesión exitoso (GET)',
            ip_address=ip_addr
        )
        return redirect('login')


class SwitchUserView(LoginRequiredMixin, View):
    """
    Permite a los superusuarios impersonar a otros usuarios para pruebas.
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse({'success': False, 'message': 'No autorizado.'}, status=403)
            
        try:
            data = json.loads(request.body)
            target_user_id = data.get('user_id')
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'message': 'JSON inválido.'}, status=400)
            
        if not target_user_id:
            return JsonResponse({'success': False, 'message': 'ID de usuario requerido.'}, status=400)
            
        from django.contrib.auth.models import User
        target_user = User.objects.filter(id=target_user_id).first()
        if not target_user:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado.'}, status=404)
            
        login(request, target_user)
        return JsonResponse({'success': True, 'redirect_url': redirect('dashboard').url})


class DashboardGeneralView(LoginRequiredMixin, TemplateView):
    """
    Dashboard de inicio general con estadísticas agregadas del sistema TIC.
    Reemplaza dashboardActivos.php (1.769 líneas con SQL embebido).
    """
    template_name = 'core/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.services.dashboard_service import obtener_kpis_generales
        context['kpis'] = obtener_kpis_generales()
        return context

class UsuariosDashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista para el módulo de Gestión de Usuarios.
    """
    template_name = 'core/usuarios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.models import Rol
        from tickets.models import GrupoResolutor
        from mantenedores.models import Unidad
        context['roles_disponibles'] = Rol.objects.filter(activo=True).order_by('nombre')
        context['grupos_disponibles'] = GrupoResolutor.objects.filter(activo=True).order_by('nombre')
        context['unidades'] = Unidad.objects.all().order_by('nombre')
        return context
class UsuarioListView(LoginRequiredMixin, View):
    """
    API Server-Side para DataTables de Usuarios.
    """
    def post(self, request, *args, **kwargs):
        dt = parse_datatables_params(request)
        dt['length'] = int(request.POST.get('length', 10))

        from core.services.usuario_service import UsuarioService
        result = UsuarioService.obtener_usuarios_para_datatable(
            dt['start'], dt['length'], dt['search_value'],
            dt['order_column_index'], dt['order_dir'], dt['columns_data']
        )

        response = {
            'draw': dt['draw'],
            'recordsTotal': result['recordsTotal'],
            'recordsFiltered': result['recordsFiltered'],
            'data': result['data']
        }
        return JsonResponse(response)


class UsuarioActionView(LoginRequiredMixin, View):
    """
    API JSON/multipart para acciones CRUD de operadores/usuarios.
    Soporta tanto JSON como FormData (para upload de foto).
    """
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get('_method', '').upper() == 'PUT':
            request.method = 'PUT'
        return super().dispatch(request, *args, **kwargs)

    def _parse_request(self, request):
        """Extrae datos del request tanto de JSON como de multipart."""
        if request.content_type and 'multipart/form-data' in request.content_type:
            return {
                'rut': request.POST.get('rut', ''),
                'nombres': request.POST.get('nombres', ''),
                'apellidos': request.POST.get('apellidos', ''),
                'email': request.POST.get('email', ''),
                'unidad': request.POST.get('unidad', ''),
                'cargo': request.POST.get('cargo', ''),
                'grado': request.POST.get('grado', ''),
                'contrasena': request.POST.get('contrasena', ''),
                'id': request.POST.get('id'),
                'foto': request.FILES.get('foto'),
                'is_active': str(request.POST.get('is_active', 'true')).lower() == 'true',
                'rol_id': request.POST.get('rol', None)
            }
            try:
                data['grupos'] = json.loads(request.POST.get('grupos', '[]'))
            except (json.JSONDecodeError, TypeError, ValueError):
                data['grupos'] = []
            return data
        try:
            data = json.loads(request.body)
            data['foto'] = None
            return data
        except (json.JSONDecodeError, TypeError, ValueError):
            return None

    def post(self, request, *args, **kwargs):
        """
        Crear nuevo usuario.
        """
        data = self._parse_request(request)
        if not data:
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from core.services.usuario_service import UsuarioService
            user = UsuarioService.crear_usuario(
                rut=data.get('rut', ''),
                nombres=data.get('nombres', ''),
                apellidos=data.get('apellidos', ''),
                correo=data.get('email', ''),
                unidad=data.get('unidad', ''),
                cargo=data.get('cargo', ''),
                grado=data.get('grado', ''),
                contrasena=data.get('contrasena', ''),
                foto=data.get('foto'),
                grupos=data.get('grupos', []),
                rol_id=data.get('rol_id'),
                is_active=data.get('is_active', True)
            )
            
            # LOG AUDITORIA
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='User',
                registro_id=user.id,
                detalles=f"Creado operador {user.username} - {user.get_full_name()} ({data.get('cargo', '')}, Unidad: {data.get('unidad', '')}, Grado: {data.get('grado', '')})",
                ip_address=get_client_ip(request)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario registrado con éxito en el sistema.',
                'data': {'id': user.id, 'username': user.username}
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un usuario con esos datos.'}, status=400)

    def put(self, request, *args, **kwargs):
        """
        Actualizar usuario.
        """
        data = self._parse_request(request)
        if not data:
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        user_id_str = data.get('id')
        if not user_id_str:
            return JsonResponse({'success': False, 'message': 'ID de usuario requerido.'}, status=400)
        user_id = int(user_id_str)

        rut = data.get('rut', '')
        nombres = data.get('nombres', '')
        apellidos = data.get('apellidos', '')
        correo = data.get('email', '')
        unidad = data.get('unidad', '')
        cargo = data.get('cargo', '')
        grado = data.get('grado', '')
        contrasena = data.get('contrasena', '')

        try:
            from core.services.usuario_service import UsuarioService
            user_prev = UsuarioService.obtener_usuario_por_id(user_id)
            if not user_prev:
                return JsonResponse({'success': False, 'message': 'El usuario no existe.'}, status=400)
            
            # Guardamos estado previo para auditar diferencias
            perfil_prev = getattr(user_prev, 'perfil', None)
            detalles_cambios = f"Modificado usuario {user_prev.username}: "
            cambios = []
            if rut and user_prev.username != rut.strip(): cambios.append(f"RUT '{user_prev.username}' -> '{rut}'")
            if user_prev.first_name != nombres.strip(): cambios.append(f"nombres '{user_prev.first_name}' -> '{nombres}'")
            if user_prev.last_name != apellidos.strip(): cambios.append(f"apellidos '{user_prev.last_name}' -> '{apellidos}'")
            if user_prev.email != correo.strip().lower(): cambios.append(f"correo '{user_prev.email}' -> '{correo}'")
            if perfil_prev:
                if perfil_prev.unidad != unidad.strip(): cambios.append(f"unidad '{perfil_prev.unidad}' -> '{unidad}'")
                if perfil_prev.cargo != cargo.strip(): cambios.append(f"cargo '{perfil_prev.cargo}' -> '{cargo}'")
                if perfil_prev.grado != grado.strip(): cambios.append(f"grado '{perfil_prev.grado}' -> '{grado}'")
                if data.get('foto'): cambios.append("foto actualizada")
            else:
                cambios.append("perfil inicial creado")
            if contrasena and contrasena.strip(): cambios.append("cambio de contraseña")

            user = UsuarioService.actualizar_usuario(
                user_id=user_id,
                nombres=nombres,
                apellidos=apellidos,
                correo=correo,
                unidad=unidad,
                cargo=cargo,
                grado=grado,
                rut=rut,
                contrasena=contrasena,
                foto=data.get('foto'),
                grupos=data.get('grupos', []),
                rol_id=data.get('rol_id'),
                is_active=data.get('is_active', True)
            )

            # LOG AUDITORIA
            detalles_cambios += ", ".join(cambios) if cambios else "sin cambios significativos"
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.MODIFICAR,
                tabla='User',
                registro_id=user_id,
                detalles=detalles_cambios,
                ip_address=get_client_ip(request)
            )

            return JsonResponse({'success': True, 'message': 'Datos de usuario actualizados con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un usuario con esos datos.'}, status=400)

    def delete(self, request, *args, **kwargs):
        """
        Eliminar usuario.
        """
        try:
            data = json.loads(request.body)
            user_id = int(data.get('id', 0))
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from core.services.usuario_service import UsuarioService
            user_prev = UsuarioService.obtener_usuario_por_id(user_id)
            if not user_prev:
                return JsonResponse({'success': False, 'message': 'El usuario a eliminar no existe.'}, status=400)

            username_antiguo = user_prev.username
            nombre_antiguo = user_prev.get_full_name()

            UsuarioService.eliminar_usuario(user_id, request.user.id)

            # LOG AUDITORIA
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.ELIMINAR,
                tabla='User',
                registro_id=user_id,
                detalles=f"Eliminado operador {username_antiguo} - {nombre_antiguo}",
                ip_address=get_client_ip(request)
            )

            return JsonResponse({'success': True, 'message': 'Usuario eliminado con éxito del sistema.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': extract_validation_error(e)}, status=400)
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Ya existe un usuario con esos datos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

class FuncionarioSearchAPIView(LoginRequiredMixin, View):
    """Búsqueda de funcionarios para Select2 por RUT, nombres o apellidos."""
    def get(self, request, *args, **kwargs):
        from core.models import Funcionario
        from django.db.models import Q
        
        q = request.GET.get('q', '').strip()
        qs = Funcionario.objects.all()
        
        if q:
            qs = qs.filter(
                Q(rut__icontains=q) | 
                Q(nombres__icontains=q) | 
                Q(apellidos__icontains=q)
            )
            
        qs = qs[:20]  # Limitar a 20 resultados para performance
        
        results = []
        for f in qs:
            results.append({
                'id': f.id,
                'text': f"{f.nombres} {f.apellidos} ({f.rut})"
            })
            
        return JsonResponse({'results': results})

class FuncionarioCreateAPIView(LoginRequiredMixin, View):
    """Creación on-the-fly de Funcionarios desde modal."""
    def post(self, request, *args, **kwargs):
        from core.models import Funcionario
        from mantenedores.models import Unidad
        from core.services.usuario_service import UsuarioService
        
        try:
            data = json.loads(request.body)
            rut = data.get('rut', '').strip()
            nombres = data.get('nombres', '').strip()
            apellidos = data.get('apellidos', '').strip()
            correo = data.get('correo', '').strip()
            cargo_id = data.get('cargo', '')
            unidad_nombre = data.get('unidad', '').strip()
            
            if not rut or not nombres or not apellidos:
                return JsonResponse({'success': False, 'message': 'RUT, nombres y apellidos son obligatorios.'}, status=400)
                
            rut_norm = UsuarioService.normalizar_rut(rut)
            
            if Funcionario.objects.filter(rut=rut_norm).exists():
                return JsonResponse({'success': False, 'message': 'Ya existe un funcionario con este RUT.'}, status=400)
                
            unidad = None
            if unidad_nombre:
                unidad = Unidad.objects.filter(nombre=unidad_nombre).first()
                
            from mantenedores.models import Cargo
            cargo = None
            if cargo_id:
                cargo = Cargo.objects.filter(id=cargo_id).first()
                
            func = Funcionario.objects.create(
                rut=rut_norm,
                nombres=nombres,
                apellidos=apellidos,
                correo=correo,
                unidad=unidad,
                cargo=cargo
            )
            
            return JsonResponse({
                'success': True, 
                'data': {
                    'id': func.id,
                    'text': f"{func.nombres} {func.apellidos} ({func.rut})"
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
