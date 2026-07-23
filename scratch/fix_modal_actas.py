import re

def fix_modal_and_correo(html_path, js_path):
    # 1. Update HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    old_correo_div = r'<div class="form-row">\s*<div class="form-group col-md-12">\s*<label style="font-weight:600; font-size:0.85rem; color:#334155;">Correo Electrónico <span style="color:#94a3b8;font-weight:400;">\(opcional\)</span></label>\s*<input type="email" id="correo_nuevo" name="correo_nuevo" class="ms-input form-control" placeholder="usuario@correo.cl">\s*</div>\s*</div>'
    
    new_fields = """<div class="form-row">
              <div class="form-group col-md-12">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Correo Electrónico <span style="color:#94a3b8;font-weight:400;">(opcional)</span></label>
                <input type="email" id="correo_nuevo" name="correo_nuevo" class="ms-input form-control" placeholder="usuario@correo.cl">
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Cargo / Rol</label>
                <select id="cargo_nuevo" name="cargo_nuevo" class="ms-input form-control">
                  <option value="">-- Seleccionar Cargo --</option>
                  {% for c in cargos %}
                    <option value="{{ c.nombre }}">{{ c.nombre }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Unidad / Servicio</label>
                <select id="unidad_nueva" name="unidad_nueva" class="ms-input form-control">
                  <option value="">-- Seleccionar Unidad --</option>
                  {% for u in unidades %}
                    <option value="{{ u.nombre }}">{{ u.nombre }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>"""
            
    html = re.sub(old_correo_div, new_fields, html, flags=re.DOTALL)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    # 2. Update JS
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    # a) Fill correo in autofill
    old_fill = r"\$\('#rec-nombres'\)\.val\(user\.nombres \|\| ''\);\s*\$\('#rec-apellidos'\)\.val\(user\.apellidos \|\| ''\);"
    new_fill = "$('#rec-nombres').val(user.nombres || '');\n                            $('#rec-apellidos').val(user.apellidos || '');\n                            $('#rec-correo').val(user.correo || '');"
    js = re.sub(old_fill, new_fill, js)
    
    # b) Change payload for UserCreateApiView
    old_data = r"const data = \{\s*rut: \$\('#rut_nuevo'\)\.val\(\),\s*first_name: \$\('#nombres_nuevo'\)\.val\(\),\s*last_name: \$\('#apellidos_nuevo'\)\.val\(\),\s*email: \$\('#correo_nuevo'\)\.val\(\)\s*\};"
    new_data = """const data = {
            rut: $('#rut_nuevo').val(),
            nombres: $('#nombres_nuevo').val(),
            apellidos: $('#apellidos_nuevo').val(),
            correo: $('#correo_nuevo').val(),
            cargo: $('#cargo_nuevo').val(),
            unidad: $('#unidad_nueva').val()
        };"""
    js = re.sub(old_data, new_data, js)
    
    # c) Fix JS success response reading (the API returns res.data? Wait, UserCreateApiView returns `res.data` probably. I need to make sure I get the actual object)
    # The API returns: return JsonResponse({'success': True, 'message': 'Funcionario creado', 'user': {'id': func.id, 'rut': func.rut, 'nombres': func.nombres, 'apellidos': func.apellidos, 'correo': func.correo}})
    # And then update form:
    old_success = r"\$\('#rec-rut'\)\.val\(res\.user\.rut\);\s*\$\('#rec-nombres'\)\.val\(res\.user\.nombres\);\s*\$\('#rec-apellidos'\)\.val\(res\.user\.apellidos\);"
    new_success = """$('#rec-rut').val(res.user.rut);
                    $('#rec-nombres').val(res.user.nombres);
                    $('#rec-apellidos').val(res.user.apellidos);
                    $('#rec-correo').val(res.user.correo || '');"""
    js = re.sub(old_success, new_success, js)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("Corrections applied successfully.")

fix_modal_and_correo(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html', r'c:\proyectos\ticsystem\static\js\actas.js')
