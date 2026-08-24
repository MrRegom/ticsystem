import json
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import PermisoRequeridoMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from tickets.models import Ticket, Prioridad, Categoria, TicketHistorial, GrupoResolutor
from tickets.services.ticket_service import TicketService
from tickets.repositories.ticket_repository import TicketRepository
from equipos.models import Equipo
from mantenedores.models import Unidad, Cargo
from django.contrib.auth.models import User

class TicketsDashboardView(PermisoRequeridoMixin, LoginRequiredMixin, TemplateView):
    permiso_requerido = 'VER_TICKETS'
    template_name = 'tickets/tickets.html'

    ESTADOS_ACTIVOS = [
        Ticket.Estado.NUEVO,
        Ticket.Estado.ASIGNADO,
        Ticket.Estado.EN_PROCESO,
        # ESCALADO eliminado: al reasignar siempre vuelve a ASIGNADO
    ]
    # Los PENDIENTE_PROVEEDOR se consultan por separado y se muestran en columna EN_PROCESO
    ESTADOS_ACTIVOS_DB = [
        Ticket.Estado.NUEVO,
        Ticket.Estado.ASIGNADO,
        Ticket.Estado.EN_PROCESO,
        Ticket.Estado.PENDIENTE_PROVEEDOR,
    ]
    # Estados terminales — van a la vista Historial
    ESTADOS_TERMINALES = [
        Ticket.Estado.RESUELTO,
        Ticket.Estado.CERRADO,
        Ticket.Estado.CANCELADO,
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Solo estados activos para el Kanban (6 columnas)
        context['estados_kanban'] = [
            {'id': e, 'nombre': dict(Ticket.Estado.choices)[e]}
            for e in self.ESTADOS_ACTIVOS
        ]
        
        context['rango_filtro'] = self.request.GET.get('rango', 'semana')

        context['prioridades'] = list(Prioridad.objects.all().values('id', 'nombre', 'color_hex'))
        context['categorias'] = list(Categoria.objects.filter(activa=True).values('id', 'nombre'))
        from tickets.models import GrupoResolutor
        context['grupos_resolutores'] = list(GrupoResolutor.objects.filter(activo=True).values('id', 'nombre'))
        # Filtrar técnicos para asignar usando permisos dinámicos
        is_dispatcher = False
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol:
            if self.request.user.perfil.rol.tiene_permiso('DESPACHAR_TICKETS'):
                is_dispatcher = True
        
        if self.request.user.is_superuser:
            is_dispatcher = True

        # Todos ven únicamente a los técnicos de sus propios grupos, incluso si son despachadores.
        # Esto fuerza a que los tickets entre áreas se envíen a la cola del Grupo Resolutor y no "a dedo".
        if hasattr(self.request.user, 'grupos_resolutores'):
            user_grupos = self.request.user.grupos_resolutores.all()
            if user_grupos.exists():
                tecnicos_qs = User.objects.filter(grupos_resolutores__in=user_grupos, is_active=True, perfil__rol__permisos__RECIBIR_TICKETS=True).distinct()
            else:
                tecnicos_qs = User.objects.none()
        else:
            tecnicos_qs = User.objects.none()
        
        # Si es superusuario y no tiene grupos, le mostramos todos por si necesita administrar
        if self.request.user.is_superuser and not tecnicos_qs.exists():
             tecnicos_qs = User.objects.filter(is_active=True, perfil__rol__permisos__RECIBIR_TICKETS=True).distinct()
            
        # Agrupar técnicos por Grupo Resolutor para el frontend
        grupos_activos = GrupoResolutor.objects.filter(activo=True).prefetch_related('miembros')
        
        tecnicos_por_grupo = []
        tecnicos_ya_agrupados = set()
        
        for g in grupos_activos:
            miembros = []
            for u in tecnicos_qs.filter(grupos_resolutores=g).exclude(first_name=''):
                miembros.append({
                    'id': u.id,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                })
                tecnicos_ya_agrupados.add(u.id)
                
            if miembros:
                tecnicos_por_grupo.append({
                    'grupo_nombre': g.nombre,
                    'miembros': miembros
                })
        
        # Buscar los técnicos que tienen permiso pero no están en ningún grupo
        sin_grupo = []
        for u in tecnicos_qs.exclude(id__in=tecnicos_ya_agrupados).exclude(first_name=''):
            sin_grupo.append({
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
            })
            
        if sin_grupo:
            tecnicos_por_grupo.append({
                'grupo_nombre': 'Otros Técnicos',
                'miembros': sin_grupo
            })
            
        context['tecnicos_por_grupo'] = tecnicos_por_grupo
        context['todos_usuarios'] = list(User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))
        context['cargos'] = list(Cargo.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))

        # Tickets activos agrupados por estado para el Kanban
        from django.db.models import Q
        from django.utils import timezone
        from datetime import timedelta
        
        base_query = Ticket.objects.filter(estado__in=self.ESTADOS_ACTIVOS_DB)
        
        # Filtro de fecha
        rango = self.request.GET.get('rango', 'semana')
        hoy = timezone.now()
        if rango == 'hoy':
            base_query = base_query.filter(fecha_creacion__date=hoy.date())
        elif rango == 'semana':
            base_query = base_query.filter(fecha_creacion__gte=hoy - timedelta(days=7))
        elif rango == 'mes':
            base_query = base_query.filter(fecha_creacion__gte=hoy - timedelta(days=30))
        # Si es 'todos', no filtramos por fecha
        
        # Filtros de Permisos y Grupos para el Kanban
        grupo_filtro = self.request.GET.get('grupo', 'mis_grupos')
        context['grupo_filtro'] = grupo_filtro
        
        is_dispatcher = False
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol:
            # Mesa de Ayuda o Coordinadores suelen tener GESTIONAR o DESPACHAR
            if self.request.user.perfil.rol.tiene_permiso('DESPACHAR_TICKETS') or self.request.user.perfil.rol.tiene_permiso('GESTIONAR_TICKETS'):
                is_dispatcher = True
        if self.request.user.is_superuser:
            is_dispatcher = True
            
        if not is_dispatcher and grupo_filtro == 'todos':
            grupo_filtro = 'mis_grupos'
            context['grupo_filtro'] = 'mis_grupos'
            
        if grupo_filtro == 'mis_grupos':
            base_query = base_query.filter(
                Q(responsable=self.request.user) |
                Q(grupo_resolutor__miembros=self.request.user) |
                Q(creador=self.request.user)
            ).distinct()
        elif grupo_filtro == 'mis_tickets':
            base_query = base_query.filter(responsable=self.request.user)
        elif grupo_filtro.isdigit():
            if not is_dispatcher and not self.request.user.grupos_resolutores.filter(id=int(grupo_filtro)).exists():
                grupo_filtro = 'mis_grupos'
                context['grupo_filtro'] = 'mis_grupos'
                base_query = base_query.filter(
                    Q(responsable=self.request.user) |
                    Q(grupo_resolutor__miembros=self.request.user) |
                    Q(creador=self.request.user)
                ).distinct()
            else:
                base_query = base_query.filter(grupo_resolutor_id=int(grupo_filtro))
        elif grupo_filtro == 'todos':
            pass
            
        # Pasar los grupos disponibles al frontend
        if is_dispatcher:
            context['grupos_filtro_opciones'] = GrupoResolutor.objects.filter(activo=True)
        else:
            context['grupos_filtro_opciones'] = self.request.user.grupos_resolutores.filter(activo=True)
        context['is_dispatcher'] = is_dispatcher
                
        tickets_db = base_query.select_related('solicitante', 'responsable', 'activo', 'prioridad')

        kanban = {e: [] for e in self.ESTADOS_ACTIVOS}
        for t in tickets_db:
            # Los tickets PENDIENTE_PROVEEDOR se muestran dentro de la columna EN_PROCESO
            kanban_key = Ticket.Estado.EN_PROCESO if t.estado == Ticket.Estado.PENDIENTE_PROVEEDOR else t.estado
            if kanban_key in kanban:
                kanban[kanban_key].append({
                    'id': t.id,
                    'correlativo': t.correlativo,
                    'descripcion': t.descripcion,
                    'solicitante': t.solicitante.nombre_completo if t.solicitante else 'Desconocido',
                    'tecnico': t.responsable.get_full_name() or t.responsable.username if t.responsable else 'Sin asignar',
                    'grupo': t.grupo_resolutor.nombre if t.grupo_resolutor else 'Mesa de Ayuda',
                    'prioridad': t.prioridad.nombre if t.prioridad else 'Normal',
                    'prioridad_color': t.prioridad.color_hex if t.prioridad else '#64748b',
                    'pma': t.activo.pmalugar if t.activo else None,
                    'fecha': t.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                    'fecha_creacion_corta': t.fecha_creacion.strftime('%d/%m/%Y'),
                    'fecha_creacion_hora': t.fecha_creacion.strftime('%H:%M'),
                    'fecha_vencimiento_iso': t.fecha_vencimiento_sla.isoformat() if t.fecha_vencimiento_sla else None,
                    'en_pausa_sla': t.en_pausa_sla,
                    'is_sla_vencido': t.is_sla_vencido,
                    'pct_sla': t.porcentaje_tiempo_transcurrido
                })
        import json
        context['kanban_data'] = json.dumps(kanban)

        # Solo enviamos el conteo para no saturar la memoria
        # El historial se cargará vía AJAX con DataTables
        historial_query = Ticket.objects.filter(estado__in=self.ESTADOS_TERMINALES)
        if not is_dispatcher:
            user_groups = self.request.user.grupos_resolutores.filter(activo=True)
            historial_query = historial_query.filter(grupo_resolutor__in=user_groups)
            
        context['historial_count'] = historial_query.count()

        return context

class TicketActionView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'VER_TICKETS'
    def post(self, request, *args, **kwargs):
        # Validación extra de seguridad: solo quienes gestionan pueden crear
        if not request.user.is_superuser and not (hasattr(request.user, 'perfil') and request.user.perfil.rol and request.user.perfil.rol.tiene_permiso('GESTIONAR_TICKETS')):
            return JsonResponse({'success': False, 'message': 'No tiene permisos para crear tickets.'}, status=403)
            
        try:
            data = json.loads(request.body)
            # El solicitante lo elige el operador en el frontend
            solicitante_id = data.get('solicitante_id')
            if not solicitante_id:
                return JsonResponse({'success': False, 'message': 'Debe seleccionar un solicitante.'}, status=400)
                
            ticket = TicketService.crear_ticket(data, creador=request.user, solicitante_id=solicitante_id)

            # Obtener la prioridad con color para retornarla al frontend
            prio = ticket.prioridad
            equipo = ticket.activo

            ticket_data = {
                'id': ticket.id,
                'correlativo': ticket.correlativo,
                'descripcion': ticket.descripcion,
                'solicitante': ticket.solicitante.nombre_completo,
                'tecnico': 'Sin asignar',
                'grupo': ticket.grupo_resolutor.nombre if ticket.grupo_resolutor else 'Mesa de Ayuda',
                'prioridad': prio.nombre if prio else 'Normal',
                'prioridad_color': prio.color_hex if prio else '#64748b',
                'pma': equipo.pmalugar if equipo else None,
                'fecha': ticket.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                'fecha_vencimiento_iso': ticket.fecha_vencimiento_sla.isoformat() if ticket.fecha_vencimiento_sla else None,
                'en_pausa_sla': ticket.en_pausa_sla,
            }

            return JsonResponse({'success': True, 'ticket': ticket_data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            ticket_id = data.get('id')
            nuevo_estado = data.get('estado')
            comentario = data.get('comentario', '')
            
            if not ticket_id or not nuevo_estado:
                return JsonResponse({'success': False, 'message': 'Faltan datos'}, status=400)
                
            TicketService.cambiar_estado(ticket_id, nuevo_estado, usuario=request.user, comentario=comentario)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketDetailApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'VER_TICKETS'
    def get(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = Ticket.objects.select_related(
                'solicitante', 'responsable', 'activo', 'prioridad', 'categoria'
            ).get(id=ticket_id)
            
            historial_db = TicketHistorial.objects.filter(ticket=ticket).select_related('usuario').order_by('-fecha')
            
            historial = [{
                'id': h.id,
                'usuario': h.usuario.get_full_name() or h.usuario.username,
                'accion': h.accion,
                'valor_anterior': h.valor_anterior,
                'valor_nuevo': h.valor_nuevo,
                'comentario': h.comentario,
                'fecha': h.fecha.strftime('%d/%m/%Y %H:%M')
            } for h in historial_db]
            
            puede_resolver, _ = TicketService.validar_puede_resolver(ticket, request.user)
            es_responsable = bool(ticket.responsable and ticket.responsable.id == request.user.id)

            data = {
                'id': ticket.id,
                'correlativo': ticket.correlativo,
                'estado': ticket.get_estado_display(),
                'estado_id': ticket.estado,
                'prioridad': ticket.prioridad.nombre if ticket.prioridad else '-',
                'categoria': ticket.categoria.nombre if ticket.categoria else '-',
                'solicitante': ticket.solicitante.nombre_completo if ticket.solicitante else '-',
                'responsable_id': ticket.responsable.id if ticket.responsable else '',
                'grupo_resolutor_id': ticket.grupo_resolutor.id if ticket.grupo_resolutor else '',
                'responsable': ticket.responsable.get_full_name() or ticket.responsable.username if ticket.responsable else 'Sin asignar',
                'activo': f"{ticket.activo.articulo.nombre} {ticket.activo.marca.nombre} - {ticket.activo.serial_number or 'Sin Serie'}" if ticket.activo else 'Ninguno',
                'pma': ticket.activo.pmalugar if ticket.activo else 'No registra',
                'descripcion': ticket.descripcion,
                'fecha_creacion': ticket.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
                'fecha_vencimiento_iso': ticket.fecha_vencimiento_sla.isoformat() if ticket.fecha_vencimiento_sla else None,
                'en_pausa_sla': ticket.en_pausa_sla,
                'historial': historial,
                # Flags para el frontend — controlan visibilidad de botones
                'puede_resolver': puede_resolver,
                'es_responsable': es_responsable,
            }

            # CMDB Intelligence
            if ticket.activo:
                from django.utils import timezone
                from datetime import timedelta
                hace_30_dias = timezone.now() - timedelta(days=30)
                fallas = Ticket.objects.filter(activo=ticket.activo, fecha_creacion__gte=hace_30_dias).count()
                if fallas >= 3:
                    data['cmdb_warning'] = f"Este equipo ha presentado {fallas} fallas en los últimos 30 días."
            
            return JsonResponse({'success': True, 'ticket': data})
        except Ticket.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Ticket no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketAssignApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = ('GESTIONAR_TICKETS', 'DESPACHAR_TICKETS', 'RECIBIR_TICKETS')
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            tecnico_id = data.get('tecnico_id')
            grupo_id = data.get('grupo_id')
            comentario = data.get('comentario', '').strip()
            
            if not tecnico_id and not grupo_id:
                return JsonResponse({'success': False, 'message': 'ID de técnico o equipo resolutor requerido.'}, status=400)
                
            TicketService.asignar_ticket(ticket_id, request.user, tecnico_id=tecnico_id, grupo_id=grupo_id, comentario=comentario)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketCommentApiView(LoginRequiredMixin, View):
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            comentario = data.get('comentario')
            if not comentario:
                return JsonResponse({'success': False, 'message': 'Comentario vacío.'}, status=400)
                
            historial = TicketService.agregar_comentario(ticket_id, request.user, comentario)
            return JsonResponse({'success': True, 'historial': {
                'id': historial.id,
                'usuario': historial.usuario.get_full_name() or historial.usuario.username,
                'accion': historial.accion,
                'comentario': historial.comentario,
                'fecha': historial.fecha.strftime('%d/%m/%Y %H:%M')
            }})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketResolveApiView(LoginRequiredMixin, View):
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            solucion = data.get('solucion')
            if not solucion:
                return JsonResponse({'success': False, 'message': 'La solución es obligatoria.'}, status=400)
                
            bitacora_data = None
            if data.get('crear_bitacora'):
                bitacora_data = {
                    'tipo_registro': data.get('tipo_registro'),
                    'falla_reportada': data.get('falla_reportada'),
                    'actividades_realizadas': data.get('actividades_realizadas')
                }
                
            ticket = TicketService.resolver_ticket(ticket_id, request.user, solucion, bitacora_data)
            return JsonResponse({'success': True, 'estado': ticket.get_estado_display()})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketTakeApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = ('GESTIONAR_TICKETS', 'DESPACHAR_TICKETS', 'RECIBIR_TICKETS', 'VER_TICKETS')
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = TicketService.tomar_ticket(ticket_id, request.user)
            return JsonResponse({'success': True, 'nuevo_estado': ticket.get_estado_display()})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketReactivateApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    """Reactiva un ticket PENDIENTE_PROVEEDOR devolviendolo a EN_PROCESO."""
    permiso_requerido = ('GESTIONAR_TICKETS', 'RECIBIR_TICKETS', 'VER_TICKETS')
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            comentario = data.get('comentario', '').strip() or 'Proveedor atendido. Reanudando proceso.'
            ticket = TicketService.cambiar_estado(
                ticket_id,
                Ticket.Estado.EN_PROCESO,
                usuario=request.user,
                comentario=comentario
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class SwitchUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Debes estar logueado para usar el modo desarrollador.'}, status=403)
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            user_to_login = User.objects.get(id=user_id)
            login(request, user_to_login)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class UserSearchApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query or len(query) < 2:
            return JsonResponse({'results': []})
        
        from django.db.models import Q
        from core.models import Funcionario
        
        users = Funcionario.objects.filter(
            Q(rut__icontains=query) |
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query)
        )[:20]
        
        results = []
        for u in users:
            cargo = u.cargo if u.cargo else 'Sin Cargo'
            unidad = u.unidad.nombre if u.unidad else 'Sin Unidad'
            
            label = f"{u.nombre_completo} ({u.rut}) - {cargo} / {unidad}"
            results.append({
                'id': u.id,
                'text': label,
                'rut': u.rut,
                'nombres': u.nombres,
                'apellidos': u.apellidos,
                'correo': u.correo or '',
                'cargo': u.cargo.nombre if u.cargo else '',
                'unidad': u.unidad.nombre if u.unidad else ''
            })
            
        return JsonResponse({'results': results})

class UserCreateApiView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            rut = data.get('rut', '').strip().upper()
            nombres = data.get('nombres', '').strip()
            apellidos = data.get('apellidos', '').strip()
            cargo_nombre = data.get('cargo', '').strip()
            unidad_nombre = data.get('unidad', '').strip()
            correo = data.get('correo', '').strip()
            
            if not rut or not nombres or not apellidos:
                return JsonResponse({'success': False, 'message': 'RUT, Nombres y Apellidos son obligatorios.'}, status=400)
                
            from django.db import transaction
            from core.models import Funcionario
            from mantenedores.models import Unidad
            
            with transaction.atomic():
                if Funcionario.objects.filter(rut=rut).exists():
                    return JsonResponse({'success': False, 'message': 'El RUT ya está registrado.'}, status=400)
                
                unidad_obj = None
                if unidad_nombre:
                    unidad_obj = Unidad.objects.filter(nombre=unidad_nombre).first()
                    
                cargo_obj = None
                if cargo_nombre:
                    cargo_obj = Cargo.objects.filter(nombre=cargo_nombre).first()
                
                # Crear Funcionario
                func = Funcionario.objects.create(
                    rut=rut,
                    nombres=nombres,
                    apellidos=apellidos,
                    correo=correo,
                    unidad=unidad_obj,
                    cargo=cargo_obj
                )
                
            unidad_str = func.unidad.nombre if func.unidad else 'Sin Unidad'
            label = f"{func.nombre_completo} ({rut}) - Funcionario / {unidad_str}"
            return JsonResponse({'success': True, 'user': {
                    'id': func.id, 
                    'text': label,
                    'rut': func.rut,
                    'nombres': func.nombres,
                    'apellidos': func.apellidos,
                    'correo': func.correo,
                    'unidad': func.unidad.nombre if func.unidad else '',
                    'cargo': func.cargo.nombre if func.cargo else ''
                }})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketTakeApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'VER_TICKETS'
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            TicketService.tomar_ticket(ticket_id, request.user)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

class TicketSyncApiView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'VER_TICKETS'
    def get(self, request, *args, **kwargs):
        """
        Devuelve el conteo de tickets y datos ligeros para el Kanban auto-refresh.
        """
        # Para optimizar, solo traemos los tickets activos.
        tickets_db = Ticket.objects.filter(
            estado__in=TicketsDashboardView.ESTADOS_ACTIVOS
        ).values('id', 'estado', 'correlativo', 'responsable__username')
        
        kanban_sync = {e: [] for e in TicketsDashboardView.ESTADOS_ACTIVOS}
        for t in tickets_db:
            if t['estado'] in kanban_sync:
                kanban_sync[t['estado']].append(t['id'])
                
        return JsonResponse({'success': True, 'sync': kanban_sync})

class KEDBSearchApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query or len(query) < 3:
            return JsonResponse({'results': []})
            
        from django.db.models import Q
        from conocimiento.models import ArticuloConocimiento
        
        articulos = ArticuloConocimiento.objects.filter(
            Q(titulo__icontains=query) |
            Q(sintomas__icontains=query)
        )[:5]
        
        results = []
        for art in articulos:
            results.append({
                'id': art.id,
                'titulo': art.titulo,
                'sintomas': art.sintomas[:100] + '...' if len(art.sintomas) > 100 else art.sintomas,
                'solucion': art.solucion
            })
            
        return JsonResponse({'results': results})


class TicketNotificacionesApiView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        from tickets.models import Notificacion
        
        todas = Notificacion.objects.filter(usuario=request.user)
        no_leidas = todas.filter(leida=False)
        count = no_leidas.count()
        
        recent_notif = list(todas.order_by('-fecha_creacion')[:10])
        
        results = []
        for n in recent_notif:
            descripcion_corta = n.mensaje
            if len(descripcion_corta) > 50:
                descripcion_corta = descripcion_corta[:47] + "..."
                
            results.append({
                'id': n.id,
                'correlativo': n.ticket.correlativo if n.ticket else 'Sistema',
                'ticket_id': n.ticket.id if n.ticket else None,
                'descripcion': descripcion_corta,
                'leida': n.leida,
                'fecha': n.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            })
            
        return JsonResponse({
            'success': True,
            'count': count,
            'tickets': results
        })

class NotificacionMarcarLeidaApiView(LoginRequiredMixin, View):
    def post(self, request, notificacion_id, *args, **kwargs):
        from tickets.models import Notificacion
        try:
            noti = Notificacion.objects.get(id=notificacion_id, usuario=request.user)
            noti.leida = True
            noti.save()
            return JsonResponse({'success': True})
        except Notificacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Notificación no encontrada'}, status=404)

class NotificacionMarcarTodasLeidasApiView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        from tickets.models import Notificacion
        Notificacion.objects.filter(usuario=request.user, leida=False).update(leida=True)
        return JsonResponse({'success': True})


from django.db.models import Q

class TicketHistorialDataTablesView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    """
    Endpoint AJAX para cargar el historial de tickets cerrados en DataTables Server-Side.
    Soporta paginación, búsqueda global y ordenamiento nativo en la base de datos para manejar millones de registros.
    """
    permiso_requerido = 'VER_TICKETS'

    def get(self, request, *args, **kwargs):
        # Determinar si el usuario tiene visión global (is_dispatcher)
        is_dispatcher = False
        if hasattr(request.user, 'perfil') and request.user.perfil.rol:
            if request.user.perfil.rol.tiene_permiso('DESPACHAR_TICKETS') or request.user.perfil.rol.tiene_permiso('GESTIONAR_TICKETS'):
                is_dispatcher = True
        if request.user.is_superuser:
            is_dispatcher = True

        # Query base: Solo tickets terminales
        query = Ticket.objects.filter(estado__in=[Ticket.Estado.RESUELTO, Ticket.Estado.CERRADO, Ticket.Estado.CANCELADO])
        
        if not is_dispatcher:
            user_groups = request.user.grupos_resolutores.filter(activo=True)
            query = query.filter(grupo_resolutor__in=user_groups)

        total_records = query.count()

        # Búsqueda (Search)
        search_value = request.GET.get('search[value]', '').strip()
        if search_value:
            query = query.filter(
                Q(correlativo__icontains=search_value) |
                Q(descripcion__icontains=search_value) |
                Q(solicitante__nombres__icontains=search_value) |
                Q(solicitante__apellidos__icontains=search_value) |
                Q(responsable__first_name__icontains=search_value) |
                Q(responsable__last_name__icontains=search_value)
            )

        records_filtered = query.count()

        # Ordenamiento (Ordering)
        order_column_index = request.GET.get('order[0][column]', '6') # Por defecto Fecha Creación
        order_dir = request.GET.get('order[0][dir]', 'desc')

        # Mapeo de columnas de DataTables al modelo Django
        columns_mapping = {
            '0': 'correlativo',
            '1': 'descripcion',
            '2': 'estado',
            '3': 'prioridad__nombre',
            '4': 'solicitante__nombres',
            '5': 'responsable__first_name',
            '6': 'fecha_creacion',
            '7': 'fecha_cierre',
        }

        order_by = columns_mapping.get(order_column_index, 'fecha_creacion')
        if order_dir == 'desc':
            order_by = f'-{order_by}'

        query = query.order_by(order_by)

        # Paginación (Pagination)
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 25))
        
        if length > 0:
            query = query[start:start + length]

        # Serialización
        data = []
        for t in query.select_related('solicitante', 'responsable', 'prioridad'):
            data.append({
                'id': t.id, # Para abrir el offcanvas
                'correlativo': f'<strong>{t.correlativo}</strong>',
                'descripcion': t.descripcion[:60] + ('...' if len(t.descripcion) > 60 else ''),
                'estado': f'<span class="badge-estado badge-{t.estado}">{t.get_estado_display()}</span>',
                'prioridad': f'<span class="card-prio-badge" style="background:{t.prioridad.color_hex if t.prioridad else "#64748b"}">{t.prioridad.nombre if t.prioridad else "Normal"}</span>',
                'solicitante': t.solicitante.nombre_completo if t.solicitante else '-',
                'tecnico': t.responsable.get_full_name() or t.responsable.username if t.responsable else '-',
                'fecha_creacion': t.fecha_creacion.strftime('%d/%m/%Y'),
                'fecha_cierre': t.fecha_cierre.strftime('%d/%m/%Y') if t.fecha_cierre else '-',
            })

        return JsonResponse({
            'draw': int(request.GET.get('draw', 1)),
            'recordsTotal': total_records,
            'recordsFiltered': records_filtered,
            'data': data
        })
