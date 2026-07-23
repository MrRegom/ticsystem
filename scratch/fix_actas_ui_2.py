import re

def update_ui_and_api(views_path, css_path, js_path):
    # 1. Update tickets/views.py to return cargo and unidad strings
    with open(views_path, 'r', encoding='utf-8') as f:
        views = f.read()
        
    old_results_append = r"results\.append\(\{\s*'id': u\.id,\s*'text': label,\s*'rut': u\.rut,\s*'nombres': u\.nombres,\s*'apellidos': u\.apellidos,\s*'correo': u\.correo or ''\s*\}\)"
    new_results_append = """results.append({
                'id': u.id,
                'text': label,
                'rut': u.rut,
                'nombres': u.nombres,
                'apellidos': u.apellidos,
                'correo': u.correo or '',
                'cargo': cargo if u.cargo else '',
                'unidad': unidad if u.unidad else ''
            })"""
    
    views = re.sub(old_results_append, new_results_append, views)
    
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(views)
        
    # 2. Add .fluent-card to global-theme.css
    with open(css_path, 'r', encoding='utf-8') as f:
        css = f.read()
        
    if '.fluent-card' not in css:
        fluent_card_css = """
/* Fluent Card Container */
.fluent-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    padding: 16px;
}
"""
        css = css + fluent_card_css
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)
            
    # 3. Update actas.js to remove icons from "Agregar" button
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    js = js.replace('<i class="fas fa-plus"></i> Agregar', 'Agregar')
    js = js.replace('<i class="fas fa-check"></i> Agregado', 'Agregado')
    
    # Also in actas.js, when receiving search results, use the trigger correctly for select2
    # Oh wait, my JS currently does: $('#rec-cargo').val(user.cargo || '').trigger('change');
    # I already added that in a previous step! No wait, I didn't add it to actas.js? 
    # Let's check if the trigger for cargo and unidad is there.
    if "$('#rec-unidad').val(user.unidad || '').trigger('change');" not in js:
        # We need to add it to the autofill success handler!
        # Let's replace the block
        old_fill = r"\$\('#rec-correo'\)\.val\(user\.correo \|\| ''\);"
        new_fill = "$('#rec-correo').val(user.correo || '');\n                            $('#rec-cargo').val(user.cargo || '').trigger('change');\n                            $('#rec-unidad').val(user.unidad || '').trigger('change');"
        js = re.sub(old_fill, new_fill, js)
        
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("UI enhancements and autofill logic updated.")

update_ui_and_api(r'c:\proyectos\ticsystem\tickets\views.py', r'c:\proyectos\ticsystem\static\css\global-theme.css', r'c:\proyectos\ticsystem\static\js\actas.js')
