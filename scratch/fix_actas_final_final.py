import re

def fix_actas_delete_and_icons():
    # 1. Update actas/views.py
    views_path = r'c:\proyectos\ticsystem\actas\views.py'
    with open(views_path, 'r', encoding='utf-8') as f:
        views = f.read()
    
    old_anexo = """                elif detalle.tipo_item == 'ANEXO':
                    from anexos.models import AnexoIP
                    try:
                        anexo = AnexoIP.objects.get(id=detalle.id_item)
                        anexo.estado = 'DISPONIBLE'
                        anexo.save()"""
    new_anexo = """                elif detalle.tipo_item == 'ANEXO':
                    from anexos.models import Anexo
                    try:
                        anexo = Anexo.objects.get(id=detalle.id_item)
                        anexo.estado = 'Activo'
                        anexo.save()"""
                        
    if old_anexo in views:
        views = views.replace(old_anexo, new_anexo)
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views)
        print("Updated views.py")
    else:
        print("Could not find Anexo string in views.py")

    # 2. Update global-theme.css
    css_path = r'c:\proyectos\ticsystem\static\css\global-theme.css'
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
        
    old_td = """    table.dataTable tbody td {
        padding: 12px 16px;
        font-size: 0.8rem;
        color: #334155;
        vertical-align: middle;
        border-bottom: 1px solid #f1f5f9;
        border-top: none !important;
    }"""
    
    new_td = """    table.dataTable tbody td {
        padding: 12px 16px;
        font-size: 0.8rem;
        color: #334155;
        vertical-align: middle !important;
        border-bottom: 1px solid #f1f5f9;
        border-top: none !important;
    }"""
    
    if old_td in css:
        css = css.replace(old_td, new_td)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
        print("Updated global-theme.css")
    else:
        print("Could not find td styling in global-theme.css")
        
    # 3. Update actas.js icons
    js_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_js = """            { data: null, orderable: false, render: function(data, type, row) {
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
            
    new_js = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-icon-btn" style="width:26px; height:26px; font-size:13px; display:inline-flex; align-items:center; justify-content:center; text-decoration:none; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#0078d4'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';" title="Ver PDF"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="ms-icon-btn btn-delete-acta" data-id="${row.id}" style="width:26px; height:26px; font-size:13px; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#dc3545'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    if old_js in js:
        js = js.replace(old_js, new_js)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated actas.js icons")
    else:
        print("Could not find column string in JS")

fix_actas_delete_and_icons()
