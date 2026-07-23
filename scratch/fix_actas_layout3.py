import re

def fix_actas_layout(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Clean the top of the file up to {% block content %}
    # We will replace everything from {% extends ... %} up to {% block content %}
    
    clean_top = """{% extends "core/base.html" %}
{% load static %}
{% block title %}Actas Digitales{% endblock %}
{% block module_title %}Actas Digitales{% endblock %}

{% block content %}
<!-- MODAL CREAR USUARIO RAPIDO -->
<div class="modal fade" id="modalCrearUsuario" tabindex="-1" role="dialog" aria-hidden="true" style="z-index:1060;">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content rounded-0 border-0">
        <form id="form-crear-usuario" method="POST" onsubmit="return false;">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title text-uppercase"><i class="fas fa-user-plus text-white mr-2" style="font-size: 0.9rem; color: #006FB3;"></i> Añadir Funcionario Rápido</h5>
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
            <div class="form-row">
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Cargo / Rol</label>
                <select id="cargo_nuevo" name="cargo_nuevo" class="ms-input form-control">
                  <option value="">-- Seleccionar Cargo --</option>
                  {% for c in cargos %}
                    <option value="{{ c.nombre }}">{{ c.nombre }}</option>
                  {% endfor %}
                </select>
              </div>
              <div class="form-group col-md-6">
                <label style="font-weight:600; font-size:0.85rem; color:#334155;">Unidad / Servicio</label>
                <select id="unidad_nueva" name="unidad_nueva" class="ms-input form-control">
                  <option value="">-- Seleccionar Unidad --</option>
                  {% for u in unidades %}
                    <option value="{{ u.nombre }}">{{ u.nombre }}</option>
                  {% endfor %}
                </select>
              </div>
            </div>
          </div>
          <div class="modal-footer" style="border-top:1px solid #e2e8f0;">
            <button type="button" class="btn ms-btn-secondary" onclick="$('#modalCrearUsuario').modal('hide')">Cancelar</button>
            <button type="submit" class="btn ms-btn-primary" id="btn-submit-usuario"><i class="fas fa-save mr-1"></i> Guardar Funcionario</button>
          </div>
        </form>
      </div>
    </div>
</div>
"""
    # Replace from start to {% block content %} (inclusive)
    html = re.sub(r'\{%\s*extends\s*"core/base\.html"\s*%\}.*?\{%\s*block\s+content\s*%\}', clean_top, html, flags=re.DOTALL)

    # 2. Fix the "Registrar Funcionario" button
    old_btn = r'<button type="button" id="btn-add-user" class="btn ms-btn-secondary btn-sm mt-2 d-none" style="font-size: 0.75rem;"><i class="fas fa-user-plus"></i> Registrar Funcionario</button>'
    new_btn = r'<button type="button" id="btn-add-user" class="btn ms-btn-primary btn-sm mt-2 d-none" style="font-size: 0.75rem; text-decoration: none !important;">Registrar Funcionario</button>'
    html = re.sub(old_btn, new_btn, html)

    # 3. Fix the modal tabs for Equipos (remove underline by using button)
    old_tab1 = r'<a class="nav-link active font-weight-bold" data-toggle="tab" href="#tab-equipos" role="tab"><i class="fas fa-desktop mr-2" style="font-size: 0.9rem; color: #006FB3;"></i>Equipos Físicos</a>'
    new_tab1 = r'<button class="nav-link active font-weight-bold" data-toggle="tab" data-target="#tab-equipos" type="button" role="tab" style="border: none; background: transparent; text-decoration: none !important; margin-bottom: -1px;"><i class="fas fa-desktop mr-2" style="font-size: 0.9rem; color: #006FB3;"></i>Equipos Físicos</button>'
    
    old_tab2 = r'<a class="nav-link font-weight-bold" data-toggle="tab" href="#tab-anexos" role="tab"><i class="fas fa-phone-alt mr-2" style="font-size: 0.9rem; color: #006FB3;"></i>Anexos IP</a>'
    new_tab2 = r'<button class="nav-link font-weight-bold" data-toggle="tab" data-target="#tab-anexos" type="button" role="tab" style="border: none; background: transparent; text-decoration: none !important; margin-bottom: -1px;"><i class="fas fa-phone-alt mr-2" style="font-size: 0.9rem; color: #006FB3;"></i>Anexos IP</button>'
    
    # Let's also do a fallback just in case the regex doesn't match perfectly
    html = html.replace('<a class="nav-link active font-weight-bold" data-toggle="tab" href="#tab-equipos" role="tab">', '<button class="nav-link active font-weight-bold" data-toggle="tab" data-target="#tab-equipos" type="button" role="tab" style="background: transparent; border-top: none; border-left: none; border-right: none; text-decoration: none !important;">')
    html = html.replace('Equipos Físicos</a>', 'Equipos Físicos</button>')
    
    html = html.replace('<a class="nav-link font-weight-bold" data-toggle="tab" href="#tab-anexos" role="tab">', '<button class="nav-link font-weight-bold" data-toggle="tab" data-target="#tab-anexos" type="button" role="tab" style="background: transparent; border-top: none; border-left: none; border-right: none; text-decoration: none !important;">')
    html = html.replace('Anexos IP</a>', 'Anexos IP</button>')
    
    # Just to be sure the strict regex matches if we run it:
    html = re.sub(old_tab1, new_tab1, html)
    html = re.sub(old_tab2, new_tab2, html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Fixed layout, buttons, and modal duplicates.")

fix_actas_layout(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
