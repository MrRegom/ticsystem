import re

def update_actas_final(html_path, js_path, views_path):
    # 1. Update views.py to pass 'cargos'
    with open(views_path, 'r', encoding='utf-8') as f:
        views = f.read()
        
    if "'cargos':" not in views and "context['cargos']" not in views:
        views = views.replace(
            "from mantenedores.models import Edificio, Piso, Unidad", 
            "from mantenedores.models import Edificio, Piso, Unidad, Cargo"
        )
        views = views.replace(
            "context['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))",
            "context['unidades'] = list(Unidad.objects.filter(activo=True).values('id', 'nombre'))\n        context['cargos'] = list(Cargo.objects.filter(activo=True).values('id', 'nombre'))"
        )
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views)
            
    # 2. Update html_path
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Change Cargo to Select
    old_cargo = r'<input type="text" class="ms-input form-control" id="rec-cargo" placeholder="Ej: Enfermera Supervisora">'
    new_cargo = """<select class="ms-input form-control select2" id="rec-cargo" style="width: 100%;">
                                        <option value="">Seleccionar Cargo...</option>
                                        {% for c in cargos %}
                                        <option value="{{ c.nombre }}">{{ c.nombre }}</option>
                                        {% endfor %}
                                    </select>"""
    html = re.sub(old_cargo, new_cargo, html)
    
    # Add readonly to Nombres and Apellidos, and add a button next to them
    html = html.replace('id="rec-nombres" placeholder="Nombres"', 'id="rec-nombres" placeholder="Nombres" readonly')
    html = html.replace('id="rec-apellidos" placeholder="Apellidos"', 'id="rec-apellidos" placeholder="Apellidos" readonly')
    html = html.replace('id="rec-unidad" style="width: 100%;"', 'id="rec-unidad" style="width: 100%;" disabled')
    
    # Wait, if they are disabled, they won't be sent in regular form submits but here we use AJAX, so it's fine!
    
    # Let's add the button for "Add User" next to the RUT spinner
    btn_add = """<small id="rut-spinner" class="text-primary d-none"><i class="fas fa-spinner fa-spin"></i> Buscando...</small>
                                    <button type="button" id="btn-add-user" class="fluent-btn-secondary btn-sm mt-2 d-none" style="font-size: 0.75rem;"><i class="fas fa-user-plus"></i> Registrar Funcionario</button>"""
    html = html.replace('<small id="rut-spinner" class="text-primary d-none"><i class="fas fa-spinner fa-spin"></i> Buscando...</small>', btn_add)

    # We also need to add the Modal from Tickets to actas.html !
    modal_html = """
    <!-- MODAL CREAR USUARIO RAPIDO -->
<div class="modal fade" id="modalCrearUsuario" tabindex="-1" role="dialog" aria-hidden="true" style="z-index:1060;">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content rounded-0 border-0">
        <form id="form-crear-usuario" method="POST" onsubmit="return false;">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title text-uppercase"><i class="fas fa-user-plus text-white mr-2"></i> Añadir Funcionario Rápido</h5>
            <button type="button" class="close text-white" onclick="$('#modalCrearUsuario').modal('hide')">&times;</button>
          </div>
          <div class="modal-body" style="padding:20px;">
            <div class="form-group">
              <label style="font-weight:600; font-size:0.85rem; color:#334155;">RUT <span class="text-danger">*</span></label>
              <input type="text" id="rut_nuevo" name="rut_nuevo" class="ms-input form-control" required placeholder="Ej: 12345678-9">
            </div>
            <div class="form-row">
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Nombres <span class="text-danger">*</span></label>
                <input type="text" name="nombres_nuevo" id="nombres_nuevo" class="ms-input form-control" required>
              </div>
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Apellidos <span class="text-danger">*</span></label>
                <input type="text" name="apellidos_nuevo" id="apellidos_nuevo" class="ms-input form-control" required>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group col-md-12">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Correo Electrónico <span style="color:#94a3b8;font-weight:400;">(opcional)</span></label>
                <input type="email" id="correo_nuevo" name="correo_nuevo" class="ms-input form-control" placeholder="usuario@correo.cl">
              </div>
            </div>
          </div>
          <div class="modal-footer" style="border-top:1px solid #e2e8f0;">
            <button type="button" class="fluent-btn-secondary" onclick="$('#modalCrearUsuario').modal('hide')">Cancelar</button>
            <button type="submit" class="fluent-btn-primary" id="btn-submit-usuario"><i class="fas fa-save"></i> Guardar Funcionario</button>
          </div>
        </form>
      </div>
    </div>
  </div>
    """
    
    if "modalCrearUsuario" not in html:
        html = html.replace('{% endblock %}', modal_html + '\n{% endblock %}')
        
    # Also disable cargo
    html = html.replace('id="rec-cargo"', 'id="rec-cargo" disabled')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    # 3. Update js_path
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()
        
    # RUT Formatter
    rut_formatter = """
    // --- RUT FORMATTER ---
    function formatRut(rut) {
        let value = rut.replace(/[^0-9kK]/g, '').toUpperCase();
        if (value.length > 1) {
            value = value.slice(0, -1) + '-' + value.slice(-1);
        }
        return value;
    }
    
    $('#rec-rut, #rut_nuevo').on('input', function() {
        $(this).val(formatRut($(this).val()));
    });
    """
    if "function formatRut" not in js:
        js = js.replace('$(document).ready(function() {', '$(document).ready(function() {\n' + rut_formatter)

    # Replace autofill logic
    old_autofill = r"// --- AUTORRELLENO POR RUT ---.*?// --- TEXTO DIN"
    
    new_autofill = """// --- AUTORRELLENO POR RUT ---
    let typingTimer;
    $('#rec-rut').on('keyup', function() {
        clearTimeout(typingTimer);
        const rut = $(this).val().trim();
        if (rut.length > 7) {
            typingTimer = setTimeout(function() {
                $('#rut-spinner').removeClass('d-none');
                $('#btn-add-user').addClass('d-none');
                $.ajax({
                    url: '/tickets/api/search/users/?q=' + rut,
                    type: 'GET',
                    success: function(resp) {
                        $('#rut-spinner').addClass('d-none');
                        if (resp.results && resp.results.length > 0) {
                            const user = resp.results[0];
                            $('#rec-nombres').val(user.nombres || '');
                            $('#rec-apellidos').val(user.apellidos || '');
                            // Habilitar campos si hay usuario
                            $('#rec-unidad, #rec-cargo').prop('disabled', false);
                            $('#rec-nombres, #rec-apellidos').trigger('input');
                        } else {
                            // No encontrado -> obligar a agregar
                            $('#rec-nombres, #rec-apellidos').val('');
                            $('#rec-unidad, #rec-cargo').prop('disabled', true);
                            $('#rec-nombres, #rec-apellidos').trigger('input');
                            $('#btn-add-user').removeClass('d-none');
                        }
                    },
                    error: function() {
                        $('#rut-spinner').addClass('d-none');
                    }
                });
            }, 800);
        } else {
            $('#rec-nombres, #rec-apellidos').val('');
            $('#btn-add-user').addClass('d-none');
            $('#rec-unidad, #rec-cargo').prop('disabled', true);
        }
    });
    
    $('#btn-add-user').click(function() {
        $('#rut_nuevo').val($('#rec-rut').val());
        $('#nombres_nuevo, #apellidos_nuevo, #correo_nuevo').val('');
        $('#modalCrearUsuario').modal('show');
    });
    
    $('#form-crear-usuario').submit(function(e) {
        e.preventDefault();
        const btn = $('#btn-submit-usuario');
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Guardando...');
        
        const data = {
            rut: $('#rut_nuevo').val(),
            first_name: $('#nombres_nuevo').val(),
            last_name: $('#apellidos_nuevo').val(),
            email: $('#correo_nuevo').val()
        };
        
        $.ajax({
            url: '/tickets/api/search/users/create/',
            type: 'POST',
            contentType: 'application/json',
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() || window.TICKET_CONFIG?.csrfToken || '' },
            data: JSON.stringify(data),
            success: function(res) {
                btn.prop('disabled', false).html('<i class="fas fa-save"></i> Guardar Funcionario');
                if (res.success) {
                    $('#modalCrearUsuario').modal('hide');
                    $('#rec-rut').val(res.user.rut);
                    $('#rec-nombres').val(res.user.nombres);
                    $('#rec-apellidos').val(res.user.apellidos);
                    $('#rec-unidad, #rec-cargo').prop('disabled', false);
                    $('#btn-add-user').addClass('d-none');
                    $('#rec-nombres, #rec-apellidos').trigger('input');
                    Swal.fire('Éxito', 'Funcionario registrado correctamente', 'success');
                } else {
                    Swal.fire('Error', res.message || 'Error al guardar', 'error');
                }
            },
            error: function(err) {
                btn.prop('disabled', false).html('<i class="fas fa-save"></i> Guardar Funcionario');
                Swal.fire('Error', 'Error de conexión', 'error');
            }
        });
    });

    // --- TEXTO DIN"""
    
    js = re.sub(old_autofill, new_autofill, js, flags=re.DOTALL)
    
    # We must also inject CSRF token in actas.html since tickets api needs it!
    # Let's add it near the top of the body block if not present
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    if 'csrfmiddlewaretoken' not in html:
        html = html.replace('<div class="ms-wrap">', '<div class="ms-wrap">\n  {% csrf_token %}')
        html = html.replace('<div class="container-fluid py-4 ms-wrap">', '<div class="container-fluid py-4 ms-wrap">\n  {% csrf_token %}')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("UI and Logic updated for actas FINAL.")

update_actas_final(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html', r'c:\proyectos\ticsystem\static\js\actas.js', r'c:\proyectos\ticsystem\actas\views.py')
