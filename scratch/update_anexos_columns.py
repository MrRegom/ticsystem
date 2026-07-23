import re

def update_anexos_columns():
    path = r'c:\proyectos\ticsystem\static\js\anexos.js'
    with open(path, 'r', encoding='utf-8') as f:
        js = f.read()

    # We need to replace the `columns:` array
    start_str = '        columns: ['
    start_idx = js.find(start_str)
    if start_idx == -1:
        print("Could not find columns array")
        return
        
    end_str = '        ],'
    end_idx = js.find(end_str, start_idx) + len(end_str)
    
    original_columns = js[start_idx:end_idx]

    new_columns = """        columns: [
            { data: 'id', orderable: false, className: 'text-center' },
            { 
                data: 'numero_anexo',
                render: function(data, type, row) {
                    var img = row.modelo_img ? `<img src="${row.modelo_img}" style="width:32px; height:32px; padding:2px; background:#f3f2f1; border-radius:4px; object-fit:contain; flex-shrink:0;">` : `<div style="width:32px; height:32px; display:flex; align-items:center; justify-content:center; background:#f3f2f1; border-radius:4px;"><i class="fas fa-phone-alt" style="color:#605e5c;"></i></div>`;
                    return `
                    <div class="d-flex align-items-center">
                        <div style="margin-right: 12px;">${img}</div>
                        <div>
                            <div class="cell-primary">${data || 'S/N'}</div>
                        </div>
                    </div>`;
                }
            },
            { 
                data: 'modelo',
                render: function(data, type, row) {
                    return `<div class="cell-primary">${row.modelo_anexo_nombre || row.modelo || 'Sin Modelo'}</div>`;
                }
            },
            { 
                data: null,
                render: function(data, type, row) {
                    var ubi = row.unidad_nombre || 'Sin Unidad';
                    var edif = [];
                    if (row.edificio_nombre) edif.push(row.edificio_nombre);
                    var edif_str = edif.length > 0 ? edif.join(' - ') : '';
                    return `
                    <div>
                        <div class="cell-primary">${ubi}</div>
                        ${edif_str ? `<div class="cell-secondary"><i class="fas fa-hospital mr-1"></i>${edif_str}</div>` : ''}
                    </div>`;
                }
            },
            {
                data: 'pma_nombre',
                render: function(data, type, row) {
                    return `<div class="cell-secondary">${data || '-'}</div>`;
                }
            },
            {
                data: 'piso_nombre',
                render: function(data, type, row) {
                    return `<div class="cell-secondary">${data || '-'}</div>`;
                }
            },
            {
                data: 'numero_inventario',
                render: function(data, type, row) {
                    return `<div class="cell-secondary">${row.numero_inventario || '-'}</div>`;
                }
            },
            { 
                data: 'serial_number',
                render: function(data, type, row) {
                    return `<div class="cell-secondary"><i class="fas fa-barcode mr-1"></i>${row.serial_number || 'S/N'}</div>`;
                }
            },
            { 
                data: 'ip',
                render: function(data, type, row) {
                    return row.ip ? `<code class="cell-secondary">${row.ip}</code>` : `<span class="text-muted">S/IP</span>`;
                }
            },
            { 
                data: 'estado',
                render: function(data, type, row) {
                    return row.estado === 'Activo' 
                        ? `<span class="status-badge status-activo"><i class="fas fa-check-circle mr-1"></i>Activo</span>`
                        : `<span class="status-badge status-inactivo"><i class="fas fa-times-circle mr-1"></i>Inactivo</span>`;
                }
            },
            {
                data: null,
                orderable: false,
                searchable: false,
                className: 'text-right',
                render: function(data, type, row) {
                    return `
                    <div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; width:100%; transform:none !important; margin-top:0;">
                        <button class="ms-icon-btn btn-ver-anexo" data-id="${row.id}" title="Ver Anexo" style="width:26px; height:26px; font-size:12px; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#0078d4'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="ms-icon-btn btn-editar-anexo" data-id="${row.id}" title="Editar Anexo" style="width:26px; height:26px; font-size:12px; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#ffb900'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="ms-icon-btn btn-eliminar-anexo" data-id="${row.id}" title="Eliminar Anexo" style="width:26px; height:26px; font-size:12px; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#dc3545'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>`;
                }
            }
        ],"""
    
    js = js.replace(original_columns, new_columns)

    # 3. Add N° Inventario to Save logic
    # Find `var anexoData = {` and add `numero_inventario: $('#a-inventario').val(),`
    js = js.replace("serial_number: $('#a-serial').val(),", "serial_number: $('#a-serial').val(),\n            numero_inventario: $('#a-inventario').val(),")
    
    # 4. Add N° Inventario to Edit Logic
    # Find `$('#a-serial').val(data.serial_number);` and add `$('#a-inventario').val(data.numero_inventario);`
    js = js.replace("$('#a-serial').val(data.serial_number);", "$('#a-serial').val(data.serial_number);\n        $('#a-inventario').val(data.numero_inventario);")

    # 5. Clear N° Inventario in Create new Logic
    js = js.replace("$('#a-serial').val('');", "$('#a-serial').val('');\n        $('#a-inventario').val('');")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(js)

    print("Updated anexos.js columns and logic")

update_anexos_columns()
