import re

def redesign_anexos(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove inline style
    html = re.sub(r'<style>.*?</style>', '', html, flags=re.DOTALL)
    
    # 2. Fix the main wrap and header
    old_header = r'<div class="container-fluid pb-4 animate__animated animate__fadeIn" style="padding: 0 10px;">.*?</div>\s*</div>\s*</div>'
    new_header = """<div class="ms-wrap">
  <!-- Encabezado de Página -->
  <div class="ms-header">
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
  </div>

  <!-- Barra de Herramientas Superior -->
  <div class="toolbar-container border-top" style="background: white; padding: 12px 16px; border: 1px solid #e2e8f0; border-bottom: none; display: flex; justify-content: space-between; align-items: center;">
    <div class="search-wrapper" style="position: relative; width: 300px;">
      <i class="fas fa-search" style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8;"></i>
      <input type="text" id="custom-search-input" class="ms-input" placeholder="Buscar anexo, serie, modelo, IP..." style="width: 100%; padding-left: 36px;">
    </div>
  </div>

  <!-- DataGrid -->
  <div class="fluent-card border-top-0 rounded-0 rounded-bottom">
    <div class="table-responsive">
      <table id="tabla-anexos" class="fluent-table" style="width:100%;">
        <thead>
          <tr>
            <th data-col="id" style="width:30px; text-align:center;">#</th>
            <th data-col="numero_anexo">ANEXO</th>
            <th data-col="modelo">MODELO</th>
            <th data-col="serial_number">SERIAL</th>
            <th data-col="ubicacion">UBICACIÓN</th>
            <th data-col="ip">IP ADDRESS</th>
            <th data-col="estado">ESTADO</th>
            <th data-col="acciones" style="width:120px; text-align:right;">ACCIONES</th>
          </tr>
        </thead>
        <tbody>
          <!-- Ajax Data -->
        </tbody>
      </table>
    </div>
  </div>
</div>"""

    # We will use string replacement to replace from <div class="container-fluid pb-4... to </div></div></div>
    # Actually, the regex might be tricky. Let's just find the start and replace up to the first modal.
    parts = html.split('<!-- Modal Detalle del Anexo')
    if len(parts) == 2:
        top_part = parts[0]
        bottom_part = '<!-- Modal Detalle del Anexo' + parts[1]
        
        # Replace everything from <div class="container-fluid in top_part with new_header
        top_part = re.sub(r'<div class="container-fluid pb-4.*', new_header, top_part, flags=re.DOTALL)
        
        html = top_part + bottom_part
        
    # 3. Standardize all modals
    # Header:
    html = re.sub(r'<div style="background: #002a54; color: white; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between;">', '<div class="modal-header bg-primary text-white">', html)
    html = re.sub(r'<div class="modal-header"[^>]*>', '<div class="modal-header bg-primary text-white">', html)
    
    # Title:
    html = re.sub(r'<h5 style="margin: 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center; gap: 10px;">', '<h5 class="modal-title text-uppercase">', html)
    html = re.sub(r'<h5 class="modal-title"[^>]*>', '<h5 class="modal-title text-uppercase">', html)
    html = re.sub(r'<h5 class="modal-title">', '<h5 class="modal-title text-uppercase">', html)
    
    # Close button:
    html = re.sub(r'<button type="button" class="close" data-dismiss="modal" style="color: white; opacity: 0.8; text-shadow: none;">&times;</button>', '<button type="button" class="close text-white" data-dismiss="modal">&times;</button>', html)
    
    # Modals rounded corners remove
    html = re.sub(r'class="modal-content"[^>]*>', 'class="modal-content rounded-0 border-0">', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Anexos redesigned successfully.")

redesign_anexos(r'c:\proyectos\ticsystem\anexos\templates\anexos\anexos.html')
