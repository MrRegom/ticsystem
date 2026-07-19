import json
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from tickets.models import Ticket, Prioridad, Categoria, TicketHistorial, GrupoResolutor
from tickets.services.ticket_service import TicketService
from tickets.repositories.ticket_repository import TicketRepository
from equipos.models import Equipo
from mantenedores.models import Unidad, Cargo
from django.contrib.auth.models import User

class TicketsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tickets/tickets.html'

    ESTADOS_ACTIVOS = [
        Ticket.Estado.NUEVO,
        Ticket.Estado.ASIGNADO,
        Ticket.Estado.EN_PROCESO,
        Ticket.Estado.ESCALADO,
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
        context['grupos_resolutores'] = list(GrupoResolutor.objects.filter(activo=True).values('id', 'nombre'))
        # Filtrar técnicos para asignar usando permisos dinámicos
        is_dispatcher = False
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol:
            if self.request.user.perfil.rol.tiene_permiso('DESPACHAR_TICKETS'):
                is_dispatcher = True
        
        if self.request.user.is_superuser:
            is_dispatcher = True

        # Para el JSONField, en la mayoría de DBs se puede buscar una clave.
        # En Django 3.1+ se puede hacer perfil__rol__permisos__RECIBIR_TICKETS=True
        if is_dispatcher:
            tecnicos_qs = User.objects.filter(is_active=True, perfil__rol__permisos__RECIBIR_TICKETS=True).distinct()
        else:
            if hasattr(self.request.user, 'grupos_resolutores'):
                user_grupos = self.request.user.grupos_resolutores.all()
                if user_grupos.exists():
                    tecnicos_qs = User.objects.filter(grupos_resolutores__in=user_grupos, is_active=True, perfil__rol__permisos__RECIBIR_TICKETS=True).distinct()
                else:
                    tecnicos_qs = User.objects.none()
            else:

                tecnicos_qs = User.objects.none()
            
        tecnicos_list = []
        for u in tecnicos_qs.select_related('perfil__rol').exclude(first_name=''):
            rol_str = f" ({u.perfil.rol.nombre})" if hasattr(u, 'perfil') and u.perfil.rol else " (Técnico)"
            tecnicos_list.append({
                'id': u.id,
                'username': u.username,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'rol_str': rol_str
            })
        context['tecnicos'] = tecnicos_list
        context['todos_usuarios'] = list(User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name'))
        context['unidades'] = list(Unidad.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))
        context['cargos'] = list(Cargo.objects.filter(activo=True).order_by('nombre').values('id', 'nombre'))
        context['equipos'] = [
            {'id': eq.id, 'label': f"{eq.articulo.nombre} {eq.marca.nombre} - {eq.serial_number or 'Sin Serie'}"}
            for eq in Equipo.objects.select_related('articulo', 'marca').all()[:1000]
        ]

        # Tickets activos agrupados por estado para el Kanban
        from django.db.models import Q
        from django.utils import timezone
        from datetime import timedelta
        
        base_query = Ticket.objects.filter(estado__in=self.ESTADOS_ACTIVOS)
        
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
        
        # Filtro de Permisos (RBAC)
        if hasattr(self.request.user, 'perfil') and self.request.user.perfil.rol:
            rol_nombre = self.request.user.perfil.rol.nombre
            if rol_nombre == 'Técnico Terreno':
                # Solo ver los asignados a él, o a los grupos resolutores donde es miembro
                base_query = base_query.filter(
                    Q(responsable=self.request.user) |
                    Q(grupo_resolutor__miembros=self.request.user)
                ).distinct()
            elif rol_nombre in ['Super Administrador', 'Operador de Mesa de Ayuda']:
                # Ver todos los tickets (no filter applied)
                pass
                
        tickets_db = base_query.select_related('solicitante', 'responsable', 'activo', 'prioridad')

        kanban = {e: [] for e in self.ESTADOS_ACTIVOS}
        for t in tickets_db:
            if t.estado in kanban:
                kanban[t.estado].append({
                    'id': t.id,
                    'correlativo': t.correlativo,
                    'descripcion': t.descripcion,
                    'solicitante': t.solicitante.nombre_completo if t.solicitante else 'Desconocido',
                    'tecnico': t.responsable.get_full_name() or t.responsable.username if t.responsable else (f"Grupo: {t.grupo_resolutor.nombre}" if t.grupo_resolutor else 'Sin asignar'),
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

        # Tickets terminales para la vista Historial (DataTables)
        tickets_historial = Ticket.objects.filter(
            estado__in=self.ESTADOS_TERMINALES
        ).select_related('solicitante', 'responsable', 'activo', 'prioridad').order_by('-fecha_creacion')

        context['historial'] = [{
            'id': t.id,
            'correlativo': t.correlativo,
            'descripcion': t.descripcion[:60] + ('...' if len(t.descripcion) > 60 else ''),
            'estado': t.get_estado_display(),
            'estado_id': t.estado,
            'solicitante': t.solicitante.nombre_completo if t.solicitante else '-',
            'tecnico': t.responsable.username if t.responsable else '-',
            'prioridad': t.prioridad.nombre if t.prioridad else 'Normal',
            'prioridad_color': t.prioridad.color_hex if t.prioridad else '#64748b',
            'fecha_creacion': t.fecha_creacion.strftime('%d/%m/%Y'),
            'fecha_cierre': t.fecha_cierre.strftime('%d/%m/%Y') if t.fecha_cierre else '-',
        } for t in tickets_historial]

        return context

class TicketActionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
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


class TicketDetailApiView(LoginRequiredMixin, View):
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
                'historial': historial
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


class TicketAssignApiView(LoginRequiredMixin, View):
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


class TicketTakeApiView(LoginRequiredMixin, View):
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            ticket = TicketService.tomar_ticket(ticket_id, request.user)
            # Automáticamente mover a EN_PROCESO cuando lo toman, según solicitud del hospital
            if ticket.estado in [Ticket.Estado.ASIGNADO, Ticket.Estado.ESCALADO, Ticket.Estado.NUEVO]:
                TicketService.cambiar_estado(ticket_id, Ticket.Estado.EN_PROCESO, request.user, "Inicio de trabajos in-situ")
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
                'correo': u.correo or ''
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
            return JsonResponse({'success': True, 'user': {'id': func.id, 'text': label}})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)


class TicketTakeApiView(LoginRequiredMixin, View):
    def post(self, request, ticket_id, *args, **kwargs):
        try:
            TicketService.tomar_ticket(ticket_id, request.user)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

class TicketSyncApiView(LoginRequiredMixin, View):
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
        from django.db.models import Q
        
        # Obtenemos los tickets activos que podrian requerir atencion
        base_query = Ticket.objects.filter(estado__in=[Ticket.Estado.NUEVO, Ticket.Estado.ASIGNADO])
        
        user = request.user
        
        # Logica basada en el rol
        is_dispatcher = False
        if hasattr(user, 'perfil') and user.perfil.rol:
            rol_nombre = user.perfil.rol.nombre
            if rol_nombre in ['Super Administrador', 'Operador de Mesa de Ayuda', 'Mesa de Ayuda']:
                is_dispatcher = True
                
        if is_dispatcher:
            # Los dispatcher ven todos los nuevos sin asignar
            tickets = base_query.filter(responsable__isnull=True, grupo_resolutor__isnull=True)
        else:
            # Los tecnicos ven los asignados a ellos o a sus grupos resolutores
            grupos = user.grupos_resolutores.all() if hasattr(user, 'grupos_resolutores') else []
            tickets = base_query.filter(
                Q(responsable=user) | 
                Q(grupo_resolutor__in=grupos, responsable__isnull=True)
            ).distinct()
            
        count = tickets.count()
        recent_tickets = list(tickets.order_by('-fecha_creacion')[:5].values('id', 'correlativo', 'estado', 'descripcion'))
        
        # Limitar descripcion para la vista previa
        for rt in recent_tickets:
            if len(rt['descripcion']) > 50:
                rt['descripcion'] = rt['descripcion'][:47] + '...'
                
        return JsonResponse({
            'success': True,
            'count': count,
            'tickets': recent_tickets
        })
