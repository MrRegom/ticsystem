import os
import django
import json
import random
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from equipos.models import Equipo
from mantenedores.models import (
    Articulo, Marca, Modelo, PMA, EstadoEquipo, SistemaOperativo, Proveedor, AreaHospitalaria
)
from tickets.models import Ticket, GrupoResolutor
from core.models import Funcionario
from django.contrib.auth.models import User

# Datos del Excel parseado
excel_data = [
    {"Nº PMA":"E-1-23","CORRELATIVO":"AA-N1-122","IP":"10.67.192.120","SERIE":"1s12k9005lcsmp2z22gm","SERIE EQUIPO":"SMP2Z22GM","NOMBRE DE RECINTO":"Sala Preparacion Pacientes", "UNIDAD":"Consultas y Procedimientos"},
    {"Nº PMA":"E-1-46","CORRELATIVO":"AA-N1-121","IP":"10.67.192.119","SERIE":"1s12k9005lcsmp2g1l0n","SERIE EQUIPO":"SMP2G1L0N","NOMBRE DE RECINTO":"Sala Entrevista", "UNIDAD":"Farmacia"},
    {"Nº PMA":"E-1-18","CORRELATIVO":"AA-N1-114","IP":"10.67.192.113","SERIE":None,"SERIE EQUIPO":None,"NOMBRE DE RECINTO":"Sala Procedimientos - Dermatologia", "UNIDAD":"Consultas Especialidades"},
    {"Nº PMA":"J-1-24","CORRELATIVO":"AA-N1-001","IP":"10.67.192.56","SERIE":"1S12K9005LCSMP2A535W","SERIE EQUIPO":"SMP2A535W","NOMBRE DE RECINTO":"Cubículos Electro Tratamiento", "UNIDAD":"Medicina Fisica"},
    {"Nº PMA":"J-1-35","CORRELATIVO":"AA-N1-008","IP":"10.67.192.64","SERIE":"1S12K9005LCSMP2Z207W","SERIE EQUIPO":"SMP2Z207W","NOMBRE DE RECINTO":"Sala NANEAS", "UNIDAD":"Pediatria"},
    {"Nº PMA":"E-1-45","CORRELATIVO":"AA-N1-097","IP":"10.67.192.102","SERIE":"1s12k9005lcsmp2z2097","SERIE EQUIPO":"SMP2Z2097","NOMBRE DE RECINTO":"Oficina Administrativa", "UNIDAD":"Administracion"},
    {"Nº PMA":"E-1-20","CORRELATIVO":"AA-N1-115","IP":"10.67.192.114","SERIE":"1s12k9005lcsmp2z215b","SERIE EQUIPO":"SMP2Z215B","NOMBRE DE RECINTO":"Sala Procedimientos - Laser (Oftalmo.)", "UNIDAD":"Oftalmologia"},
    {"Nº PMA":"J-1-24","CORRELATIVO":"AA-N1-001-2","IP":"10.67.192.57","SERIE":"1S12K9005LCSMP2A5ZZM","SERIE EQUIPO":"SMP2A5ZZM","NOMBRE DE RECINTO":"Cubículos Electro Tratamiento", "UNIDAD":"Medicina Fisica"},
    {"Nº PMA":"E-1-7","CORRELATIVO":"AA-N1-111","IP":"10.67.192.110","SERIE":"1s12k9005lcsmp2gdsng","SERIE EQUIPO":"SMP2GDSNG","NOMBRE DE RECINTO":"Box Consulta Medica Indiferenciada", "UNIDAD":"Urgencias"},
    {"Nº PMA":"J-1-8","CORRELATIVO":"AA-N1-037","IP":"10.67.192.74","SERIE":"1S12K9005LCSMP2G1QJR","SERIE EQUIPO":"SMP2G1QJR","NOMBRE DE RECINTO":"Box Consulta", "UNIDAD":"Medicina Interna"},
    {"Nº PMA":"J-1-36","CORRELATIVO":"AA-N1-003","IP":"10.67.192.61","SERIE":"1S12K9005LCSMP2GDSPR","SERIE EQUIPO":"SMP2GDSPR","NOMBRE DE RECINTO":"Sala Estimulación Cognitiva", "UNIDAD":"Geriatria"},
    {"Nº PMA":"E-1-1","CORRELATIVO":"AA-N1-045","IP":"10.67.192.81","SERIE":"1S12K9005LCSMP2G1NDH","SERIE EQUIPO":"SMP2G1NDH","NOMBRE DE RECINTO":"Modulo Información y Agenda Medica", "UNIDAD":"OIRS"},
    {"Nº PMA":"J-1-11","CORRELATIVO":"AA-N1-006","IP":"10.67.192.63","SERIE":"1S12K9005LCSMP2Z1YX0","SERIE EQUIPO":"SMP2Z1YX0","NOMBRE DE RECINTO":"Taller Actividades Vida Diaria", "UNIDAD":"Terapia Ocupacional"},
    {"Nº PMA":"E-1-11","CORRELATIVO":"AA-N1-104","IP":"10.67.192.104","SERIE":"1S12K9005LCSMP2Z209G","SERIE EQUIPO":"SMP2Z209G","NOMBRE DE RECINTO":"Box Consulta Prof. No Medico Indif.", "UNIDAD":"Kinesiologia"},
    {"Nº PMA":"E-1-25","CORRELATIVO":"AA-N1-112","IP":"10.67.192.111","SERIE":"1S12K9005LCSMP220852","SERIE EQUIPO":"SMP220852","NOMBRE DE RECINTO":"Sala Reuniones 12 Personas", "UNIDAD":"Direccion"},
    {"Nº PMA":"E-1-33","CORRELATIVO":"AA-N1-106","IP":"10.67.192.106","SERIE":"SMP-NO-SERIE-1","SERIE EQUIPO":"SN-106","NOMBRE DE RECINTO":"Sala Procedimientos - Octavo Par", "UNIDAD":"Otorrino"},
    {"Nº PMA":"E-1-3","CORRELATIVO":"AA-N1-117","IP":"10.67.192.115","SERIE":"1s12k9005lcsmp2z1wp0","SERIE EQUIPO":"SMP2Z1WP0","NOMBRE DE RECINTO":"Modulo de Admision y Recaudacion", "UNIDAD":"Recaudacion"},
    {"Nº PMA":"J-1-1","CORRELATIVO":"AA-N1-025","IP":"10.67.192.71","SERIE":"1S12K9005LCSMP2G1L0A","SERIE EQUIPO":"SMP2G1L0A","NOMBRE DE RECINTO":"Secretaria y Recepción", "UNIDAD":"Admision"},
    {"Nº PMA":"J-1-5","CORRELATIVO":"AA-N1-042","IP":"10.67.192.78","SERIE":"1S12K9005LCSMP2GDSPE","SERIE EQUIPO":"SMP2GDSPE","NOMBRE DE RECINTO":"Modulo de Admisión y Recaudación", "UNIDAD":"Urgencia Maternal"},
    {"Nº PMA":"E-1-43","CORRELATIVO":"AA-N1-094","IP":"10.67.192.99","SERIE":"1s12k9005lcsmp2g1l0g","SERIE EQUIPO":"SMP2G1L0G","NOMBRE DE RECINTO":"Modulos Despacho Farmacia", "UNIDAD":"Farmacia Despacho"}
]

print("Iniciando Seed de Equipos y Tickets...")

# 1. Crear dependencias base
art_aio, _ = Articulo.objects.get_or_create(nombre="All In One")
art_imp, _ = Articulo.objects.get_or_create(nombre="Impresora Laser")
marca_lenovo, _ = Marca.objects.get_or_create(nombre="Lenovo")
marca_hp, _ = Marca.objects.get_or_create(nombre="HP")
mod_neo, _ = Modelo.objects.get_or_create(nombre="Thinkcentre Neo 50a 24 Gen 4", marca=marca_lenovo)
mod_lj, _ = Modelo.objects.get_or_create(nombre="LaserJet Pro M404n", marca=marca_hp)
estado_ok, _ = EstadoEquipo.objects.get_or_create(nombre="Funcional", defaults={'color_hex': "#10b981"})
so_win11, _ = SistemaOperativo.objects.get_or_create(nombre="Windows 11 Pro")

equipos_creados = []
for row in excel_data:
    sn = row['SERIE'] or row['CORRELATIVO']
    if not Equipo.objects.filter(serial_number=sn).exists():
        pma_obj, _ = PMA.objects.get_or_create(nombre=row['Nº PMA'])
        
        eq = Equipo.objects.create(
            articulo=art_aio if "SMP2" in str(row['SERIE']) else art_imp,
            marca=marca_lenovo if "SMP2" in str(row['SERIE']) else marca_hp,
            modelo=mod_neo if "SMP2" in str(row['SERIE']) else mod_lj,
            pma=pma_obj,
            correlativo=row['CORRELATIVO'],
            serial_number=sn,
            serie_corta=row['SERIE EQUIPO'],
            ip=row['IP'],
            estado=estado_ok,
            so=so_win11,
            pmalugar=f"{row['NOMBRE DE RECINTO']} / {row['UNIDAD']}"
        )
        equipos_creados.append(eq)
        print(f"Equipo creado: {eq.serial_number}")
    else:
        eq = Equipo.objects.get(serial_number=sn)
        equipos_creados.append(eq)

# 2. Crear Tickets
print(f"Equipos preparados. Generando 15 tickets...")

tecnico = User.objects.filter(is_staff=True).first()
if not tecnico:
    tecnico, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True})

func_sol, _ = Funcionario.objects.get_or_create(rut='11111111-1', defaults={'nombres': 'Juan', 'apellidos': 'Perez'})

# SLAs 
from tickets.models import Prioridad
prioridades = list(Prioridad.objects.all())
if not prioridades:
    print("WARNING: No hay prioridades configuradas. Debes correr 'python manage.py load_slas'")

from tickets.models import Categoria
cat_hw, _ = Categoria.objects.get_or_create(nombre="Hardware")
cat_sw, _ = Categoria.objects.get_or_create(nombre="Software")

descripciones = [
    "PC no enciende, se quedó la pantalla negra.",
    "El equipo está muy lento y no abre el sistema HIS.",
    "Problemas para imprimir recetas médicas.",
    "Se desconecta del WiFi constantemente en el box.",
    "Pantalla parpadea con rayas azules.",
    "Teclado no responde algunas teclas.",
    "Error al abrir Chrome, dice falta de memoria.",
    "Alerta de antivirus detectada.",
    "Solicitud de instalación de software específico.",
    "El equipo huele a quemado y se apagó de golpe.",
    "Actualización fallida de Windows.",
    "No hay conexión a la red cableada.",
    "No lee la tarjeta del médico (Lector de huella/tarjeta).",
    "El mouse no funciona correctamente.",
    "Equipo pide contraseña de administrador para iniciar."
]

estados = [
    Ticket.Estado.NUEVO, Ticket.Estado.ASIGNADO, Ticket.Estado.EN_PROCESO,
    Ticket.Estado.ESCALADO, Ticket.Estado.NUEVO, Ticket.Estado.EN_PROCESO
]

from tickets.services.ticket_service import TicketService

now = timezone.now()

tickets_agregados = 0
for i in range(15):
    eq = random.choice(equipos_creados)
    estado = random.choice(estados)
    prio = random.choice(prioridades) if prioridades else None
    
    # Crear un ticket con fecha de creación variada (desde hace 2 días hasta hace 1 hora)
    horas_atras = random.randint(1, 48)
    fecha_c = now - timedelta(hours=horas_atras)
    
    datos = {
        'descripcion': descripciones[i % len(descripciones)],
        'activo_id': eq.id,
        'categoria_id': (cat_hw.id if i % 2 == 0 else cat_sw.id),
        'tipo': Ticket.Tipo.INCIDENTE,
        'impacto': Ticket.Impacto.BAJO,
        'urgencia': Ticket.Urgencia.BAJA
    }
    
    t = TicketService.crear_ticket(datos=datos, creador=tecnico, solicitante_id=func_sol.id)
    
    # Bypass auto_now_add for fecha_creacion
    Ticket.objects.filter(id=t.id).update(fecha_creacion=fecha_c, estado=estado)
    t.refresh_from_db()
    
    # Calculate vencimiento for historical consistency
    if prio:
        t.fecha_vencimiento_sla = t.fecha_creacion + timedelta(hours=prio.sla_horas)
        Ticket.objects.filter(id=t.id).update(fecha_vencimiento_sla=t.fecha_vencimiento_sla, prioridad_id=prio.id)
        
    if estado in [Ticket.Estado.ASIGNADO, Ticket.Estado.EN_PROCESO, Ticket.Estado.ESCALADO]:
        t.responsable = tecnico
        t.save()
        
    tickets_agregados += 1
    
print(f"¡Se han generado {tickets_agregados} tickets de prueba con SLA simulado!")
