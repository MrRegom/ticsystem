import re

def fix_containers(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Define the common style to match Firma Receptor
    card_style = 'style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); background-color: #ffffff;"'

    # 1. Datos del Receptor
    old_datos = r'<h6 style="color: #002a54; font-weight: 700; margin-bottom: 16px;"><i class="far fa-id-card mr-2"></i> Datos del Receptor</h6>\s*<div class="fluent-card mb-4">'
    new_datos = f'''<div class="fluent-card mb-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="far fa-id-card mr-2"></i> Datos del Receptor</h6>
                        </div>'''
    html = re.sub(old_datos, new_datos, html)

    # 2. Equipos / Insumos
    old_equipos = r'<div class="d-flex justify-content-between align-items-center mb-3 mt-4">\s*<h6 style="color: #002a54; font-weight: 700; margin: 0;"><i class="fas fa-desktop mr-2"></i> Equipos / Insumos</h6>\s*<button type="button" class="btn ms-btn-primary btn-sm" data-toggle="modal" data-target="#modalEquipos">\s*<i class="fas fa-search"></i> Buscar Equipos\s*</button>\s*</div>\s*<div class="fluent-card mb-4">'
    new_equipos = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0 d-flex justify-content-between align-items-center">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="fas fa-desktop mr-2"></i> Equipos / Insumos</h6>
                            <button type="button" class="btn ms-btn-primary btn-sm" data-toggle="modal" data-target="#modalEquipos">
                                <i class="fas fa-search"></i> Buscar Equipos
                            </button>
                        </div>'''
    html = re.sub(old_equipos, new_equipos, html)

    # 3. Observaciones
    old_obs = r'<h6 style="color: #002a54; font-weight: 700; margin-bottom: 16px; mt-4"><i class="far fa-comment-dots mr-2"></i> Observaciones</h6>\s*<div class="fluent-card mb-4">'
    new_obs = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="far fa-comment-dots mr-2"></i> Observaciones</h6>
                        </div>'''
    html = re.sub(old_obs, new_obs, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Containers fixed successfully.")

fix_containers(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
