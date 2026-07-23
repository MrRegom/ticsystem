import re
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.contrib.auth.models import User
from core.models import PerfilUsuario
from core.repositories.usuario_repository import UsuarioRepository
from core.utils import normalizar_nombre

class UsuarioService:
    """
    Servicio de negocio para la gestión de operadores y usuarios del hospital.
    Implementa validaciones de RUT, normalización de credenciales y lógica de negocio desacoplada.
    """

    @classmethod
    def validar_rut(cls, rut: str) -> bool:
        """
        Algoritmo Módulo 11 para validación de RUT chileno.
        """
        rut = rut.replace(".", "").replace(" ", "").upper()
        if not re.match(r"^\d{7,8}-[0-9K]$", rut):
            return False
        
        cuerpo, dv = rut.split("-")
        suma = 0
        multiplo = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo = 2 if multiplo == 7 else multiplo + 1
        
        dvr = 11 - (suma % 11)
        dvr_str = '0' if dvr == 11 else 'K' if dvr == 10 else str(dvr)
        return dvr_str == dv

    @classmethod
    def normalizar_rut(cls, rut: str) -> str:
        """
        Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9).
        """
        rut = rut.replace(".", "").replace(" ", "").upper()
        if "-" not in rut and len(rut) > 1:
            rut = f"{rut[:-1]}-{rut[-1]}"
        return rut

    @classmethod
    def crear_usuario(cls, rut: str, nombres: str, apellidos: str, correo: str,
                      unidad: str, cargo: str, grado: str, contrasena: str,
                      foto=None, grupos: list = None, rol_id=None, is_active: bool = True) -> User:
        """
        Caso de uso: Crear un nuevo funcionario/operador en el sistema del hospital.
        """
        rut_clean = cls.normalizar_rut(rut)
        correo = correo.strip().lower()

        # Validar RUT matemáticamente
        if not cls.validar_rut(rut_clean):
            raise ValidationError("El RUT ingresado no es válido.")

        # Validar unicidad de RUT
        if UsuarioRepository.get_by_username(rut_clean) is not None:
            raise ValidationError("El RUT ya se encuentra registrado en el sistema.")

        # Validar campos vacíos
        if not nombres.strip() or not apellidos.strip():
            raise ValidationError("Los nombres y apellidos son campos obligatorios.")

        if not correo or "@" not in correo:
            raise ValidationError("Debe proporcionar un correo electrónico válido.")

        if not contrasena or len(contrasena) < 8:
            raise ValidationError("La contraseña debe tener un mínimo de 8 caracteres.")

        # Instanciar User Django
        user = User(
            username=rut_clean,
            email=correo,
            first_name=normalizar_nombre(nombres),
            last_name=normalizar_nombre(apellidos),
            is_active=is_active
        )
        user.set_password(contrasena)

        # Instanciar PerfilUsuario asociado
        perfil = PerfilUsuario(
            rut=rut_clean,
            unidad=normalizar_nombre(unidad),
            cargo=normalizar_nombre(cargo),
            grado=normalizar_nombre(grado),
            foto=foto
        )
        if rol_id:
            from core.models import Rol
            perfil.rol_id = rol_id

        user = UsuarioRepository.save(user, perfil)
        
        # Sincronizar automáticamente con la tabla Funcionario
        from core.models import Funcionario
        from mantenedores.models import Unidad
        
        unidad_obj = None
        if unidad and unidad.strip():
            unidad_obj = Unidad.objects.filter(nombre__iexact=unidad.strip()).first()
            
        Funcionario.objects.update_or_create(
            rut=rut_clean,
            defaults={
                'nombres': nombres.strip(),
                'apellidos': apellidos.strip(),
                'correo': correo.strip(),
                'unidad': unidad_obj
            }
        )

        if grupos is not None:
            from tickets.models import GrupoResolutor
            # grupos es un array de IDs, actualizamos las relaciones del usuario
            for g in GrupoResolutor.objects.all():
                if str(g.id) in grupos or g.id in grupos:
                    g.miembros.add(user)
                else:
                    g.miembros.remove(user)
        return user
    @classmethod
    def actualizar_usuario(cls, user_id: int, nombres: str, apellidos: str, correo: str,
                           unidad: str, cargo: str, grado: str, rut: str = None,
                           contrasena: str = None, foto=None, grupos: list = None,
                           rol_id=None, is_active: bool = True) -> User:
        """
        Caso de uso: Actualizar información de un operador, permitiendo actualizar el RUT
        y creando dinámicamente el perfil si no existe (ej: superusuario admin).
        """
        user = UsuarioRepository.get_by_id(user_id)
        if not user:
            raise ValidationError("El usuario no existe.")

        correo = correo.strip().lower()

        # Validar campos obligatorios
        if not nombres.strip() or not apellidos.strip():
            raise ValidationError("Los nombres y apellidos son obligatorios.")

        if not correo or "@" not in correo:
            raise ValidationError("Debe proporcionar un correo electrónico válido.")

        # Manejar cambio de RUT / username
        rut_clean = None
        if rut and rut.strip():
            raw_rut = rut.strip()
            # Permitir actualización de usuarios con usernames legacy (ej. admin) si no cambiaron su RUT
            if raw_rut != user.username:
                rut_clean = cls.normalizar_rut(raw_rut)
                if not cls.validar_rut(rut_clean):
                    raise ValidationError("El RUT ingresado no es válido.")
                
                # Si el RUT cambió, validar que no esté duplicado
                existing = UsuarioRepository.get_by_username(rut_clean)
                if existing is not None and existing.id != user.id:
                    raise ValidationError("El nuevo RUT ya se encuentra registrado en el sistema.")
                user.username = rut_clean

        # Actualizar datos de User
        user.first_name = normalizar_nombre(nombres)
        user.last_name = normalizar_nombre(apellidos)
        user.email = correo
        user.is_active = is_active

        if contrasena and contrasena.strip():
            if len(contrasena) < 8:
                raise ValidationError("La nueva contraseña debe tener al menos 8 caracteres.")
            user.set_password(contrasena)

        # Actualizar o crear Perfil de forma segura (tolerante a superusuarios sin perfil previo)
        try:
            perfil = user.perfil
        except PerfilUsuario.DoesNotExist:
            perfil = PerfilUsuario(user=user)

        # Guardar el RUT en el perfil
        perfil.rut = rut_clean if rut_clean else user.username
        perfil.unidad = unidad.strip() if unidad else ''
        perfil.cargo = cargo.strip() if cargo else ''
        perfil.grado = grado.strip() if grado else ''
        if rol_id:
            perfil.rol_id = rol_id
        if foto:
            perfil.foto = foto

        user = UsuarioRepository.save(user, perfil)
        
        # Sincronizar automáticamente con la tabla Funcionario
        from core.models import Funcionario
        from mantenedores.models import Unidad
        
        unidad_obj = None
        if unidad and unidad.strip():
            unidad_obj = Unidad.objects.filter(nombre__iexact=unidad.strip()).first()
            
        sync_rut = rut_clean if rut_clean else user.username
        Funcionario.objects.update_or_create(
            rut=sync_rut,
            defaults={
                'nombres': normalizar_nombre(nombres).strip(),
                'apellidos': normalizar_nombre(apellidos).strip(),
                'correo': correo.strip(),
                'unidad': unidad_obj
            }
        )
        if grupos is not None:
            from tickets.models import GrupoResolutor
            # grupos es un array de IDs, actualizamos las relaciones del usuario
            for g in GrupoResolutor.objects.all():
                if str(g.id) in grupos or g.id in grupos:
                    g.miembros.add(user)
                else:
                    g.miembros.remove(user)
        return user

    @classmethod
    def eliminar_usuario(cls, user_id: int, current_user_id: int) -> None:
        """
        Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-eliminación.
        """
        if int(user_id) == int(current_user_id):
            raise ValidationError("No es posible auto-eliminarse del sistema por seguridad.")

        user = UsuarioRepository.get_by_id(user_id)
        if not user:
            raise ValidationError("El usuario a eliminar no existe.")

        try:
            UsuarioRepository.delete(user)
        except ProtectedError:
            raise ValidationError(
                f"No se puede eliminar al usuario '{user.get_full_name() or user.username}' porque tiene registros asociados en el sistema."
            )

    @classmethod
    def obtener_usuarios_para_datatable(cls, start: int, length: int, search_value: str,
                                        order_column_index: int, order_dir: str, columns_data: list, status: str = 'active') -> dict:
        """
        Caso de uso para DataTables Server-side de Usuarios.
        """
        order_column_name = 'fecha_registro'
        if 0 <= order_column_index < len(columns_data):
            order_column_name = columns_data[order_column_index].get('data', 'fecha_registro')

        records = UsuarioRepository.get_paginated_list(
            start=start,
            length=length,
            search_value=search_value,
            order_column=order_column_name,
            order_dir=order_dir,
            status=status
        )

        total_records = UsuarioRepository.count_total(status=status)
        filtered_records = UsuarioRepository.count_filtered(search_value, status=status)

        data = []
        for r in records:
            # Obtener datos de perfil de forma segura
            perfil = getattr(r, 'perfil', None)
            foto_url = ''
            if perfil and perfil.foto and hasattr(perfil.foto, 'url'):
                foto_url = perfil.foto.url
            data.append({
                'id': r.id,
                'rut': r.username,
                'nombres': r.first_name,
                'apellidos': r.last_name,
                'email': r.email,
                'unidad': perfil.unidad if perfil else '',
                'cargo': perfil.cargo if perfil else '',
                'grado': perfil.grado if perfil else '',
                'fecha_registro': perfil.fecha_registro.strftime('%d/%m/%Y %H:%M') if perfil else '',
                'foto_url': foto_url,
                'is_active': r.is_active,
                'rol_id': getattr(perfil, 'rol_id', None) if perfil else None,
                'rol': perfil.rol.nombre if (perfil and perfil.rol_id) else 'Sin Perfil',
                'rol_icono': perfil.rol.icono if (perfil and perfil.rol_id) else 'fas fa-user-circle',
                'grupos': [{'id': g.id, 'nombre': g.nombre, 'icono': getattr(g, 'icono', 'fas fa-users')} for g in r.grupos_resolutores.all()]
            })

        return {
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        }

    @staticmethod
    def obtener_usuario_por_id(user_id: int) -> User:
        return UsuarioRepository.get_by_id(user_id)
