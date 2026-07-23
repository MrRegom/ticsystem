import re

def redesign_sla(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace Header
    new_header = """<div class="ms-wrap">
  <!-- Encabezado de Página -->
  <div class="ms-header">
    <div class="ms-header-title">
      <h1 class="ms-title">Configuración del Sistema</h1>
      <p class="ms-subtitle">Gestión de parámetros de SLA, prioridades y comportamiento del helpdesk</p>
    </div>
  </div>"""

    # We replace from <div class="container-fluid py-4"> to </div> </div> for the row mb-3
    html = re.sub(r'<div class="container-fluid py-4">\s*<div class="row mb-3">.*?</div>\s*</div>', new_header, html, flags=re.DOTALL)

    # Convert Tabs to ms-fluent-tabs
    html = html.replace('class="nav nav-tabs border-bottom"', 'class="nav nav-tabs border-bottom ms-fluent-tabs"')
    html = html.replace('bg-white border border-top-0 shadow-sm p-4', 'fluent-card p-4 border-top-0')
    
    # Replace Table Classes
    html = html.replace('class="table table-hover"', 'class="fluent-table"')
    html = html.replace('class="table table-bordered text-center"', 'class="fluent-table text-center"')
    
    # Replace Table Header Backgrounds
    html = html.replace('style="background:#002a54; color:white;"', 'style="background:#0f172a; color:white;"')
    html = html.replace('style="background:#002a54; color:white; border-radius:4px;"', 'style="background:#0f172a; color:white;"')
    html = html.replace('style="background:#006FB3; color:white; border-radius:4px; padding:12px 20px;"', 'style="background:#1e293b; color:white; padding:12px 20px;"')
    html = html.replace('style="background:#f8fafc; color:#002a54; padding:14px 16px; min-width:200px;"', 'style="background:#f1f5f9; color:#0f172a; padding:14px 16px; min-width:200px;"')
    
    # Buttons
    html = html.replace('class="btn btn-primary rounded-pill px-4"', 'class="fluent-btn-primary"')
    html = html.replace('class="btn btn-primary rounded-pill px-4" id="btn-nueva-prioridad" style="background:#006FB3;border:none;"', 'class="fluent-btn-primary" id="btn-nueva-prioridad"')
    html = html.replace('class="btn btn-primary rounded-pill px-4" id="btn-guardar-sla" style="background:#006FB3;border:none;"', 'class="fluent-btn-primary" id="btn-guardar-sla"')
    html = html.replace('class="btn btn-primary rounded-pill px-4" id="btn-guardar-prio" style="background:#006FB3;border:none;"', 'class="fluent-btn-primary" id="btn-guardar-prio"')
    html = html.replace('class="btn btn-secondary rounded-pill"', 'class="fluent-btn-secondary"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SLA redesigned successfully.")

redesign_sla(r'c:\proyectos\ticsystem\sla\templates\sla\configuracion.html')
