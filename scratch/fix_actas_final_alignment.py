import re

def fix_all_alignment_issues(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove padding from main tab-content
    # Find: <div class="tab-content fluent-card p-4 border-top-0" id="actasTabContent">
    # Replace: <div class="tab-content" id="actasTabContent">
    html = re.sub(
        r'<div class="tab-content fluent-card p-4 border-top-0" id="actasTabContent">',
        r'<div class="tab-content" id="actasTabContent">',
        html
    )

    # 2. Fix Header Buttons (Nueva Acta, Historial)
    # Remove icons and add text-decoration: none
    html = re.sub(
        r'<a class="btn ms-btn-primary active" id="nuevo-tab"[^>]*>\s*<i class="[^"]*"></i>\s*Nueva Acta\s*</a>',
        r'<a class="btn ms-btn-primary active" id="nuevo-tab" data-toggle="tab" href="#nuevo" role="tab" style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; text-decoration: none !important;">Nueva Acta</a>',
        html
    )
    
    html = re.sub(
        r'<a class="btn ms-btn-secondary" id="historial-tab"[^>]*>\s*<i class="[^"]*"></i>\s*Historial\s*</a>',
        r'<a class="btn ms-btn-secondary" id="historial-tab" data-toggle="tab" href="#historial" role="tab" style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; background: #fff; border: 1px solid #cbd5e1; color: #334155; text-decoration: none !important;">Historial</a>',
        html
    )

    # 3. Fix Card Headers (change pt-4 pb-0 to px-4 py-3 for balanced alignment)
    # This affects "Datos del Receptor", "Equipos / Insumos", "Observaciones", "Texto Principal del Acta"
    html = re.sub(
        r'class="card-header bg-white border-0 pt-4 pb-0([^"]*)"',
        r'class="card-header bg-white border-0 px-4 py-3\1"',
        html
    )
    
    # "Firma Receptor" and "Firma TIC" also have pt-4 pb-0, let's just make sure all of them are replaced globally.
    html = html.replace('class="card-header bg-white border-0 pt-4 pb-0"', 'class="card-header bg-white border-0 px-4 py-3"')
    html = html.replace('class="card-header bg-white border-0 pt-4 pb-0 d-flex justify-content-between align-items-center"', 'class="card-header bg-white border-0 px-4 py-3 d-flex justify-content-between align-items-center"')

    # 4. Fix title ms-header alignment (if it has mb-4, maybe add some px to align with cards? No, if we removed p-4 from tab-content, the cards will expand to the very edge of tab-content, which aligns with ms-header!)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Alignment issues fixed!")

fix_all_alignment_issues(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
