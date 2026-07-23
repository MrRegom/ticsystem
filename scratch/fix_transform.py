import re

def fix_transform_issue():
    # 1. Fix actas.js
    actas_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(actas_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; width:100%; margin-top:2px;">';"""
    new_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; width:100%; transform:none !important; margin-top:0;">';"""
    
    if old_js in js:
        js = js.replace(old_js, new_js)
        with open(actas_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated actas.js")
    else:
        print("Could not find ms-row-actions in actas.js")
        
    # 2. Fix equipos.js
    equipos_path = r'c:\proyectos\ticsystem\static\js\equipos.js'
    with open(equipos_path, 'r', encoding='utf-8') as f:
        eq_js = f.read()
        
    old_eq = """        html += '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:6px; justify-content:center; align-items:center; width:100%; height:100%;">';"""
    new_eq = """        html += '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:6px; justify-content:center; align-items:center; width:100%; height:100%; transform:none !important;">';"""
    
    if old_eq in eq_js:
        eq_js = eq_js.replace(old_eq, new_eq)
        with open(equipos_path, 'w', encoding='utf-8') as f:
            f.write(eq_js)
        print("Updated equipos.js")
    else:
        print("Could not find ms-row-actions in equipos.js")
        
    # 3. Update actas.html version
    actas_html_path = r'c:\proyectos\ticsystem\actas\templates\actas\actas.html'
    with open(actas_html_path, 'r', encoding='utf-8') as f:
        actas = f.read()
    if '?v=1.6' in actas:
        actas = actas.replace('?v=1.6', '?v=1.7')
        with open(actas_html_path, 'w', encoding='utf-8') as f:
            f.write(actas)
            
    # 4. Update equipos.html version
    equipos_html_path = r'c:\proyectos\ticsystem\equipos\templates\equipos\equipos.html'
    with open(equipos_html_path, 'r', encoding='utf-8') as f:
        eq_html = f.read()
    if '?v=4.2' in eq_html:
        eq_html = eq_html.replace('?v=4.2', '?v=4.3')
        with open(equipos_html_path, 'w', encoding='utf-8') as f:
            f.write(eq_html)

fix_transform_issue()
