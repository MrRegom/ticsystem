import re

def fix_actas_delete_and_buttons():
    views_path = r'c:\proyectos\ticsystem\actas\views.py'
    with open(views_path, 'r', encoding='utf-8') as f:
        views_content = f.read()
    
    # Import Acta instead of ActaEntrega
    old_view = """class ActaDeleteView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'ELIMINAR_ACTAS'
    
    def post(self, request, acta_id):
        from actas.models import ActaEntrega
        try:
            acta = ActaEntrega.objects.get(id=acta_id)"""
            
    new_view = """class ActaDeleteView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'ELIMINAR_ACTAS'
    
    def post(self, request, acta_id):
        from actas.models import Acta
        try:
            acta = Acta.objects.get(id=acta_id)"""
            
    if old_view in views_content:
        views_content = views_content.replace(old_view, new_view)
        # also replace the except clauses!
        views_content = views_content.replace("entidad='ActaEntrega'", "entidad='Acta'")
        views_content = views_content.replace("except ActaEntrega.DoesNotExist:", "except Acta.DoesNotExist:")
        
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views_content)
        print("Fixed actas/views.py model reference")
    else:
        print("Could not find view string in views.py")

    js_path = r'c:\proyectos\ticsystem\static\js\actas.js'
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
        
    old_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div style="display:flex; gap:15px; justify-content:center; align-items:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" title="Ver PDF" style="color:#0078d4; font-size:1.1rem; text-decoration:none; transition:0.2s;" onmouseover="this.style.color='#106ebe'" onmouseout="this.style.color='#0078d4'"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="btn-delete-acta" data-id="${row.id}" title="Eliminar Acta" style="background:none; border:none; color:#dc3545; font-size:1.1rem; cursor:pointer; padding:0; transition:0.2s;" onmouseover="this.style.color='#bd2130'" onmouseout="this.style.color='#dc3545'"><i class="fas fa-trash-alt"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    new_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:5px; justify-content:center;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-icon-btn" style="width:26px; height:26px; font-size:12px; display:inline-flex; align-items:center; justify-content:center; text-decoration:none;" title="Ver PDF"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="ms-icon-btn btn-delete-acta" data-id="${row.id}" style="width:26px; height:26px; font-size:12px;" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                html += '</div>';
                return html;
            }}"""
            
    if old_col in js_content:
        js_content = js_content.replace(old_col, new_col)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Fixed actas.js buttons")
    else:
        print("Could not find column string in JS")

fix_actas_delete_and_buttons()
