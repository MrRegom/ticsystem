import re

def add_delete_acta_js(js_path):
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Find the column definition
    old_col = """            { data: null, orderable: false, render: function(data, type, row) {
                if (row.pdf_url) {
                    return `<a href="${row.pdf_url}" target="_blank" class="btn btn-sm btn-danger" title="Ver PDF"><i class="fas fa-file-pdf mr-1"></i> PDF</a>`;
                } else {
                    return `<span class="badge badge-secondary">Sin PDF</span>`;
                }
            }}"""
    
    new_col = """            { data: null, orderable: false, render: function(data, type, row) {
                let html = '';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="btn btn-sm btn-danger mr-1" title="Ver PDF" style="font-size:0.75rem;"><i class="fas fa-file-pdf mr-1"></i> PDF</a>`;
                } else {
                    html += `<span class="badge badge-secondary mr-1">Sin PDF</span>`;
                }
                html += `<button type="button" class="btn btn-sm btn-danger btn-delete-acta" style="font-size:0.75rem;" data-id="${row.id}" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                return html;
            }}"""
            
    if old_col in js_content:
        js_content = js_content.replace(old_col, new_col)
    else:
        # Regex just in case
        js_content = re.sub(r"\{\s*data:\s*null,\s*orderable:\s*false,\s*render:\s*function\(data,\s*type,\s*row\)\s*\{\s*if\s*\(row\.pdf_url\).*?return.*?Sin PDF.*?\}\s*\}\}", new_col, js_content, flags=re.DOTALL)

    # Add the ajax event listener at the end of ready function, before the last `});`
    # Let's search for the last `});`
    
    delete_logic = """
    // Manejar Eliminación de Acta
    $(document).on('click', '.btn-delete-acta', function() {
        const actaId = $(this).data('id');
        Swal.fire({
            title: '¿Eliminar Acta?',
            text: "Esta acción no se puede deshacer.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: `/actas/api/${actaId}/delete/`,
                    type: 'POST',
                    headers: {'X-CSRFToken': getCookie('csrftoken') || $('input[name="csrfmiddlewaretoken"]').val()},
                    success: function(res) {
                        if (res.status === 'success') {
                            Swal.fire('¡Eliminada!', 'El acta ha sido eliminada correctamente.', 'success');
                            $('#tabla-historial-actas').DataTable().ajax.reload(null, false);
                        } else {
                            Swal.fire('Error', res.message || 'Error al eliminar', 'error');
                        }
                    },
                    error: function() {
                        Swal.fire('Error', 'Ocurrió un error en el servidor.', 'error');
                    }
                });
            }
        });
    });
});"""
    # Replace last }); with the logic
    js_content = js_content.rstrip()
    if js_content.endswith("});"):
        js_content = js_content[:-3] + delete_logic
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("JS Updated")

add_delete_acta_js(r'c:\proyectos\ticsystem\static\js\actas.js')
