import re

def fix_anexos_js():
    js_path = r'c:\proyectos\ticsystem\static\js\anexos.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js = f.read()

    # Add open/close drawer functions at the end
    drawer_funcs = """
// ==========================================
// DRAWERS
// ==========================================
window.openAnexoDrawer = function() {
    $('#anexo-drawer').addClass('open');
    $('#anexo-drawer-overlay').addClass('active');
};
window.closeAnexoDrawer = function() {
    $('#anexo-drawer').removeClass('open');
    $('#anexo-drawer-overlay').removeClass('active');
};
"""
    if 'window.openAnexoDrawer' not in js:
        js += drawer_funcs

    # Replace modal initializations
    js = js.replace("$('.select2-modal').select2({", "$('.select2-drawer').select2({")
    js = js.replace("dropdownParent: $('#modalAnexo'),", "dropdownParent: $('#anexo-drawer'),")
    js = js.replace("$('.select2-modal').val('').trigger('change.select2');", "$('.select2-drawer').val('').trigger('change.select2');")

    # Replace modal show/hide with drawer open/close
    js = js.replace("$('#modalAnexoLabel').text('Información Técnica del Equipo');", "$('#anexo-drawer-title').html('<i class=\"fas fa-phone-alt\" style=\"color:#0078d4; margin-right:8px;\"></i> Información Técnica del Equipo');")
    js = js.replace("$('#modalAnexoLabel').text('Editar Anexo');", "$('#anexo-drawer-title').html('<i class=\"fas fa-phone-alt\" style=\"color:#0078d4; margin-right:8px;\"></i> Editar Anexo');")
    
    js = js.replace("$('#modalAnexo').modal('show');", "openAnexoDrawer();")
    js = js.replace("$('#modalAnexo').modal('hide');", "closeAnexoDrawer();")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("Fixed anexos.js references to modalAnexo")

fix_anexos_js()
