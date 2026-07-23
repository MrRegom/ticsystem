import re

def update_actas_ui(html_path, js_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    old_row = r'<div class="col-md-6 mb-3">.*?<label class="form-label" style="font-size: 0.8rem; font-weight: 600;">Nombre Completo \*</label>.*?</div>.*?<div class="col-md-6 mb-3">.*?<label class="form-label" style="font-size: 0.8rem; font-weight: 600;">RUT \*</label>.*?</div>'
    
    new_row = """<div class="col-md-4 mb-3">
                                    <label class="form-label" style="font-size: 0.8rem; font-weight: 600;">RUT *</label>
                                    <input type="text" class="ms-input form-control" id="rec-rut" placeholder="12.345.678-K">
                                    <small id="rut-spinner" class="text-primary d-none"><i class="fas fa-spinner fa-spin"></i> Buscando...</small>
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label" style="font-size: 0.8rem; font-weight: 600;">Nombres *</label>
                                    <input type="text" class="ms-input form-control" id="rec-nombres" placeholder="Nombres">
                                </div>
                                <div class="col-md-4 mb-3">
                                    <label class="form-label" style="font-size: 0.8rem; font-weight: 600;">Apellidos *</label>
                                    <input type="text" class="ms-input form-control" id="rec-apellidos" placeholder="Apellidos">
                                </div>"""
                                
    html = re.sub(old_row, new_row, html, flags=re.DOTALL)
    
    # Change other form-controls to ms-input form-control
    html = html.replace('class="form-control"', 'class="ms-input form-control"')
    html = html.replace('class="ms-input ms-input form-control"', 'class="ms-input form-control"')
    html = html.replace('class="form-control select2"', 'class="ms-input form-control select2"')

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    # JS modifications
    
    # Text replacement for the preview
    js = js.replace("$('#rec-nombre').on('input', function() { $('#txt-receptor, #txt-receptor2').text($(this).val() || '[RECEPTOR]'); });", 
                    "$('#rec-nombres, #rec-apellidos').on('input', function() { const n = $('#rec-nombres').val() || ''; const a = $('#rec-apellidos').val() || ''; const full = (n + ' ' + a).trim(); $('#txt-receptor, #txt-receptor2').text(full || '[RECEPTOR]'); });")
                    
    # Generate action payload
    js = js.replace("const nombre = $('#rec-nombre').val().trim();", 
                    "const nombres = $('#rec-nombres').val().trim();\n        const apellidos = $('#rec-apellidos').val().trim();\n        const nombre = (nombres + ' ' + apellidos).trim();")
    
    # Reset fields
    js = js.replace("$('#rec-nombre, #rec-rut, #rec-cargo, #rec-correo, #acta-observaciones').val('');", 
                    "$('#rec-nombres, #rec-apellidos, #rec-rut, #rec-cargo, #rec-correo, #acta-observaciones').val('');")
                    
    # Add RUT lookup logic
    autofill_logic = """
    // --- AUTORRELLENO POR RUT ---
    let typingTimer;
    $('#rec-rut').on('keyup', function() {
        clearTimeout(typingTimer);
        const rut = $(this).val().trim();
        if (rut.length > 7) {
            typingTimer = setTimeout(function() {
                $('#rut-spinner').removeClass('d-none');
                $.ajax({
                    url: '/tickets/api/search/users/?q=' + rut,
                    type: 'GET',
                    success: function(resp) {
                        $('#rut-spinner').addClass('d-none');
                        if (resp.results && resp.results.length > 0) {
                            const user = resp.results[0];
                            const parts = user.text.split(' - ')[0].split(' ');
                            if (parts.length > 1) {
                                $('#rec-nombres').val(parts[0]);
                                $('#rec-apellidos').val(parts.slice(1).join(' '));
                            } else {
                                $('#rec-nombres').val(parts[0]);
                            }
                            $('#rec-nombres, #rec-apellidos').trigger('input');
                        }
                    },
                    error: function() {
                        $('#rut-spinner').addClass('d-none');
                    }
                });
            }, 800);
        }
    });
    """
    
    if "// --- AUTORRELLENO POR RUT ---" not in js:
        js = js.replace('// --- TEXTO DINÁMICO ---', autofill_logic + '\n    // --- TEXTO DINÁMICO ---')
        # Handle case where file might have strange encoding char
        js = js.replace('// --- TEXTO DINMICO ---', autofill_logic + '\n    // --- TEXTO DINMICO ---')
        js = js.replace('// --- TEXTO DIN?MICO ---', autofill_logic + '\n    // --- TEXTO DINÁMICO ---')

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("UI and Logic updated for actas.")

update_actas_ui(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html', r'c:\proyectos\ticsystem\static\js\actas.js')
