import re

def rewrite_modal_to_drawer():
    html_path = r'c:\proyectos\ticsystem\anexos\templates\anexos\anexos.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the start of the modalAnexo
    start_str = '<!-- Modal Formulario Anexo -->'
    if start_str not in html:
        print("Could not find modal start")
        return
        
    start_idx = html.find(start_str)
    
    # Find the end of the modalAnexo
    # It ends before {% endblock %}
    end_str = '{% endblock %}'
    end_idx = html.find(end_str, start_idx)
    
    if end_idx == -1:
        print("Could not find modal end")
        return
        
    original_modal = html[start_idx:end_idx]
    
    # We will replace it with an ms-drawer
    new_drawer = """<!-- ================================================================
  DRAWER: Registrar / Editar Anexo
================================================================ -->
<div class="ms-drawer-overlay" id="anexo-drawer-overlay" onclick="closeAnexoDrawer()"></div>
<div class="ms-drawer" id="anexo-drawer" style="width: 520px; right: -520px;">
  <div class="ms-drawer-header">
    <h3 class="ms-drawer-title" id="anexo-drawer-title"><i class="fas fa-phone-alt" style="color:#0078d4; margin-right:8px;"></i> Información Técnica del Equipo</h3>
    <button class="ms-drawer-close" onclick="closeAnexoDrawer()"><i class="fas fa-times"></i></button>
  </div>
  <div class="ms-drawer-body" style="padding: 20px;">
    <form id="form-anexo" novalidate>
      <input type="hidden" id="anexo-id">
      
      <!-- IDENTIDAD -->
      <div style="font-size: 11px; font-weight: 600; color: #605e5c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #edebe9; display: flex; align-items: center; gap: 8px;">
        <i class="fas fa-barcode" style="color: #0078d4;"></i> Identidad del Anexo
      </div>

      <div class="ms-form-grid" style="margin-bottom: 16px;">
        <div class="ms-form-group">
          <label class="ms-label">NÚMERO ANEXO <span style="color:#a4262c;">*</span></label>
          <div class="input-group input-group-sm">
            <div class="input-group-prepend">
              <span class="input-group-text bg-light"><i class="fas fa-hashtag"></i></span>
            </div>
            <input type="text" class="form-control" id="a-numero" placeholder="Ej: 320645" required style="border-radius:0;">
          </div>
        </div>
        <div class="ms-form-group">
          <label class="ms-label">MARCA <span style="color:#a4262c;">*</span></label>
          <select class="ms-input select2-drawer" id="a-marca" required style="margin-bottom:0;">
            <option value="">Seleccionar Marca</option>
            {% for m in marcas %}
            <option value="{{ m.nombre }}" data-id="{{ m.id }}">{{ m.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group">
          <label class="ms-label">MODELO <span style="color:#a4262c;">*</span></label>
          <select class="ms-input select2-drawer" id="a-modelo-anexo" required style="margin-bottom:0;">
            <option value="">Seleccionar Modelo</option>
            {% for ma in modelos_anexos %}
            <option value="{{ ma.id }}" data-marca="{{ ma.marca__id|default:'' }}" data-imagen="{% if ma.imagen %}/media/{{ ma.imagen }}{% endif %}">{{ ma.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group" style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
          <div style="background: white; border: 1px dashed #e2e8f0; padding: 10px; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; margin-bottom: 5px;">
            <img id="a-imagen-preview" src="/static/img/placeholder_equipo.png" style="max-width: 100%; max-height: 100%; object-fit: contain;">
          </div>
          <small class="text-muted font-weight-bold" style="font-size: 0.65rem;">VISTA PREVIA</small>
        </div>
      </div>

      <!-- UBICACIÓN -->
      <div style="font-size: 11px; font-weight: 600; color: #605e5c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #edebe9; display: flex; align-items: center; gap: 8px;">
        <i class="fas fa-map-marker-alt" style="color: #0078d4;"></i> Ubicación Topológica
      </div>

      <div class="ms-form-grid" style="margin-bottom: 16px;">
        <div class="ms-form-group">
          <label class="ms-label">EDIFICIO</label>
          <select class="ms-input select2-drawer" id="a-edificio" style="margin-bottom:0;">
            <option value="">Todos</option>
            {% for e in edificios %}
            <option value="{{ e.id }}">{{ e.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group">
          <label class="ms-label">PISO</label>
          <select class="ms-input select2-drawer" id="a-piso" style="margin-bottom:0;">
            <option value="">Todos</option>
            {% for p in pisos %}
            <option value="{{ p.id }}" data-edificio="{{ p.edificio__id }}">{{ p.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group">
          <label class="ms-label">UNIDAD / SERVICIO</label>
          <select class="ms-input select2-drawer" id="a-unidad" style="margin-bottom:0;">
            <option value="">Todas</option>
            {% for u in unidades %}
            <option value="{{ u.id }}">{{ u.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group">
          <label class="ms-label">RECINTO</label>
          <select class="ms-input select2-drawer" id="a-recinto" style="margin-bottom:0;">
            <option value="">Todos</option>
            {% for r in recintos %}
            <option value="{{ r.id }}" data-piso="{{ r.piso_id }}" data-unidad="{{ r.unidad_id }}">{{ r.nombre }}</option>
            {% endfor %}
          </select>
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">PMA <span style="color:#a4262c;">*</span></label>
          <select class="ms-input select2-drawer" id="a-pma" required style="margin-bottom:0;">
            <option value="">Seleccionar PMA</option>
            {% for pma in pmas %}
            <option value="{{ pma.id }}" data-recinto="{{ pma.recinto_id }}">{{ pma.nombre }}</option>
            {% endfor %}
          </select>
        </div>
      </div>

      <!-- RED Y ESTADO -->
      <div style="font-size: 11px; font-weight: 600; color: #605e5c; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #edebe9; display: flex; align-items: center; gap: 8px;">
        <i class="fas fa-network-wired" style="color: #0078d4;"></i> Red y Estado
      </div>

      <div class="ms-form-grid" style="margin-bottom: 16px;">
        <div class="ms-form-group">
          <label class="ms-label">IP ADDRESS</label>
          <input type="text" class="ms-input" id="a-ip" placeholder="10.x.x.x" style="margin-bottom:0;">
        </div>
        <div class="ms-form-group">
          <label class="ms-label">SERIAL NUMBER</label>
          <input type="text" class="ms-input" id="a-serial" placeholder="Serial..." style="margin-bottom:0;">
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">ESTADO</label>
          <select class="ms-input" id="a-estado" style="margin-bottom:0;">
            <option value="Activo">Activo</option>
            <option value="Inactivo">Inactivo</option>
          </select>
        </div>
        <div class="ms-form-group" style="grid-column: span 2;">
          <label class="ms-label">COMENTARIO / OBS. TÉCNICA</label>
          <textarea class="ms-input" id="a-comentario" rows="3" placeholder="Información técnica adicional..." style="margin-bottom:0;"></textarea>
        </div>
      </div>
    </form>
  </div>
  <div class="ms-drawer-footer">
    <button class="ms-btn-secondary" onclick="closeAnexoDrawer()" style="background: white; color: #323130; border: 1px solid #8a8886;">Cancelar</button>
    <button class="ms-btn-primary" id="btn-guardar-anexo"><i class="fas fa-save"></i> Guardar Anexo</button>
  </div>
</div>
"""
    html = html.replace(original_modal, new_drawer)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Replaced modal with drawer in anexos.html")

rewrite_modal_to_drawer()
