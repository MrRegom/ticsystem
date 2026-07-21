import os
from io import BytesIO
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
from reportlab.lib.units import inch

def generar_pdf_acta(acta, firmas_paths=None, datos_ui_detalles=None):
    """
    Genera un PDF moderno para el Acta dada usando ReportLab y retorna el archivo BytesIO.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=45, leftMargin=45, topMargin=50, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Colores corporativos modernos
    COLOR_PRIMARY = colors.HexColor("#002a54")
    COLOR_SECONDARY = colors.HexColor("#006FB3")
    COLOR_TEXT = colors.HexColor("#334155")
    COLOR_LIGHT_BG = colors.HexColor("#f8fafc")
    COLOR_BORDER = colors.HexColor("#e2e8f0")

    styles.add(ParagraphStyle(name='Center', alignment=1, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle(name='Right', alignment=2, textColor=colors.HexColor("#64748b"), fontSize=10))
    styles.add(ParagraphStyle(name='Justify', alignment=4, leading=16, textColor=COLOR_TEXT, fontSize=10))
    
    styles.add(ParagraphStyle(
        name='ModernH1', 
        fontName='Helvetica-Bold', 
        fontSize=12, 
        textColor=COLOR_PRIMARY, 
        spaceAfter=12,
        spaceBefore=16
    ))
    
    styles.add(ParagraphStyle(
        name='TableBody', 
        fontName='Helvetica', 
        fontSize=9, 
        alignment=1, 
        textColor=COLOR_TEXT
    ))
    
    elements = []
    
    # 1. HEADER (Logos y Título)
    logo_minsal_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_minsal.png')
    logo_hmm_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo_hospital.png') # Placeholder
    
    title_html = (
        f"<font color='{COLOR_PRIMARY}' size=14><b>ACTA DE ENTREGA DE EQUIPAMIENTO</b></font><br/>"
        f"<font color='{COLOR_SECONDARY}' size=9><i>PLATAFORMA TECNOLÓGICA - HOSPITAL MARGA MARGA</i></font><br/>"
        f"<font color='#94a3b8' size=8>Código de Acta: <b>{acta.codigo}</b></font>"
    )
    
    header_data = [
        [
            Image(logo_hmm_path, width=70, height=70) if os.path.exists(logo_hmm_path) else Paragraph("<font color='#94a3b8'>[Logo HMM]</font>", styles['Center']),
            Paragraph(title_html, styles['Center'])
        ]
    ]
    t_header = Table(header_data, colWidths=[100, 420])
    t_header.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t_header)
    
    # Línea separadora moderna
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=15))
    
    # Fecha
    fecha_str = acta.fecha.strftime("%d de %B de %Y - %H:%M") if acta.fecha else ""
    elements.append(Paragraph(f"Emitido en Viña del Mar, {fecha_str}", styles['Right']))
    elements.append(Spacer(1, 20))
    
    # 2. IDENTIFICACIÓN DEL RECEPTOR
    elements.append(Paragraph("I. IDENTIFICACIÓN DEL RECEPTOR", styles['ModernH1']))
    
    receptor_data = [
        [Paragraph("<b>Nombre Completo:</b>", styles['TableBody']), acta.receptor_nombre],
        [Paragraph("<b>RUT:</b>", styles['TableBody']), acta.receptor_rut or "No especificado"],
        [Paragraph("<b>Unidad/Servicio:</b>", styles['TableBody']), acta.receptor_unidad or "No especificado"],
        [Paragraph("<b>Cargo/Función:</b>", styles['TableBody']), acta.receptor_cargo or "No especificado"]
    ]
    t_receptor = Table(receptor_data, colWidths=[120, 400])
    t_receptor.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('TEXTCOLOR', (0,0), (-1,-1), COLOR_TEXT),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, COLOR_BORDER),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
    ]))
    elements.append(t_receptor)
    elements.append(Spacer(1, 25))
    
    # 3. DETALLE DEL EQUIPAMIENTO
    elements.append(Paragraph("II. DETALLE DEL EQUIPAMIENTO ENTREGADO", styles['ModernH1']))
    
    # Encabezado de la tabla de equipos
    header_equip = [
        Paragraph("<b>Nombre del Bien</b>", ParagraphStyle('TH', parent=styles['TableBody'], textColor=colors.white)),
        Paragraph("<b>Especificaciones / Marca / Modelo</b>", ParagraphStyle('TH', parent=styles['TableBody'], textColor=colors.white)),
        Paragraph("<b>N° de Serie / ID</b>", ParagraphStyle('TH', parent=styles['TableBody'], textColor=colors.white))
    ]
    equip_data = [header_equip]
    
    # Si tenemos los datos del UI (marcamodelo detallado) los usamos, si no, fallback
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
        ('BACKGROUND', (0,0), (-1,0), COLOR_SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
    ]))
    elements.append(t_equip)
    elements.append(Spacer(1, 25))
    
    # 4. TEXTO LEGAL
    elements.append(Paragraph("III. TÉRMINOS DE ENTREGA", styles['ModernH1']))
    
    texto1 = f"Mediante la presente, se hace entrega a la Unidad/Servicio <b>{acta.receptor_unidad or 'N/A'}</b>, cuyo receptor es <b>{acta.receptor_nombre}</b>, del equipamiento detallado en este documento, para su uso exclusivo en funciones institucionales del Hospital Marga Marga."
    texto2 = f"El receptor <b>{acta.receptor_nombre}</b> declara recibir conforme el o los equipos detallados previamente, y asume total responsabilidad por su cuidado, mantención, buen uso y resguardo físico."
    texto3 = "Ante cualquier anomalía, desperfecto técnico, pérdida, robo o extravío, se deberá informar de manera oportuna a la Unidad TIC (Soporte Técnico) para gestionar las acciones correctivas o administrativas correspondientes."
    
    # Caja para el texto legal
    legal_data = [[
        Paragraph(f"{texto1}<br/><br/>{texto2}<br/><br/>{texto3}", styles['Justify'])
    ]]
    t_legal = Table(legal_data, colWidths=[520])
    t_legal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    elements.append(t_legal)
    elements.append(Spacer(1, 20))
    
    # 5. OBSERVACIONES
    if acta.observaciones:
        elements.append(Paragraph("IV. OBSERVACIONES ADICIONALES", styles['ModernH1']))
        obs_data = [[Paragraph(acta.observaciones, styles['Justify'])]]
        t_obs = Table(obs_data, colWidths=[520])
        t_obs.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('PADDING', (0,0), (-1,-1), 12),
        ]))
        elements.append(t_obs)
        elements.append(Spacer(1, 30))
    else:
        elements.append(Spacer(1, 40))
        
    # 6. FIRMAS
    firma_rec_path = firmas_paths.get('receptor') if firmas_paths else (acta.firma_receptor.path if acta.firma_receptor else None)
    firma_tic_path = firmas_paths.get('tic') if firmas_paths else (acta.firma_encargado.path if acta.firma_encargado else None)
    
    img_rec = Image(firma_rec_path, width=160, height=80) if firma_rec_path and os.path.exists(firma_rec_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    img_tic = Image(firma_tic_path, width=160, height=80) if firma_tic_path and os.path.exists(firma_tic_path) else Paragraph("<i>(Firma)</i>", styles['Center'])
    
    encargado_nombre = acta.encargado.get_full_name() if acta.encargado else "Encargado TIC"
    
    # Títulos debajo de las firmas con diseño más formal
    titulo_rec = f"<font color='{COLOR_PRIMARY}'><b>{acta.receptor_nombre.upper()}</b></font><br/><font color='#64748b' size=8>RECEPTOR DEL EQUIPO</font>"
    titulo_tic = f"<font color='{COLOR_PRIMARY}'><b>{encargado_nombre.upper()}</b></font><br/><font color='#64748b' size=8>RESPONSABLE TIC - H.M.M.</font>"

    firmas_data = [
        [img_rec, img_tic],
        [Paragraph(titulo_rec, styles['Center']), Paragraph(titulo_tic, styles['Center'])]
    ]
    t_firmas = Table(firmas_data, colWidths=[260, 260])
    t_firmas.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        # Línea sutil superior para las firmas
        ('LINEABOVE', (0,1), (0,1), 1.5, COLOR_PRIMARY),
        ('LINEABOVE', (1,1), (1,1), 1.5, COLOR_PRIMARY),
        ('TOPPADDING', (0,1), (-1,1), 8),
    ]))
    elements.append(t_firmas)
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
