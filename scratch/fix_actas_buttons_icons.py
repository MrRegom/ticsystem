import re

def fix_actas_buttons_icons(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    old_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div style="display:flex; gap:6px; justify-content:flex-start;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-btn-primary" title="Ver PDF" style="text-decoration:none; padding:4px 10px; font-size:12px; border-radius:4px;"><i class="fas fa-file-pdf"></i> PDF</a>`;
                } else {
                    html += `<span class="badge badge-secondary" style="padding:6px 10px;">Sin PDF</span>`;
                }
                html += `<button type="button" class="btn-delete-acta" data-id="${row.id}" title="Eliminar Acta" style="background-color:#fce8e6; color:#d93025; border:1px solid transparent; border-radius:4px; padding:4px 10px; cursor:pointer; font-size:12px; display:flex; align-items:center; justify-content:center; transition:0.2s;" onmouseover="this.style.backgroundColor='#fad2cf'; this.style.borderColor='#d93025';" onmouseout="this.style.backgroundColor='#fce8e6'; this.style.borderColor='transparent';"><i class="fas fa-trash-alt"></i></button>`;
                html += '</div>';
                return html;
            }}"""
    
    new_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div style="display:flex; gap:15px; justify-content:center; align-items:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" title="Ver PDF" style="color:#0078d4; font-size:1.1rem; text-decoration:none; transition:0.2s;" onmouseover="this.style.color='#106ebe'" onmouseout="this.style.color='#0078d4'"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="btn-delete-acta" data-id="${row.id}" title="Eliminar Acta" style="background:none; border:none; color:#dc3545; font-size:1.1rem; cursor:pointer; padding:0; transition:0.2s;" onmouseover="this.style.color='#bd2130'" onmouseout="this.style.color='#dc3545'"><i class="fas fa-trash-alt"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    if old_col in js_content:
        js_content = js_content.replace(old_col, new_col)
    else:
        print("Could not find the exact old column string, using regex...")
        js_content = re.sub(r"\{\s*data:\s*null,\s*orderable:\s*false,\s*render:\s*function\(data,\s*type,\s*row\)\s*\{\s*let\s*html.*?return\s*html;\s*\}\}", new_col, js_content, flags=re.DOTALL)
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("Buttons reduced to icons in actas.js")

fix_actas_buttons_icons(r'c:\proyectos\ticsystem\static\js\actas.js')
