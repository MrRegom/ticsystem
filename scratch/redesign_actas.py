import re

def redesign_actas(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Fluent Header
    new_header = """<div class="ms-wrap">
  <!-- Encabezado de Página -->
  <div class="ms-header">
    <div class="ms-header-title">
      <h1 class="ms-title">Gestión de Actas Digitales</h1>
      <p class="ms-subtitle">Generación, firma y seguimiento de activos institucionales</p>
    </div>
  </div>"""

    # Replace the container-fluid and row mb-3 header
    html = re.sub(r'<div class="container-fluid py-4">\s*<div class="row mb-3">.*?</div>\s*</div>', new_header, html, flags=re.DOTALL)

    # Convert the tabs to a fluent look
    # We will just change the classes a bit or remove Bootstrap shadows
    html = html.replace('class="nav nav-tabs border-bottom"', 'class="nav nav-tabs border-bottom ms-fluent-tabs"')
    html = html.replace('bg-white p-4 border border-top-0 shadow-sm rounded-bottom', 'fluent-card p-4 border-top-0')
    
    # Fluent Cards
    html = html.replace('style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: none;"', 'class="fluent-card"')
    html = html.replace('class="card mb-4" class="fluent-card"', 'class="fluent-card mb-4"')
    html = html.replace('class="card mb-4"', 'class="fluent-card mb-4"')
    html = html.replace('class="card-body"', 'class="fluent-card-header"') # Wait, maybe not body -> header, let's just keep card-body for inner padding or use fluent content classes.
    # Actually, card-body is fine, but fluent-card usually just has padding. Let's just swap the borders.
    html = html.replace('style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);"', 'class="fluent-card"')
    
    # Modals
    html = html.replace('class="modal-header" style="background: #006FB3; color: white;"', 'class="modal-header bg-primary text-white"')
    html = html.replace('class="modal-title"', 'class="modal-title text-uppercase"')
    html = html.replace('class="modal-content" style="border-radius: 0; border: none;"', 'class="modal-content rounded-0 border-0"')
    html = html.replace('btn btn-primary', 'btn fluent-btn-primary')

    # Tables
    html = html.replace('class="table table-hover w-100"', 'class="fluent-table"')
    html = html.replace('class="table table-sm table-hover w-100"', 'class="fluent-table"')
    html = html.replace('class="table table-hover mb-0"', 'class="fluent-table"')
    html = html.replace('style="background: #002a54; color: white;"', 'style="background: #0f172a; color: white;"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Actas redesigned successfully.")

redesign_actas(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
