import re

def update_anexos_html():
    path = r'c:\proyectos\ticsystem\anexos\templates\anexos\anexos.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the table headers
    # <th class="text-center" style="width: 50px;">ID</th>
    # <th>Anexo</th>
    # <th>Modelo</th>
    # <th>Serial</th>
    # <th>Ubicación</th>
    # <th>IP</th>
    # <th>Estado</th>
    old_th = """                      <th class="text-center" style="width: 50px;">ID</th>
                      <th>Anexo</th>
                      <th>Modelo</th>
                      <th>Serial</th>
                      <th>Ubicación</th>
                      <th>IP</th>
                      <th>Estado</th>"""
    new_th = """                      <th class="text-center" style="width: 50px;">ID</th>
                      <th>Anexo</th>
                      <th>Modelo</th>
                      <th>Ubicación</th>
                      <th>PMA</th>
                      <th>Piso</th>
                      <th>N° Inventario</th>
                      <th>Serial</th>
                      <th>IP</th>
                      <th>Estado</th>"""
    html = html.replace(old_th, new_th)

    # 2. Add N° Inventario to the drawer
    old_inputs = """        <div class="ms-form-group">
          <label class="ms-label">SERIAL NUMBER</label>
          <input type="text" class="ms-input" id="a-serial" placeholder="Serial..." style="margin-bottom:0;">
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">ESTADO</label>"""
    new_inputs = """        <div class="ms-form-group">
          <label class="ms-label">SERIAL NUMBER</label>
          <input type="text" class="ms-input" id="a-serial" placeholder="Serial..." style="margin-bottom:0;">
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">N° INVENTARIO</label>
          <input type="text" class="ms-input" id="a-inventario" placeholder="Ej: AF-000345" style="margin-bottom:0;">
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">ESTADO</label>"""
    html = html.replace(old_inputs, new_inputs)

    # Bump version
    html = html.replace("anexos.js' %}?v=1.2", "anexos.js' %}?v=1.3")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Updated anexos.html")

update_anexos_html()
