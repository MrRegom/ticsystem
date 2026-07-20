from django.contrib.auth.models import User
from tickets.models import Ticket, Categoria, Prioridad
from core.models import Funcionario
from equipos.models import Equipo
from tickets.services.ticket_service import TicketService

def run_qa():
    print("=== INICIANDO QA DE FLUJO DE TICKETS (SERVICES) ===")
    
    # 1. Obtener usuarios de prueba
    dispatcher = User.objects.filter(perfil__rol__permisos__DESPACHAR_TICKETS=True).first()
    tecnico = User.objects.filter(perfil__rol__permisos__RECIBIR_TICKETS=True).first()
    
    if not dispatcher or not tecnico:
        print("ERROR: No se encontraron usuarios de prueba con los permisos adecuados.")
        return

    print(f"[+] Dispatcher seleccionado: {dispatcher.username} (Rol: {dispatcher.perfil.rol.nombre})")
    print(f"[+] Técnico seleccionado: {tecnico.username} (Rol: {tecnico.perfil.rol.nombre})")

    # Obtener dependencias
    solicitante = Funcionario.objects.first()
    if not solicitante:
        solicitante = Funcionario.objects.create(rut='11111111-1', nombres='Funcionario', apellidos='Prueba')
        
    categoria = Categoria.objects.first()
    if not categoria:
        categoria = Categoria.objects.create(nombre='Hardware')
        
    prioridad = Prioridad.objects.first()
    if not prioridad:
        prioridad = Prioridad.objects.create(nombre='Baja', sla_horas=24)
        
    equipo = Equipo.objects.first()
    
    print("\n--- PASO 1: CREACIÓN DE TICKET (Mesa de Ayuda) ---")
    datos = {
        'solicitante_id': solicitante.id,
        'categoria_id': categoria.id,
        'prioridad_id': prioridad.id,
        'asunto': 'Falla de pantalla en consulta',
        'descripcion': 'El monitor principal parpadea y se apaga.',
    }
    if equipo:
        datos['equipo_id'] = equipo.id

    ticket = TicketService.crear_ticket(datos, dispatcher, solicitante.id)
    print(f"[*] Creado Ticket {ticket.correlativo} (ID: {ticket.id}) - Estado: {ticket.estado}")

    print("\n--- PASO 2: ASIGNACIÓN DE TICKET (Mesa de Ayuda -> Técnico Nivel 2) ---")
    ticket = TicketService.asignar_ticket(ticket.id, dispatcher, tecnico_id=tecnico.id)
    print(f"[*] Estado actual: {ticket.estado}, Responsable: {ticket.responsable.username}")

    print("\n--- PASO 3: TÉCNICO PAUSA EL TICKET (Pendiente Proveedor) ---")
    try:
        ticket = TicketService.cambiar_estado(ticket.id, 'PENDIENTE_PROVEEDOR', usuario=tecnico, comentario='Falta repuesto')
        print(f"[*] Estado actual: {ticket.estado}")
    except Exception as e:
        print("Error en PAUSA:", e)

    print("\n--- PASO 4: TÉCNICO CIERRA EL TICKET (Resuelto) ---")
    try:
        ticket = TicketService.resolver_ticket(ticket.id, 'Se cambió el cable VGA', tecnico)
        print(f"[*] Estado actual: {ticket.estado}")
    except Exception as e:
        print("Fallo al resolver:", e)
        try:
            ticket = TicketService.cambiar_estado(ticket.id, 'RESUELTO', usuario=tecnico, resolucion='Se cambió el cable VGA')
            print(f"[*] Estado actual (por cambiar_estado): {ticket.estado}")
        except Exception as e:
            print("Error fatal al cerrar:", e)
    
    print("\n=== QA FINALIZADO CON ÉXITO ===")

run_qa()
