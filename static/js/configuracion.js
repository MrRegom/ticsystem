/**
 * configuracion.js
 * Lógica del módulo de Configuración del Sistema:
 * - Renderiza la Matriz SLA visual con colores y datos.
 * - Gestiona la edición de celdas SLA (modal).
 * - CRUD de Prioridades.
 */
$(document).ready(function() {

    // --- UTILIDADES ---
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

    const CSRF = getCookie('csrftoken');

    // =============================================
    // MATRIZ SLA — Renderizado dinámico
    // =============================================
    const matrizData = window.SLA_DATA || {};
    const impactos = window.IMPACTOS || [];
    const urgencias = window.URGENCIAS || [];

    function minutosATexto(mins) {
        if (mins < 60) return `${mins} min`;
        const h = Math.floor(mins / 60);
        const m = mins % 60;
        return m > 0 ? `${h}h ${m}m` : `${h}h`;
    }

    function renderizarMatriz() {
        const $tbody = $('#tabla-matriz-sla tbody');
        $tbody.empty();

        impactos.forEach(function(imp) {
            const impVal = imp.val;
            const impLabel = imp.label;

            let row = `<tr>
                <td class="font-weight-bold text-left align-middle" style="background:#ffffff; box-shadow: 0 1.6px 3.6px 0 rgba(0,0,0,0.132), 0 0.3px 0.9px 0 rgba(0,0,0,0.108); color:#323130; padding:14px 16px; min-width:220px; border-radius:4px;">
                    <i class="fas fa-circle ms-mr-2" style="font-size:0.6rem; color:#8a8886;"></i>${impLabel}
                </td>`;

            urgencias.forEach(function(urg) {
                const urgVal = urg.val;
                const celda = (matrizData[impVal] || {})[urgVal];

                if (celda) {
                    const color = celda.prioridad_color || '#94a3b8';
                    const darkerColor = color;
                    row += `<td
                        class="sla-cell text-center"
                        data-sla-id="${celda.id}"
                        data-impacto="${impVal}"
                        data-urgencia="${urgVal}"
                        data-imp-label="${impLabel}"
                        data-urg-label="${urg.label}"
                        style="cursor:pointer; padding:0; background:#ffffff; border-radius:4px; box-shadow: 0 1.6px 3.6px 0 rgba(0,0,0,0.132), 0 0.3px 0.9px 0 rgba(0,0,0,0.108); transition: transform 0.15s, box-shadow 0.15s; position:relative;"
                        onmouseover="this.style.transform='scale(1.02)';this.style.boxShadow='0 6.4px 14.4px 0 rgba(0,0,0,0.132), 0 1.2px 3.6px 0 rgba(0,0,0,0.108)';this.style.zIndex='10';"
                        onmouseout="this.style.transform='';this.style.boxShadow='0 1.6px 3.6px 0 rgba(0,0,0,0.132), 0 0.3px 0.9px 0 rgba(0,0,0,0.108)';this.style.zIndex='';">
                        
                        <div style="padding: 14px; background: white; border-top: 4px solid ${color}; border-radius:4px; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 8px;">
                            <span style="background-color: ${color}15; color: ${color}; padding: 3px 12px; border-radius: 12px; font-weight: 700; font-size: 0.75rem;">${celda.prioridad_nombre}</span>
                            <div style="font-size:0.7rem; color:#64748b; line-height:1.4;">
                                <div><i class="fas fa-bolt text-muted mr-1" style="font-size:0.6rem;"></i>1ª Resp: <strong style="color:#1e293b;">${minutosATexto(celda.tiempo_respuesta_minutos)}</strong></div>
                                <div><i class="fas fa-clock text-muted mr-1" style="font-size:0.6rem;"></i>Resol: <strong style="color:#1e293b;">${celda.tiempo_resolucion_horas}h</strong></div>
                            </div>
                            <i class="fas fa-pencil-alt mt-1" style="color:#cbd5e1; font-size:0.75rem; transition: color 0.2s;" onmouseover="this.style.color='${color}'" onmouseout="this.style.color='#cbd5e1'"></i>
                        </div>
                    </td>`;
                } else {
                    row += `<td style="background:#f1f5f9; cursor:pointer; text-align:center; padding:14px; color:#94a3b8; border:1px dashed #cbd5e1; font-size:0.75rem;">
                        Sin configurar
                    </td>`;
                }
            });

            row += '</tr>';
            $tbody.append(row);
        });
    }

    renderizarMatriz();

    // =============================================
    // EDITAR CELDA SLA
    // =============================================
    $(document).on('click', '.sla-cell[data-sla-id]', function() {
        const $cell = $(this);
        const slaId = $cell.data('sla-id');
        const impLabel = $cell.data('imp-label');
        const urgLabel = $cell.data('urg-label');

        // Buscar datos de la celda
        const impVal = $cell.data('impacto');
        const urgVal = $cell.data('urgencia');
        const celda = (matrizData[impVal] || {})[urgVal];

        if (!celda) return;

        $('#sla-edit-id').val(slaId);
        $('#sla-cell-desc').html(`<i class="fas fa-table mr-2"></i>${impLabel} &mdash; Urgencia: ${urgLabel}`);
        $('#sla-prioridad').val(celda.prioridad_id);
        $('#sla-respuesta').val(celda.tiempo_respuesta_minutos);
        $('#sla-resolucion').val(celda.tiempo_resolucion_horas);

        $('#modalEditarSLA').modal('show');
    });

    $('#btn-guardar-sla').click(function() {
        const slaId = $('#sla-edit-id').val();
        const data = {
            id: slaId,
            prioridad_id: $('#sla-prioridad').val(),
            tiempo_respuesta_minutos: parseInt($('#sla-respuesta').val()),
            tiempo_resolucion_horas: parseInt($('#sla-resolucion').val())
        };

        if (!data.prioridad_id || !data.tiempo_respuesta_minutos || !data.tiempo_resolucion_horas) {
            Swal.fire('Campos Incompletos', 'Por favor complete todos los campos.', 'warning');
            return;
        }

        $.ajax({
            url: '/sla/api/matrix/',
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify(data),
            headers: { 'X-CSRFToken': CSRF },
            success: function(res) {
                if (res.success) {
                    // Actualizar los datos locales del SLA
                    const impVal = parseInt($('.sla-cell[data-sla-id="'+slaId+'"]').data('impacto'));
                    const urgVal = parseInt($('.sla-cell[data-sla-id="'+slaId+'"]').data('urgencia'));
                    const selectedPrio = $('#sla-prioridad option:selected');
                    
                    if (matrizData[impVal] && matrizData[impVal][urgVal]) {
                        matrizData[impVal][urgVal].prioridad_id = parseInt(data.prioridad_id);
                        matrizData[impVal][urgVal].prioridad_nombre = selectedPrio.text().split(' (')[0];
                        matrizData[impVal][urgVal].tiempo_respuesta_minutos = data.tiempo_respuesta_minutos;
                        matrizData[impVal][urgVal].tiempo_resolucion_horas = data.tiempo_resolucion_horas;
                    }
                    
                    $('#modalEditarSLA').modal('hide');
                    renderizarMatriz();
                    // Re-adjuntar los nuevos colores desde la DB requeriría otro GET; 
                    // por ahora actualizamos lo que sabemos.
                    Swal.fire({ title: '¡Guardado!', text: 'SLA actualizado correctamente.', icon: 'success', timer: 2000, showConfirmButton: false });
                } else {
                    Swal.fire('Error', res.message, 'error');
                }
            },
            error: function() {
                Swal.fire('Error', 'No se pudo guardar la configuración.', 'error');
            }
        });
    });

    // =============================================
    // PRIORIDADES — CRUD
    // =============================================
    function cargarPrioridades() {
        $.ajax({
            url: '/sla/api/prioridades/',
            type: 'GET',
            success: function(res) {
                const $tbody = $('#prioridades-tbody');
                $tbody.empty();
                if (!res.data || res.data.length === 0) {
                    $tbody.append('<tr><td colspan="5" class="text-center text-muted py-3">No hay prioridades registradas.</td></tr>');
                    return;
                }
                res.data.forEach(function(p, i) {
                    $tbody.append(`
                        <tr class="ms-list-row">
                            <td>${i + 1}</td>
                            <td>
                                <span style="background:${p.color_hex}; color:white; padding:4px 10px; border-radius:12px; font-size:11px; font-weight:600;">${p.nombre}</span>
                            </td>
                            <td>
                                <div style="display:inline-block; width:16px; height:16px; background:${p.color_hex}; border-radius:50%; border:1px solid #edebe9; vertical-align:middle;"></div>
                                <code class="ms-ml-2" style="color:#605e5c;">${p.color_hex}</code>
                            </td>
                            <td>
                                <span style="font-size:0.85rem; color:#323130;">
                                    <i class="far fa-clock ms-mr-2" style="color:#0078d4;"></i>${p.sla_horas} horas
                                </span>
                            </td>
                            <td class="text-center">
                                <div class="ms-table-actions">
                                    <button class="ms-icon-btn ms-icon-btn-edit btn-edit-prio" 
                                        data-id="${p.id}" data-nombre="${p.nombre}" data-sla="${p.sla_horas}" data-color="${p.color_hex}" title="Editar">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="ms-icon-btn ms-icon-btn-delete btn-del-prio" 
                                        data-id="${p.id}" data-nombre="${p.nombre}" title="Eliminar">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                    `);
                });
            }
        });
    }

    cargarPrioridades();

    // Nueva prioridad
    $('#btn-nueva-prioridad').click(function() {
        $('#prio-edit-id').val('');
        $('#prio-nombre').val('');
        $('#prio-sla').val('');
        $('#prio-color').val('#3b82f6');
        $('#modal-prio-title').html('<i class="fas fa-flag mr-2"></i>Nueva Prioridad');
        $('#modalPrioridad').modal('show');
    });

    // Editar prioridad
    $(document).on('click', '.btn-edit-prio', function() {
        const btn = $(this);
        $('#prio-edit-id').val(btn.data('id'));
        $('#prio-nombre').val(btn.data('nombre'));
        $('#prio-sla').val(btn.data('sla'));
        $('#prio-color').val(btn.data('color'));
        $('#modal-prio-title').html('<i class="fas fa-pencil-alt mr-2"></i>Editar Prioridad');
        $('#modalPrioridad').modal('show');
    });

    // Eliminar prioridad
    $(document).on('click', '.btn-del-prio', function() {
        const btn = $(this);
        Swal.fire({
            title: '¿Eliminar Prioridad?',
            text: `Está a punto de eliminar la prioridad "${btn.data('nombre')}". Esta acción no se puede deshacer.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444',
            cancelButtonText: 'Cancelar',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: '/sla/api/prioridades/action/',
                    type: 'DELETE',
                    contentType: 'application/json',
                    data: JSON.stringify({ id: btn.data('id') }),
                    headers: { 'X-CSRFToken': CSRF },
                    success: function(res) {
                        if (res.success) {
                            cargarPrioridades();
                            Swal.fire({ title: '¡Eliminada!', text: res.message, icon: 'success', timer: 2000, showConfirmButton: false });
                        } else {
                            Swal.fire('Error', res.message, 'error');
                        }
                    }
                });
            }
        });
    });

    // Guardar prioridad (crear o editar)
    $('#btn-guardar-prio').click(function() {
        const id = $('#prio-edit-id').val();
        const data = {
            nombre: $('#prio-nombre').val().trim(),
            sla_horas: $('#prio-sla').val(),
            color_hex: $('#prio-color').val()
        };

        if (!data.nombre || !data.sla_horas) {
            Swal.fire('Campos Incompletos', 'El nombre y el SLA son obligatorios.', 'warning');
            return;
        }

        const method = id ? 'PUT' : 'POST';
        if (id) data.id = parseInt(id);

        $.ajax({
            url: '/sla/api/prioridades/action/',
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(data),
            headers: { 'X-CSRFToken': CSRF },
            success: function(res) {
                if (res.success) {
                    $('#modalPrioridad').modal('hide');
                    cargarPrioridades();
                    Swal.fire({ title: '¡Guardado!', text: res.message, icon: 'success', timer: 2000, showConfirmButton: false });
                } else {
                    Swal.fire('Error', res.message, 'error');
                }
            },
            error: function() {
                Swal.fire('Error', 'No se pudo guardar la prioridad.', 'error');
            }
        });
    });

});
