$(document).ready(function() {
    // --- SIGNATURE PADS ---
    const canvasRec = document.getElementById('canvas-receptor');
    const canvasTic = document.getElementById('canvas-tic');
    
    // Resize canvases to fit container
    function resizeCanvas() {
        const ratio = Math.max(window.devicePixelRatio || 1, 1);
        [canvasRec, canvasTic].forEach(c => {
            if (!c) return;
            const width = c.parentElement.clientWidth;
            // set logical width/height
            c.width = width * ratio;
            c.height = 150 * ratio;
            c.style.width = width + "px";
            c.style.height = "150px";
            c.getContext("2d").scale(ratio, ratio);
        });
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    const sigReceptor = new SignaturePad(canvasRec, { penColor: 'rgb(0, 0, 0)' });
    const sigTic = new SignaturePad(canvasTic, { penColor: 'rgb(0, 0, 0)' });

    sigReceptor.addEventListener("beginStroke", () => { document.getElementById('ph-receptor').style.display = 'none'; });
    sigTic.addEventListener("beginStroke", () => { document.getElementById('ph-tic').style.display = 'none'; });

    $('#clear-signature-receptor').click(function() {
        sigReceptor.clear();
        document.getElementById('ph-receptor').style.display = 'block';
    });
    $('#clear-signature-tic').click(function() {
        sigTic.clear();
        document.getElementById('ph-tic').style.display = 'block';
    });

    // --- DATA TABLES ---
    let itemsSeleccionados = [];

    // Tabla Historial (Server Side)
    const tablaHistorial = $('#tabla-historial-actas').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/actas/api/',
            type: 'POST',
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() || getCookie('csrftoken')}
        },
        columns: [
            { data: 'codigo', render: function(data, type, row) { return '<strong>#'+data+'</strong>'; } },
            { data: 'fecha' },
            { data: 'receptor' },
            { data: 'estado', render: function(d) {
                return `<span class="badge badge-${d==='borrador'?'secondary':'success'}">${d.toUpperCase()}</span>`;
            }},
            { data: 'encargado' },
            { data: null, orderable: false, render: function(data, type, row) {
                if (row.pdf_url) {
                    return `<a href="${row.pdf_url}" target="_blank" class="btn btn-sm btn-danger" title="Ver PDF"><i class="fas fa-file-pdf mr-1"></i> PDF</a>`;
                } else {
                    return `<span class="badge badge-secondary">Sin PDF</span>`;
                }
            }}
        ],
        order: [[1, 'desc']],
        language: { url: "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json" }
    });

    // Datatables para selección en Modal (client side o server side según si existen endpoints)
    // Asumiendo que usamos los endpoints de equipos/api/ y anexos/api/
    const dtBuscarEquipos = $('#dt-buscar-equipos').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/equipos/api/',
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        },
        columns: [
            { data: null, orderable: false, render: function(data, type, row) {
                return `<button type="button" class="btn btn-sm btn-primary btn-add-item" data-tipo="EQUIPO" data-id="${row.id}" data-articulo="${row.articulo}" data-marcamodelo="${row.marca} ${row.modelo}" data-serie="${row.serial_number}"><i class="fas fa-plus"></i> Agregar</button>`;
            }},
            { data: 'articulo' },
            { data: 'marca' },
            { data: 'modelo' },
            { data: 'serial_number' },
            { data: 'estado' }
        ],
        language: { url: "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json" }
    });

    const dtBuscarAnexos = $('#dt-buscar-anexos').DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/anexos/api/',
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')}
        },
        columns: [
            { data: null, orderable: false, render: function(data, type, row) {
                return `<button type="button" class="btn btn-sm btn-primary btn-add-item" data-tipo="ANEXO" data-id="${row.id}" data-articulo="Anexo IP ${row.numero_anexo}" data-marcamodelo="${row.marca} ${row.modelo}" data-serie="${row.serial_number}"><i class="fas fa-plus"></i> Agregar</button>`;
            }},
            { data: 'numero_anexo' },
            { data: 'modelo' },
            { data: 'ip' },
            { data: null, render: function(data, type, row) { return row.pma_nombre || 'N/A'; } },
            { data: 'estado' }
        ],
        language: { url: "//cdn.datatables.net/plug-ins/1.10.21/i18n/Spanish.json" }
    });

    $('#btn-buscar-equipos').click(function() {
        $('#modalInventario').modal('show');
        dtBuscarEquipos.columns.adjust();
        dtBuscarAnexos.columns.adjust();
    });

    // Manejar Agregar Ítem
    $(document).on('click', '.btn-add-item', function() {
        const btn = $(this);
        const item = {
            tipo_item: btn.data('tipo'),
            id_item: btn.data('id'),
            articulo: btn.data('articulo'),
            marcamodelo: btn.data('marcamodelo'),
            serie: btn.data('serie') || 'S/N'
        };
        
        // Evitar duplicados
        if(itemsSeleccionados.find(i => i.tipo_item === item.tipo_item && i.id_item === item.id_item)) {
            Swal.fire('Atención', 'El ítem ya fue agregado.', 'warning');
            return;
        }

        itemsSeleccionados.push(item);
        actualizarTablaSeleccionados();
        
        btn.removeClass('btn-primary').addClass('btn-success').html('<i class="fas fa-check"></i> Agregado');
        setTimeout(() => btn.removeClass('btn-success').addClass('btn-primary').html('<i class="fas fa-plus"></i> Agregar'), 1500);
    });

    function actualizarTablaSeleccionados() {
        const tbody = $('#tabla-items-seleccionados tbody');
        tbody.empty();
        
        if (itemsSeleccionados.length === 0) {
            tbody.append('<tr id="tr-no-items"><td colspan="5" class="text-center text-muted py-4">No se han seleccionado equipos.</td></tr>');
            return;
        }

        itemsSeleccionados.forEach((item, index) => {
            let icon = item.tipo_item === 'EQUIPO' ? 'fa-desktop' : 'fa-phone-alt';
            let tr = `<tr>
                <td>${index + 1}</td>
                <td><i class="fas ${icon} text-muted mr-2"></i><strong>${item.articulo}</strong></td>
                <td>${item.marcamodelo}</td>
                <td style="font-family: monospace;">${item.serie}</td>
                <td class="text-right">
                    <button type="button" class="btn btn-sm btn-danger btn-remove-item" data-index="${index}" title="Quitar equipo"><i class="fas fa-trash-alt"></i></button>
                </td>
            </tr>`;
            tbody.append(tr);
        });
    }

    $(document).on('click', '.btn-remove-item', function() {
        const idx = $(this).data('index');
        itemsSeleccionados.splice(idx, 1);
        actualizarTablaSeleccionados();
    });

    // --- TEXTO DINÁMICO ---
    $('#rec-nombre').on('input', function() { $('#txt-receptor, #txt-receptor2').text($(this).val() || '[RECEPTOR]'); });
    $('#rec-unidad').on('change', function() { $('#txt-unidad').text($(this).val() || '[UNIDAD]'); });

    // --- GENERAR ACTA ---
    $('#btn-generar-acta').click(function() {
        const btn = $(this);
        const originalText = btn.html();

        const nombre = $('#rec-nombre').val().trim();
        const rut = $('#rec-rut').val().trim();
        const unidad = $('#rec-unidad').val();
        
        if (!nombre || !rut || !unidad) {
            Swal.fire('Faltan Datos', 'Debe completar el Nombre, RUT y Unidad del receptor.', 'warning');
            return;
        }
        if (itemsSeleccionados.length === 0) {
            Swal.fire('Sin Equipamiento', 'Debe seleccionar al menos un equipo o insumo.', 'warning');
            return;
        }
        if (sigReceptor.isEmpty() || sigTic.isEmpty()) {
            Swal.fire('Firmas Incompletas', 'Ambas firmas (Receptor y encargado TIC) son obligatorias para generar el acta.', 'warning');
            return;
        }

        const data = {
            receptor_nombre: nombre,
            receptor_rut: rut,
            receptor_unidad: unidad,
            receptor_cargo: $('#rec-cargo').val().trim(),
            email_receptor: $('#rec-correo').val().trim(),
            observaciones: $('#acta-observaciones').val().trim(),
            encargado: $('#encargado-tic').val(),
            detalles: itemsSeleccionados,
            firma_receptor_b64: sigReceptor.toDataURL(),
            firma_tic_b64: sigTic.toDataURL()
        };

        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin mr-2"></i> Generando PDF...');

        $.ajax({
            url: '/actas/api/generate/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function(res) {
                if (res.success) {
                    // Resetear form
                    $('#rec-nombre, #rec-rut, #rec-cargo, #rec-correo, #acta-observaciones').val('');
                    $('#rec-unidad').val('').trigger('change');
                    itemsSeleccionados = [];
                    actualizarTablaSeleccionados();
                    $('#clear-signature-receptor, #clear-signature-tic').click();
                    
                    // Mostrar success y abrir PDF
                    Swal.fire({
                        title: '¡Acta Generada!',
                        text: 'El acta ha sido creada y firmada con éxito.',
                        icon: 'success',
                        confirmButtonText: 'Aceptar'
                    }).then((result) => {
                        if (res.pdf_url) {
                            window.open(res.pdf_url, '_blank');
                        }
                    });
                    tablaHistorial.ajax.reload();
                    $('#historial-tab').tab('show');
                } else {
                    Swal.fire('Error', res.message, 'error');
                }
            },
            error: function(err) {
                Swal.fire('Error del Servidor', 'Ocurrió un error inesperado al generar el acta.', 'error');
                console.error(err);
            },
            complete: function() {
                btn.prop('disabled', false).html(originalText);
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
