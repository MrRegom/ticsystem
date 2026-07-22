$(document).ready(function() {

    
    // --- RUT FORMATTER & VALIDATOR ---
    function formatRut(rut) {
        let value = rut.replace(/[^0-9kK]/g, '').toUpperCase();
        if (value.length > 1) {
            value = value.slice(0, -1) + '-' + value.slice(-1);
        }
        return value;
    }
    
    function isValidRut(rut) {
        if (!/^[0-9]+-[0-9kK]{1}$/.test(rut)) return false;
        let t = parseInt(rut.split('-')[0], 10);
        let m = 0, s = 1;
        while (t > 0) {
            s = (s + t % 10 * (9 - m++ % 6)) % 11;
            t = Math.floor(t / 10);
        }
        let v = (s > 0) ? (s - 1) + '' : 'K';
        return (v === rut.split('-')[1].toUpperCase());
    }
    
    $('#rec-rut, #rut_nuevo').on('input', function() {
        let formatted = formatRut($(this).val());
        $(this).val(formatted);
        
        if (formatted.length > 7) {
            if (isValidRut(formatted)) {
                $(this).removeClass('is-invalid').addClass('is-valid');
            } else {
                $(this).removeClass('is-valid').addClass('is-invalid');
            }
        } else {
            $(this).removeClass('is-valid is-invalid');
        }
    });

    
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
                let html = '<div class="ms-row-actions" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:8px; justify-content:center; align-items:center; margin-top:2px;">';
                if (row.pdf_url) {
                    html += `<a href="${row.pdf_url}" target="_blank" class="ms-icon-btn" style="width:26px; height:26px; font-size:13px; display:inline-flex; align-items:center; justify-content:center; text-decoration:none; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#0078d4'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';" title="Ver PDF"><i class="fas fa-file-pdf"></i></a>`;
                } else {
                    html += `<span class="badge badge-secondary">Sin PDF</span>`;
                }
                html += `<button type="button" class="ms-icon-btn btn-delete-acta" data-id="${row.id}" style="width:26px; height:26px; font-size:13px; color:#8a8886; transition:0.2s;" onmouseover="this.style.color='#dc3545'; this.style.background='#f3f2f1';" onmouseout="this.style.color='#8a8886'; this.style.background='transparent';" title="Eliminar Acta"><i class="fas fa-trash"></i></button>`;
                html += '</div>';
                return html;
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
                return `<button type="button" class="btn ms-btn-primary btn-sm btn-add-item" style="text-decoration: none !important;" data-tipo="EQUIPO" data-id="${row.id}" data-articulo="${row.articulo}" data-marcamodelo="${row.marca} ${row.modelo}" data-serie="${row.serial_number}">Agregar</button>`;
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
                return `<button type="button" class="btn ms-btn-primary btn-sm btn-add-item" style="text-decoration: none !important;" data-tipo="ANEXO" data-id="${row.id}" data-articulo="Anexo IP ${row.numero_anexo}" data-marcamodelo="${row.marca} ${row.modelo}" data-serie="${row.serial_number}">Agregar</button>`;
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
        
        btn.removeClass('ms-btn-primary').addClass('btn-success').html('Agregado');
        setTimeout(() => btn.removeClass('btn-success').addClass('ms-btn-primary').html('Agregar'), 1500);
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

    
    // --- AUTORRELLENO POR RUT ---
    let typingTimer;
    $('#rec-rut').on('keyup', function() {
        clearTimeout(typingTimer);
        const rut = $(this).val().trim();
        if (rut.length > 7) {
            typingTimer = setTimeout(function() {
                $('#rut-spinner').removeClass('d-none');
                $('#btn-add-user').addClass('d-none');
                $.ajax({
                    url: '/tickets/api/search/users/?q=' + rut,
                    type: 'GET',
                    success: function(resp) {
                        $('#rut-spinner').addClass('d-none');
                        if (resp.results && resp.results.length > 0) {
                            const user = resp.results[0];
                            $('#rec-nombres').val(user.nombres || '');
                            $('#rec-apellidos').val(user.apellidos || '');
                            $('#rec-correo').val(user.correo || '');
                            $('#rec-cargo').val(user.cargo || '').trigger('change');
                            $('#rec-unidad').val(user.unidad || '').trigger('change');
                            // Habilitar campos si hay usuario
                            $('#rec-unidad, #rec-cargo').prop('disabled', false);
                            $('#rec-nombres, #rec-apellidos').trigger('input');
                        } else {
                            // No encontrado -> obligar a agregar
                            $('#rec-nombres, #rec-apellidos').val('');
                            $('#rec-unidad, #rec-cargo').prop('disabled', true);
                            $('#rec-nombres, #rec-apellidos').trigger('input');
                            $('#btn-add-user').removeClass('d-none');
                        }
                    },
                    error: function() {
                        $('#rut-spinner').addClass('d-none');
                    }
                });
            }, 800);
        } else {
            $('#rec-nombres, #rec-apellidos').val('');
            $('#btn-add-user').addClass('d-none');
            $('#rec-unidad, #rec-cargo').prop('disabled', true);
        }
    });
    
    $('#btn-add-user').click(function() {
        $('#rut_nuevo').val($('#rec-rut').val());
        $('#nombres_nuevo, #apellidos_nuevo, #correo_nuevo').val('');
        $('#modalCrearUsuario').modal('show');
    });
    
    $('#form-crear-usuario').submit(function(e) {
        e.preventDefault();
        const btn = $('#btn-submit-usuario');
        btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Guardando...');
        
        const data = {
            rut: $('#rut_nuevo').val(),
            nombres: $('#nombres_nuevo').val(),
            apellidos: $('#apellidos_nuevo').val(),
            correo: $('#correo_nuevo').val(),
            cargo: $('#cargo_nuevo').val(),
            unidad: $('#unidad_nueva').val()
        };
        
        $.ajax({
            url: '/tickets/api/search/users/create/',
            type: 'POST',
            contentType: 'application/json',
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() || window.TICKET_CONFIG?.csrfToken || '' },
            data: JSON.stringify(data),
            success: function(res) {
                btn.prop('disabled', false).html('<i class="fas fa-save"></i> Guardar Funcionario');
                if (res.success) {
                    $('#modalCrearUsuario').modal('hide');
                    $('#rec-rut').val(res.user.rut);
                    $('#rec-nombres').val(res.user.nombres);
                    $('#rec-apellidos').val(res.user.apellidos);
                    $('#rec-correo').val(res.user.correo || '');
                      $('#rec-unidad').val(res.user.unidad || '').trigger('change');
                      $('#rec-cargo').val(res.user.cargo || '').trigger('change');
                      $('#rec-unidad, #rec-cargo').prop('disabled', false);
                    $('#btn-add-user').addClass('d-none');
                    $('#rec-nombres, #rec-apellidos').trigger('input');
                    Swal.fire('Éxito', 'Funcionario registrado correctamente', 'success');
                } else {
                    Swal.fire('Error', res.message || 'Error al guardar', 'error');
                }
            },
            error: function(err) {
                btn.prop('disabled', false).html('<i class="fas fa-save"></i> Guardar Funcionario');
                Swal.fire('Error', 'Error de conexión', 'error');
            }
        });
    });

    // --- TEXTO DINÁMICO ---
    $('#rec-nombres, #rec-apellidos').on('input', function() { const n = $('#rec-nombres').val() || ''; const a = $('#rec-apellidos').val() || ''; const full = (n + ' ' + a).trim(); $('#txt-receptor, #txt-receptor2').text(full || '[RECEPTOR]'); });
    $('#rec-unidad').on('change', function() { $('#txt-unidad').text($(this).val() || '[UNIDAD]'); });

    // --- GENERAR ACTA ---
    $('#btn-generar-acta').click(function() {
        const btn = $(this);
        const originalText = btn.html();

        const nombres = $('#rec-nombres').val().trim();
        const apellidos = $('#rec-apellidos').val().trim();
        const nombre = (nombres + ' ' + apellidos).trim();
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
                    $('#rec-nombres, #rec-apellidos, #rec-rut, #rec-cargo, #rec-correo, #acta-observaciones').val('');
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
});