import re

def fix_icons_and_modal_buttons(html_path, js_path):
    # 1. Update actas.html Icons
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Make icons in the h6 tags smaller (for Datos del Receptor, Equipos, Observaciones, Texto, Firmas)
    html = re.sub(
        r'<i class="([^"]+) mr-2"></i>',
        r'<i class="\1 mr-2" style="font-size: 0.9rem; color: #006FB3;"></i>',
        html
    )

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    # 2. Update actas.js Buttons
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    js = js.replace('class="btn btn-sm btn-primary btn-add-item"', 'class="btn ms-btn-primary btn-sm btn-add-item" style="text-decoration: none !important;"')
    
    # Also update the jQuery addClass/removeClass to use ms-btn-primary if it was btn-primary
    js = js.replace("removeClass('btn-primary')", "removeClass('ms-btn-primary')")
    js = js.replace("addClass('btn-primary')", "addClass('ms-btn-primary')")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("Icons and modal buttons fixed.")

fix_icons_and_modal_buttons(
    r'c:\proyectos\ticsystem\actas\templates\actas\actas.html',
    r'c:\proyectos\ticsystem\static\js\actas.js'
)
