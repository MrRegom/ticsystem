$(document).ready(function() {
    // CSRF Setup
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({ beforeSend: function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", csrftoken); }});

    // Inicializar Select2
    $('.select2-drawer').select2({
        dropdownParent: $('#anexo-drawer'),
        width: '100%',
        theme: 'bootstrap4'
    });

    // Lógica para filtrar Pisos según Edificio
    $('#a-edificio').on('change', function() {
        var edif_id = $(this).val();
        $('#a-piso option').each(function() {
            if ($(this).val() === "") $(this).show();
            else {
                if ($(this).data('edificio') == edif_id || edif_id === "") $(this).show();
                else $(this).hide();
            }
        });
        $('#a-piso').val('').trigger('change.select2');
    });

    // Lógica para filtrar Recintos según Piso o Unidad
    $('#a-piso, #a-unidad').on('change', function() {
        var piso_id = $('#a-piso').val();
        var unidad_id = $('#a-unidad').val();
        $('#a-recinto option').each(function() {
            if ($(this).val() === "") $(this).show();
            else {
                var show = true;
                if (piso_id && $(this).data('piso') != piso_id) show = false;
                if (unidad_id && $(this).data('unidad') != unidad_id) show = false;
                if (show) $(this).show();
                else $(this).hide();
            }
        });
        $('#a-recinto').val('').trigger('change.select2');
    });

    // Lógica para filtrar PMA según Recinto
    $('#a-recinto').on('change', function() {
        var rec_id = $(this).val();
        $('#a-pma option').each(function() {
            if ($(this).val() === "") $(this).show();
            else {
                if ($(this).data('recinto') == rec_id || rec_id === "") $(this).show();
                else $(this).hide();
            }
        });
        $('#a-pma').val('').trigger('change.select2');
    });

    // Lógica para filtrar ModeloAnexo según Marca y previsualizar imagen
    $('#a-marca').on('change', function() {
        var marca_id = $(this).find('option:selected').data('id');
        $('#a-modelo-anexo option').each(function() {
            if ($(this).val() === "") $(this).show();
            else {
                if ($(this).data('marca') == marca_id || !marca_id) $(this).show();
                else $(this).hide();
            }
        });
        $('#a-modelo-anexo').val('').trigger('change.select2');
    });

    $('#a-modelo-anexo').on('change', function() {
        var imgUrl = $(this).find('option:selected').data('imagen');
        if (imgUrl) {
            $('#a-imagen-preview').attr('src', imgUrl);
        } else {
            $('#a-imagen-preview').attr('src', '/static/img/placeholder_equipo.png');
        }
    });

    // Validar y auto-formatear IP Address
    $('#a-ip').on('input', function(e) {
        let input = e.target;
        let val = input.value.replace(/[^0-9.]/g, '');
        val = val.replace(/\.+/g, '.'); // Evitar doble punto
        
        let parts = val.split('.');
        if (parts.length > 4) parts = parts.slice(0, 4);
        
        for (let i = 0; i < parts.length; i++) {
            if (parts[i].length > 3) {
                if (i < 3 && parts.length === i + 1) {
                    parts.push(parts[i].substring(3));
                    parts[i] = parts[i].substring(0, 3);
                } else {
                    parts[i] = parts[i].substring(0, 3);
                }
            }
        }
        input.value = parts.join('.');
    });

    // Inicializar DataTable
    var tablaAnexos = $('#tabla-anexos').DataTable({
        serverSide: true,
        processing: true,
        responsive: true,
        pagingType: "full_numbers",
        ajax: {
            url: '/anexos/api/',
            type: 'POST',
            error: function (xhr, error, code) {
                console.error("Error al cargar Anexos:", error);
            }
        },
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Buscar...",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
            infoEmpty: "Mostrando 0 registros",
            infoFiltered: "(filtrado de _MAX_ registros totales)",
            zeroRecords: "No se encontraron registros",
            loadingRecords: "Cargando...",
            processing: "Procesando...",
            paginate: {
                first: "&laquo;",
                last: "&raquo;",
                next: "&rsaquo;",
                previous: "&lsaquo;"
            }
        },
        columns: [
            { data: 'id', orderable: false, className: 'text-center' },
            { 
                data: 'numero_anexo',
                render: function(data, type, row) {
                    var img = row.modelo_img ? `<div class="ms-table-img-wrapper"><img src="${row.modelo_img}"></div>` : `<div class="ms-table-img-wrapper"><i class="fas fa-phone-alt"></i></div>`;
                    return `
                    <div class="d-flex align-items-center">
                        <div class="ms-mr-2">${img}</div>
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
                    var edif = row.edificio_nombre || 'Sin Edificio';
                    var ubi = row.unidad_nombre || '';
                    return `
                    <div>
                        <div class="cell-primary">${edif}</div>
                        ${ubi ? `<div class="cell-secondary">${ubi}</div>` : ''}
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
                render: function(data) {
                    var bg = data === 'Activo' ? '#dff6dd' : '#fde7e9';
                    var color = data === 'Activo' ? '#107c10' : '#a4262c';
                    return `<span style="background:${bg}; color:${color}; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600;">${data}</span>`;
                }
            },
            {
                data: null,
                orderable: false,
                className: 'text-center',
                render: function(data, type, row) {
                    return `
                    <div class="ms-table-actions">
                        <button class="ms-icon-btn ms-icon-btn-view btn-ver-anexo" data-id="${row.id}" title="Ver Anexo">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="ms-icon-btn ms-icon-btn-edit btn-editar-anexo" data-id="${row.id}" title="Editar Anexo">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="ms-icon-btn ms-icon-btn-delete btn-eliminar-anexo" data-id="${row.id}" title="Eliminar Anexo">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>`;
                }
            }
        ]
    });

    // Botón Nuevo Anexo
    $('#btn-nuevo').on('click', function() {
        $('#form-anexo')[0].reset();
        $('#form-anexo').removeClass('was-validated');
        $('#anexo-id').val('');
        $('.select2-drawer').val('').trigger('change.select2');
        $('#anexo-drawer-title').html('<i class="fas fa-phone-alt" ></i> Información Técnica del Equipo');
        $('#a-imagen-preview').attr('src', '/static/img/placeholder_equipo.png');
        
        var ciscoOption = $('#a-marca option').filter(function() { return $(this).text().toUpperCase().includes('CISCO'); }).first();
        if(ciscoOption.length) {
            $('#a-marca').val(ciscoOption.val()).trigger('change.select2');
        }
        
        openAnexoDrawer();
    });

    // Guardar Anexo
    $('#btn-guardar-anexo').on('click', function() {
        if (!$('#form-anexo')[0].checkValidity()) {
            $('#form-anexo').addClass('was-validated');
            return;
        }

        var data = {
            id: $('#anexo-id').val(),
            numero_anexo: $('#a-numero').val(),
            marca: $('#a-marca').val(),
            modelo: $('#a-modelo-anexo option:selected').text(),
            modelo_anexo: $('#a-modelo-anexo').val(),
            edificio: $('#a-edificio').val(),
            piso: $('#a-piso').val(),
            unidad: $('#a-unidad').val(),
            ip: $('#a-ip').val(),
            serial_number: $('#a-serial').val(),
            numero_inventario: $('#a-inventario').val(),
            pma: $('#a-pma').val(),
            estado: $('#a-estado').val(),
            comentario: $('#a-comentario').val()
        };

        var url = '/anexos/api/action/';
        var type = data.id ? 'PUT' : 'POST';

        $.ajax({
            url: url,
            type: type,
            data: JSON.stringify(data),
            contentType: 'application/json'
        }).done(function(r) {
            if (r.success) {
                closeAnexoDrawer();
                Swal.fire({ icon: 'success', title: 'Éxito', text: r.message, confirmButtonColor: '#002a54' });
                tablaAnexos.ajax.reload(null, false);
            } else {
                Swal.fire({ icon: 'error', title: 'Error', text: r.message, confirmButtonColor: '#002a54' });
            }
        }).fail(function(x) {
            Swal.fire({ icon: 'error', title: 'Error', text: x.responseJSON ? x.responseJSON.message : 'Error de conexión.', confirmButtonColor: '#002a54' });
        });
    });

    // Editar Anexo (Debe obtener los datos primero)
    // Ya que la vista de ActionView actual no tiene un GET por ID, usamos los datos de la fila del Datatable para precargar.
    $('#tabla-anexos').on('click', '.btn-editar-anexo', function() {
        var tr = $(this).closest('tr');
        var row = tablaAnexos.row(tr);
        if (tr.hasClass('child')) {
            row = tablaAnexos.row(tr.prev());
        }
        var data = row.data();

        $('#form-anexo')[0].reset();
        $('#form-anexo').removeClass('was-validated');
        
        $('#anexo-id').val(data.id);
        $('#a-numero').val(data.numero_anexo);
        $('#a-marca').val(data.marca).trigger('change.select2');
        $('#a-modelo-anexo').val(data.modelo_anexo_id).trigger('change.select2');        
        var imgUrl = $('#a-modelo-anexo option:selected').data('imagen');
        $('#a-imagen-preview').attr('src', imgUrl || '/static/img/placeholder_equipo.png');
        
        $('#a-edificio').val(data.edificio_id).trigger('change.select2');
        $('#a-piso').val(data.piso_id).trigger('change.select2');
        $('#a-unidad').val(data.unidad_id).trigger('change.select2');
        
        // Find the recinto corresponding to the pma to auto-fill a-recinto
        var pmaOption = $('#a-pma option[value="'+data.pma_id+'"]');
        if (pmaOption.length && pmaOption.data('recinto')) {
            $('#a-recinto').val(pmaOption.data('recinto')).trigger('change.select2');
        } else {
            $('#a-recinto').val('').trigger('change.select2');
        }
        
        $('#a-pma').val(data.pma_id).trigger('change.select2');
        $('#a-ip').val(data.ip);
        $('#a-serial').val(data.serial_number);
        $('#a-inventario').val(data.numero_inventario);
        $('#a-estado').val(data.estado);
        $('#a-comentario').val(data.observacion || data.comentario);

        $('#anexo-drawer-title').html('<i class="fas fa-phone-alt" ></i> Editar Anexo');
        openAnexoDrawer();
    });

    // Ver Anexo - Abre el modal de detalle (split layout, igual al de Equipos)
    $('#tabla-anexos').on('click', '.btn-ver-anexo', function() {
        var tr = $(this).closest('tr');
        var row = tablaAnexos.row(tr);
        if (tr.hasClass('child')) row = tablaAnexos.row(tr.prev());
        var d = row.data();
        if (!d) return;

        // Panel izquierdo
        $('#av-imagen').attr('src', d.modelo_img || '/static/img/placeholder_equipo.png');
        $('#av-numero').text(d.numero_anexo || 'S/N');
        $('#av-modelo-texto').text(d.modelo_anexo_nombre || d.modelo || 'Sin Modelo');
        $('#av-serial-badge').text(d.serial_number || 'S/SERIAL');
        $('#av-estado').text(d.estado || '-');
        $('#av-sysid').text(d.id);

        // Panel derecho - Ubicación
        $('#av-edificio').text(d.edificio_nombre || '-');
        $('#av-piso').text(d.piso_nombre || '-');
        $('#av-unidad').text(d.unidad_nombre || '-');
        // Recinto y PMA no vienen en el datatable, los obtenemos del PMA nombre
        $('#av-recinto').text('-');
        $('#av-pma').text(d.pma_nombre || '-');

        // Especificaciones
        $('#av-marca').text(d.marca || '-');
        $('#av-ip').text(d.ip || 'Sin IP asignada');
        $('#av-comentario').text(d.observacion || d.comentario || 'Sin observaciones');

        $('#modalVerAnexo').modal('show');
    });

    // Eliminar Anexo
    $('#tabla-anexos').on('click', '.btn-eliminar-anexo', function() {
        var id = $(this).data('id');
        Swal.fire({
            title: '¿Estás seguro?',
            text: "No podrás revertir esto. El anexo será eliminado.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/anexos/api/action/',
                    type: 'DELETE',
                    data: JSON.stringify({id: id}),
                    contentType: 'application/json'
                }).done(function(r) {
                    if (r.success) {
                        Swal.fire('Eliminado', r.message, 'success');
                        tablaAnexos.ajax.reload(null, false);
                    } else {
                        Swal.fire('Error', r.message, 'error');
                    }
                });
            }
        });
    });
});

// ==========================================
// DRAWERS
// ==========================================
window.openAnexoDrawer = function() {
    document.getElementById('anexo-drawer').style.right = '0';
    $('#anexo-drawer-overlay').addClass('active');
};
window.closeAnexoDrawer = function() {
    document.getElementById('anexo-drawer').style.right = '-520px';
    $('#anexo-drawer-overlay').removeClass('active');
};
