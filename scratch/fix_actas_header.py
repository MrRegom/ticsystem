import re

def reformat_actas(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Header and Tabs
    old_header = r'<div class="row mb-3">\s*<div class="col-12">\s*<div class="ms-header">\s*<div class="ms-header-title">\s*<h1 class="ms-title">Gestión de Actas Digitales</h1>\s*<p class="ms-subtitle">Generación, firma y seguimiento de activos institucionales</p>\s*</div>\s*</div>\s*</div>\s*</div>\s*<!-- Pestañas -->\s*<ul class="nav nav-tabs border-bottom ms-fluent-tabs" id="actasTab" role="tablist" style="border-color: #e2e8f0;">\s*<li class="nav-item" role="presentation">\s*<a class="nav-link active" id="nuevo-tab" data-toggle="tab" href="#nuevo" role="tab" style="font-weight: 600; color: #002a54;">\s*<i class="far fa-file-alt mr-2"></i>Nueva Acta\s*</a>\s*</li>\s*<li class="nav-item" role="presentation">\s*<a class="nav-link" id="historial-tab" data-toggle="tab" href="#historial" role="tab" style="color: #64748b;">\s*<i class="fas fa-history mr-2"></i>Historial\s*</a>\s*</li>\s*</ul>'

    new_header = '''<!-- ENCABEZADO MICROSOFT FLUENT -->
    <div class="ms-header d-flex justify-content-between align-items-center mb-4 pb-3" style="border-bottom: 1px solid #e2e8f0;">
        <div class="ms-title-area">
            <h2 style="text-transform: uppercase; font-weight: 700; color: #002a54; margin: 0; font-size: 1.5rem; letter-spacing: -0.5px;">Gestión de Actas Digitales</h2>
            <p style="color: #64748b; font-size: 0.9rem; margin-top: 4px; margin-bottom: 0;">Generación, firma y seguimiento de activos institucionales</p>
        </div>
        <div class="ms-command-bar">
            <!-- Botones como Pestañas -->
            <ul class="nav nav-pills m-0" id="actasTab" role="tablist" style="gap: 8px;">
                <li class="nav-item" role="presentation">
                    <a class="btn ms-btn-primary active" id="nuevo-tab" data-toggle="tab" href="#nuevo" role="tab" style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem;">
                        <i class="far fa-file-alt mr-2"></i> Nueva Acta
                    </a>
                </li>
                <li class="nav-item" role="presentation">
                    <a class="btn ms-btn-secondary" id="historial-tab" data-toggle="tab" href="#historial" role="tab" style="padding: 6px 16px; border-radius: 4px; font-size: 0.85rem; background: #fff; border: 1px solid #cbd5e1; color: #334155;">
                        <i class="fas fa-history mr-2"></i> Historial
                    </a>
                </li>
            </ul>
        </div>
    </div>'''

    html = re.sub(old_header, new_header, html, flags=re.IGNORECASE)

    # 2. Update Texto Principal del Acta container
    card_style = 'style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); background-color: #ffffff;"'
    
    old_texto = r'<h6 style="color: #002a54; font-weight: 700; margin-bottom: 16px;"><i class="far fa-file-word mr-2"></i> Texto Principal del Acta</h6>\s*<div class="fluent-card mb-4" style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: none; background: #f8fafc;">'
    new_texto = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="far fa-file-word mr-2"></i> Texto Principal del Acta</h6>
                        </div>
                        <div class="fluent-card mb-4" style="display:none;">''' # This handles the extra div tag implicitly since we can't remove the closing tag easily. Wait, if I do that, the opening tag `<div class="fluent-card mb-4"...>` is replaced by TWO divs? No, I will replace the H6 + DIV with DIV + HEADER + DIV.
    
    new_texto = f'''<div class="fluent-card mb-4 mt-4" {card_style}>
                        <div class="card-header bg-white border-0 pt-4 pb-0">
                            <h6 style="font-weight: 700; color: #002a54; margin: 0;"><i class="far fa-file-word mr-2"></i> Texto Principal del Acta</h6>
                        </div>'''
    # We also need to strip the extra `<div class="fluent-card...>`
    html = re.sub(old_texto, new_texto, html, flags=re.IGNORECASE)


    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Formatting applied successfully.")

reformat_actas(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
