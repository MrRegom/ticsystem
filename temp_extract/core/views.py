import json
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from core.services.auditoria_service import AuditoriaService
from core.models import LogAuditoria

def _get_client_ip(request):
    """
    Función de utilidad para extraer la IP real del cliente.
    Considera entornos detrás de proxy inverso (Nginx, Balanceadores).
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
        ip_addr = _get_client_ip(request)

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
        ip_addr = _get_client_ip(request)
        logout(request)
        AuditoriaService.registrar_accion(
            usuario=username,
            accion=LogAuditoria.Accion.LOGOUT,
            tabla='User',
            registro_id=None,
            detalles='Cierre de sesión exitoso (POST)',
            ip_address=ip_addr
        )
        return JsonResponse({'success': True, 'redirect_url': '/login/'})

    def get(self, request, *args, **kwargs):
        username = request.user.username if request.user.is_authenticated else 'Anónimo'
        ip_addr = _get_client_ip(request)
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


class DashboardGeneralView(LoginRequiredMixin, TemplateView):
    """
    Dashboard de inicio general con estadísticas agregadas del sistema.
    """
    template_name = 'core/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add basic stats here if needed later
        return context

class UsuariosDashboardView(LoginRequiredMixin, TemplateView):
    """
    Vista para el módulo de Gestión de Usuarios.
    """
    template_name = 'core/usuarios.html'



class UsuarioListView(LoginRequiredMixin, View):
    """
    API Server-Side para DataTables de Usuarios.
    """
    def post(self, request, *args, **kwargs):
        params = request.POST
        
        draw = int(params.get('draw', 1))
        start = int(params.get('start', 0))
        length = int(params.get('length', 10))
        search_value = params.get('search[value]', '').strip()
        
        order_column_index = int(params.get('order[0][column]', 0))
        order_dir = params.get('order[0][dir]', 'asc')

        columns_data = []
        i = 0
        while f'columns[{i}][data]' in params:
            columns_data.append({
                'data': params.get(f'columns[{i}][data]'),
                'name': params.get(f'columns[{i}][name]'),
                'searchable': params.get(f'columns[{i}][searchable]') == 'true',
                'orderable': params.get(f'columns[{i}][orderable]') == 'true',
            })
            i += 1

        from core.services.usuario_service import UsuarioService
        result = UsuarioService.obtener_usuarios_para_datatable(
            start=start,
            length=length,
            search_value=search_value,
            order_column_index=order_column_index,
            order_dir=order_dir,
            columns_data=columns_data
        )

        response = {
            'draw': draw,
            'recordsTotal': result['recordsTotal'],
            'recordsFiltered': result['recordsFiltered'],
            'data': result['data']
        }
        return JsonResponse(response)


class UsuarioActionView(LoginRequiredMixin, View):
    """
    API JSON para acciones CRUD de operadores/usuarios.
    """
    def post(self, request, *args, **kwargs):
        """
        Crear nuevo usuario.
        """
        try:
            data = json.loads(request.body)
            rut = data.get('rut', '')
            nombres = data.get('nombres', '')
            apellidos = data.get('apellidos', '')
            correo = data.get('email', '')
            unidad = data.get('unidad', '')
            cargo = data.get('cargo', '')
            grado = data.get('grado', '')
            contrasena = data.get('contrasena', '')
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        try:
            from core.services.usuario_service import UsuarioService
            user = UsuarioService.crear_usuario(
                rut=rut,
                nombres=nombres,
                apellidos=apellidos,
                correo=correo,
                unidad=unidad,
                cargo=cargo,
                grado=grado,
                contrasena=contrasena
            )
            
            # LOG AUDITORIA
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.CREAR,
                tabla='User',
                registro_id=user.id,
                detalles=f"Creado operador {user.username} - {user.get_full_name()} ({cargo}, Unidad: {unidad}, Grado: {grado})",
                ip_address=_get_client_ip(request)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario registrado con éxito en el sistema.',
                'data': {'id': user.id, 'username': user.username}
            })
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': e.message}, status=400)

    def put(self, request, *args, **kwargs):
        """
        Actualizar usuario.
        """
        try:
            data = json.loads(request.body)
            user_id = int(data.get('id', 0))
            rut = data.get('rut', '')
            nombres = data.get('nombres', '')
            apellidos = data.get('apellidos', '')
            correo = data.get('email', '')
            unidad = data.get('unidad', '')
            cargo = data.get('cargo', '')
            grado = data.get('grado', '')
            contrasena = data.get('contrasena', '')
        except (json.JSONDecodeError, TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Petición inválida.'}, status=400)

        if not user_id:
            return JsonResponse({'success': False, 'message': 'ID de usuario requerido.'}, status=400)

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
                contrasena=contrasena
            )

            # LOG AUDITORIA
            detalles_cambios += ", ".join(cambios) if cambios else "sin cambios significativos"
            AuditoriaService.registrar_accion(
                usuario=request.user.username,
                accion=LogAuditoria.Accion.MODIFICAR,
                tabla='User',
                registro_id=user_id,
                detalles=detalles_cambios,
                ip_address=_get_client_ip(request)
            )

            return JsonResponse({'success': True, 'message': 'Datos de usuario actualizados con éxito.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': e.message}, status=400)

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
                ip_address=_get_client_ip(request)
            )

            return JsonResponse({'success': True, 'message': 'Usuario eliminado con éxito del sistema.'})
        except ValidationError as e:
            return JsonResponse({'success': False, 'message': e.message}, status=400)
