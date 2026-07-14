from datetime import datetime
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.models import User
from tickets.models import Ticket, TicketHistorial, Prioridad, Categoria, GrupoResolutor
from tickets.repositories.ticket_repository import TicketRepository
from equipos.repositories.equipo_repository import EquipoRepository
from tickets.services.notificacion_service import NotificacionService

class TicketService:
    """
    Capa de Reglas de Negocio (Service) para Tickets.
    Maneja la creación, cambios de estado y registro inmutable en el historial.
    """

    @staticmethod
    def _generar_correlativo() -> str:
        """
        Genera un correlativo secuencial anual único y thread-safe.
        Usa select_for_update() para bloquear la fila durante la transacción
        y evitar duplicados en entornos concurrentes.
        """
        anio_actual = timezone.now().year
        # Contar tickets del año actual (dentro del mismo bloque @transaction.atomic del llamador)
        count = Ticket.objects.select_for_update().filter(
            correlativo__startswith=f"TCK-{anio_actual}-"
        ).count()
        return f"TCK-{anio_actual}-{count + 1:04d}"

    @staticmethod
    @transaction.atomic
    def crear_ticket(datos: dict, creador: User, solicitante_id: int) -> Ticket:
        # Validar equipo si se provee — el id puede llegar como string desde el form
        equipo_id = datos.get('activo_id') or None
        equipo = None
        if equipo_id:
            try:
                equipo = EquipoRepository.get_by_id(int(equipo_id))
            except (ValueError, TypeError):
                equipo = None
            if not equipo:
                raise ValueError("El Activo proporcionado no existe.")
                
        from core.models import Funcionario
        solicitante = Funcionario.objects.filter(id=solicitante_id).first()
        if not solicitante:
            raise ValueError("El Funcionario solicitante no existe.")

        impacto = int(datos.get('impacto', Ticket.Impacto.BAJO))
        urgencia = int(datos.get('urgencia', Ticket.Urgencia.BAJA))

        ticket = Ticket(
            correlativo=TicketService._generar_correlativo(),
            estado=Ticket.Estado.NUEVO,
            creador=creador,
            solicitante=solicitante,
            activo=equipo,
            tipo=datos.get('tipo', Ticket.Tipo.INCIDENTE),
            impacto=impacto,
            urgencia=urgencia,
            descripcion=datos.get('descripcion', '').strip(),
            anexo_contacto=datos.get('anexo_contacto', '').strip()
        )
        
        # Calcular SLA si la matriz existe
        from sla.models import SLAMatrix
        from datetime import timedelta
        matriz = SLAMatrix.objects.filter(impacto=impacto, urgencia=urgencia).first()
        if matriz:
            ticket.prioridad_id = matriz.prioridad_id
            ticket.fecha_vencimiento_sla = timezone.now() + timedelta(hours=matriz.tiempo_resolucion_horas)
        else:
            if datos.get('prioridad_id'):
                ticket.prioridad_id = datos['prioridad_id']
                
        if datos.get('categoria_id'):
            ticket.categoria_id = datos['categoria_id']
            # Enrutamiento automático al grupo resolutor
            from tickets.models import Categoria
            cat = Categoria.objects.filter(id=datos['categoria_id']).first()
            if cat and cat.grupo_resolutor_id:
                ticket.grupo_resolutor_id = cat.grupo_resolutor_id
            
        ticket.save()

        # Auditoría inmutable
        TicketHistorial.objects.create(
            ticket=ticket,
            usuario=creador,
            accion="Ticket Creado vía Mesa de Ayuda",
            comentario=datos.get('descripcion', '')
        )
        
        # Enviar correo de notificación
        NotificacionService.notificar_creacion(ticket)

        return ticket

    @staticmethod
    @transaction.atomic
    def cambiar_estado(ticket_id: int, nuevo_estado: str, usuario: User, comentario: str = "") -> Ticket:
        ticket = TicketRepository.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket no encontrado.")

        if nuevo_estado not in [choice[0] for choice in Ticket.Estado.choices]:
            raise ValueError("Estado inválido.")

        estado_anterior = ticket.estado
        ticket.estado = nuevo_estado

        if nuevo_estado == Ticket.Estado.ASIGNADO and not ticket.fecha_asignacion:
            ticket.fecha_asignacion = timezone.now()
            
        if nuevo_estado in [Ticket.Estado.CERRADO, Ticket.Estado.RESUELTO]:
            ticket.fecha_cierre = timezone.now()

        ticket.save()

        TicketHistorial.objects.create(
            ticket=ticket,
            usuario=usuario,
            accion=f"Cambio de Estado: {estado_anterior} -> {nuevo_estado}",
            valor_anterior=estado_anterior,
            valor_nuevo=nuevo_estado,
            comentario=comentario
        )

        # Si el ticket se resolvió/cerró y tiene un activo asociado, anotarlo en su Bitácora automáticamente.
        if nuevo_estado in [Ticket.Estado.CERRADO, Ticket.Estado.RESUELTO] and estado_anterior not in [Ticket.Estado.CERRADO, Ticket.Estado.RESUELTO]:
            if ticket.activo:
                from equipos.models import BitacoraEquipo
                BitacoraEquipo.objects.create(
                    equipo=ticket.activo,
                    tecnico=usuario,
                    tipo_registro=BitacoraEquipo.TipoRegistro.MANTENCION,
                    fecha_mantenimiento=timezone.now().date(),
                    fecha_devolucion=timezone.now().date(),
                    solicitante=ticket.solicitante.nombres + " " + ticket.solicitante.apellidos if ticket.solicitante else None,
                    falla_reportada=f"[Ticket {ticket.correlativo}] {ticket.descripcion}"[:255],
                    actividades_realizadas=comentario if comentario else f"Ticket {nuevo_estado.lower()}"
                )

        return ticket

    @staticmethod
    @transaction.atomic
    def asignar_ticket(ticket_id: int, usuario: User, tecnico_id: int = None, grupo_id: int = None, comentario: str = None) -> Ticket:
        """
        Asigna el ticket a un técnico específico o a un grupo resolutor.
        """
        ticket = TicketRepository.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket no encontrado.")

        if not tecnico_id and not grupo_id:
            raise ValueError("Debe seleccionar un técnico o un equipo resolutor.")

        if tecnico_id:
            tecnico = User.objects.filter(id=tecnico_id).first()
            if not tecnico:
                raise ValueError("Técnico no encontrado.")

            if ticket.responsable and ticket.responsable.id == int(tecnico_id):
                raise ValueError("El ticket ya está asignado a este técnico.")

            tecnico_anterior = ticket.responsable.username if ticket.responsable else "Ninguno"
            ticket.responsable = tecnico
            
            if ticket.estado == Ticket.Estado.NUEVO:
                ticket.estado = Ticket.Estado.ASIGNADO
                ticket.fecha_asignacion = timezone.now()
                
            ticket.save()

            TicketHistorial.objects.create(
                ticket=ticket,
                usuario=usuario,
                accion="Técnico Asignado",
                valor_anterior=tecnico_anterior,
                valor_nuevo=tecnico.username,
                comentario=comentario
            )
        elif grupo_id:
            grupo = GrupoResolutor.objects.filter(id=grupo_id).first()
            if not grupo:
                raise ValueError("Equipo resolutor no encontrado.")

            if ticket.grupo_resolutor and ticket.grupo_resolutor.id == int(grupo_id) and not ticket.responsable:
                raise ValueError("El ticket ya está asignado a este equipo resolutor.")

            grupo_anterior = ticket.grupo_resolutor.nombre if ticket.grupo_resolutor else "Ninguno"
            ticket.grupo_resolutor = grupo
            ticket.responsable = None # Quitamos el técnico individual al reasignar al grupo general
            
            # Resetear estado para que el nuevo grupo lo vea en su bandeja de entrada (ASIGNADO o ESCALADO)
            if ticket.estado == Ticket.Estado.NUEVO:
                ticket.estado = Ticket.Estado.ASIGNADO
            elif ticket.estado == Ticket.Estado.EN_PROCESO:
                ticket.estado = Ticket.Estado.ESCALADO
                
            ticket.fecha_asignacion = timezone.now()
            ticket.save()

            TicketHistorial.objects.create(
                ticket=ticket,
                usuario=usuario,
                accion="Equipo Resolutor Asignado (Escalado/Reasignado)",
                valor_anterior=grupo_anterior,
                valor_nuevo=grupo.nombre,
                comentario=comentario
            )

        return ticket

    @staticmethod
    @transaction.atomic
    def tomar_ticket(ticket_id: int, usuario: User) -> Ticket:
        """
        Un técnico (miembro de un grupo o en general) se auto-asigna el ticket.
        """
        ticket = TicketRepository.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket no encontrado.")

        if ticket.responsable and ticket.responsable.id == usuario.id:
            raise ValueError("Ya tienes asignado este ticket.")
            
        tecnico_anterior = ticket.responsable.username if ticket.responsable else "Ninguno"
        ticket.responsable = usuario
        
        if ticket.estado == Ticket.Estado.NUEVO or ticket.estado == Ticket.Estado.ESCALADO:
            ticket.estado = Ticket.Estado.ASIGNADO
            ticket.fecha_asignacion = timezone.now()
            
        ticket.save()

        TicketHistorial.objects.create(
            ticket=ticket,
            usuario=usuario,
            accion="Ticket Tomado (Self-Assign)",
            valor_anterior=tecnico_anterior,
            valor_nuevo=usuario.username
        )

        return ticket

    @staticmethod
    @transaction.atomic
    def agregar_comentario(ticket_id: int, usuario: User, comentario: str) -> TicketHistorial:
        ticket = TicketRepository.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket no encontrado.")
            
        if not comentario or not comentario.strip():
            raise ValueError("El comentario no puede estar vacío.")

        historial = TicketHistorial.objects.create(
            ticket=ticket,
            usuario=usuario,
            accion="Comentario Añadido",
            comentario=comentario.strip()
        )
        return historial

    @staticmethod
    @transaction.atomic
    def resolver_ticket(ticket_id: int, usuario: User, solucion: str, bitacora_data: dict = None) -> Ticket:
        ticket = TicketRepository.get_ticket_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket no encontrado.")
            
        if not solucion or not solucion.strip():
            raise ValueError("La solución no puede estar vacía.")

        estado_anterior = ticket.estado
        ticket.estado = Ticket.Estado.RESUELTO
        ticket.solucion = solucion.strip()
        ticket.fecha_cierre = timezone.now()
        ticket.save()

        TicketHistorial.objects.create(
            ticket=ticket,
            usuario=usuario,
            accion=f"Ticket Resuelto",
            valor_anterior=estado_anterior,
            valor_nuevo=Ticket.Estado.RESUELTO,
            comentario=f"Solución: {solucion.strip()}"
        )

        if bitacora_data and ticket.activo:
            from equipos.models import BitacoraEquipo
            BitacoraEquipo.objects.create(
                equipo=ticket.activo,
                tecnico=usuario,
                fecha_mantenimiento=timezone.localdate(),
                fecha_devolucion=timezone.localdate(),
                solicitante=ticket.solicitante.nombre_completo if ticket.solicitante else None,
                falla_reportada=bitacora_data.get('falla_reportada', ''),
                actividades_realizadas=bitacora_data.get('actividades_realizadas', solucion.strip()),
                servicio_unidad=ticket.activo.pma.recinto.unidad.nombre if ticket.activo.pma and ticket.activo.pma.recinto and ticket.activo.pma.recinto.unidad else None,
                tipo_registro=bitacora_data.get('tipo_registro', BitacoraEquipo.TipoRegistro.MANTENCION)
            )

        # Enviar correo de notificación
        NotificacionService.notificar_resolucion(ticket, solucion.strip())

        return ticket
