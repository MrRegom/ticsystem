import re

def fix_alignment_and_cache():
    # 1. Update actas.js flex container to stretch fully and center
    js_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    old_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center;">';"""
    new_js = """                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; width:100%; height:100%; min-height:40px;">';"""
            
    if old_js in js:
        js = js.replace(old_js, new_js)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated actas.js")
    else:
        print("Could not find ms-row-actions in actas.js")
        
    # 2. Update base.html to bust global-theme.css cache
    base_path = r'c:\proyectos\ticsystem\core\templates\core\base.html'
    with open(base_path, 'r', encoding='utf-8') as f:
        base = f.read()
    
    old_base = '<link rel="stylesheet" href="/static/css/global-theme.css?v=5">'
    new_base = '<link rel="stylesheet" href="/static/css/global-theme.css?v=6">'
    
    if old_base in base:
        base = base.replace(old_base, new_base)
        with open(base_path, 'w', encoding='utf-8') as f:
            f.write(base)
        print("Updated base.html cache buster")
    else:
        print("Could not find global-theme cache buster in base.html")
        
    # 3. Update actas.html to bust actas.js cache
    actas_path = r'c:\proyectos\ticsystem\actas\templates\actas\actas.html'
    with open(actas_path, 'r', encoding='utf-8') as f:
        actas = f.read()
    
    old_actas = '<script src="/static/js/actas.js?v=1.0"></script>'
    new_actas = '<script src="/static/js/actas.js?v=1.3"></script>'
    
    if old_actas in actas:
        actas = actas.replace(old_actas, new_actas)
        with open(actas_path, 'w', encoding='utf-8') as f:
            f.write(actas)
        print("Updated actas.html cache buster")
    else:
        print("Could not find actas.js cache buster in actas.html")

fix_alignment_and_cache()
