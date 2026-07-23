import re

def fix_all(views_path, html_path, js_path):
    # 1. Fix views.py (500 Error JSON serializable)
    with open(views_path, 'r', encoding='utf-8') as f:
        views = f.read()
        
    views = views.replace(
        "'cargo': cargo if u.cargo else '',",
        "'cargo': u.cargo.nombre if u.cargo else '',"
    )
    views = views.replace(
        "'unidad': unidad if u.unidad else ''",
        "'unidad': u.unidad.nombre if u.unidad else ''"
    )
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(views)
        
    # 2. Fix html_path (Button classes)
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    html = html.replace('class="fluent-btn-secondary', 'class="btn ms-btn-secondary')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    # 3. Add JS RUT Validator visual feedback
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    validator_js = """
    // --- RUT FORMATTER & VALIDATOR ---
    function formatRut(rut) {
        let value = rut.replace(/[^0-9kK]/g, '').toUpperCase();
        if (value.length > 1) {
            value = value.slice(0, -1) + '-' + value.slice(-1);
        }
        return value;
    }
    
    function isValidRut(rut) {
        if (!/^[0-9]+-[0-9kK]{1}$/.test(rut)) return false;
        let t = parseInt(rut.split('-')[0], 10);
        let m = 0, s = 1;
        while (t > 0) {
            s = (s + t % 10 * (9 - m++ % 6)) % 11;
            t = Math.floor(t / 10);
        }
        let v = (s > 0) ? (s - 1) + '' : 'K';
        return (v === rut.split('-')[1].toUpperCase());
    }
    
    $('#rec-rut, #rut_nuevo').on('input', function() {
        let formatted = formatRut($(this).val());
        $(this).val(formatted);
        
        if (formatted.length > 7) {
            if (isValidRut(formatted)) {
                $(this).removeClass('is-invalid').addClass('is-valid');
            } else {
                $(this).removeClass('is-valid').addClass('is-invalid');
            }
        } else {
            $(this).removeClass('is-valid is-invalid');
        }
    });
"""
    # Replace the old RUT formatter block completely
    old_formatter = r"// --- RUT FORMATTER ---.*?\}\);"
    js = re.sub(old_formatter, validator_js, js, flags=re.DOTALL)
    
    # In the autofill logic, let's make sure we only search if isValidRut is true!
    old_search = r"if \(rut\.length > 7\) \{"
    new_search = "if (rut.length > 7 && isValidRut(rut)) {"
    js = js.replace(old_search, new_search)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("Fixes applied successfully.")

fix_all(r'c:\proyectos\ticsystem\tickets\views.py', r'c:\proyectos\ticsystem\actas\templates\actas\actas.html', r'c:\proyectos\ticsystem\static\js\actas.js')
