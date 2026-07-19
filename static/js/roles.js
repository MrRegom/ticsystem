let rolesData = [];

$(document).ready(function() {
    // Inicializar data
    if (typeof INITIAL_ROLES !== 'undefined') {
        rolesData = INITIAL_ROLES;
        renderList(rolesData);
    }

    // Inicializar Select2 para el icono
    function formatIcon(icon) {
        if (!icon.id) return icon.text;
        var iconClass = icon.id;
        var $icon = $(
            '<span><i class="' + iconClass + '" style="margin-right:8px; font-size:16px;"></i> ' + icon.text + '</span>'
        );
        return $icon;
    }

    $('#icono').select2({
        theme: 'bootstrap4',
        templateResult: formatIcon,
        templateSelection: formatIcon,
        dropdownParent: $('#role-drawer') // importante para que se vea por encima del drawer
    });

    // Búsqueda en tiempo real
    $('#search-input').on('input', function() {
        const query = $(this).val().toLowerCase();
        const filtered = rolesData.filter(r => 
            r.nombre.toLowerCase().includes(query) || 
            (r.descripcion && r.descripcion.toLowerCase().includes(query))
        );
        renderList(filtered);
    });

    // Guardar Rol
    $('#form-rol').on('submit', function(e) {
        e.preventDefault();
        
        const rolId = $('#rol_id').val();
        const method = rolId ? 'PUT' : 'POST';
        const url = '/api/roles/';
        
        const permisos = {};
        $('.perm-toggle').each(function() {
            if ($(this).is(':checked')) {
                permisos[$(this).val()] = true;
            }
        });

        const data = {
            id: rolId,
            nombre: $('#nombre').val(),
            descripcion: $('#descripcion').val(),
            icono: $('#icono').val(),
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
                    closeDrawer();
                    window.location.reload();
                } else {
                    alert(resp.message || 'Error al guardar el rol.');
                }
            }
        });
    });
});

// Renderizar la lista
function renderList(roles) {
    const listContainer = $('#roles-list');
    listContainer.empty();

    if (roles.length === 0) {
        listContainer.html('<div style="padding: 40px; text-align: center; color: #605e5c;">No se encontraron roles.</div>');
        return;
    }

    roles.forEach(rol => {
        const iconHtml = rol.icono ? `<i class="${rol.icono}" style="margin-right:10px; font-size:18px; color:#0078d4;"></i>` : '';
        const estadoHtml = rol.activo 
            ? `<span style="color:#107c10; font-weight:600;"><i class="fas fa-check-circle"></i> Activo</span>` 
            : `<span style="color:#a4262c; font-weight:600;"><i class="fas fa-times-circle"></i> Inactivo</span>`;
        
        const row = `
            <div class="ms-list-row" onclick="openDrawer('editar', ${rol.id})">
                <div style="font-weight:600; color:#323130; display:flex; align-items:center;">
                    ${iconHtml}
                    ${rol.nombre}
                </div>
                <div style="color:#605e5c; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${rol.descripcion || ''}">
                    ${rol.descripcion || '-'}
                </div>
                <div style="color:#605e5c; font-size: 0.85rem;">
                    ${rol.permisos_count} permisos
                </div>
                <div style="color:#605e5c; font-size: 0.85rem;">
                    ${rol.usuarios_count} usuarios
                </div>
                <div>
                    ${estadoHtml}
                </div>
                <div style="text-align:right;">
                    <button class="ms-icon-btn" onclick="event.stopPropagation(); openDrawer('editar', ${rol.id})" title="Editar Rol">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        `;
        listContainer.append(row);
    });
}

// Renderizar Toggle Permisos
function renderPermisos(rolPermisos = {}) {
    const container = $('#permisos-container');
    container.empty();
    
    PERMISOS_DISPONIBLES.forEach(p => {
        const isChecked = rolPermisos[p.id] ? 'checked' : '';
        const row = `
            <div style="display:flex; justify-content:space-between; align-items:center; padding: 10px 0; border-bottom: 1px solid #f3f2f1;">
                <div>
                    <div style="font-weight:600; font-size:14px; color:#323130;">${p.nombre}</div>
                    <div style="font-size:12px; color:#605e5c;">Módulo: ${p.modulo}</div>
                </div>
                <div>
                    <label class="ms-toggle">
                        <input type="checkbox" class="perm-toggle" value="${p.id}" ${isChecked}>
                        <span class="ms-toggle-slider"></span>
                    </label>
                </div>
            </div>
        `;
        container.append(row);
    });
}

// Drawer Functions
function openDrawer(action, rolId = null) {
    if (action === 'crear') {
        $('#drawer-title').text('Nuevo Rol');
        $('#form-rol')[0].reset();
        $('#rol_id').val('');
        $('#icono').val('fas fa-user-circle').trigger('change');
        renderPermisos({});
        showDrawer();
    } else if (action === 'editar' && rolId) {
        $('#drawer-title').text('Editar Rol');
        
        $.ajax({
            url: `/api/roles/${rolId}/`,
            type: 'GET',
            success: function(resp) {
                if(resp.success) {
                    $('#rol_id').val(resp.data.id);
                    $('#nombre').val(resp.data.nombre);
                    $('#descripcion').val(resp.data.descripcion);
                    if (resp.data.icono) {
                        $('#icono').val(resp.data.icono).trigger('change');
                    } else {
                        $('#icono').val('fas fa-user-circle').trigger('change');
                    }
                    $('#activo').val(resp.data.activo.toString());
                    renderPermisos(resp.data.permisos);
                    showDrawer();
                } else {
                    alert('Error al obtener datos del rol.');
                }
            }
        });
    }
}

function showDrawer() {
    $('#drawer-overlay').fadeIn(200);
    $('#role-drawer').addClass('open');
}

function closeDrawer() {
    $('#role-drawer').removeClass('open');
    $('#drawer-overlay').fadeOut(200);
}

// Helpers
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
