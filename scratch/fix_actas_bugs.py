import re

def fix_actas_delete_bug_and_ui():
    views_path = r'c:\proyectos\ticsystem\actas\views.py'
    with open(views_path, 'r', encoding='utf-8') as f:
        views_content = f.read()
    
    # Import ActaEntrega in the view
    old_view = """class ActaDeleteView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'ELIMINAR_ACTAS'
    
    def post(self, request, acta_id):
        try:
            acta = ActaEntrega.objects.get(id=acta_id)"""
            
    new_view = """class ActaDeleteView(PermisoRequeridoMixin, LoginRequiredMixin, View):
    permiso_requerido = 'ELIMINAR_ACTAS'
    
    def post(self, request, acta_id):
        from actas.models import ActaEntrega
        try:
            acta = ActaEntrega.objects.get(id=acta_id)"""
            
    if old_view in views_content:
        views_content = views_content.replace(old_view, new_view)
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(views_content)
        print("Fixed actas/views.py")
    else:
        print("Could not find view string in views.py")

    html_path = r'c:\proyectos\ticsystem\actas\templates\actas\actas.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    old_th = "<th>Acciones</th>"
    new_th = "<th class=\"text-center\">Acciones</th>"
    
    if old_th in html_content:
        html_content = html_content.replace(old_th, new_th)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("Fixed actas.html")
    else:
        print("Could not find th in html")

fix_actas_delete_bug_and_ui()
