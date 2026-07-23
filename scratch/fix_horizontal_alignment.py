import re

def fix_alignment_issues():
    # 1. Fix actas.js alignment (Horizontal and Vertical)
    actas_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(actas_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; margin-top:6px;">';"""
    # Use display: flex, width: 100%, justify-content: center.
    # To fix vertical alignment visually, we'll keep margin-top: 2px since font-size 13px icons look a bit higher than 12px text.
    new_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; width:100%; margin-top:2px;">';"""
    
    if old_js in js:
        js = js.replace(old_js, new_js)
    else:
        # Fallback if it's the previous version
        old_js2 = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; margin-top:2px;">';"""
        if old_js2 in js:
            js = js.replace(old_js2, new_js)

    with open(actas_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    # 2. Fix equipos.js grid width and alignment
    equipos_path = r'c:\proyectos\ticsystem\static\js\equipos.js'
    with open(equipos_path, 'r', encoding='utf-8') as f:
        eq_js = f.read()
        
    # Change the grid column from 70px to 100px for actions so the 3 buttons fit perfectly, and align to right or center.
    old_grid = "grid-template-columns: 200px 1fr 120px 70px 120px 120px 110px 110px 70px;"
    new_grid = "grid-template-columns: 200px 1fr 120px 70px 120px 120px 110px 110px 100px;"
    
    if old_grid in eq_js:
        eq_js = eq_js.replace(old_grid, new_grid)
        
    # Also update the header grid template in equipos.html to match!
    
    # Fix the actions wrapper in equipos.js
    old_actions = """        html += '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0;">';"""
    new_actions = """        html += '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:6px; justify-content:center; align-items:center; width:100%; height:100%;">';"""
    
    if old_actions in eq_js:
        eq_js = eq_js.replace(old_actions, new_actions)
        
    with open(equipos_path, 'w', encoding='utf-8') as f:
        f.write(eq_js)
        
    # 3. Update equipos.html header grid to match 100px
    eq_html_path = r'c:\proyectos\ticsystem\equipos\templates\equipos\equipos.html'
    with open(eq_html_path, 'r', encoding='utf-8') as f:
        eq_html = f.read()
        
    if old_grid in eq_html:
        eq_html = eq_html.replace(old_grid, new_grid)
        with open(eq_html_path, 'w', encoding='utf-8') as f:
            f.write(eq_html)

fix_alignment_issues()
