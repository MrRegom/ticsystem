import re

def rewrite_pdf_generator(py_path):
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()

    # Fix header data and column sizes
    old_header = """    header_data = [
        [
            Image(logo_hmm_path, width=70, height=70) if os.path.exists(logo_hmm_path) else Paragraph("<font color='#94a3b8'>[Logo HMM]</font>", styles['Center']),
            Paragraph(title_html, styles['Center'])
        ]
    ]
    t_header = Table(header_data, colWidths=[100, 420])"""

    new_header = """    header_data = [
        [
            Image(logo_hmm_path, width=120, height=50, kind='proportional') if os.path.exists(logo_hmm_path) else Paragraph("<font color='#94a3b8'>[Logo HMM]</font>", styles['Center']),
            Paragraph(title_html, styles['Center']),
            ""
        ]
    ]
    t_header = Table(header_data, colWidths=[130, 260, 130])"""
    py_content = py_content.replace(old_header, new_header)

    # Fix spacing and date
    old_date = """    elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=15))
    
    # Fecha
    fecha_str = acta.fecha.strftime("%d de %B de %Y - %H:%M") if acta.fecha else ""
    elements.append(Paragraph(f"Emitido en Viña del Mar, {fecha_str}", styles['Right']))
    elements.append(Spacer(1, 20))
    
    # 2. IDENTIFICACIÓN DEL RECEPTOR"""

    new_date = """    elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=10))
    
    # Fecha
    if acta.fecha:
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        mes = meses[acta.fecha.month - 1]
        fecha_str = acta.fecha.strftime(f"%d de {mes} de %Y - %H:%M")
    else:
        fecha_str = ""
    elements.append(Paragraph(f"Emitido en Viña del Mar, {fecha_str}", styles['Right']))
    elements.append(Spacer(1, 10))
    
    # 2. IDENTIFICACIÓN DEL RECEPTOR"""
    
    # Let's use regex for date because of potential encoding issues in previous string
    py_content = re.sub(r"elements\.append\(HRFlowable\(width=\"100%\", thickness=1, color=COLOR_SECONDARY, spaceBefore=0, spaceAfter=15\)\).*?# 2\. IDENTIFICACI.N DEL RECEPTOR", new_date, py_content, flags=re.DOTALL)

    # Reduce spacers
    py_content = py_content.replace("elements.append(Spacer(1, 25))", "elements.append(Spacer(1, 15))")
    py_content = py_content.replace("elements.append(Spacer(1, 30))", "elements.append(Spacer(1, 15))")
    py_content = py_content.replace("elements.append(Spacer(1, 40))", "elements.append(Spacer(1, 20))")
    
    # Reduce table padding
    old_equip_padding = """        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),"""
    new_equip_padding = """        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),"""
    py_content = py_content.replace(old_equip_padding, new_equip_padding)

    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)
        
    print("PDF script updated.")

rewrite_pdf_generator(r'c:\proyectos\ticsystem\actas\utils\pdf_generator.py')
