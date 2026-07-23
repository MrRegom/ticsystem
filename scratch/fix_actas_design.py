import re

def fix_actas_design():
    # 1. Update global-theme.css for dataTables
    css_path = r'c:\proyectos\ticsystem\static\css\global-theme.css'
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
        
    old_thead = """    /* Header Oscuro */
    table.dataTable thead th {
        background: #0f172a !important; /* Azul oscuro casi negro */
        color: #ffffff !important;
        font-size: 0.65rem;
    }"""
    
    new_thead = """    /* Header Microsoft Fluent para DataTables */
    table.dataTable thead th {
        background: #faf9f8 !important;
        color: #605e5c !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        border-bottom: 1px solid #edebe9 !important;
        border-top: none !important;
        padding: 6px 16px !important;
    }"""
    
    if old_thead in css:
        css = css.replace(old_thead, new_thead)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
        print("Updated global-theme.css")
    else:
        print("Could not find thead in global-theme.css")
        
    # 2. Update actas.html to remove inline backgrounds
    html_path = r'c:\proyectos\ticsystem\actas\templates\actas\actas.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    old_inline1 = '<thead style="background: #0f172a; color: white;">'
    new_inline = '<thead>'
    
    if old_inline1 in html:
        html = html.replace(old_inline1, new_inline)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Updated actas.html")
    else:
        print("Could not find inline thead in actas.html")
        
    # 3. Update actas.js to fix icons alignment and click event
    js_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_js = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:5px; justify-content:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-icon-btn" style="width:26px; height:26px; font-size:12px; display:inline-flex; align-items:center; justify-content:center; text-decoration:none;" title="Ver PDF"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="ms-icon-btn btn-delete-acta" data-id="${row.id}" style="width:26px; height:26px; font-size:12px;" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    new_js = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:5px; justify-content:center; align-items:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-icon-btn" style="width:26px; height:26px; font-size:12px; display:inline-flex; align-items:center; justify-content:center; text-decoration:none;" title="Ver PDF"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="ms-icon-btn btn-delete-acta" data-id="${row.id}" style="width:26px; height:26px; font-size:12px;" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    if old_js in js:
        js = js.replace(old_js, new_js)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated actas.js")
    else:
        print("Could not find column string in JS")

fix_actas_design()
