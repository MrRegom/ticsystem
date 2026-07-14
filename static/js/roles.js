$(document).ready(function() {
    // Inicializar DataTable
    const table = $('#roles-table').DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        responsive: true,
        order: [[0, 'asc']]
    });

    // Función para renderizar los checkboxes de permisos
    function renderPermisos(rolPermisos = {}) {
        const container = $('#permisos-container');
        container.empty();
        
        PERMISOS_DISPONIBLES.forEach(p => {
            const isChecked = rolPermisos[p.id] ? 'checked' : '';
            const col = `
                <div class="col-md-6 mb-3">
                    <div class="custom-control custom-switch">
                        <input type="checkbox" class="custom-control-input perm-checkbox" id="perm_${p.id}" value="${p.id}" ${isChecked}>
                        <label class="custom-control-label" for="perm_${p.id}">
                            <span class="font-weight-bold d-block text-dark" style="font-size: 0.85rem;">${p.nombre}</span>
                            <span class="text-muted small">Módulo: ${p.modulo}</span>
                        </label>
                    </div>
                </div>
            `;
            container.append(col);
        });
    }

    // Nuevo Rol
    $('#btn-nuevo-rol').on('click', function() {
        $('#form-rol')[0].reset();
        $('#rol_id').val('');
        renderPermisos({});
        $('#modalRolLabel').text('Nuevo Rol');
        $('#modalRol').modal('show');
    });

    // Editar Rol
    $('.btn-edit-rol').on('click', function() {
        const rolId = $(this).data('id');
        
        // Fetch rol data via API
        $.ajax({
            url: `/api/roles/${rolId}/`,
            type: 'GET',
            success: function(resp) {
                if(resp.success) {
                    $('#rol_id').val(resp.data.id);
                    $('#nombre').val(resp.data.nombre);
                    $('#descripcion').val(resp.data.descripcion);
                    $('#activo').val(resp.data.activo.toString());
                    renderPermisos(resp.data.permisos);
                    $('#modalRolLabel').text('Editar Rol: ' + resp.data.nombre);
                    $('#modalRol').modal('show');
                } else {
                    alert('Error al obtener datos del rol.');
                }
            }
        });
    });

    // Guardar Rol
    $('#form-rol').on('submit', function(e) {
        e.preventDefault();
        
        const rolId = $('#rol_id').val();
        const method = rolId ? 'PUT' : 'POST';
        const url = '/api/roles/';
        
        const permisos = {};
        $('.perm-checkbox').each(function() {
            if ($(this).is(':checked')) {
                permisos[$(this).val()] = true;
            }
        });

        const data = {
            id: rolId,
            nombre: $('#nombre').val(),
            descripcion: $('#descripcion').val(),
            activo: $('#activo').val() === 'true',
            permisos: permisos
        };

        $.ajax({
            url: url,
            type: method,
            data: JSON.stringify(data),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(resp) {
                if(resp.success) {
                    $('#modalRol').modal('hide');
                    window.location.reload();
                } else {
                    alert(resp.message || 'Error al guardar el rol.');
                }
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
