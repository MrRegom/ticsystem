import os
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

def generar_pdf_acta(acta, firmas_paths=None):
    """
    Genera un PDF para el Acta dada usando ReportLab y retorna el archivo BytesIO.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))
    styles.add(ParagraphStyle(name='Justify', alignment=4, leading=14))
    styles.add(ParagraphStyle(name='TableHeader', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1))
    styles.add(ParagraphStyle(name='TableBody', fontName='Helvetica', fontSize=9, alignment=1))
    
    elements = []
    
    # 1. HEADER (Logos y Título)
    # Buscamos si existe un logo de Marga Marga en static
    logo_minsal_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_minsal.png')
    logo_hmm_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_hospital.png') # Placeholder
    
    header_data = [
        [
            Image(logo_minsal_path, width=100, height=50) if os.path.exists(logo_minsal_path) else Paragraph("<b>MINSAL</b>", styles['Center']),
            Paragraph("<b>COMPROBANTE DE ENTREGA Y RECEPCIÓN</b><br/><font size=10><i>SOPORTE TÉCNICO E INFRAESTRUCTURA TIC - H.M.M.</i></font>", styles['Center']),
            Image(logo_hmm_path, width=80, height=80) if os.path.exists(logo_hmm_path) else Paragraph("<b>HOSPITAL<br/>MARGA MARGA</b>", styles['Center'])
        ]
    ]
    t_header = Table(header_data, colWidths=[120, 290, 120])
    t_header.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_header)
    elements.append(Spacer(1, 20))
    
    # Fecha
    fecha_str = acta.fecha.strftime("%d/%m/%Y %H:%M") if acta.fecha else ""
    elements.append(Paragraph(f"Viña del Mar, {fecha_str}", styles['Right']))
    elements.append(Spacer(1, 15))
    
    # 2. IDENTIFICACIÓN DEL RECEPTOR
    elements.append(Paragraph("<b>I. IDENTIFICACIÓN DEL RECEPTOR</b>", ParagraphStyle('H1', parent=styles['Normal'], backColor=colors.HexColor("#002a54"), textColor=colors.white, padding=5)))
    elements.append(Spacer(1, 10))
    
    receptor_data = [
        ["Nombre:", acta.receptor_nombre],
        ["RUT:", acta.receptor_rut or ""],
        ["Unidad/Servicio:", acta.receptor_unidad or ""],
        ["Cargo:", acta.receptor_cargo or ""]
    ]
    t_receptor = Table(receptor_data, colWidths=[120, 410])
    t_receptor.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_receptor)
    elements.append(Spacer(1, 15))
    
    # 3. DETALLE DEL EQUIPAMIENTO
    elements.append(Paragraph("<b>II. DETALLE DEL EQUIPAMIENTO ENTREGADO</b>", ParagraphStyle('H2', parent=styles['Normal'], backColor=colors.HexColor("#002a54"), textColor=colors.white, padding=5)))
    elements.append(Spacer(1, 10))
    
    equip_data = [["Nombre del Bien", "Especificaciones / Marca / Modelo", "N° de Serie / ID"]]
    for d in acta.detalles.all():
        equip_data.append([
            Paragraph(d.articulo or "", styles['TableBody']),
            Paragraph(f"{d.tipo_item} {d.id_item}", styles['TableBody']), # Puede mejorarse si se guarda la marca en detalle
            Paragraph(d.serie or "S/N", styles['TableBody'])
        ])
    
    t_equip = Table(equip_data, colWidths=[150, 230, 150])
    t_equip.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f0f0f0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(t_equip)
    elements.append(Spacer(1, 15))
    
    # 4. TEXTO LEGAL
    texto1 = f"Mediante la presente, se hace entrega a la Unidad/Servicio <b>{acta.receptor_unidad or 'N/A'}</b>, cuyo receptor es <b>{acta.receptor_nombre}</b>, del equipamiento detallado en este documento, para su uso en funciones institucionales."
    texto2 = f"El receptor <b>{acta.receptor_nombre}</b> declara recibir conforme el o los equipos y asume responsabilidad por su cuidado, mantención y uso adecuado."
    texto3 = "Ante cualquier anomalía, pérdida, robo o extravío, se deberá informar oportunamente a la Unidad TIC para gestionar las acciones correspondientes."
    
    elements.append(Paragraph(texto1, styles['Justify']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(texto2, styles['Justify']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(texto3, styles['Justify']))
    elements.append(Spacer(1, 15))
    
    # 5. OBSERVACIONES
    if acta.observaciones:
        elements.append(Paragraph("<b>III. OBSERVACIONES ADICIONALES</b>", ParagraphStyle('H3', parent=styles['Normal'], backColor=colors.HexColor("#002a54"), textColor=colors.white, padding=5)))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(acta.observaciones, styles['Normal']))
        elements.append(Spacer(1, 30))
    else:
        elements.append(Spacer(1, 40))
        
    # 6. FIRMAS
    # Si recibimos rutas físicas de firmas (firmas_paths) o usamos las del acta
    firma_rec_path = firmas_paths.get('receptor') if firmas_paths else (acta.firma_receptor.path if acta.firma_receptor else None)
    firma_tic_path = firmas_paths.get('tic') if firmas_paths else (acta.firma_encargado.path if acta.firma_encargado else None)
    
    img_rec = Image(firma_rec_path, width=150, height=75) if firma_rec_path and os.path.exists(firma_rec_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    img_tic = Image(firma_tic_path, width=150, height=75) if firma_tic_path and os.path.exists(firma_tic_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    
    encargado_nombre = acta.encargado.get_full_name() if acta.encargado else "Encargado TIC"
    
    firmas_data = [
        [img_rec, img_tic],
        [Paragraph(f"<b>{acta.receptor_nombre}</b><br/>Receptor", styles['Center']), Paragraph(f"<b>{encargado_nombre}</b><br/>Responsable TIC", styles['Center'])]
    ]
    t_firmas = Table(firmas_data, colWidths=[265, 265])
    t_firmas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LINEABOVE', (0,1), (0,1), 1, colors.black),
        ('LINEABOVE', (1,1), (1,1), 1, colors.black),
    ]))
    elements.append(t_firmas)
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
