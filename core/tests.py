from django.test import TestCase
from django.core.exceptions import ValidationError


class AuditoriaServiceTests(TestCase):
    """
    Pruebas unitarias para validar el registro de logs de auditoría.
    """
    def test_registrar_accion_exitosa(self):
        from core.services.auditoria_service import AuditoriaService
        from core.models import LogAuditoria

        log = AuditoriaService.registrar_accion(
            usuario='test_admin',
            accion=LogAuditoria.Accion.CREAR,
            tabla='CorreoInstitucional',
            registro_id=45,
            detalles='Creación de cuenta de prueba',
            ip_address='192.168.1.100'
        )

        self.assertIsNotNone(log.id)
        self.assertEqual(log.usuario, 'test_admin')
        self.assertEqual(log.accion, LogAuditoria.Accion.CREAR)
        self.assertEqual(log.tabla, 'CorreoInstitucional')
        self.assertEqual(log.registro_id, '45')
        self.assertEqual(log.detalles, 'Creación de cuenta de prueba')
        self.assertEqual(log.ip_address, '192.168.1.100')
        self.assertIsNotNone(log.fecha_registro)


class UsuarioServiceTests(TestCase):
    """
    Pruebas unitarias para validar las reglas de negocio en UsuarioService.
    """
    def setUp(self):
        # Necesitamos un usuario creador para poder probar eliminación, etc.
        from django.contrib.auth.models import User
        from core.models import PerfilUsuario
        self.admin_user = User.objects.create_user(
            username='11111111-1',
            email='admin@hospitalfricke.cl',
            first_name='Admin',
            last_name='Soto',
            is_active=True
        )
        self.admin_perfil = PerfilUsuario.objects.create(
            user=self.admin_user,
            rut='11111111-1',
            unidad='Informática',
            cargo='Administrador',
            grado='10'
        )

    def test_validar_rut_usuario(self):
        from core.services.usuario_service import UsuarioService
        self.assertTrue(UsuarioService.validar_rut('19000000-1'))
        self.assertTrue(UsuarioService.validar_rut('12.345.678-5'))
        self.assertFalse(UsuarioService.validar_rut('19.000.000-2'))

    def test_normalizar_rut_usuario(self):
        from core.services.usuario_service import UsuarioService
        self.assertEqual(UsuarioService.normalizar_rut('19.000.000-1'), '19000000-1')
        self.assertEqual(UsuarioService.normalizar_rut('123456789'), '12345678-9')

    def test_crear_usuario_valido(self):
        from core.services.usuario_service import UsuarioService
        user = UsuarioService.crear_usuario(
            rut='12.345.678-5',
            nombres='Juan Pedro',
            apellidos='Pérez Rojas',
            correo='juan.perez@hospitalfricke.cl',
            unidad='Urgencias',
            cargo='Enfermero',
            grado='15',
            contrasena='SecurePass123!'
        )
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, '12345678-5')
        self.assertEqual(user.perfil.unidad, 'Urgencias')
        self.assertEqual(user.perfil.grado, '15')

    def test_crear_usuario_rut_invalido(self):
        from core.services.usuario_service import UsuarioService
        with self.assertRaises(ValidationError):
            UsuarioService.crear_usuario(
                rut='12.345.678-9',  # DV inválido
                nombres='Juan',
                apellidos='Pérez',
                correo='juan.perez@hospitalfricke.cl',
                unidad='Urgencias',
                cargo='Enfermero',
                grado='15',
                contrasena='SecurePass123!'
            )

    def test_crear_usuario_duplicado(self):
        from core.services.usuario_service import UsuarioService
        # El rut '11.111.111-1' ya está en setUp
        with self.assertRaises(ValidationError):
            UsuarioService.crear_usuario(
                rut='11.111.111-1',
                nombres='Otro',
                apellidos='Usuario',
                correo='otro@hospitalfricke.cl',
                unidad='Informática',
                cargo='Operador',
                grado='12',
                contrasena='SecurePass123!'
            )

    def test_actualizar_usuario(self):
        from core.services.usuario_service import UsuarioService
        user = UsuarioService.crear_usuario(
            rut='12.345.678-5',
            nombres='Juan',
            apellidos='Pérez',
            correo='juan.perez@hospitalfricke.cl',
            unidad='Urgencias',
            cargo='Enfermero',
            grado='15',
            contrasena='SecurePass123!'
        )
        # Modificar incluyendo cambio de RUT
        updated_user = UsuarioService.actualizar_usuario(
            user_id=user.id,
            nombres='Juan Carlos',
            apellidos='Pérez',
            correo='jc.perez@hospitalfricke.cl',
            unidad='UCI',
            cargo='Enfermero Supervisor',
            grado='13',
            rut='14.852.369-K'
        )
        self.assertEqual(updated_user.username, '14852369-K')
        self.assertEqual(updated_user.first_name, 'Juan Carlos')
        self.assertEqual(updated_user.email, 'jc.perez@hospitalfricke.cl')
        self.assertEqual(updated_user.perfil.rut, '14852369-K')
        self.assertEqual(updated_user.perfil.unidad, 'UCI')
        self.assertEqual(updated_user.perfil.cargo, 'Enfermero Supervisor')
        self.assertEqual(updated_user.perfil.grado, '13')

    def test_actualizar_usuario_sin_perfil(self):
        from django.contrib.auth.models import User
        from core.services.usuario_service import UsuarioService
        # Crear un usuario directamente por base de datos, sin perfil
        user_sin_perfil = User.objects.create_user(
            username='55555555-5',
            email='reinaldo@hospitalfricke.cl',
            first_name='Reinaldo',
            last_name='Gomez',
            is_active=True
        )
        
        # Al actualizar el usuario, el servicio debe crear el PerfilUsuario dinámicamente sin fallar
        updated_user = UsuarioService.actualizar_usuario(
            user_id=user_sin_perfil.id,
            nombres='Reinaldo Modificado',
            apellidos='Gomez Suarez',
            correo='reinaldo.g@hospitalfricke.cl',
            unidad='TIC',
            cargo='Profesional',
            grado='15',
            rut='55555555-5'
        )
        self.assertEqual(updated_user.first_name, 'Reinaldo Modificado')
        self.assertEqual(updated_user.perfil.unidad, 'TIC')
        self.assertEqual(updated_user.perfil.rut, '55555555-5')

    def test_eliminar_usuario_impidiendo_auto_eliminacion(self):
        from core.services.usuario_service import UsuarioService
        user_to_delete = UsuarioService.crear_usuario(
            rut='12.345.678-5',
            nombres='Juan',
            apellidos='Pérez',
            correo='juan.perez@hospitalfricke.cl',
            unidad='Urgencias',
            cargo='Enfermero',
            grado='15',
            contrasena='SecurePass123!'
        )
        
        # Intentar auto-eliminarse debe fallar
        with self.assertRaises(ValidationError):
            UsuarioService.eliminar_usuario(user_to_delete.id, user_to_delete.id)
            
        # Admin elimina a Juan: debe funcionar
        UsuarioService.eliminar_usuario(user_to_delete.id, self.admin_user.id)
        self.assertIsNone(UsuarioService.obtener_usuario_por_id(user_to_delete.id))

    def test_datatable_usuarios(self):
        from core.services.usuario_service import UsuarioService
        result = UsuarioService.obtener_usuarios_para_datatable(
            start=0,
            length=10,
            search_value='Admin',
            order_column_index=0,
            order_dir='asc',
            columns_data=[{'data': 'rut'}]
        )
        self.assertEqual(result['recordsTotal'], 1)
        self.assertEqual(result['recordsFiltered'], 1)
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0]['rut'], '11111111-1')

