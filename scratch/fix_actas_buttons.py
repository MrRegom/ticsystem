import re

def fix_actas_buttons(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    old_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="btn btn-sm btn-danger mr-1" title="Ver PDF" style="font-size:0.75rem;"><i class="fas fa-file-pdf mr-1"></i> PDF</a>`;
                } else {
                    html += `<span class="badge badge-secondary mr-1">Sin PDF</span>`;
                }
                html += `<button type="button" class="btn btn-sm btn-danger btn-delete-acta" style="font-size:0.75rem;" data-id="${row.id}" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                return html;
            }}"""
    
    new_col = """            { data: null, orderable: false, render: function(data, type, row) {
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
            
    if old_col in js_content:
        js_content = js_content.replace(old_col, new_col)
    else:
        # Regex fallback
        js_content = re.sub(r"\{\s*data:\s*null,\s*orderable:\s*false,\s*render:\s*function\(data,\s*type,\s*row\)\s*\{\s*let\s*html.*?return\s*html;\s*\}\}", new_col, js_content, flags=re.DOTALL)
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("Buttons fixed in actas.js")

fix_actas_buttons(r'c:\proyectos\ticsystem\static\js\actas.js')
