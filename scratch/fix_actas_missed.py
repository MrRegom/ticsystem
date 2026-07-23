import re

def fix_missed_containers(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    card_style = 'style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); background-color: #ffffff;"'

    # 1. Equipos
    old_equipos = r'<div class="d-flex justify-content-between align-items-center mb-3">\s*<h6 style="color: #002a54; font-weight: 700; margin: 0;"><i class="fas fa-desktop mr-2"></i> Equipos / Insumos</h6>\s*<button type="button" class="fluent-btn-primary" id="btn-buscar-equipos" style="background: #006FB3; border: none;">\s*<i class="fas fa-search mr-1"></i> Buscar Equipos\s*</button>\s*</div>\s*<div class="fluent-card mb-4">'
    
    new_equipos = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0 d-flex justify-content-between align-items-center">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="fas fa-desktop mr-2"></i> Equipos / Insumos</h6>
                            <button type="button" class="btn ms-btn-primary btn-sm" id="btn-buscar-equipos" style="font-size: 0.75rem;">
                                <i class="fas fa-search mr-1"></i> Buscar Equipos
                            </button>
                        </div>'''
                        
    html = re.sub(old_equipos, new_equipos, html)

    # 2. Observaciones
    old_obs = r'<h6 style="color: #002a54; font-weight: 700; margin-bottom: 16px;"><i class="far fa-comment-alt mr-2"></i> Observaciones</h6>\s*<div class="fluent-card mb-4">'
    
    new_obs = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="far fa-comment-alt mr-2"></i> Observaciones</h6>
                        </div>'''
                        
    html = re.sub(old_obs, new_obs, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Fixed missed containers.")

fix_missed_containers(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
