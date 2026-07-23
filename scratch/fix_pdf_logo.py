import re

def fix_pdf_logo(py_path):
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()

    # Find the header_data section
    old_header = """    header_data = [
        [
            Image(logo_minsal_path, width=90, height=45) if os.path.exists(logo_minsal_path) else Paragraph("<font color='#94a3b8'>[Logo Minsal]</font>", styles['Center']),
            Paragraph(title_html, styles['Center']),
            Image(logo_hmm_path, width=70, height=70) if os.path.exists(logo_hmm_path) else Paragraph("<font color='#94a3b8'>[Logo HMM]</font>", styles['Center'])
        ]
    ]
    t_header = Table(header_data, colWidths=[100, 320, 100])"""

    new_header = """    header_data = [
        [
            Image(logo_hmm_path, width=70, height=70) if os.path.exists(logo_hmm_path) else Paragraph("<font color='#94a3b8'>[Logo HMM]</font>", styles['Center']),
            Paragraph(title_html, styles['Center'])
        ]
    ]
    t_header = Table(header_data, colWidths=[100, 420])"""

    if old_header in py_content:
        py_content = py_content.replace(old_header, new_header)
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(py_content)
        print("PDF header fixed.")
    else:
        print("Could not find the exact old_header block to replace.")

fix_pdf_logo(r'c:\proyectos\ticsystem\actas\utils\pdf_generator.py')
