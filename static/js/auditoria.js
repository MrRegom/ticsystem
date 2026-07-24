$(document).ready(function() {
    let table = $('#auditoriaTable').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: API_URL,
            type: 'GET',
            data: function (d) {
                // Agregar filtros al request
                d.modulo = $('#filterModulo').val();
                d.accion = $('#filterAccion').val();
                d.usuario = $('#filterUsuario').val();
                d.fecha_inicio = $('#filterDesde').val();
                d.fecha_fin = $('#filterHasta').val();
            }
        },
        columns: [
            { data: 'fecha', name: 'fecha', orderable: true },
            { data: 'usuario', name: 'usuario', orderable: false, render: function(data) {
                return `<div style="font-weight: 600; color: #0078d4;">${data}</div>`;
            }},
            { data: 'accion', name: 'accion', orderable: false, render: function(data) {
                let badgeClass = 'badge-accion-acceso';
                if (data === 'Creación' || data === 'CREAR') badgeClass = 'badge-accion-crear';
                else if (data === 'Modificación' || data === 'MODIFICAR') badgeClass = 'badge-accion-modificar';
                else if (data === 'Eliminación' || data === 'ELIMINAR') badgeClass = 'badge-accion-eliminar';
                else if (data.includes('Login') || data.includes('LOGIN')) badgeClass = 'badge-accion-login';
                
                return `<span class="badge-action ${badgeClass}">${data}</span>`;
            }},
            { data: 'modulo', name: 'modulo', orderable: false, render: function(data) {
                return `<div style="font-weight: 600; color: #323130;">${data}</div>`;
            }},
            { data: 'detalles', name: 'detalles', orderable: false, render: function(data) {
                return `<div style="font-size: 12px; color: #605e5c; max-width: 400px; white-space: normal; word-break: break-all;">${data}</div>`;
            }},
            { data: 'ip', name: 'ip', orderable: false, render: function(data) {
                return `<div style="font-family: monospace; font-size: 11px;">${data}</div>`;
            }}
        ],
        order: [[0, 'desc']], // Ordenar por fecha desc por defecto
        pageLength: 20,
        lengthMenu: [10, 20, 50, 100],
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
        },
        dom: '<"fluent-header"lf>rt<"fluent-footer"ip>',
    });

    // Refrescar al hacer click en Filtrar
    $('#btnFiltrar').on('click', function() {
        table.ajax.reload();
    });

    // Refrescar con Enter en el input de usuario
    $('#filterUsuario').on('keypress', function(e) {
        if(e.which === 13) {
            table.ajax.reload();
        }
    });
});
