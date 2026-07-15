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
    $('.select2-modal').select2({
        dropdownParent: $('#modalAnexo'),
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

    // Lógica para filtrar ModeloAnexo según Marca
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

    // Inicializar DataTable
    var tablaAnexos = $('#tabla-anexos').DataTable({
        serverSide: true,
        processing: true,
        responsive: true,
        ajax: {
            url: '/anexos/api/',
            type: 'POST',
            error: function (xhr, error, code) {
                console.error("Error al cargar Anexos:", error);
            }
        },
        language: {
            url: "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json",
            search: "_INPUT_",
            searchPlaceholder: "Buscar..."
        },
        dom: '<"top">rt<"bottom"ilp><"clear">',
        columns: [
            { data: 'id', orderable: false, className: 'text-center' },
            { 
                data: 'numero_anexo',
                render: function(data, type, row) {
                    var img = row.modelo_img ? `<img src="${row.modelo_img}" style="width:100%; object-fit:contain;">` : `<i class="fas fa-phone-alt fa-lg"></i>`;
                    return `
                    <div class="d-flex align-items-center">
                        <div class="icon-square">${img}</div>
                        <div>
                            <div class="cell-primary">${data || 'S/N'}</div>
                            <div class="cell-secondary">ID: ${row.id}</div>
                        </div>
                    </div>`;
                }
            },
            { 
                data: 'modelo',
                render: function(data, type, row) {
                    var mod = row.modelo_anexo_nombre || row.modelo || 'Sin Modelo';
                    return `
                    <div>
                        <div class="cell-primary">${mod}</div>
                        <div class="cell-secondary"><i class="fas fa-barcode mr-1"></i>${row.serial_number || 'S/N'}</div>
                    </div>`;
                }
            },
            { 
                data: 'ubicacion',
                render: function(data, type, row) {
                    var ubi = row.unidad_nombre || row.pma_lugar || 'Sin Unidad';
                    var edif = [];
                    if (row.edificio_nombre) edif.push(row.edificio_nombre);
                    if (row.piso_nombre) edif.push(row.piso_nombre);
                    var edif_str = edif.length > 0 ? edif.join(' - ') : 'S/U';
                    
                    return `
                    <div>
                        <div class="cell-primary">${ubi}</div>
                        <div class="cell-secondary"><i class="fas fa-hospital mr-1"></i>${edif_str}</div>
                    </div>`;
                }
            },
            { 
                data: 'ip',
                render: function(data, type, row) {
                    var st = row.estado === 'Activo' 
                        ? `<span class="status-badge status-activo"><i class="fas fa-check-circle mr-1"></i>Activo</span>`
                        : `<span class="status-badge status-inactivo"><i class="fas fa-times-circle mr-1"></i>Inactivo</span>`;
                    var ip_str = row.ip ? `<i class="fas fa-network-wired mr-1"></i>${row.ip}` : '<i class="fas fa-network-wired mr-1"></i>S/IP';
                    return `
                    <div>
                        <div class="mb-1">${st}</div>
                        <div class="cell-secondary">${ip_str}</div>
                    </div>`;
                }
            },
            {
                data: null,
                orderable: false,
                searchable: false,
                className: 'text-right',
                render: function(data, type, row) {
                    return `
                        <button class="action-btn-square text-primary btn-ver-anexo" data-id="${row.id}" title="Ver Anexo">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn-square text-success btn-editar-anexo" data-id="${row.id}" title="Editar Anexo">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn-square text-danger btn-eliminar-anexo" data-id="${row.id}" title="Eliminar Anexo">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    `;
                }
            }
        ]
    });

    // Custom Search
    $('#custom-search-input').on('keyup', function() {
        tablaAnexos.search(this.value).draw();
    });

    // Botón Nuevo Anexo
    $('#btn-nuevo').on('click', function() {
        $('#form-anexo')[0].reset();
        $('#form-anexo').removeClass('was-validated');
        $('#anexo-id').val('');
        $('.select2-modal').val('').trigger('change.select2');
        $('#modalAnexoLabel').text('Información Técnica del Equipo');
        
        var ciscoOption = $('#a-marca option').filter(function() { return $(this).text().toUpperCase().includes('CISCO'); }).first();
        if(ciscoOption.length) {
            $('#a-marca').val(ciscoOption.val()).trigger('change.select2');
        }
        
        $('#modalAnexo').modal('show');
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
            modelo_anexo: $('#a-modelo-anexo').val(),
            edificio: $('#a-edificio').val(),
            piso: $('#a-piso').val(),
            unidad: $('#a-unidad').val(),
            ip: $('#a-ip').val(),
            serial_number: $('#a-serial').val(),
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
                $('#modalAnexo').modal('hide');
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
        $('#a-estado').val(data.estado);
        $('#a-comentario').val(data.observacion || data.comentario);

        $('#modalAnexoLabel').text('Editar Anexo');
        $('#modalAnexo').modal('show');
    });

    // Ver Anexo (Read Only)
    $('#tabla-anexos').on('click', '.btn-ver-anexo', function() {
        Swal.fire({ icon: 'info', title: 'Funcionalidad en desarrollo', text: 'Vista detallada de anexo.'});
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
