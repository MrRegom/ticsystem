import re

def better_redesign_actas(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the main header area while keeping container-fluid
    old_header = r'<div class="row mb-3">.*?<h1 class="h4 mb-0 text-gray-800".*?</h1>.*?<p class="text-muted mb-0".*?</p>.*?</div>.*?</div>'
    new_header = """<div class="row mb-3">
        <div class="col-12">
            <div class="ms-header">
                <div class="ms-header-title">
                    <h1 class="ms-title">Gestión de Actas Digitales</h1>
                    <p class="ms-subtitle">Generación, firma y seguimiento de activos institucionales</p>
                </div>
            </div>
        </div>
    </div>"""
    html = re.sub(old_header, new_header, html, flags=re.DOTALL)
    
    # 2. Tabs styling
    html = html.replace('class="nav nav-tabs border-bottom"', 'class="nav nav-tabs border-bottom ms-fluent-tabs"')
    
    # 3. Tab content wrapper
    html = html.replace('class="tab-content bg-white p-4 border border-top-0 shadow-sm rounded-bottom"', 'class="tab-content fluent-card p-4 border-top-0"')
    
    # 4. Form Cards (Keep the card body, just make the card fluent)
    html = html.replace('class="card mb-4" style="border: 1px solid #e2e8f0; border-radius: 8px; box-shadow: none;"', 'class="fluent-card mb-4"')
    html = html.replace('class="card mb-4"', 'class="fluent-card mb-4"')
    
    # 5. The "Buscar Equipos" button
    html = html.replace('btn btn-primary btn-sm rounded-pill px-3', 'fluent-btn-primary')
    
    # 6. Tables
    html = html.replace('table table-sm table-hover', 'fluent-table')
    html = html.replace('class="table"', 'class="fluent-table"')
    html = html.replace('style="background: #002a54; color: white;"', 'style="background: #0f172a; color: white;"')
    
    # 7. Big submit button
    html = html.replace('btn btn-primary btn-lg btn-block mb-2', 'fluent-btn-primary w-100')
    html = html.replace('style="background: #006FB3; border: none; font-weight: 700; font-size: 1.1rem; padding: 12px;"', 'style="font-size: 1.1rem; padding: 12px; height: auto;"')
    
    # 8. Signature Cards
    # In the right column:
    # <div class="card-header bg-white border-bottom-0 pt-4 pb-0 d-flex justify-content-between align-items-center">
    html = html.replace('class="card-header bg-white border-bottom-0 pt-4 pb-0 d-flex justify-content-between align-items-center"', 'class="card-header bg-white border-0 pt-4 pb-0 d-flex justify-content-between align-items-center"')

    # Fix modal standardizations that were wiped when I restored the file
    if 'class="modal-content' in html:
        html = re.sub(r'<div class="modal-header"[^>]*>', '<div class="modal-header bg-primary text-white">', html)
        html = re.sub(r'<h5 class="modal-title"[^>]*>', '<h5 class="modal-title text-uppercase">', html)
        html = re.sub(r'<button type="button" class="close" data-dismiss="modal"[^>]*>&times;</button>', '<button type="button" class="close text-white" data-dismiss="modal">&times;</button>', html)
        html = re.sub(r'class="modal-content"[^>]*>', 'class="modal-content rounded-0 border-0">', html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Actas redesigned properly.")

better_redesign_actas(r'c:\proyectos\ticsystem\actas\templates\actas\actas.html')
