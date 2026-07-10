                                                                                                                             /**
 * equipos.js
 * Controlador frontend para el módulo de Inventario de Equipos.
 */

var EquiposApp = (function($) {

    var dtEquipos = null;

    // Elementos DOM
    var el = {
        table: '#tabla-equipos',
        btnNuevo: '#btn-nuevo',
        modal: '#modalEquipo',
        form: '#form-equipo',
        alert: '#equipo-error-alert',
        kpiTotal: '#kpi-total span'
    };

    // Campos del formulario
    var f = {
        id: '#e-id',
        articulo: '#e-articulo',
        marca: '#e-marca',
        modelo: '#e-modelo',
        serial: '#e-serial_number',
        correlativo: '#e-correlativo',
        so: '#e-so',
        ip: '#e-ip',
        piso: '#e-piso',
        unidad: '#e-unidad',
        recinto: '#e-recinto',
        pma: '#e-pma',
        estado: '#e-estado',
        proveedor: '#e-proveedor'
    };

    function csrfToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function initDataTable() {
        dtEquipos = $(el.table).DataTable({
            serverSide: true,
            processing: true,
            ajax: {
                url: '/equipos/api/',
                type: 'POST',
                headers: { 'X-CSRFToken': csrfToken() },
                dataSrc: function(json) {
                    $(el.kpiTotal).text(json.recordsTotal || 0);
                    return json.data;
                }
            },
            language: { url: "https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json" },
            order: [[6, 'desc']], // Por fecha creacion
            columns: [
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-center',
                    render: function(data, type, row, meta) {
                        return '<span style="font-size:0.75rem; color:#64748b;">'+(meta.row + meta.settings._iDisplayStart + 1)+'</span>';
                    }
                },
                { 
                    data: 'articulo',
                    render: function(data, type, row) {
                        var img = row.imagen ? row.imagen : '/static/img/placeholder_equipo.png';
                        var art = data || 'Desconocido';
                        var m = row.marca || 'Genérica';
                        var mod = row.modelo || 'Genérico';
                        return '<div style="display:flex; align-items:center; gap:12px;">' +
                               '<img src="'+img+'" style="width:28px; height:28px; object-fit:contain;">' +
                               '<div>' +
                                 '<span class="cell-title">'+art+'</span>' +
                                 '<span class="cell-subtitle">'+m+' '+mod+'</span>' +
                               '</div></div>';
                    }
                },
                { 
                    data: 'edificio',
                    render: function(data, type, row) {
                        var ed = data || 'SIN EDIFICIO';
                        var u = row.unidad || 'Sin Unidad';
                        return '<span class="cell-title" style="text-transform:uppercase;">'+ed+'</span>' +
                               '<span class="cell-subtitle">'+u+'</span>';
                    }
                },
                { 
                    data: 'pma',
                    render: function(data) {
                        return '<span style="font-size:0.8rem; color:#334155; font-weight:500;">'+(data || 'N/A')+'</span>';
                    }
                },
                { 
                    data: 'piso',
                    className: 'text-center',
                    render: function(data) {
                        return '<span style="font-size:0.8rem; font-weight:600; color:#475569;">'+(data || '-')+'</span>';
                    }
                },
                { 
                    data: 'serial_number',
                    className: 'text-center',
                    render: function(data) {
                        return '<span class="pill-serial">'+(data || 'N/A')+'</span>';
                    }
                },
                { 
                    data: 'ip',
                    className: 'text-center',
                    render: function(data) {
                        return '<span style="font-size:0.75rem; color:#64748b;">'+(data || 'N/A')+'</span>';
                    }
                },
                { 
                    data: 'estado',
                    className: 'text-center',
                    render: function(data, type, row) {
                        return '<span class="pill-estado"><span class="pill-estado status-dot" style="background-color:'+(row.estado_color||'#cbd5e1')+'; padding:0; border:none; width:6px; height:6px;"></span>'+(data || 'S/E')+'</span>';
                    }
                },
                {
                    data: null,
                    orderable: false,
                    searchable: false,
                    className: 'text-right',
                    render: function(data, type, row) {
                        return '<button type="button" class="action-btn-square ic-view mr-1" data-id="'+row.id+'" title="Ver Detalles"><i class="fas fa-eye"></i></button>' +
                               '<button type="button" class="action-btn-square ic-edit mr-1" data-id="'+row.id+'" title="Editar"><i class="fas fa-edit"></i></button>' +
                               '<button type="button" class="action-btn-square ic-delete delete" data-id="'+row.id+'" title="Eliminar"><i class="fas fa-trash-alt"></i></button>';
                    }
                }
            ]
        });
    }

    function initSelect2() {
        if ($.fn.select2) {
            $('.select2').select2({
                theme: 'bootstrap4',
                width: '100%',
                dropdownParent: $(el.modal)
            });
        }
    }

    function initCascades() {
        // Marca -> Modelo
        $(f.marca).on('change', function() {
            var m_id = $(this).val();
            var $mod = $(f.modelo);
            $mod.prop('disabled', !m_id).val('').trigger('change');
            $mod.find('option').each(function() {
                if (!$(this).val() || $(this).data('marca') == m_id) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            });
        });

        // Cascadas de Ubicación (Filtros visuales en el modal)
        function filterRecintosYPmas() {
            var p_id = $(f.piso).val();
            var u_id = $(f.unidad).val();
            var $rec = $(f.recinto);
            
            // Filtro visual rápido: ocultamos opciones que no hagan match
            $rec.val('').trigger('change');
            $rec.find('option').each(function() {
                var v = $(this).val();
                if (!v) return;
                var show = true;
                if (p_id && $(this).data('piso') != p_id) show = false;
                if (u_id && $(this).data('unidad') != u_id) show = false;
                
                if(show) $(this).show(); else $(this).hide();
            });
        }

        function filterPmas() {
            var r_id = $(f.recinto).val();
            var $pma = $(f.pma);
            
            $pma.val('').trigger('change');
            $pma.find('option').each(function() {
                var v = $(this).val();
                if (!v) return;
                if (r_id && $(this).data('recinto') != r_id) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
        }

        $(f.piso).on('change', filterRecintosYPmas);
        $(f.unidad).on('change', filterRecintosYPmas);
        $(f.recinto).on('change', filterPmas);
    }

    function initEvents() {
        $(el.btnNuevo).on('click', function() {
            abrirModal();
        });

        $(el.form).on('submit', function(e) {
            e.preventDefault();
            guardarEquipo();
        });

        // Delegación de clics en la tabla
        $(el.table).on('click', '.ic-view', function(e) {
            e.preventDefault();
            var id = $(this).data('id');
            verEquipoInfo(id);
        });

        $(el.table).on('click', '.ic-edit', function(e) {
            e.preventDefault();
            var id = $(this).data('id');
            cargarEquipo(id);
        });

        $(el.table).on('click', '.ic-delete', function(e) {
            e.preventDefault();
            var id = $(this).data('id');
            if(confirm("¿Seguro que desea eliminar este equipo?")) {
                eliminarEquipo(id);
            }
        });
    }

    function abrirModal() {
        $(el.alert).addClass('d-none').text('');
        $(el.form)[0].reset();
        $(f.id).val('');
        
        // Reset select2
        $('.select2').val('').trigger('change.select2');
        
        // Disable dependientes
        $(f.modelo).prop('disabled', true);
        
        $(el.modal).modal('show');
    }

    function guardarEquipo() {
        var data = {
            id: $(f.id).val() || null,
            articulo_id: $(f.articulo).val(),
            marca_id: $(f.marca).val(),
            modelo_id: $(f.modelo).val(),
            serial_number: $(f.serial).val(),
            correlativo: $(f.correlativo).val(),
            so_id: $(f.so).val(),
            ip: $(f.ip).val(),
            pma_id: $(f.pma).val(),
            estado_id: $(f.estado).val(),
            proveedor_id: $(f.proveedor).val()
        };

        $(el.alert).addClass('d-none');

        $.ajax({
            url: '/equipos/api/action/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': csrfToken() },
            success: function(resp) {
                if(resp.success) {
                    $(el.modal).modal('hide');
                    dtEquipos.ajax.reload(null, false);
                } else {
                    $(el.alert).removeClass('d-none').text(resp.message || 'Error al guardar.');
                }
            },
            error: function(err) {
                var msg = "Error de conexión o validación.";
                if (err.responseJSON && err.responseJSON.message) {
                    msg = err.responseJSON.message;
                }
                $(el.alert).removeClass('d-none').text(msg);
            }
        });
    }

    function cargarEquipo(id) {
        $.ajax({
            url: '/equipos/api/' + id + '/ver/',
            type: 'GET',
            success: function(resp) {
                abrirModal();
                var eq = resp.data;
                
                $(f.id).val(eq.id);
                $(f.serial).val(eq.serial_number);
                $(f.correlativo).val(eq.correlativo);
                $(f.ip).val(eq.ip);
                
                // Set selects y trigger (cuidado con el orden por las cascadas)
                $(f.articulo).val(eq.articulo_id).trigger('change');
                $(f.so).val(eq.so_id).trigger('change');
                $(f.estado).val(eq.estado_id).trigger('change');
                $(f.proveedor).val(eq.proveedor_id).trigger('change');
                
                // Marca -> Modelo
                $(f.marca).val(eq.marca_id).trigger('change');
                setTimeout(function() {
                    $(f.modelo).val(eq.modelo_id).trigger('change');
                }, 100);

                // PMA (no requiere triggerar la cascada si solo lo seteamos)
                $(f.pma).val(eq.pma_id).trigger('change');
                
            },
            error: function() {
                alert("No se pudo cargar la información del equipo.");
            }
        });
    }

    function verEquipoInfo(id) {
        $.ajax({
            url: '/equipos/api/' + id + '/ver/',
            type: 'GET',
            success: function(resp) {
                var eq = resp.data;
                
                // Imagen y Resumen
                $('#v-imagen').attr('src', eq.imagen || '/static/img/placeholder_equipo.png');
                $('#v-articulo').text(eq.articulo || 'Sin Especificar');
                $('#v-serial').text(eq.serial_number || 'N/A');
                $('#v-estado').text(eq.estado || 'S/E');
                
                // Ubicación
                $('#v-edificio').text(eq.edificio || '-');
                $('#v-piso').text(eq.piso || '-');
                $('#v-unidad').text(eq.unidad || '-');
                $('#v-pma').text(eq.pma || '-');
                
                // Especificaciones
                var mrk = eq.marca || 'Genérica';
                var mod = eq.modelo || 'Genérico';
                $('#v-marca-modelo').text(mrk + ' ' + mod);
                $('#v-ip').text(eq.ip || 'Sin IP');
                $('#v-so').text(eq.so || 'N/A');
                $('#v-proveedor').text(eq.proveedor || 'Sin Proveedor');
                
                // Auditoria
                $('#v-sysid').text(eq.id);
                // Si la BD retorna un updated_at se puede poner aqui.
                $('#v-fecha').text('Actualizado recientemente');
                
                $('#modalVerEquipo').modal('show');
            },
            error: function() {
                alert("Error al cargar los detalles.");
            }
        });
    }

    function eliminarEquipo(id) {
        $.ajax({
            url: '/equipos/api/action/',
            type: 'POST',
            data: JSON.stringify({ action: 'delete', id: id }),
            contentType: 'application/json',
            headers: { 'X-CSRFToken': csrfToken() },
            success: function(resp) {
                if(resp.success) {
                    dtEquipos.ajax.reload(null, false);
                } else {
                    alert(resp.message);
                }
            },
            error: function() {
                alert("Error al intentar eliminar.");
            }
        });
    }

    // Constructor/Init
    return {
        init: function() {
            initSelect2();
            initCascades();
            initDataTable();
            initEvents();
        }
    };

})(jQuery);

$(document).ready(function() {
    EquiposApp.init();
});
