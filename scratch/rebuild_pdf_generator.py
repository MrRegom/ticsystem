import os

def generate_new_pdf_generator(py_path):
    code = """import os
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.units import inch

def generar_pdf_acta(acta, firmas_paths=None, datos_ui_detalles=None):
    \"\"\"
    Genera un PDF para el Acta dada usando ReportLab y retorna el archivo BytesIO.
    Diseño compacto de una hoja, estilo Comprobante de Entrega.
    \"\"\"
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    
    COLOR_PRIMARY = colors.HexColor("#002a54")
    COLOR_SECONDARY = colors.HexColor("#006FB3")
    COLOR_TEXT = colors.black
    COLOR_BORDER = colors.black

    styles.add(ParagraphStyle(name='Center', alignment=1, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle(name='Right', alignment=2, textColor=COLOR_TEXT, fontSize=9))
    styles.add(ParagraphStyle(name='Justify', alignment=4, leading=14, textColor=COLOR_TEXT, fontSize=9))
    
    styles.add(ParagraphStyle(
        name='TableBody', 
        fontName='Helvetica', 
        fontSize=9, 
        alignment=1, 
        textColor=COLOR_TEXT
    ))
    
    styles.add(ParagraphStyle(
        name='SectionTitle', 
        fontName='Helvetica-Bold', 
        fontSize=10, 
        textColor=colors.white,
        alignment=0
    ))
    
    def section_header(title):
        return Table([[Paragraph(f"<b>{title}</b>", styles['SectionTitle'])]], 
                     colWidths=[520], 
                     style=TableStyle([
                         ('BACKGROUND', (0,0), (-1,-1), COLOR_PRIMARY), 
                         ('TOPPADDING', (0,0), (-1,-1), 4), 
                         ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                         ('ALIGN', (0,0), (-1,-1), 'LEFT')
                     ]))
    
    elements = []
    
    encargado_nombre = acta.encargado.get_full_name() if acta.encargado else "Soporte TI"
    
    # 1. HEADER
    logo_hmm_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logoHospital.jpeg')
    
    title_html = (
        f"<font color='black' size=12><b>COMPROBANTE DE ENTREGA Y RECEPCIÓN</b></font><br/>"
        f"<font color='black' size=9><i>SOPORTE TÉCNICO E INFRAESTRUCTURA TIC - H.M.M.</i></font>"
    )
    
    if acta.fecha:
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        mes = meses[acta.fecha.month - 1]
        fecha_str = acta.fecha.strftime(f"%d de {mes} de %Y")
    else:
        fecha_str = ""
        
    header_data = [
        [
            Image(logo_hmm_path, width=100, height=45, kind='proportional') if os.path.exists(logo_hmm_path) else Paragraph("<b>MINSAL</b>", styles['Center']),
            Paragraph(title_html, styles['Center']),
            Paragraph(f"<b>HOSPITAL<br/>MARGA MARGA</b>", ParagraphStyle('RightBold', alignment=2, fontName='Helvetica-Bold', fontSize=10))
        ]
    ]
    t_header = Table(header_data, colWidths=[120, 280, 120])
    t_header.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_header)
    
    # Fecha align right, code underneath
    elements.append(Spacer(1, 15))
    elements.append(Paragraph(f"Viña del Mar, {fecha_str}", styles['Right']))
    elements.append(Spacer(1, 15))
    
    # 2. IDENTIFICACIÓN DEL RECEPTOR
    elements.append(section_header("I. IDENTIFICACIÓN DEL RECEPTOR"))
    
    receptor_data = [
        [Paragraph("<b>Nombre:</b>", styles['TableBody']), Paragraph(acta.receptor_nombre, styles['TableBody'])],
        [Paragraph("<b>RUT:</b>", styles['TableBody']), Paragraph(acta.receptor_rut or "No especificado", styles['TableBody'])],
        [Paragraph("<b>Unidad/Servicio:</b>", styles['TableBody']), Paragraph(acta.receptor_unidad or "No especificado", styles['TableBody'])],
        [Paragraph("<b>Cargo:</b>", styles['TableBody']), Paragraph(acta.receptor_cargo or "No especificado", styles['TableBody'])]
    ]
    t_receptor = Table(receptor_data, colWidths=[120, 400])
    t_receptor.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(Spacer(1, 5))
    elements.append(t_receptor)
    elements.append(Spacer(1, 15))
    
    # 3. DETALLE DEL EQUIPAMIENTO
    elements.append(section_header("II. DETALLE DEL EQUIPAMIENTO ENTREGADO"))
    
    header_equip = [
        Paragraph("<b>Nombre del Bien</b>", ParagraphStyle('TH', parent=styles['TableBody'])),
        Paragraph("<b>Especificaciones / Marca / Modelo</b>", ParagraphStyle('TH', parent=styles['TableBody'])),
        Paragraph("<b>Nº de Serie / ID</b>", ParagraphStyle('TH', parent=styles['TableBody']))
    ]
    equip_data = [header_equip]
    
    if datos_ui_detalles and len(datos_ui_detalles) > 0:
        for item in datos_ui_detalles:
            equip_data.append([
                Paragraph(item.get('articulo', ''), styles['TableBody']),
                Paragraph(item.get('marcamodelo', f"{item.get('tipo_item')} {item.get('id_item')}"), styles['TableBody']),
                Paragraph(item.get('serie', 'S/N'), styles['TableBody'])
            ])
    else:
        for d in acta.detalles.all():
            equip_data.append([
                Paragraph(d.articulo or "", styles['TableBody']),
                Paragraph(f"{d.tipo_item} {d.id_item}", styles['TableBody']),
                Paragraph(d.serie or "S/N", styles['TableBody'])
            ])
    
    t_equip = Table(equip_data, colWidths=[140, 240, 140])
    t_equip.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ]))
    elements.append(Spacer(1, 5))
    elements.append(t_equip)
    elements.append(Spacer(1, 15))
    
    # 4. TEXTO LEGAL
    texto1 = f"<i>Mediante la presente, se hace entrega a la Unidad/Servicio <b>{acta.receptor_unidad or 'N/A'}</b>, cuyo receptor es <b>{acta.receptor_nombre}</b>, del equipamiento detallado en este documento, para su uso en funciones institucionales.</i>"
    texto2 = f"<i>El receptor <b>{acta.receptor_nombre}</b> declara recibir conforme el o los equipos y asume responsabilidad por su cuidado, mantención y uso adecuado.</i>"
    texto3 = f"<i>Ante cualquier anomalía, pérdida, robo o extravío, se deberá informar oportunamente a la Unidad TIC (Soporte Técnico) para gestionar las acciones correspondientes.</i>"
    
    legal_data = [[ Paragraph(f"{texto1}<br/><br/>{texto2}<br/><br/>{texto3}", styles['Justify']) ]]
    t_legal = Table(legal_data, colWidths=[520])
    t_legal.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(t_legal)
    elements.append(Spacer(1, 15))
    
    # 5. OBSERVACIONES
    if acta.observaciones:
        elements.append(section_header("III. OBSERVACIONES ADICIONALES"))
        obs_data = [[Paragraph(f"<i>{acta.observaciones}</i>", styles['Justify'])]]
        t_obs = Table(obs_data, colWidths=[520])
        t_obs.setStyle(TableStyle([
            ('PADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(Spacer(1, 5))
        elements.append(t_obs)
        elements.append(Spacer(1, 15))
    else:
        elements.append(Spacer(1, 15))
        
    # 6. FIRMAS
    # For signatures we use 200px width max
    firma_rec_path = firmas_paths.get('receptor') if firmas_paths else (acta.firma_receptor.path if acta.firma_receptor else None)
    firma_tic_path = firmas_paths.get('tic') if firmas_paths else (acta.firma_encargado.path if acta.firma_encargado else None)
    
    img_rec = Image(firma_rec_path, width=120, height=60) if firma_rec_path and os.path.exists(firma_rec_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    img_tic = Image(firma_tic_path, width=120, height=60) if firma_tic_path and os.path.exists(firma_tic_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    
    titulo_rec = f"<b>{acta.receptor_nombre}</b><br/><font size=8>Receptor</font>"
    titulo_tic = f"<b>{encargado_nombre}</b><br/><font size=8>Responsable TIC</font>"

    firmas_data = [
        [img_rec, img_tic],
        [Paragraph(titulo_rec, styles['Center']), Paragraph(titulo_tic, styles['Center'])]
    ]
    t_firmas = Table(firmas_data, colWidths=[260, 260])
    t_firmas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LINEABOVE', (0,1), (0,1), 1, colors.black),
        ('LINEABOVE', (1,1), (1,1), 1, colors.black),
        ('TOPPADDING', (0,1), (-1,1), 4),
    ]))
    
    # Try to keep signatures together with the content by putting them after a spacer
    # ReportLab handles page breaks automatically, but we want it compact.
    elements.append(Spacer(1, 30))
    elements.append(t_firmas)
    
    # Footer
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("<font color='gray' size=7><i>Hospital Marga Marga - Generado Digitalmente por TIC System | Página 1</i></font>", styles['Center']))
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
"""
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(code)
    
    print("PDF generator fully rewritten to match Fricke compact style.")

generate_new_pdf_generator(r'c:\proyectos\ticsystem\actas\utils\pdf_generator.py')
