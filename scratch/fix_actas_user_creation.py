import re

def fix_user_create(js_path, py_path):
    # 1. Update tickets/views.py
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()
        
    old_return = r"return JsonResponse\(\{'success': True, 'user': \{'id': func\.id, 'text': label\}\}\)"
    new_return = """return JsonResponse({'success': True, 'user': {
                    'id': func.id, 
                    'text': label,
                    'rut': func.rut,
                    'nombres': func.nombres,
                    'apellidos': func.apellidos,
                    'correo': func.correo,
                    'unidad': func.unidad.nombre if func.unidad else '',
                    'cargo': func.cargo.nombre if func.cargo else ''
                }})"""
    
    py_content = re.sub(old_return, new_return, py_content)
    
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)
        
    # 2. Update actas.js
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
        
    old_js = r"(\$\('#rec-correo'\)\.val\(res\.user\.correo \|\| ''\);)\s*(\$\('#rec-unidad, #rec-cargo'\)\.prop\('disabled', false\);)"
    new_js = r"\1\n                      $('#rec-unidad').val(res.user.unidad || '').trigger('change');\n                      $('#rec-cargo').val(res.user.cargo || '').trigger('change');\n                      \2"
    
    js_content = re.sub(old_js, new_js, js_content)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("Fixed user creation return data and filling logic.")

fix_user_create(
    r'c:\proyectos\ticsystem\static\js\actas.js',
    r'c:\proyectos\ticsystem\tickets\views.py'
)
