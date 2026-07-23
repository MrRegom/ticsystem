import re

def better_redesign_anexos(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove inline style
    html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
    
    # 2. Update Header
    old_header = r'<div class="page-header-top".*?</div>\s*</div>\s*</div>'
    new_header = """<div class="ms-header">
    <div class="ms-header-title">
      <h1 class="ms-title">Gestión de Anexos Telefónicos</h1>
      <p class="ms-subtitle">Directorio centralizado y administración de equipos IP</p>
    </div>
    <div class="ms-header-actions">
        <button id="btn-nuevo" class="fluent-btn-primary">
          <i class="fas fa-plus"></i> Nuevo Anexo
        </button>
        <button id="btn-export-excel" class="fluent-btn-secondary" style="margin-left: 8px;">
          <i class="fas fa-file-excel"></i> Excel
        </button>
    </div>
  </div>"""
    html = re.sub(old_header, new_header, html, flags=re.DOTALL)

    # 3. Add ms-wrap to the container
    html = html.replace('class="container-fluid pb-4 animate__animated animate__fadeIn"', 'class="container-fluid pb-4 animate__animated animate__fadeIn ms-wrap"')
    
    # 4. Search bar
    html = html.replace('class="toolbar-container border-top" style="border-radius: 8px 8px 0 0 !important; border: 1px solid #e2e8f0;"', 'class="toolbar-container border-top" style="background: white; padding: 12px 16px; border: 1px solid #e2e8f0; border-bottom: none; display: flex; justify-content: space-between; align-items: center;"')
    
    # 5. DataGrid
    html = html.replace('class="datagrid-container"', 'class="fluent-card border-top-0 rounded-0 rounded-bottom"')
    html = html.replace('class="table"', 'class="fluent-table"')
    html = html.replace('style="background: #002a54 !important; /* Azul Marga Marga */ color: #ffffff !important;"', 'style="background: #0f172a; color: white;"')

    # Modals styling
    if 'class="modal-content' in html:
        html = re.sub(r'<div style="background: #002a54; color: white; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between;">', '<div class="modal-header bg-primary text-white">', html)
        html = re.sub(r'<div class="modal-header"[^>]*>', '<div class="modal-header bg-primary text-white">', html)
        html = re.sub(r'<h5 style="margin: 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center; gap: 10px;">', '<h5 class="modal-title text-uppercase">', html)
        html = re.sub(r'<h5 class="modal-title"[^>]*>', '<h5 class="modal-title text-uppercase">', html)
        html = re.sub(r'<button type="button" class="close" data-dismiss="modal"[^>]*>&times;</button>', '<button type="button" class="close text-white" data-dismiss="modal">&times;</button>', html)
        html = re.sub(r'class="modal-content"[^>]*>', 'class="modal-content rounded-0 border-0">', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Anexos redesigned properly.")

better_redesign_anexos(r'c:\proyectos\ticsystem\anexos\templates\anexos\anexos.html')
