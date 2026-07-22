                                                                                                                             /**
 * equipos.js
 * Controlador frontend para el módulo de Inventario de Equipos.
 * Refactorizado a Microsoft Fluent Design (ms-list) — v40
 */

// ============================================================
// MOTOR MS-LIST (paginación client-side sobre respuesta del API)
// ============================================================
var EqState = {
    data: [],           // Todos los registros cargados
    filtered: [],       // Filtrados por búsqueda/estado/unidad
    page: 1,
    pageSize: 20,
    currentEquipoId: null
};

function eqShowToast(msg, isError) {
    var icon = document.getElementById('ms-toast-icon');
    var text = document.getElementById('ms-toast-text');
    var toast = document.getElementById('ms-toast');
    
    if (window.toastTimeout) clearTimeout(window.toastTimeout);
    
    icon.className = isError ? 'fas fa-exclamation-triangle ms-toast-icon' : 'fas fa-check-circle ms-toast-icon';
    icon.style.color = isError ? '#a4262c' : '#107c10';
    if (isError) toast.classList.add('error'); else toast.classList.remove('error');
    
    text.textContent = msg;
    
    toast.classList.remove('show');
    void toast.offsetWidth; // Force reflow to restart animation
    toast.classList.add('show');
    
    window.toastTimeout = setTimeout(function() { toast.classList.remove('show'); }, 3500);
}

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

function eqAvatarColor(seed) {
    var colors = ['#0078d4','#d13438','#107c10','#881798','#038387','#498205','#c19c00'];
    var hash = 0;
    for (var i = 0; i < seed.length; i++) hash = seed.charCodeAt(i) + ((hash << 5) - hash);
    return colors[Math.abs(hash) % colors.length];
}

function eqRenderRows() {
    var rows = EqState.data;
    var body = document.getElementById('eq-list-body');
    if (!body) return;
    if (rows.length === 0) {
        body.innerHTML = '<div style="text-align:center;padding:48px;color:#605e5c;font-size:14px;"><i class="fas fa-box-open" style="font-size:32px;color:#edebe9;display:block;margin-bottom:12px;"></i>No se encontraron equipos con los filtros aplicados.</div>';
        document.getElementById('eq-info').textContent = '';
        document.getElementById('eq-pagination').innerHTML = '';
        return;
    }
    var html = '';
    rows.forEach(function(eq) {
        var img = eq.imagen ? eq.imagen : '/static/img/placeholder_equipo.png';
        var articulo = eq.articulo || 'Desconocido';
        var marca = eq.marca || '';
        var modelo = eq.modelo || '';
        var color = eq.estado_color || '#edebe9';
        var edificio = eq.edificio ? eq.edificio : 'Sin Edificio';
        var unidad = eq.unidad || 'Sin Unidad';
        var pma = eq.pma || '-';
        var piso = eq.piso || '-';
        var estado = eq.estado || 'S/E';
        var inv = eq.num_inventario || '-';
        var serial = eq.serial_number || 'N/A';
        var ip = eq.ip || 'N/A';
        html += '<div class="ms-list-row" onclick="eqOpenView(' + eq.id + ')" style="grid-template-columns: 200px 1fr 120px 70px 120px 120px 110px 110px 100px; font-size: 11px;">';
        
        // Col 1: Artículo / Modelo
        html += '<div class="ms-identity">';
        html += '  <img src="' + img + '" style="width:24px;height:24px;object-fit:contain;flex-shrink:0;background:#f3f2f1;padding:2px;">';
        html += '  <div class="ms-user-info">';
        html += '    <span class="ms-user-name" style="font-size: 11px;">' + articulo + '</span>';
        html += '    <span class="ms-user-email" style="color:#605e5c; font-size: 10px;">' + marca + ' ' + modelo + '</span>';
        html += '  </div>';
        html += '</div>';
        
        // Col 2: Ubicación
        html += '<div style="min-width:0;"><div class="ms-user-name" style="font-size:11px;">' + edificio + '</div><div class="ms-user-email" style="font-size:10px;">' + unidad + '</div></div>';
        
        // Col 3: PMA
        html += '<div style="font-size:11px;color:#323130;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + pma + '</div>';
        
        // Col 4: Piso
        html += '<div style="font-size:11px;color:#323130;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + piso + '</div>';
        
        // Col 5: N° Inventario
        html += '<div style="font-size:11px;color:#107c10;font-weight:600;font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + inv + '</div>';
        
        // Col 6: N° Serie
        html += '<div style="font-size:11px;color:#0078d4;font-weight:600;font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + serial + '</div>';
        
        // Col 7: IP / Red
        html += '<div style="font-size:11px;color:#323130;font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">' + ip + '</div>';
        
        // Col 8: Estado
        html += '<div><span class="ms-status"><span class="ms-status-dot" style="background:' + color + ';"></span><span style="font-size:11px;">' + estado + '</span></span></div>';
        
        // Col 9: Acciones
        html += '<div class="ms-row-actions" onclick="event.stopPropagation();" style="position:static; opacity:1; background:transparent; padding:0; display:flex; gap:6px; justify-content:center; align-items:center; width:100%; height:100%; transform:none !important;">';
        html += '  <button class="ms-icon-btn" style="width:26px; height:26px; font-size: 12px;" title="Ver Detalle" onclick="eqOpenView(' + eq.id + ')"><i class="fas fa-eye"></i></button>';
        html += '  <button class="ms-icon-btn" style="width:26px; height:26px; font-size: 12px;" title="Bitácora" onclick="eqOpenBitacora(' + eq.id + ',\'' + serial + '\')" ><i class="fas fa-history"></i></button>';
        html += '  <button class="ms-icon-btn" style="width:26px; height:26px; font-size: 12px;" title="Editar" onclick="eqEdit(' + eq.id + ')" ><i class="fas fa-edit"></i></button>';
        html += '</div>';
        
        html += '</div>';
    });
    body.innerHTML = html;
    
    // Info
    var total = EqState.totalRecords || 0;
    var start = (EqState.page - 1) * EqState.pageSize;
    var from = total > 0 ? start + 1 : 0;
    var to = Math.min(start + EqState.pageSize, total);
    document.getElementById('eq-info').textContent = 'Mostrando ' + from + '-' + to + ' de ' + total + ' equipos';
    
    // Paginación Windowed
    var pages = Math.ceil(total / EqState.pageSize);
    var pag = document.getElementById('eq-pagination');
    var ph = '';
    
    if (pages > 1) {
        ph += '<button onclick="eqGoPage(1)" style="width:28px;height:28px;border:1px solid #edebe9;background:white;font-size:12px;cursor:pointer;" title="Primera">&laquo;</button>';
        ph += '<button onclick="eqGoPage(' + Math.max(1, EqState.page - 1) + ')" style="width:28px;height:28px;border:1px solid #edebe9;background:white;font-size:12px;cursor:pointer;margin-right:8px;" title="Anterior">&lsaquo;</button>';
        
        var startPage = Math.max(1, EqState.page - 2);
        var endPage = Math.min(pages, EqState.page + 2);
        
        for (var p = startPage; p <= endPage; p++) {
            var active = (p === EqState.page) ? 'background:#0078d4;color:white;border-color:#0078d4;' : '';
            ph += '<button onclick="eqGoPage(' + p + ')" style="width:28px;height:28px;border:1px solid #edebe9;background:white;font-size:12px;cursor:pointer;' + active + '">' + p + '</button>';
        }
        
        ph += '<button onclick="eqGoPage(' + Math.min(pages, EqState.page + 1) + ')" style="width:28px;height:28px;border:1px solid #edebe9;background:white;font-size:12px;cursor:pointer;margin-left:8px;" title="Siguiente">&rsaquo;</button>';
        ph += '<button onclick="eqGoPage(' + pages + ')" style="width:28px;height:28px;border:1px solid #edebe9;background:white;font-size:12px;cursor:pointer;" title="Última">&raquo;</button>';
    }
    pag.innerHTML = ph;
}

function eqGoPage(p) { 
    if (EqState.page !== p) {
        EqState.page = p; 
        eqLoadList(); // Fetch nueva página al servidor
    }
}

function eqApplyFilters() {
    EqState.page = 1; // Reiniciar a la página 1 cuando cambia algún filtro
    eqLoadList();
}

function eqLoadList() {
    var q = (document.getElementById('eq-search').value || '').toLowerCase();
    var estado = (document.getElementById('eq-filter-estado').value || '');
    var unidad = (document.getElementById('eq-filter-unidad').value || '');
    var start = (EqState.page - 1) * EqState.pageSize;

    $.ajax({
        url: '/equipos/api/',
        type: 'POST',
        headers: { 'X-CSRFToken': csrfToken() },
        data: {
            'draw': 1,
            'start': start,
            'length': EqState.pageSize,
            'search[value]': q,
            'estado': estado,
            'unidad': unidad,
            'order[0][column]': 0,
            'order[0][dir]': 'desc',
            'columns[0][data]': 'id',
            'columns[0][name]': '',
            'columns[0][searchable]': 'false',
            'columns[0][orderable]': 'true',
            'columns[1][data]': 'articulo',
            'columns[1][name]': '',
            'columns[1][searchable]': 'true',
            'columns[1][orderable]': 'true',
            'columns[2][data]': 'edificio',
            'columns[2][name]': '',
            'columns[2][searchable]': 'true',
            'columns[2][orderable]': 'true',
            'columns[3][data]': 'pma',
            'columns[3][name]': '',
            'columns[3][searchable]': 'true',
            'columns[3][orderable]': 'false',
            'columns[4][data]': 'piso',
            'columns[4][name]': '',
            'columns[4][searchable]': 'true',
            'columns[4][orderable]': 'false',
            'columns[5][data]': 'serial_number',
            'columns[5][name]': '',
            'columns[5][searchable]': 'true',
            'columns[5][orderable]': 'false',
            'columns[6][data]': 'ip',
            'columns[6][name]': '',
            'columns[6][searchable]': 'true',
            'columns[6][orderable]': 'false',
            'columns[7][data]': 'estado',
            'columns[7][name]': '',
            'columns[7][searchable]': 'true',
            'columns[7][orderable]': 'false'
        },
        success: function(resp) {
            EqState.data = resp.data || [];
            EqState.filtered = EqState.data; // Para compatibilidad con Optimistic UI
            EqState.totalRecords = resp.recordsFiltered || 0;
            
            // Actualizar KPIs si el backend los envía
            if (resp.kpi) {
                var eTotal = document.getElementById('kpi-total');
                var eOp = document.getElementById('kpi-operativos');
                var eSop = document.getElementById('kpi-soporte');
                var eAle = document.getElementById('kpi-alertas');
                if (eTotal) eTotal.textContent = resp.kpi.total;
                if (eOp) eOp.textContent = resp.kpi.operativos;
                if (eSop) eSop.textContent = resp.kpi.soporte;
                if (eAle) eAle.textContent = resp.kpi.alertas;
            }

            eqRenderRows();
        },
        error: function(xhr, status, err) {
            console.error('Error cargando inventario:', status, err, xhr.responseText);
            document.getElementById('eq-list-body').innerHTML = '<div style="text-align:center;padding:32px;color:#a4262c;"><i class="fas fa-exclamation- tectonic-triangle"></i> Error al cargar el inventario. Revisa la consola.</div>';
        }
    });
}

// ============================================================
// DRAWER (Registrar / Editar)
// ============================================================
function eqOpenDrawer() {
    document.getElementById('equipo-drawer').style.right = '0';
    document.getElementById('equipo-drawer-overlay').classList.add('active');
}
function eqCloseDrawer() {
    document.getElementById('equipo-drawer').style.right = '-520px';
    document.getElementById('equipo-drawer-overlay').classList.remove('active');
}

// ============================================================
// MODAL VISTA (Contact Card)
// ============================================================
function eqOpenView(id) {
    EqState.currentEquipoId = id;
    
    // Carga "Optimista": usar datos ya disponibles en memoria para abrir de inmediato
    var eqList = EqState.filtered.find(function(e) { return e.id === id; });
    if (eqList) {
        document.getElementById('ev-imagen').src = eqList.imagen || '/static/img/placeholder_equipo.png';
        document.getElementById('ev-articulo').textContent = eqList.articulo || '-';
        document.getElementById('ev-marca-modelo').textContent = (eqList.marca || '') + ' ' + (eqList.modelo || '');
        var badge = document.getElementById('ev-estado-badge');
        badge.textContent = eqList.estado || '-';
        badge.style.background = eqList.estado_color ? eqList.estado_color + '22' : '#dff6dd';
        badge.style.color = eqList.estado_color || '#107c10';
        document.getElementById('ev-serial').textContent = eqList.serial_number || 'N/A';
        document.getElementById('ev-so').textContent = eqList.so || 'Cargando...';
        document.getElementById('ev-ip').textContent = eqList.ip || 'N/A';
        document.getElementById('ev-proveedor').textContent = 'Cargando...';
        document.getElementById('ev-edificio').textContent = eqList.edificio || 'N/A';
        document.getElementById('ev-unidad').textContent = eqList.unidad || 'N/A';
        document.getElementById('ev-recinto').textContent = 'Cargando...';
        document.getElementById('ev-pma').textContent = eqList.pma || 'N/A';
    }

    // Mostrar el modal INMEDIATAMENTE al hacer click (Cero delay para el usuario)
    document.getElementById('eq-view-overlay').classList.add('active');

    // Cargar detalles completos silenciosamente en segundo plano
    $.ajax({
        url: '/equipos/api/' + id + '/ver/',
        type: 'GET',
        success: function(resp) {
            var eq = resp.data;
            document.getElementById('ev-imagen').src = eq.imagen || '/static/img/placeholder_equipo.png';
            document.getElementById('ev-articulo').textContent = eq.articulo || '-';
            document.getElementById('ev-marca-modelo').textContent = (eq.marca || '') + ' ' + (eq.modelo || '');
            var badge = document.getElementById('ev-estado-badge');
            badge.textContent = eq.estado || '-';
            badge.style.background = eq.estado_color ? eq.estado_color + '22' : '#dff6dd';
            badge.style.color = eq.estado_color || '#107c10';
            document.getElementById('ev-serial').textContent = eq.serial_number || 'N/A';
            document.getElementById('ev-so').textContent = eq.so || 'N/A';
            document.getElementById('ev-ip').textContent = eq.ip || 'N/A';
            document.getElementById('ev-proveedor').textContent = eq.proveedor || 'N/A';
            document.getElementById('ev-edificio').textContent = eq.edificio || 'N/A';
            document.getElementById('ev-unidad').textContent = eq.unidad || 'N/A';
            document.getElementById('ev-recinto').textContent = eq.recinto || 'N/A';
            document.getElementById('ev-pma').textContent = eq.pma || 'N/A';
        }
    });
}
function eqCloseView() { document.getElementById('eq-view-overlay').classList.remove('active'); }

// ============================================================
// MODAL BITÁCORA
// ============================================================
function eqOpenBitacora(id, serial) {
    EqState.currentEquipoId = id;
    
    // Limpiar formulario y resetear selects antes de llenarlos
    $('#form-bitacora')[0].reset();
    $('#b-falla, #b-unidad, #b-solicitante').val(null).trigger('change');
    
    document.getElementById('b-equipo-sn-header').textContent = serial || '';
    document.getElementById('b-equipo-id').value = id;
    document.getElementById('eq-bitacora-overlay').classList.add('active');
    
    // Autocompletar Fecha Ingreso con la fecha/hora actual
    var now = new Date();
    var pad = function(n) { return n < 10 ? '0' + n : n; };
    var nowStr = now.getFullYear() + '-' + pad(now.getMonth()+1) + '-' + pad(now.getDate()) + 'T' + pad(now.getHours()) + ':' + pad(now.getMinutes());
    document.getElementById('b-fecha-mtto').value = nowStr;

    // Obtener datos del equipo para pre-seleccionar la Unidad
    $.ajax({
        url: '/equipos/api/' + id + '/ver/',
        type: 'GET',
        success: function(resp) {
            if (resp.success && resp.data.unidad) {
                var val = resp.data.unidad;
                var $sel = $('#b-unidad');
                
                // Intentar seleccionar por value directo
                $sel.val(val);
                
                // Si falló por diferencias de espacios, usar filter y extraer el value real
                if (!$sel.val()) {
                    var exactVal = $sel.find('option').filter(function() {
                        return $(this).text().trim().toLowerCase() === val.trim().toLowerCase();
                    }).attr('value');
                    
                    if (exactVal) {
                        $sel.val(exactVal);
                    }
                }
                
                // IMPORTANTE: Forzar actualización de UI para Select2 y DOM
                $sel.trigger('change').trigger('change.select2');
            }
        }
    });

    cargarBitacora(id);
}
function eqCloseBitacora() { document.getElementById('eq-bitacora-overlay').classList.remove('active'); }

function eqEdit(id) {
    eqCloseView();
    cargarEquipo(id);
}

function eqGuardar() {
    var form = document.getElementById('form-equipo');
    
    // Los Select2 ocultan el <select> original. Si es required y está vacío,
    // HTML5 reportValidity() falla silenciosamente sin mostrar el tooltip.
    var missingFieldNames = [];
    
    $(form).find('select[required], input[required]').each(function() {
        if (!$(this).val()) {
            var label = $(this).closest('.ms-form-group').find('.ms-label').text().replace('*', '').trim();
            if (!label) label = $(this).attr('placeholder') || 'Campo sin nombre';
            if (!missingFieldNames.includes(label)) missingFieldNames.push(label);
        }
    });
    
    // Validar también los radios de estado
    if ($('input[name="e-estado"]:checked').length === 0) {
        missingFieldNames.push('Disponibilidad');
    }
    
    evaluarBordesObligatorios();

    if (missingFieldNames.length > 0) {
        var alertEl = document.getElementById('equipo-error-alert');
        if (alertEl) {
            alertEl.style.display = 'block';
            alertEl.textContent = 'Faltan campos obligatorios: ' + missingFieldNames.join(', ');
        }
        return; // Detenemos aquí para evitar el fallo silencioso
    }

    if (form.reportValidity()) {
        $(form).trigger('submit');
    }
}

var EquiposApp = (function($) {

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
        area: '#e-area',
        unidad: '#e-unidad',
        piso: '#e-piso',
        sector: '#e-sector',
        recinto: '#e-recinto',
        pma: '#e-pma',
        estado: '#e-estado',
        proveedor: '#e-proveedor'
    };

    // Elementos UI principales
    var el = {
        modal: '#equipo-drawer',
        alert: '#equipo-error-alert'
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

    // initDataTable reemplazado por eqLoadList() (motor ms-list)

    function initSelect2() {
        if ($.fn.select2) {
            // Selects del Drawer de Equipo
            $('#equipo-drawer .select2-eq').select2({
                theme: 'bootstrap4',
                width: '100%',
                dropdownParent: $('#equipo-drawer')
            });
            
            // Selects del Modal de Bitácora
            $('#eq-bitacora-overlay .select2-bitacora').select2({
                theme: 'bootstrap4',
                width: '100%'
            });
            
            // Select2 AJAX para Funcionario (Solicitante) en Bitácora
            $('#b-solicitante').select2({
                theme: 'bootstrap4',
                dropdownParent: $('body'),
                placeholder: '-- Buscar por RUT o Nombre --',
                allowClear: true,
                width: '100%',
                ajax: {
                    url: '/api/funcionarios/search/',
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return { q: params.term };
                    },
                    processResults: function (data) {
                        return { results: data.results };
                    },
                    cache: true
                },
                minimumInputLength: 2,
                placeholder: '-- Buscar por RUT o Nombre --',
                allowClear: true,
                language: {
                    noResults: function() {
                        return '<div style="padding:10px; text-align:center;">' +
                            '<div style="color:#64748b; font-size:0.85rem; margin-bottom:8px;">No se encontraron resultados</div>' +
                            '<button type="button" class="btn btn-sm btn-primary btn-add-funcionario-inline">' +
                            '<i class="fas fa-plus"></i> Registrar Nuevo Funcionario</button>' +
                            '</div>';
                    },
                    inputTooShort: function() { return 'Escribe 2 o más caracteres...'; },
                    searching: function() { return 'Buscando...'; }
                },
                escapeMarkup: function (markup) { return markup; }
            });
        }
    }

    function initCascades() {
        $(f.marca).on('change', function() {
            var m_id = $(this).val();
            var $mod = $(f.modelo);
            
            if ($mod.data('select2')) {
                $mod.select2('destroy');
            }
            
            $mod.prop('disabled', !m_id).val('');
            var countOptions = 0;
            var lastOptionVal = '';
            
            $mod.find('option').each(function() {
                if (!$(this).val()) return; // skip default
                if ($(this).data('marca') == m_id) {
                    $(this).show();
                    $(this).prop('disabled', false);
                    countOptions++;
                    lastOptionVal = $(this).val();
                } else {
                    $(this).hide();
                    $(this).prop('disabled', true);
                }
            });
            
            // Auto-seleccionar si solo hay 1 modelo
            if (countOptions === 1) {
                $mod.val(lastOptionVal);
            }
            
            $mod.select2({
                theme: 'bootstrap4',
                width: '100%',
                dropdownParent: $('body')
            });
            
            // Forzamos el change para que se actualice la foto
            $mod.trigger('change');
        });

        // Modelo -> Imagen (o Articulo -> Imagen)
        function actualizarImagenPreview() {
            var $modSelected = $(f.modelo).find('option:selected');
            var imgMod = $modSelected.attr('data-imagen');
            var $artSelected = $(f.articulo).find('option:selected');
            var imgArt = $artSelected.attr('data-imagen');
            
            var img = '';
            if (imgMod && imgMod.trim() !== '' && imgMod !== 'None') {
                img = imgMod;
            } else if (imgArt && imgArt.trim() !== '' && imgArt !== 'None') {
                img = imgArt;
            }
            
            if (img) {
                $('#e-modelo-preview').attr('src', img);
            } else {
                $('#e-modelo-preview').attr('src', '/static/img/placeholder_equipo.png');
            }
        }

        $(f.articulo).on('change', actualizarImagenPreview);
        $(f.modelo).on('change', actualizarImagenPreview);

        // Validar y auto-formatear IP Address
        $(f.ip).on('input', function(e) {
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

        // Cascadas de Ubicación (Filtros visuales en el modal)
        
        // Piso -> Unidad (A través de los Recintos que comparten ese piso)
        $(f.piso).on('change', function() {
            var p_id = $(this).val();
            var $uni = $(f.unidad);
            
            if ($uni.data('select2')) $uni.select2('destroy');
            $uni.prop('disabled', !p_id).val('');
            
            // Encontrar qué unidades tienen recintos en este piso
            var validUnidades = {};
            $(f.recinto).find('option').each(function() {
                var v = $(this).val();
                if (!v) return;
                if (!p_id || $(this).data('piso') == p_id) {
                    var u_id = $(this).data('unidad');
                    if (u_id) validUnidades[u_id] = true;
                }
            });
            
            $uni.find('option').each(function() {
                var v = $(this).val();
                if (!v || validUnidades[v]) {
                    $(this).show();
                    $(this).prop('disabled', false);
                } else {
                    $(this).hide();
                    $(this).prop('disabled', true);
                }
            });
            
            $uni.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
            $uni.trigger('change');
            
            filterRecintos();
        });

        function filterRecintos() {
            var p_id = $(f.piso).val();
            var u_id = $(f.unidad).val();
            var $rec = $(f.recinto);
            
            if ($rec.data('select2')) $rec.select2('destroy');
            
            // Habilitar si hay al menos piso o unidad
            var enable = (p_id || u_id);
            $rec.prop('disabled', !enable).val('');
            
            $rec.find('option').each(function() {
                var v = $(this).val();
                if (!v) return;
                var show = true;
                if (p_id && $(this).data('piso') != p_id) show = false;
                if (u_id && $(this).data('unidad') != u_id) show = false;
                
                if(show) {
                    $(this).show();
                    $(this).prop('disabled', false);
                } else {
                    $(this).hide();
                    $(this).prop('disabled', true);
                }
            });
            
            $rec.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
            $rec.trigger('change');
        }

        function filterPmas() {
            var r_id = $(f.recinto).val();
            var $pma = $(f.pma);
            
            if ($pma.data('select2')) $pma.select2('destroy');
            
            $pma.prop('disabled', !r_id).val('');
            $pma.find('option').each(function() {
                var v = $(this).val();
                if (!v) return;
                if (r_id && $(this).data('recinto') != r_id) {
                    $(this).hide();
                    $(this).prop('disabled', true);
                } else {
                    $(this).show();
                    $(this).prop('disabled', false);
                }
            });
            
            $pma.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
        }

        $(f.unidad).on('change', filterRecintos);
        $(f.recinto).on('change', filterPmas);
    }

    window.evaluarBordesObligatorios = function() {
        var form = $('#form-equipo');
        form.find('select[required]').each(function() {
            var container = $(this).next('.select2-container');
            if (!container.length) container = $(this).siblings('.select2-container');
            
            if ($(this).val()) {
                container.removeClass('ms-required-invalid').addClass('ms-required-valid');
            } else {
                container.removeClass('ms-required-valid').addClass('ms-required-invalid');
            }
        });
        
        // Estado operativo
        if ($('input[name="e-estado"]:checked').length > 0) {
            $('#e-estado-container').removeClass('ms-required-invalid').addClass('ms-required-valid').css({'padding-left': '8px'});
        } else {
            $('#e-estado-container').removeClass('ms-required-valid').addClass('ms-required-invalid').css({'padding-left': '8px'});
        }
    }

    function initEvents() {
        // Btn Nuevo → Drawer
        $('#btn-nuevo-equipo').on('click', function() {
            abrirModal();
        });
        
        // Validacion en tiempo real
        $('#form-equipo').on('change', 'select[required], input[name="e-estado"]', function() {
            evaluarBordesObligatorios();
        });

        // Submit del formulario del Drawer
        $('#form-equipo').on('submit', function(e) {
            e.preventDefault();
            guardarEquipo();
        });

        // Botones del modal de vista (Contact Card)
        $('#btn-view-edit').on('click', function() {
            if (EqState.currentEquipoId) {
                eqCloseView();
                cargarEquipo(EqState.currentEquipoId);
            }
        });
        $('#btn-view-qr').on('click', function() {
            if (EqState.currentEquipoId) {
                window.open('/equipos/' + EqState.currentEquipoId + '/qr/', '_blank');
            }
        });
        $('#btn-view-bitacora').on('click', function() {
            if (EqState.currentEquipoId) {
                var sn = document.getElementById('ev-serial').textContent || '';
                eqCloseView();
                eqOpenBitacora(EqState.currentEquipoId, sn);
            }
        });

        // Filtros de búsqueda
        $('#eq-search').on('input', eqApplyFilters);
        $('#eq-filter-estado').on('change', eqApplyFilters);
        $('#eq-filter-unidad').on('change', eqApplyFilters);
    }

    function abrirModal() {
        var alertEl = document.getElementById('equipo-error-alert');
        if (alertEl) { alertEl.style.display = 'none'; alertEl.textContent = ''; }
        document.getElementById('form-equipo').reset();
        $(f.id).val('');
        // Reset Select2 del Drawer
        $('#equipo-drawer .select2-eq').val('').trigger('change.select2');
        // Reset chips de estado
        $('input[name="e-estado"]').prop('checked', false);
        $('#e-estado-container label').css({'border-color': '#edebe9', 'background': '#faf9f8', 'color': '#323130', 'font-weight': '500'});
        // Disable cascadas
        $(f.modelo).prop('disabled', true);
        $(f.unidad).prop('disabled', true);
        $(f.recinto).prop('disabled', true);
        $(f.pma).prop('disabled', true);
        document.getElementById('equipo-drawer-title').textContent = 'Registrar Activo';
        
        // Reset validacion
        setTimeout(evaluarBordesObligatorios, 50);
        
        eqOpenDrawer();
    }
        


    function guardarEquipo() {
        var data = {
            id: $(f.id).val() || null,
            articulo_id: $(f.articulo).val(),
            marca_id: $(f.marca).val(),
            modelo_id: $(f.modelo).val(),
            serial_number: $(f.serial).val(),
            so_id: $(f.so).val(),
            ip: $(f.ip).val(),
            pma_id: $(f.pma).val(),
            estado_id: $('input[name="e-estado"]:checked').val(),
            proveedor_id: $(f.proveedor).val(),
            correlativo: $('#e-correlativo').val() || null,
            num_inventario: $('#e-num_inventario').val() || null,
            
            // Campos Enterprise
            mac_address: $('#e-mac_address').val() || null,
            switch_ip: $('#e-switch_ip').val() || null,
            patch_panel: $('#e-patch_panel').val() || null,
            puerto_red: $('#e-puerto_red').val() || null,
            orden_compra: $('#e-orden_compra').val() || null,
            fecha_compra: $('#e-fecha_compra').val() || null,
            vencimiento_garantia: $('#e-vencimiento_garantia').val() || null
        };

        $(el.alert).addClass('d-none');

        var isUpdate = data.id ? true : false;

        var doSaveAjax = function(finalData) {
            $.ajax({
                url: '/equipos/api/action/',
                type: isUpdate ? 'PUT' : 'POST',
                data: JSON.stringify(finalData),
                contentType: 'application/json',
                headers: { 'X-CSRFToken': csrfToken() },
                success: function(resp) {
                    if(resp.success) {
                        eqCloseDrawer();
                        eqLoadList(); // Refrescar lista ms-list
                        eqShowToast(resp.message || 'Activo guardado correctamente.');
                    } else {
                        var alertEl = document.getElementById('equipo-error-alert');
                        alertEl.style.display = 'block';
                        alertEl.textContent = resp.message || 'Error al guardar.';
                    }
                },
                error: function(err) {
                    var msg = 'Error de conexión o validación.';
                    if (err.responseJSON && err.responseJSON.message) msg = err.responseJSON.message;
                    var alertEl = document.getElementById('equipo-error-alert');
                    alertEl.style.display = 'block';
                    alertEl.textContent = msg;
                }
            });
        };

        // Si es una actualización y cambió el PMA (Ubicación Física)
        var currentPma = data.pma_id ? String(data.pma_id) : '';
        var originalPma = window.original_pma_id ? String(window.original_pma_id) : '';
        
        if (isUpdate && currentPma !== originalPma && currentPma !== '') {
            Swal.fire({
                title: 'Motivo del Cambio de Ubicación',
                text: 'El sistema ha detectado que cambiaste el Punto de Montaje (Ubicación) de este equipo. Por favor clasifica este cambio:',
                icon: 'question',
                input: 'radio',
                inputOptions: {
                    'MOVIMIENTO': 'Movimiento Real (Traslado de equipo)',
                    'CORRECCION': 'Corrección de dato (Error de tipeo previo)'
                },
                inputValue: 'MOVIMIENTO', // default
                showCancelButton: true,
                confirmButtonText: 'Guardar Equipo',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#002a54',
                inputValidator: function(value) {
                    if (!value) {
                        return 'Debes seleccionar el motivo para continuar.';
                    }
                }
            }).then(function(result) {
                if (result.isConfirmed) {
                    data.motivo_edicion_pma = result.value;
                    doSaveAjax(data);
                }
            });
        } else {
            // Cambio normal, se guarda directamente
            doSaveAjax(data);
        }
    }

    function cargarEquipo(id) {
        $.ajax({
            url: '/equipos/api/' + id + '/',
            type: 'GET',
            success: function(resp) {
                abrirModal(); // Limpia y abre el Drawer
                var eq = resp.data;
                document.getElementById('equipo-drawer-title').textContent = 'Editar Activo';
                
                // Guardamos el PMA original para comparar luego
                window.original_pma_id = eq.pma;
                
                $(f.id).val(eq.id);
                $(f.serial).val(eq.serial_number);
                $(f.ip).val(eq.ip);
                
                // Nuevos campos Enterprise
                $('#e-mac_address').val(eq.mac_address || '');
                $('#e-switch_ip').val(eq.switch_ip || '');
                $('#e-patch_panel').val(eq.patch_panel || '');
                $('#e-puerto_red').val(eq.puerto_red || '');
                $('#e-orden_compra').val(eq.orden_compra || '');
                $('#e-fecha_compra').val(eq.fecha_compra || '');
                $('#e-vencimiento_garantia').val(eq.vencimiento_garantia || '');
                $('#e-correlativo').val(eq.correlativo || '');
                $('#e-num_inventario').val(eq.num_inventario || '');
                // Set selects simples (no cascada)
                $(f.articulo).val(eq.articulo).trigger('change');
                $(f.so).val(eq.so).trigger('change');
                if (eq.estado) {
                    var $radio = $('input[name="e-estado"][value="' + eq.estado + '"]');
                    $radio.prop('checked', true);
                    // Activar el visual del chip
                    eqEstadoChipSelect($radio[0]);
                } else {
                    $('input[name="e-estado"]').prop('checked', false);
                }
                $(f.proveedor).val(eq.proveedor).trigger('change');
                
                // Marca -> habilitar modelos -> setear modelo -> actualizar imagen
                $(f.marca).val(eq.marca).trigger('change');
                setTimeout(function() {
                    $(f.modelo).val(eq.modelo).trigger('change');
                    // Forzar previsualización de imagen tras setear modelo
                    setTimeout(function() {
                        actualizarImagenPreview();
                        // Además: si la imagen viene de la API, mostrarla directamente
                        if (resp.data.imagen) {
                            $('#e-imagen-preview').attr('src', resp.data.imagen);
                        }
                    }, 100);
                }, 150);

                // =============================================================
                // UBICACIÓN: carga silenciosa sin trigger para evitar race conditions
                // Paso 1: Setear Piso de forma silenciosa (sin trigger)
                // =============================================================
                if (eq.piso) {
                    $(f.piso).val(eq.piso);
                    // Re-init select2 para reflejar el valor
                    if ($(f.piso).data('select2')) $(f.piso).select2('destroy');
                    $(f.piso).select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
                }
                
                // Paso 2: Setear Unidad de forma silenciosa (habilitar y setear)
                if (eq.unidad) {
                    var $uni = $(f.unidad);
                    if ($uni.data('select2')) $uni.select2('destroy');
                    $uni.prop('disabled', false);
                    $uni.val(eq.unidad);
                    $uni.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
                }
                
                // Paso 3: Filtrar recintos con piso+unidad ya seteados, luego setear el recinto correcto
                setTimeout(function() {
                    // Ejecutar filterRecintos pero SIN resetear el valor (version silenciosa)
                    var p_id = $(f.piso).val();
                    var u_id = $(f.unidad).val();
                    var $rec = $(f.recinto);
                    
                    if ($rec.data('select2')) $rec.select2('destroy');
                    $rec.prop('disabled', false);
                    
                    // Filtrar opciones del recinto segun piso y unidad
                    $rec.find('option').each(function() {
                        var v = $(this).val();
                        if (!v) return;
                        var show = true;
                        if (p_id && $(this).data('piso') != p_id) show = false;
                        if (u_id && $(this).data('unidad') != u_id) show = false;
                        if (show) {
                            $(this).show().prop('disabled', false);
                        } else {
                            $(this).hide().prop('disabled', true);
                        }
                    });
                    
                    // Ahora setear el recinto real del equipo
                    $rec.val(eq.recinto);
                    $rec.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
                    
                    // Paso 4: Filtrar PMAs segun el recinto seteado, luego setear el PMA
                    setTimeout(function() {
                        var r_id = eq.recinto;
                        var $pma = $(f.pma);
                        
                        if ($pma.data('select2')) $pma.select2('destroy');
                        $pma.prop('disabled', false);
                        
                        // Filtrar opciones del PMA segun recinto
                        $pma.find('option').each(function() {
                            var v = $(this).val();
                            if (!v) return;
                            if (r_id && $(this).data('recinto') != r_id) {
                                $(this).hide().prop('disabled', true);
                            } else {
                                $(this).show().prop('disabled', false);
                            }
                        });
                        
                        // Setear el PMA real del equipo
                        $pma.val(eq.pma);
                        $pma.select2({theme: 'bootstrap4', width: '100%', dropdownParent: $(el.modal)});
                        
                        setTimeout(evaluarBordesObligatorios, 50);
                        
                    }, 100);
                }, 100);
                
            },
            error: function() {
                alert('No se pudo cargar la información del equipo.');
            }
        });
    }

    function cargarBitacora(id) {
        var $tl = $('#bitacora-timeline');
        $tl.html('<div class="text-center py-5"><div class="spinner-border text-primary" role="status"></div></div>');
        $.ajax({
            url: '/equipos/api/' + id + '/bitacora/',
            type: 'GET',
            success: function(resp) {
                if(resp.success && resp.data.length > 0) {
                    var html = '';
                    resp.data.forEach(function(b) {
                        html += '<div style="border-left: 2px solid #edebe9; padding-left: 20px; position: relative; margin-bottom: 24px; padding-bottom: 8px;">';
                        html += '<div style="position: absolute; left: -7px; top: 0; width: 12px; height: 12px; border-radius: 50%; background: #0078d4; border: 2px solid #ffffff; box-shadow: 0 0 0 1px #0078d4;"></div>';
                        
                        if (b.source === 'SISTEMA') {
                            html += '<div style="display:flex; justify-content:space-between; align-items:center;">';
                            html += '  <div style="font-weight: 600; font-size: 14px; color: #323130;">Registro #' + b.id + ' <span style="display:inline-block; margin-left: 8px; padding: 2px 6px; font-size: 11px; font-weight: 600; border-radius: 2px; background: #fff4ce; color: #795548;">' + b.tipo_registro + '</span></div>';
                            html += '  <div style="font-size: 12px; color: #605e5c;">Ingreso: ' + b.fecha + '</div>';
                            html += '</div>';
                            
                            html += '<div style="font-size: 12px; color: #605e5c; margin-top:6px; margin-bottom: 12px; display:flex; flex-wrap:wrap; gap:16px;">';
                            html += '  <span><i class="fas fa-user-tie" style="color:#0078d4; width:16px;"></i> <b>Técnico:</b> ' + b.tecnico + '</span>';
                            html += '  <span><i class="fas fa-user" style="color:#0078d4; width:16px;"></i> <b>Solicitante:</b> ' + b.solicitante + '</span>';
                            html += '</div>';
                            
                            html += '<div style="background: #ffffff; border: 1px solid #edebe9; border-radius: 4px; padding: 12px; margin-bottom: 8px; box-shadow: 0 1.6px 3.6px 0 rgba(0,0,0,0.065), 0 0.3px 0.9px 0 rgba(0,0,0,0.06);">';
                            html += '  <div style="font-size: 13px; font-weight: 600; color: #323130; margin-bottom: 4px;"><i class="fas fa-microchip" style="color:#0078d4; margin-right:6px;"></i> Acción: ' + b.accion + '</div>';
                            html += '  <div style="font-size: 13px; color: #605e5c; padding-top: 4px; border-top: 1px solid #edebe9; margin-top: 6px;">' + b.detalles + '</div>';
                            html += '</div>';
                        } else {
                            var isMantencion = (b.tipo_registro === 'Mantención');
                            var displayTipo = isMantencion ? 'Soporte' : b.tipo_registro;
                            
                            var badgeStyle = isMantencion ? 'background: #fff4ce; color: #795548;' : 'background: #deecf9; color: #005a9e;';
                            
                            html += '<div style="display:flex; justify-content:space-between; align-items:flex-start;">';
                            html += '  <div style="font-weight: 600; font-size: 14px; color: #323130;">Registro #' + b.id + ' <span style="display:inline-block; margin-left: 8px; padding: 2px 6px; font-size: 11px; font-weight: 600; border-radius: 2px; ' + badgeStyle + '">' + displayTipo + '</span></div>';
                            var entregaText = '';
                            if (isMantencion) {
                                entregaText = ' | Entrega: ' + (b.fecha_devolucion || '<span style="color:#a4262c; font-weight:600;"><i class="fas fa-clock" style="margin-right:4px;"></i>Pendiente</span>');
                            }
                            html += '  <div style="font-size: 12px; color: #605e5c; text-align:right;">Ingreso: ' + b.fecha_mantenimiento + '<br>' + entregaText + '</div>';
                            html += '</div>';
                            
                            html += '<div style="font-size: 12px; color: #605e5c; margin-top:2px; margin-bottom: 12px; display:flex; flex-wrap:wrap; gap:16px;">';
                            html += '  <span><i class="fas fa-user-tie" style="color:#0078d4; width:16px;"></i> <b>Técnico:</b> ' + b.tecnico + '</span>';
                            html += '  <span><i class="fas fa-user" style="color:#0078d4; width:16px;"></i> <b>Solicitante:</b> ' + b.solicitante + '</span>';
                            html += '  <span><i class="fas fa-building" style="color:#0078d4; width:16px;"></i> <b>Unidad:</b> ' + b.servicio_unidad + '</span>';
                            html += '</div>';
                            
                            if(b.falla_reportada) {
                                html += '<div style="background: #ffffff; border: 1px solid #edebe9; border-radius: 4px; padding: 12px; margin-bottom: 8px; box-shadow: 0 1.6px 3.6px 0 rgba(0,0,0,0.065), 0 0.3px 0.9px 0 rgba(0,0,0,0.06); border-left: 3px solid #d13438;">';
                                html += '  <div style="font-size: 13px; font-weight: 600; color: #d13438; margin-bottom: 4px;"><i class="fas fa-exclamation-circle" style="margin-right:6px;"></i> Falla o Motivo Reportado</div>';
                                html += '  <div style="font-size: 13px; color: #323130;">' + b.falla_reportada + '</div>';
                                html += '</div>';
                            }
                            if(b.actividades_realizadas) {
                                var actHtml = b.actividades_realizadas.replace(/\[Cierre\]/g, '<span style="background:#107c10; color:white; padding:2px 6px; border-radius:2px; font-size:11px; font-weight:600; margin: 0 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.2);">CIERRE</span>');
                                html += '<div style="background: #f3f2f1; border: 1px solid #e1dfdd; border-radius: 4px; padding: 12px; margin-bottom: 8px;">';
                                html += '  <div style="font-size: 13px; font-weight: 600; color: #0078d4; margin-bottom: 4px;"><i class="fas fa-wrench" style="margin-right:6px;"></i> Acción Realizada</div>';
                                html += '  <div style="font-size: 13px; color: #323130; line-height:1.4;">' + actHtml + '</div>';
                                html += '</div>';
                            }
                            
                            // Boton para cerrar mantención pendiente
                            if (b.tipo_registro === 'Mantención' && !b.fecha_devolucion) {
                                html += '<div class="mt-3 text-right">';
                                html += '  <button type="button" class="ms-btn-primary btn-cerrar-mantencion" data-id="' + b.id + '" data-eq="' + id + '" style="display:inline-flex;">';
                                html += '    <i class="fas fa-check"></i> Cerrar Mantención';
                                html += '  </button>';
                                html += '</div>';
                            }
                        }
                        html += '</div>';
                    });
                    $tl.html(html);
                } else {
                    $tl.html('<div class="alert alert-light text-center" style="border: 1px dashed #cbd5e1;"><i class="fas fa-info-circle mb-2" style="font-size:24px; color:#94a3b8; display:block;"></i>No hay registros en la bitácora de este equipo.</div>');
                }
            },
            error: function() {
                $tl.html('<div class="alert alert-danger">Error al cargar bitácora.</div>');
            }
        });
    }

    function abrirBitacora(id, sn) {
        $('#b-equipo-id').val(id);
        
        // Actualizar titulo del modal y header card
        $('#b-equipo-sn').text(sn);
        $('#b-equipo-sn-header').text(sn);
        $('#b-equipo-estado').text('-');
        $('#b-equipo-ubicacion').text('-');
        $('#b-imagen').attr('src', '/static/img/placeholder_equipo.png');
        
        // Resetear formulario primero para limpiar selects
        $('#form-bitacora')[0].reset();
        $('#b-falla, #b-unidad, #b-solicitante').val(null).trigger('change');
        
        // Fetch equipo details for the header card
        $.ajax({
            url: '/equipos/api/' + id + '/ver/',
            type: 'GET',
            success: function(resp) {
                var eq = resp.data;
                $('#b-imagen').attr('src', eq.imagen || '/static/img/placeholder_equipo.png');
                $('#b-equipo-sn-header').text(eq.serial_number || sn);
                $('#b-equipo-estado').text(eq.estado || 'S/E');
                var ubicacion = [];
                if (eq.edificio) ubicacion.push(eq.edificio);
                if (eq.unidad) ubicacion.push(eq.unidad);
                $('#b-equipo-ubicacion').text(ubicacion.join(' - ') || '-');
                
                // Preseleccionar unidad en el select de la bitacora
                if (eq.unidad) {
                    var $bUnidad = $('#b-unidad');
                    var match = $bUnidad.find('option').filter(function() {
                        return $(this).text() === eq.unidad;
                    }).val();
                    if (match) {
                        $bUnidad.val(match).trigger('change');
                    }
                }
            }
        });
        
        // Set default date to today
        var today = new Date(new Date().getTime() - (new Date().getTimezoneOffset() * 60000)).toISOString().split('T')[0];
        $('#b-fecha-mtto').val(today);
        
        $('#modalBitacora').modal('show');
        cargarBitacora(id);
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
                $('#v-recinto').text(eq.recinto || '-');
                $('#v-pma').text(eq.pma || '-');
                
                // Especificaciones
                var mrk = eq.marca || 'Genérica';
                var mod = eq.modelo || 'Genérico';
                $('#v-marca-modelo').text(mrk + ' ' + mod);
                $('#v-ip').text(eq.ip || 'Sin IP');
                $('#v-so').text(eq.so || 'N/A');
                $('#v-proveedor').text(eq.proveedor || 'Sin Proveedor');
                
                // Auditoria
                $('#v-sysid').text(eq.id || '#');
                var modPor = eq.usuario_modificador || 'Sistema';
                var modFec = eq.fecha_modificacion || 'N/A';
                $('#v-fecha').html('Actualizado por <b>' + modPor + '</b> el ' + modFec);
                
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
                    // Recargar el ms-list (reemplaza dtEquipos.ajax.reload)
                    eqLoadList();
                    eqShowToast('Equipo eliminado correctamente.');
                } else {
                    Swal.fire('Error', resp.message, 'error');
                }
            },
            error: function() {
                Swal.fire('Error', 'Error al intentar eliminar.', 'error');
            }
        });
    }

    // Constructor/Init
    return {
        init: function() {
            // Exponer funciones necesarias al scope global
            window.cargarEquipo = cargarEquipo;
            window.cargarBitacora = cargarBitacora;
            
            initSelect2();
            initCascades();
            // initDataTable() — reemplazado por eqLoadList() (motor ms-list)
            initEvents();
            // Eventos Bitacora
            $('#btn-toggle-bitacora').on('click', function() {
                $('#collapseFormBitacora').slideToggle(250);
            });
            $('#btn-cancel-bitacora').on('click', function() {
                $('#collapseFormBitacora').slideUp(250);
            });
            
            $('#tabla-equipos').on('click', '.ic-bitacora', function(e) {
                e.preventDefault();
                abrirBitacora($(this).data('id'), $(this).data('sn'));
            });
            
            // ============================================================
            // Event delegation para el botón "Registrar Nuevo Funcionario"
            // dentro del dropdown de Select2 (no puede usar onclick inline
            // porque Select2 lo destruye al renderizar).
            // ============================================================
            $(document).on('click', '.btn-add-funcionario-inline', function(e) {
                e.stopPropagation(); // Evitar que Select2 cierre el dropdown con el click
                $('#b-solicitante').select2('close');
                // Fix de z-index para modal apilado sobre otro modal
                $('#modalFuncionario').modal('show');
            });
            
            // Fix z-index para Bootstrap modales apilados (Bitácora > Funcionario)
            $('#modalFuncionario').on('shown.bs.modal', function() {
                var zIndex = 1050 + 10 * $('.modal:visible').length;
                $(this).css('z-index', zIndex);
                $('.modal-backdrop').not('.modal-stack').last().css('z-index', zIndex - 1).addClass('modal-stack');
            });
            
            // Accion: Cerrar Mantención pendiente
            $('#bitacora-timeline').on('click', '.btn-cerrar-mantencion', function(e) {
                e.preventDefault();
                var bitacoraId = $(this).data('id');
                var eqId = $(this).data('eq');
                
                Swal.fire({
                    title: 'Cerrar Mantención',
                    customClass: { 
                        container: 'swal-top-modal',
                        confirmButton: 'ms-btn-primary',
                        cancelButton: 'ms-btn-secondary ml-2'
                    },
                    buttonsStyling: false,
                    html: `
                        <div class="text-left mt-2">
                            <label style="font-size:0.95rem; font-weight:600; color:#323130;">Escribe la Resolución del problema antes de cerrar el caso</label>
                            <textarea id="swal-actividades" class="ms-input w-100 mt-2" style="resize:vertical;" rows="5" placeholder="Detalles de la entrega o resolución técnica..."></textarea>
                        </div>
                    `,
                    showCancelButton: true,
                    confirmButtonText: '<i class="fas fa-check"></i> Cerrar Mantención',
                    cancelButtonText: 'Cancelar',
                    preConfirm: () => {
                        return {
                            actividades: document.getElementById('swal-actividades').value
                        };
                    }
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Obtener el registro actual para saber si hay que concatenar texto (el backend no concatena)
                        // Para simplificar, haremos un PUT enviando solo lo necesario, el backend reemplaza si enviamos actividades.
                        // Wait, backend reemplaza. Necesito enviar actividades antiguas + nuevas.
                        // Pero no tengo las antiguas crudas aqui (puedo obtenerlas si hago GET primero, o pasar un endpoint especial).
                        // Para no complicar, enviaremos la peticion al backend pero con "append_actividades: true" no existe en la API.
                        // Lo mejor es hacer un GET rapido o simplemente guardar la fecha si no escriben actividades.
                        
                        $.ajax({
                            url: '/equipos/api/bitacora/' + bitacoraId + '/',
                            type: 'PUT',
                            data: JSON.stringify({
                                cierre_automatico: true,
                                extra_actividades: result.value.actividades
                            }),
                            contentType: 'application/json',
                            headers: { 'X-CSRFToken': csrfToken() },
                            success: function(resp) {
                                if (resp.success) {
                                    Swal.fire('Guardado', 'Mantención cerrada correctamente.', 'success');
                                    cargarBitacora(eqId);
                                    eqLoadList(); // Refrescar lista y KPIs
                                } else {
                                    Swal.fire('Error', resp.message, 'error');
                                }
                            },
                            error: function(err) {
                                var msg = 'Error al cerrar la mantención';
                                if (err.responseJSON && err.responseJSON.message) msg = err.responseJSON.message;
                                Swal.fire('Error', msg, 'error');
                            }
                        });
                    }
                });
            });
            
            $('#form-bitacora').on('submit', function(e) {
                e.preventDefault();
                var btn = $('#btn-guardar-bitacora');
                btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Guardando...');
                
                var data = {
                    tipo_registro: $('#b-tipo').val(),
                    fecha_mantenimiento: $('#b-fecha-mtto').val(),
                    falla_reportada: $('#b-falla').val(),
                    actividades_realizadas: $('#b-actividades').val(),
                    solicitante: $('#b-solicitante').val(),
                    servicio_unidad: $('#b-unidad').val()
                };
                
                var eq_id = $('#b-equipo-id').val();
                
                $.ajax({
                    url: '/equipos/api/' + eq_id + '/bitacora/',
                    type: 'POST',
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    headers: { 'X-CSRFToken': csrfToken() },
                    success: function(resp) {
                        btn.prop('disabled', false).html('<i class="fas fa-save mr-1"></i> Guardar Registro');
                        if(resp.success) {
                            Swal.fire('Guardado', 'Registro de bitácora creado correctamente.', 'success');
                            $('#collapseFormBitacora').slideUp(250);
                            $('#form-bitacora')[0].reset();
                            $('#b-falla, #b-unidad, #b-solicitante').val(null).trigger('change');
                            cargarBitacora(eq_id); // Recargar timeline
                            eqLoadList(); // Refrescar lista y KPIs
                        } else {
                            Swal.fire('Error', resp.message, 'error');
                        }
                    },
                    error: function(err) {
                        btn.prop('disabled', false).html('<i class="fas fa-save mr-1"></i> Guardar Registro');
                        var msg = "Error al guardar.";
                        if(err.responseJSON && err.responseJSON.message) msg = err.responseJSON.message;
                        Swal.fire('Error', msg, 'error');
                    }
                });
            });
            
            // ============================================================
            // Validador de RUT Chileno (idéntico al de Tickets)
            // ============================================================
            function validarRutEq(rut) {
                if (!/^[0-9]+[-]{1}[0-9kK]{1}$/.test(rut)) return false;
                var tmp = rut.split('-');
                var digv = tmp[1];
                var rutNum = tmp[0];
                if (digv === 'K') digv = 'k';
                return (dvEq(rutNum) === digv);
            }
            function dvEq(T) {
                var M = 0, S = 1;
                for (; T; T = Math.floor(T / 10))
                    S = (S + T % 10 * (9 - M++ % 6)) % 11;
                return S ? String(S - 1) : 'k';
            }

            // Live validation del RUT al tipear en el modal de Funcionario
            $(document).on('input', '#f-rut', function() {
                var valLimpio = this.value.replace(/[^0-9kK]/gi, '').toUpperCase();
                if (valLimpio.length > 1) {
                    var cuerpo = valLimpio.slice(0, -1);
                    var dv    = valLimpio.slice(-1);
                    this.value = cuerpo + '-' + dv;
                } else {
                    this.value = valLimpio;
                }
                var val = this.value.trim();
                var $fb = $('#rut_feedback_eq');
                if (val === '') {
                    $(this).removeClass('is-valid is-invalid');
                    $fb.attr('class', 'form-text text-muted').html('Ingresa el RUT con guion y dígito verificador.');
                    return;
                }
                if (validarRutEq(val)) {
                    $(this).removeClass('is-invalid').addClass('is-valid');
                    $fb.attr('class', 'form-text text-success font-weight-bold').html('<i class="fas fa-check-circle"></i> RUT Válido');
                } else {
                    $(this).removeClass('is-valid').addClass('is-invalid');
                    $fb.attr('class', 'form-text text-danger font-weight-bold').html('<i class="fas fa-times-circle"></i> RUT Inválido');
                }
            });

            // Verificar existencia del RUT en la BD al perder el foco (blur)
            // — alerta inmediata antes de que el usuario llene el resto del formulario
            $(document).on('blur', '#f-rut', function() {
                var val = $(this).val().trim();
                var $fb = $('#rut_feedback_eq');
                if (!validarRutEq(val)) return; // Ya está marcado como inválido, nada que verificar

                $fb.attr('class', 'form-text text-muted').html('<i class="fas fa-spinner fa-spin"></i> Verificando RUT en el sistema...');

                $.ajax({
                    url: '/api/funcionarios/search/?q=' + encodeURIComponent(val),
                    type: 'GET',
                    success: function(data) {
                        // El endpoint de búsqueda devuelve {results: [{id, text}]}
                        var existe = data.results && data.results.length > 0 &&
                            data.results.some(function(r) {
                                // Verificar si el texto del resultado contiene el RUT exacto
                                return r.text && r.text.indexOf('(' + val + ')') !== -1;
                            });

                        if (existe) {
                            $('#f-rut').removeClass('is-valid').addClass('is-invalid');
                            $fb.attr('class', 'form-text text-danger font-weight-bold')
                               .html('<i class="fas fa-exclamation-triangle"></i> Este RUT ya está registrado en el sistema. Selecciónalo en la búsqueda del solicitante.');
                            // Deshabilitar el botón guardar para evitar duplicados
                            $('#btn-guardar-funcionario').prop('disabled', true);
                        } else {
                            $('#f-rut').removeClass('is-invalid').addClass('is-valid');
                            $fb.attr('class', 'form-text text-success font-weight-bold')
                               .html('<i class="fas fa-check-circle"></i> RUT Válido · No existe en el sistema');
                            $('#btn-guardar-funcionario').prop('disabled', false);
                        }
                    },
                    error: function() {
                        // Si falla la verificación, permitir continuar (el backend validará al guardar)
                        $fb.attr('class', 'form-text text-muted').html('Ingresa el RUT con guion y dígito verificador.');
                    }
                });
            });

            // Botón Guardar del modal Funcionario
            $('#btn-guardar-funcionario').on('click', function() {
                var rut = $('#f-rut').val().trim();
                if (!validarRutEq(rut)) {
                    Swal.fire('RUT Inválido', 'Por favor ingresa un RUT chileno válido (Ej: 12345678-9).', 'warning');
                    $('#f-rut').focus();
                    return;
                }
                var nombres   = $('#f-nombres').val().trim();
                var apellidos = $('#f-apellidos').val().trim();
                if (!nombres || !apellidos) {
                    Swal.fire('Campos requeridos', 'Nombres y Apellidos son obligatorios.', 'warning');
                    return;
                }

                var btn = $(this);
                btn.prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Guardando...');

                var data = {
                    rut:       rut,
                    nombres:   nombres,
                    apellidos: apellidos,
                    correo:    $('#f-correo').val().trim(),
                    cargo:     $('#f-cargo').val(),
                    unidad:    $('#f-unidad-func').val()
                };

                $.ajax({
                    url: '/api/funcionarios/crear/',
                    type: 'POST',
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    headers: { 'X-CSRFToken': csrfToken() },
                    success: function(resp) {
                        btn.prop('disabled', false).html('<i class="fas fa-save mr-1"></i> Guardar Funcionario');
                        if (resp.success) {
                            $('#modalFuncionario').modal('hide');
                            $('#form-funcionario')[0].reset();
                            $('#f-rut').removeClass('is-valid is-invalid');
                            $('#rut_feedback_eq').attr('class', 'form-text text-muted').html('Ingresa el RUT con guion y dígito verificador.');
                            // Agregar y seleccionar la nueva opción en Select2
                            var newOption = new Option(resp.data.text, resp.data.id, true, true);
                            $('#b-solicitante').append(newOption).trigger('change');
                            Swal.fire({icon: 'success', title: 'Funcionario creado', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000});
                        } else {
                            Swal.fire('Error', resp.message || 'Error al guardar.', 'error');
                        }
                    },
                    error: function(err) {
                        btn.prop('disabled', false).html('<i class="fas fa-save mr-1"></i> Guardar Funcionario');
                        var msg = 'Error al guardar funcionario.';
                        if (err.responseJSON && err.responseJSON.message) msg = err.responseJSON.message;
                        Swal.fire('Error', msg, 'error');
                    }
                });
            });

            // Limpiar el modal al cerrarse
            $('#modalFuncionario').on('hidden.bs.modal', function() {
                $('#form-funcionario')[0].reset();
                $('#f-rut').removeClass('is-valid is-invalid');
                $('#rut_feedback_eq').attr('class', 'form-text text-muted').html('Ingresa el RUT con guion y dígito verificador.');
            });

        }  // ← fin de initEvents()
    };     // ← fin de return { init: function() {...} }

})(jQuery);

$(document).ready(function() {
    EquiposApp.init();
    // Cargar la lista ms-list al iniciar la página
    eqLoadList();
});

// Función Global para exportar a Excel
window.eqExportExcel = function() {
    var q = $('#eq-search').val() || '';
    var estado = $('#eq-filter-estado').val() || '';
    var unidad = $('#eq-filter-unidad').val() || '';
    
    var url = '/equipos/exportar/?q=' + encodeURIComponent(q) + 
              '&estado=' + encodeURIComponent(estado) + 
              '&unidad=' + encodeURIComponent(unidad);
              
    window.location.href = url;
};

// Función Global para el visual de chips de estado
window.eqEstadoChipSelect = function(radio) {
    // Reset todos
    $('input[name="e-estado"]').closest('label').css({
        'border-color': '#edebe9',
        'background': '#faf9f8',
        'color': '#323130',
        'font-weight': '500'
    });
    // Activar el seleccionado
    var color = $(radio).data('color') || '#0078d4';
    $(radio).closest('label').css({
        'border-color': color,
        'background': color + '15',
        'color': color,
        'font-weight': '600'
    });
};
