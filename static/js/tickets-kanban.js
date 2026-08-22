document.addEventListener('DOMContentLoaded', function() {

    var CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]') ?
        document.querySelector('[name=csrfmiddlewaretoken]').value : window.TICKET_CONFIG.csrfToken;
    var kanbanData = window.TICKET_CONFIG.kanbanData;

    /* ---- Cambio de vistas ---- */
    window.switchView = function(view) {
        document.querySelectorAll('.view-panel').forEach(function(p) { p.classList.remove('active'); });
        document.querySelectorAll('.view-toggle-btn').forEach(function(b) { b.classList.remove('active'); });
        document.getElementById('panel-' + view).classList.add('active');
        document.getElementById('btn-view-' + view).classList.add('active');
        if (view === 'historial' && typeof $ !== 'undefined' && !$.fn.DataTable.isDataTable('#tabla-historial')) {
            $('#tabla-historial').DataTable({
                language: { url: window.TICKET_CONFIG.datatablesLanguageUrl },
                order: [[6, 'desc']], pageLength: 25,
            });
        }
        if (view === 'listado') {
            renderListado();
        }
    };

    window.filterTickets = function() {
        var input = document.getElementById('kanban-search');
        if (!input) return;
        var filter = input.value.toLowerCase();
        
        // Filtrar tarjetas de Kanban
        var cards = document.querySelectorAll('.kanban-card');
        cards.forEach(function(card) {
            var text = card.textContent || card.innerText;
            if (text.toLowerCase().indexOf(filter) > -1) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        });
        
        // Filtrar filas del Listado
        var rows = document.querySelectorAll('.listado-row');
        rows.forEach(function(row) {
            var text = row.textContent || row.innerText;
            if (text.toLowerCase().indexOf(filter) > -1) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    };

    /* ---- Construir tarjeta ---- */
    function buildCard(t) {
        var card = document.createElement('div');
        card.className = 'kanban-card';
        card.dataset.id = t.id;
        card.style.borderLeftColor = t.prioridad_color || '#cbd5e1';
        card.setAttribute('onclick', 'openOffcanvas(' + t.id + ')');
        
        card.dataset.vencimiento = t.fecha_vencimiento_iso || '';
        card.dataset.enPausa = t.en_pausa_sla ? '1' : '';
        card.dataset.estado = t.estado || ''; // We might need state if it's passed

        card.innerHTML =
            '<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">' +
                '<div style="display: flex; flex-direction: column; gap: 2px;">' +
                    '<span class="card-correlativo" style="color: #0f172a; font-size: 0.7rem; font-weight: 700;">' + t.correlativo + '</span>' +
                    '<span style="font-size: 0.6rem; color:#64748b; font-weight:600;"><i class="far fa-calendar-alt"></i> ' + (t.fecha_creacion_corta || '') + ' <span style="color: #3b82f6;">' + (t.fecha_creacion_hora || '') + '</span></span>' +
                '</div>' +
                '<span class="card-prio-badge" style="background:' + (t.prioridad_color || '#94a3b8') + '; color: #fff; padding: 2px 4px; font-size: 0.55rem; font-weight: 700; border-radius: 3px; text-transform: uppercase;">' + t.prioridad + '</span>' +
            '</div>' +
            (function() {
                var parts = t.descripcion.split('\n');
                var subject = parts[0].replace(/(ASUNTO:\s*)+/ig, '').trim();
                var detail = parts.length > 1 ? parts.slice(1).join(' ').replace(/(DETALLE:\s*)+/ig, '').trim() : '';
                return '<div class="card-desc" style="margin-bottom: 8px; line-height: 1.3; font-size: 0.75rem;">' +
                       '<div style="color: #0f172a;"><strong style="font-weight:700;">ASUNTO:</strong> ' + subject + '</div>' +
                       (detail ? '<div style="color: #475569; margin-top: 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis;"><strong style="font-weight:600;">DETALLE:</strong> ' + detail + '</div>' : '') +
                       '</div>';
            })() +
            '<div class="sla-timer-display" style="font-size:0.7rem; font-weight:600; margin-bottom:6px;"></div>' +
            (t.pma ? '<div class="card-pma" style="font-size:0.65rem; color:#64748b; margin-bottom:6px;"><i class="fas fa-map-marker-alt"></i> ' + t.pma + '</div>' : '') +
            '<div class="card-meta" style="font-size: 0.65rem; color: #64748b; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; padding-top: 6px;">' +
                '<span style="font-weight: 600;"><i class="fas fa-layer-group"></i> ' + (t.grupo || 'Mesa de Ayuda') + '</span>' +
                '<span style="' + (t.tecnico === 'Sin asignar' ? 'color: #94a3b8;' : 'color: #3b82f6; font-weight: 600;') + ' text-align: right; max-width: 120px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="' + t.tecnico + '"><i class="fas ' + (t.tecnico === 'Sin asignar' ? 'fa-user-times' : 'fa-user-check') + '"></i> ' + t.tecnico + '</span>' +
            '</div>';
        return card;
    }

    /* ---- Render inicial ---- */
    Object.keys(kanbanData).forEach(function(estadoId) {
        var tickets = kanbanData[estadoId];
        var col   = document.getElementById('column-' + estadoId);
        var badge = document.getElementById('count-'  + estadoId);
        if (!col) return;
        col.innerHTML = '';
        if (badge) badge.textContent = tickets.length;
        
        if (tickets.length === 0) {
            col.innerHTML = getEmptyStateHtml(estadoId);
        } else {
            tickets.forEach(function(t) { 
                t.estado = estadoId; // Inject state to help timer
                col.appendChild(buildCard(t)); 
            });
        }
    });

    function renderListado() {
        var container = document.getElementById('listado-container');
        if (!container) return;
        container.innerHTML = '';
        
        var estados = [
            { id: 'NUEVO', label: 'Nuevo', color: '#3b82f6', icon: 'fa-inbox' },
            { id: 'ASIGNADO', label: 'Asignado', color: '#ca8a04', icon: 'fa-user' },
            { id: 'EN_PROCESO', label: 'En Proceso', color: '#10b981', icon: 'fa-cogs' },
            { id: 'ESCALADO', label: 'Escalado', color: '#ef4444', icon: 'fa-arrow-up' }
        ];

        estados.forEach(function(estado) {
            var tickets = kanbanData[estado.id] || [];
            
            var tableHtml = '<div style="margin-bottom: 10px; border: 1px solid #e2e8f0;">' +
                            '<div style="background: ' + estado.color + '15; padding: 10px 15px; border-bottom: 2px solid ' + estado.color + '; display: flex; justify-content: space-between; align-items: center;">' +
                            '<h4 style="margin: 0; font-size: 14px; font-weight: 700; color: ' + estado.color + ';"><i class="fas ' + estado.icon + ' mr-2"></i>' + estado.label + '</h4>' +
                            '<span style="background: ' + estado.color + '; color: #fff; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600;">' + tickets.length + '</span>' +
                            '</div>';
            
            if (tickets.length === 0) {
                tableHtml += '<div style="padding: 15px; text-align: center; color: #94a3b8; font-size: 13px;">No hay tickets en este estado.</div></div>';
                container.innerHTML += tableHtml;
                return;
            }

            tableHtml += '<table style="width: 100%; border-collapse: collapse; font-size: 13px;">' +
                         '<thead><tr style="background: #f8fafc; color: #475569; text-align: left; border-bottom: 1px solid #e2e8f0;">' +
                         '<th style="padding: 8px 12px; width: 10%;">Ticket</th>' +
                         '<th style="padding: 8px 12px; width: 35%;">Asunto</th>' +
                         '<th style="padding: 8px 12px; width: 10%;">Prioridad</th>' +
                         '<th style="padding: 8px 12px; width: 10%;">Fecha</th>' +
                         '<th style="padding: 8px 12px; width: 15%;">Grupo</th>' +
                         '<th style="padding: 8px 12px; width: 10%;">Técnico</th>' +
                         '<th style="padding: 8px 12px; text-align: right; width: 10%;">Acción</th>' +
                         '</tr></thead><tbody>';

            tickets.forEach(function(t) {
                var parts = t.descripcion.split('\n');
                var subject = parts[0].replace(/(ASUNTO:\s*)+/ig, '').trim();
                
                tableHtml += '<tr class="listado-row" style="border-bottom: 1px solid #e2e8f0; cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background=\'#f1f5f9\'" onmouseout="this.style.background=\'#fff\'" onclick="openOffcanvas(' + t.id + ')">' +
                             '<td style="padding: 10px 12px;"><span style="font-weight: 700; color: #0f172a;">' + t.correlativo + '</span></td>' +
                             '<td style="padding: 10px 12px;"><div style="color: #0f172a; font-weight: 600; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; text-overflow: ellipsis; line-height: 1.3;">' + subject + '</div></td>' +
                             '<td style="padding: 10px 12px;"><span style="background: ' + (t.prioridad_color || '#94a3b8') + '; color: #fff; padding: 2px 6px; font-size: 11px; font-weight: 700;">' + t.prioridad + '</span></td>' +
                             '<td style="padding: 10px 12px; color: #475569;">' + t.fecha_creacion_corta + '</td>' +
                             '<td style="padding: 10px 12px; color: #475569;">' + (t.grupo || 'Mesa de Ayuda') + '</td>' +
                             '<td style="padding: 10px 12px; color: ' + (t.tecnico === 'Sin asignar' ? '#94a3b8' : '#3b82f6') + ';">' + t.tecnico + '</td>' +
                             '<td style="padding: 10px 12px; text-align: right;"><button class="ms-btn-primary" style="padding: 4px 8px; font-size: 11px; border-radius: 0; background: #3b82f6; border: none;">Ver Detalles</button></td>' +
                             '</tr>';
            });
            tableHtml += '</tbody></table></div>';
            container.innerHTML += tableHtml;
        });
        window.filterTickets(); // Apply current search filter
    }

    function getEmptyStateHtml(estadoId) {
        var icons = {
            'NUEVO': '<i class="fas fa-inbox"></i>',
            'ASIGNADO': '<i class="fas fa-user"></i>',
            'EN_PROCESO': '<i class="fas fa-cogs"></i>',
            'ESCALADO': '<i class="fas fa-arrow-up"></i>'
        };
        var colors = {
            'NUEVO': '#3b82f6',
            'ASIGNADO': '#ca8a04',
            'EN_PROCESO': '#10b981',
            'ESCALADO': '#ef4444'
        };
        var texts = {
            'NUEVO': 'Cuando se creen nuevos tickets,<br>aparecerán aquí.',
            'ASIGNADO': 'Tickets asignados a técnicos.',
            'EN_PROCESO': 'Arrastra un ticket aquí<br>para marcarlo como en proceso.',
            'ESCALADO': 'Arrastra un ticket aquí<br>si requiere escalamiento.'
        };
        
        var icon = icons[estadoId] || '<i class="fas fa-box-open"></i>';
        var color = colors[estadoId] || '#64748b';
        var text = texts[estadoId] || 'No hay tickets en este estado.';
        
        return '<div class="kanban-empty-state">' +
               '<div class="empty-icon" style="color: ' + color + ';">' + icon + '</div>' +
               '<div class="empty-title">No hay tickets</div>' +
               '<div class="empty-text">' + text + '</div>' +
               '</div>';
    }

    function updateColumnEmptyState(colContainer, estadoId) {
        var cards = colContainer.querySelectorAll('.kanban-card');
        var empty = colContainer.querySelector('.kanban-empty-state');
        if (cards.length === 0) {
            if (!empty) {
                colContainer.innerHTML = getEmptyStateHtml(estadoId);
            }
        } else {
            if (empty) {
                empty.remove();
            }
        }
    }

    /* ---- SLA Timer Engine ---- */
    function updateSlaTimers() {
        var now = new Date();
        
        // Helper function to calculate SLA text
        function getSlaHtml(vencimientoIso, enPausa, estado) {
            var isTerminal = ['RESUELTO', 'CERRADO', 'CANCELADO'].indexOf(estado) !== -1;
            
            if (isTerminal) {
                return '<span style="color:#10b981;"><i class="fas fa-check-circle"></i> SLA Detenido</span>';
            }
            if (enPausa) {
                return '<span style="color:#94a3b8;"><i class="fas fa-pause-circle"></i> SLA en Pausa</span>';
            }
            if (!vencimientoIso) {
                return '';
            }

            var vencimiento = new Date(vencimientoIso);
            var diffMs = vencimiento - now;
            var expired = diffMs < 0;
            diffMs = Math.abs(diffMs);

            var diffMins = Math.floor(diffMs / 60000);
            var h = Math.floor(diffMins / 60);
            var m = diffMins % 60;
            var timeStr = (h > 0 ? h + 'h ' : '') + m + 'm';

            if (expired) {
                return '<span style="color:#ef4444;" class="blink-icon"><i class="fas fa-exclamation-triangle"></i> Vencido hace ' + timeStr + '</span>';
            } else {
                if (diffMins < 60) {
                    return '<span style="color:#f97316;"><i class="fas fa-clock"></i> Quedan ' + timeStr + '</span>';
                } else if (diffMins < 120) {
                    return '<span style="color:#f59e0b;"><i class="fas fa-clock"></i> Quedan ' + timeStr + '</span>';
                } else {
                    return '<span style="color:#10b981;"><i class="fas fa-clock"></i> Quedan ' + timeStr + '</span>';
                }
            }
        }

        // Kanban cards
        document.querySelectorAll('.kanban-card').forEach(function(card) {
            var display = card.querySelector('.sla-timer-display');
            if (!display) return;
            var estado = card.parentElement.dataset.estado || '';
            display.innerHTML = getSlaHtml(card.dataset.vencimiento, card.dataset.enPausa, estado);
        });
        
        // Offcanvas detail
        var ocSla = document.getElementById('oc-tk-sla');
        if (ocSla && ocSla.dataset.vencimiento) {
            ocSla.innerHTML = getSlaHtml(ocSla.dataset.vencimiento, ocSla.dataset.enPausa, ocSla.dataset.estado);
        }
    }

    // Run SLA Timers immediately and every minute
    updateSlaTimers();
    setInterval(updateSlaTimers, 60000);

    /* ---- Drag & Drop ---- */
    if (typeof Sortable !== 'undefined') {
        document.querySelectorAll('.kanban-items').forEach(function(col) {
            new Sortable(col, {
                group: 'kanban', animation: 150, ghostClass: 'sortable-ghost',
                onEnd: function(evt) {
                    var fromCol = evt.from, toCol = evt.to;
                    if (fromCol === toCol) return;
                    
                    var ticketId = evt.item.dataset.id;
                    var nuevoEstado = toCol.parentElement.dataset.estado;
                    var nombreEstado = toCol.parentElement.querySelector('.kanban-col-title').textContent;

                    var oldRef = fromCol.children[evt.oldIndex] || null;

                    // Usar setTimeout para asegurar que SortableJS termina de limpiar su DOM interno (quitar ghost)
                    setTimeout(function() {
                        Swal.fire({
                            title: '¿Mover a ' + nombreEstado + '?',
                            text: "Se registrará en la bitácora.",
                            icon: 'question',
                            showCancelButton: true,
                            confirmButtonColor: '#002855',
                            cancelButtonColor: '#94a3b8',
                            confirmButtonText: 'Sí, mover',
                            cancelButtonText: 'Cancelar'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                fetch('/tickets/api/action/', {
                                    method: 'PUT',
                                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                                    body: JSON.stringify({ id: ticketId, estado: nuevoEstado })
                                })
                                .then(function(r) { return r.json(); })
                                .then(function(res) {
                                    if (res.success) {
                                        document.getElementById('count-' + toCol.parentElement.dataset.estado).textContent = toCol.children.length;
                                        document.getElementById('count-' + fromCol.parentElement.dataset.estado).textContent = fromCol.children.length;
                                    } else {
                                        Swal.fire('Error', res.message || 'No se pudo cambiar el estado.', 'error');
                                        fromCol.insertBefore(evt.item, oldRef);
                                    }
                                })
                                .catch(function() {
                                    Swal.fire('Error', 'Sin conexión.', 'error');
                                    fromCol.insertBefore(evt.item, oldRef);
                                });
                            } else {
                                fromCol.insertBefore(evt.item, oldRef);
                            }
                        });
                    }, 50);
                }
            });
        });
    }

    /* ---- Reset modal ---- */
    var modalEl = document.getElementById('modalNuevoTicket');
    if (modalEl && typeof $ !== 'undefined') {
        $(modalEl).on('hidden.bs.modal', function() {
            document.getElementById('form-nuevo-ticket').reset();
            var btn = document.getElementById('btn-submit-ticket');
            if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-save"></i> Crear Ticket'; }
        });
    }

    /* ---- Submit via AJAX ---- */
    var form = document.getElementById('form-nuevo-ticket');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            e.stopPropagation();

            var solicitante = form.querySelector('[name="solicitante_id"]').value;
            var tipo        = form.querySelector('input[name="tipo"]:checked').value;
            var categoria   = form.querySelector('[name="categoria_id"]').value;
            var impacto     = form.querySelector('input[name="impacto"]:checked') ? form.querySelector('input[name="impacto"]:checked').value : form.querySelector('[name="impacto"]').value;
            var urgencia    = form.querySelector('input[name="urgencia"]:checked') ? form.querySelector('input[name="urgencia"]:checked').value : form.querySelector('[name="urgencia"]').value;
            var anexo       = form.querySelector('[name="anexo_contacto"]').value;
            var correo      = form.querySelector('[name="correo_contacto"]').value;
            var descripcion = form.querySelector('[name="descripcion"]').value.trim();

            if (!solicitante || !categoria || !descripcion) {
                if (!solicitante) $('#solicitante-select').next('.select2-container').addClass('ms-val-error');
                if (!categoria) $('select[name="categoria_id"]').next('.select2-container').addClass('ms-val-error');
                if (!descripcion) $('[name="descripcion"]').addClass('ms-val-error');
                
                Swal.fire({ icon: 'warning', title: 'Campos requeridos', text: 'Solicitante, Categoría y Descripción son obligatorios.', confirmButtonColor: '#002855' });
                return false;
            }

            var btn = document.getElementById('btn-submit-ticket');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creando...';

            var payload = { 
                solicitante_id: solicitante,
                tipo: tipo,
                categoria_id: categoria, 
                impacto: impacto,
                urgencia: urgencia,
                descripcion: descripcion,
                anexo_contacto: anexo,
                correo_contacto: correo
            };
            var activoId = form.querySelector('[name="activo_id"]').value;
            if (activoId) payload.activo_id = activoId;

            fetch('/tickets/api/action/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify(payload)
            })
            .then(function(r) { return r.json(); })
            .then(function(res) {
                if (res.success) {
                    if (typeof $ !== 'undefined') $(modalEl).modal('hide');
                    var t = res.ticket;
                    var colNuevo = document.getElementById('column-NUEVO');
                    if (colNuevo && t) {
                        colNuevo.insertBefore(buildCard(t), colNuevo.firstChild);
                        var badge = document.getElementById('count-NUEVO');
                        if (badge) badge.textContent = colNuevo.children.length;
                    }
                    Swal.fire({
                        icon: 'success', title: '¡Ticket Creado!',
                        html: 'Ticket <strong>' + (t ? t.correlativo : '') + '</strong> registrado en el tablero.',
                        confirmButtonColor: '#002855', timer: 2500, timerProgressBar: true
                    });
                } else {
                    Swal.fire({ icon: 'error', title: 'Error', text: res.message || 'No se pudo crear el ticket.' });
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-save"></i> Crear Ticket';
                }
            })
            .catch(function(err) {
                console.error('Error AJAX:', err);
                Swal.fire('Error de conexión', 'No se pudo contactar el servidor. Revisa la consola.', 'error');
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-save"></i> Crear Ticket';
            });

            return false;
        });
    }

    /* ---- OFFCANVAS LOGIC ---- */
    window.openOffcanvas = function(ticketId) {
        document.getElementById('oc-backdrop').classList.add('show');
        document.getElementById('oc-ticket').classList.add('show');
        document.getElementById('oc-tk-correlativo').textContent = 'Cargando...';
        document.getElementById('oc-tk-desc').textContent = '';
        document.getElementById('oc-timeline').innerHTML = '<div style="text-align:center; padding:20px; color:#94a3b8;"><i class="fas fa-spinner fa-spin fa-2x"></i></div>';
        document.getElementById('oc-tk-id').value = ticketId;

        fetch('/tickets/api/ticket/' + ticketId + '/')
        .then(function(r) { return r.json(); })
        .then(function(res) {
            if (res.success) {
                var t = res.ticket;
                document.getElementById('oc-tk-correlativo').textContent = t.correlativo;
                document.getElementById('oc-tk-estado').textContent = t.estado;
                document.getElementById('oc-tk-prioridad').textContent = t.prioridad;
                
                var slaEl = document.getElementById('oc-tk-sla');
                if (slaEl) {
                    slaEl.dataset.vencimiento = t.fecha_vencimiento_iso || '';
                    slaEl.dataset.enPausa = t.en_pausa_sla ? '1' : '';
                    slaEl.dataset.estado = t.estado_id || '';
                }
                if (typeof updateSlaTimers === 'function') updateSlaTimers();

                document.getElementById('oc-tk-categoria').textContent = t.categoria;
                document.getElementById('oc-tk-solicitante').textContent = t.solicitante;
                document.getElementById('oc-tk-activo').textContent = t.activo;
                document.getElementById('oc-tk-pma').textContent = t.pma;
                var parts = t.descripcion.split('\\n');
                var subject = parts[0].replace(/^ASUNTO:\\s*/i, '');
                var detail = parts.length > 1 ? parts.slice(1).join('<br>').replace(/DETALLE:\\s*/i, '').trim() : '';
                document.getElementById('oc-tk-desc').innerHTML = '<div style="font-weight: 700; color: #0f172a; margin-bottom: 6px;">' + subject + '</div>' + 
                                                                  (detail ? '<div style="font-weight: 400; color: #475569;">' + detail + '</div>' : '');
                
                // Guardar si tiene equipo en data attribute para el resolver
                document.getElementById('btn-resolver-tk').dataset.tieneEquipo = (t.activo !== 'Ninguno') ? 'true' : 'false';
                
                // CMDB Warning
                var cmdbAlert = document.getElementById('oc-cmdb-warning');
                if (t.cmdb_warning) {
                    if (!cmdbAlert) {
                        cmdbAlert = document.createElement('div');
                        cmdbAlert.id = 'oc-cmdb-warning';
                        cmdbAlert.style.cssText = 'background: #fef2f2; border: 1px solid #ef4444; color: #b91c1c; padding: 12px; border-radius: 8px; margin-bottom: 16px; font-size: 0.85rem; font-weight: 600;';
                        document.querySelector('.oc-body').insertBefore(cmdbAlert, document.querySelector('.oc-body').firstChild);
                    }
                    cmdbAlert.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + t.cmdb_warning;
                    cmdbAlert.style.display = 'block';
                } else if (cmdbAlert) {
                    cmdbAlert.style.display = 'none';
                }
                
                var btnResolver = document.getElementById('btn-resolver-tk');
                var btnTomar = document.getElementById('btn-tomar-tk');
                var btnPausar = document.getElementById('btn-pausar-tk');
                var asignacionSection = document.getElementById('oc-section-asignacion');
                var formComentario = document.getElementById('form-comentario');
                
                var isClosed = (t.estado_id === 'RESUELTO' || t.estado_id === 'CERRADO');

                // Lógica de visibilidad
                if (asignacionSection) asignacionSection.style.display = isClosed ? 'none' : 'block';
                if (formComentario) formComentario.style.display = isClosed ? 'none' : 'block';
                
                btnResolver.style.display = (!isClosed) ? 'inline-block' : 'none';
                if (btnPausar) {
                    btnPausar.style.display = (!isClosed && t.estado_id !== 'PENDIENTE_PROVEEDOR') ? 'inline-block' : 'none';
                }
                if (btnTomar) {
                    if (t.estado_id === 'NUEVO' || t.estado_id === 'ESCALADO') {
                        btnTomar.style.display = 'inline-block';
                        btnTomar.innerHTML = '<i class="fas fa-hand-paper"></i> Tomar Ticket';
                    } else if ((t.estado_id === 'ASIGNADO' || t.estado_id === 'EN_PROCESO') && t.responsable_id != CURRENT_USER_ID) {
                        btnTomar.style.display = 'inline-block';
                        btnTomar.innerHTML = '<i class="fas fa-user-plus"></i> Reasignarme Ticket';
                    } else {
                        btnTomar.style.display = 'none';
                    }
                }
                
                var sel = document.getElementById('oc-select-tecnico');
                sel.value = t.responsable_id ? 'tec_' + t.responsable_id : (t.grupo_resolutor_id ? 'grp_' + t.grupo_resolutor_id : '');
                sel.dataset.initialValue = sel.value; // Guardar valor inicial
                
                var btnAsignar = document.getElementById('btn-asignar');
                btnAsignar.disabled = true;
                btnAsignar.style.opacity = '0.5';

                renderTimeline(t.historial);
            } else {
                Swal.fire('Error', 'No se pudo cargar el ticket.', 'error');
                closeOffcanvas();
            }
        });
    };

    window.closeOffcanvas = function() {
        document.getElementById('oc-backdrop').classList.remove('show');
        document.getElementById('oc-ticket').classList.remove('show');
    };

    function renderTimeline(hist) {
        var tl = document.getElementById('oc-timeline');
        tl.innerHTML = '';
        if (!hist || hist.length === 0) {
            tl.innerHTML = '<div style="color:#94a3b8; font-size:0.8rem;">No hay registros aún.</div>';
            return;
        }
        hist.forEach(function(h) {
            var item = document.createElement('div');
            item.className = 'tl-item';
            
            var meta = '<div class="tl-meta"><span class="tl-user">' + h.usuario + '</span><span>' + h.fecha + '</span></div>';
            var action = '<div class="tl-action">' + h.accion + '</div>';
            
            var extras = '';
            if (h.valor_anterior || h.valor_nuevo) {
                extras += '<div style="font-size:0.75rem; color:#64748b; margin-top:2px;">' + (h.valor_anterior||'-') + ' &rarr; ' + (h.valor_nuevo||'-') + '</div>';
            }
            if (h.comentario) {
                extras += '<div class="tl-content">' + h.comentario + '</div>';
            }

            item.innerHTML = meta + action + extras;
            tl.appendChild(item);
        });
    }

    // Interceptar clics en Kanban Cards
    document.getElementById('kanban-board').addEventListener('click', function(e) {
        var card = e.target.closest('.kanban-card');
        if (card) {
            openOffcanvas(card.dataset.id);
        }
    });

    document.getElementById('oc-select-tecnico').addEventListener('change', function(e) {
        var btn = document.getElementById('btn-asignar');
        var textarea = document.getElementById('oc-asignar-comentario');
        if (this.value !== this.dataset.initialValue) {
            btn.disabled = false;
            btn.style.opacity = '1';
            if (textarea) textarea.style.display = 'block';
        } else {
            btn.disabled = true;
            btn.style.opacity = '0.5';
            if (textarea) textarea.style.display = 'none';
        }
    });

    // Submit Asignar
    document.getElementById('form-asignar').addEventListener('submit', function(e) {
        var btn = document.getElementById('btn-asignar');
        var sel = document.getElementById('oc-select-tecnico');
        var tkId = document.getElementById('oc-tk-id').value;
        var selValue = sel.value;
        
        if (selValue === sel.dataset.initialValue) return;
        
        var payload = {};
        if (selValue.startsWith('tec_')) payload.tecnico_id = selValue.replace('tec_', '');
        else if (selValue.startsWith('grp_')) payload.grupo_id = selValue.replace('grp_', '');
        
        var comentarioAsignar = document.getElementById('oc-asignar-comentario');
        if (comentarioAsignar && comentarioAsignar.style.display !== 'none') {
            var val = comentarioAsignar.value.trim();
            if (!val) {
                Swal.fire('Reasignación', 'Debes ingresar el motivo de la reasignación para enviarlo al nuevo equipo/técnico.', 'warning');
                return;
            }
            payload.comentario = val;
        }
        
        btn.disabled = true;
        btn.innerHTML = '...';

        fetch('/tickets/api/ticket/' + tkId + '/assign/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify(payload)
        })
        .then(function(r) { return r.json(); })
        .then(function(res) {
            btn.innerHTML = 'Asignar';
            if(res.success) {
                sel.dataset.initialValue = selValue; // Actualizar inicial
                btn.style.opacity = '0.5'; // Dejar disabled
                Swal.fire({icon: 'success', title: 'Asignado', timer: 1500, showConfirmButton: false});
                openOffcanvas(tkId); // recargar offcanvas
                // Recargar página completa para actualizar tarjetas
                setTimeout(function(){ window.location.reload(); }, 1500);
            } else {
                btn.disabled = false;
                btn.style.opacity = '1';
                Swal.fire('Error', res.message, 'error');
            }
        });
    });

    // Submit Comentario
    document.getElementById('form-comentario').addEventListener('submit', function(e) {
        var btn = document.getElementById('btn-comentar');
        var tkId = document.getElementById('oc-tk-id').value;
        var text = document.getElementById('oc-comentario-texto').value.trim();
        
        if(!text) return;

        btn.disabled = true;
        btn.innerHTML = '...';

        fetch('/tickets/api/ticket/' + tkId + '/comment/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify({ comentario: text })
        })
        .then(function(r) { return r.json(); })
        .then(function(res) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Enviar';
            if(res.success) {
                document.getElementById('oc-comentario-texto').value = '';
                openOffcanvas(tkId); // Recargar la info para ver el nuevo comentario
            } else {
                Swal.fire('Error', res.message, 'error');
            }
        });
    });

    // Resolver Ticket - Abrir Modal
    document.getElementById('btn-resolver-tk').addEventListener('click', function() {
        var tkId = document.getElementById('oc-tk-id').value;
        var tieneEquipo = this.dataset.tieneEquipo === 'true';
        
        document.getElementById('res_ticket_id').value = tkId;
        document.getElementById('form-resolver-ticket').reset();
        
        if (tieneEquipo) {
            document.getElementById('seccion-bitacora').style.display = 'block';
            document.getElementById('campos-bitacora').style.display = 'none';
        } else {
            document.getElementById('seccion-bitacora').style.display = 'none';
        }
        
        $('#modalResolverTicket').modal('show');
    });

    // Tomar Ticket
    var btnTomarAction = document.getElementById('btn-tomar-tk');
    if (btnTomarAction) {
        btnTomarAction.addEventListener('click', function() {
            var tkId = document.getElementById('oc-tk-id').value;
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>...';
            
            fetch('/tickets/api/ticket/' + tkId + '/take/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            })
            .then(function(r) { return r.json(); })
            .then(function(res) {
                if (res.success) {
                    Swal.fire({
                        icon: 'success', title: 'Ticket Tomado', 
                        text: 'El ticket ahora está asignado a ti y en proceso.',
                        confirmButtonColor: '#002855'
                    }).then(() => window.location.reload());
                } else {
                    Swal.fire('Error', res.message, 'error');
                    btnTomarAction.disabled = false;
                    btnTomarAction.innerHTML = '<i class="fas fa-hand-paper"></i> Tomar Ticket';
                }
            })
            .catch(function(err) {
                Swal.fire('Error', 'Error de red', 'error');
                btnTomarAction.disabled = false;
                btnTomarAction.innerHTML = '<i class="fas fa-hand-paper"></i> Tomar Ticket';
            });
        });
    }

    // Modal Pausar Ticket
    var btnPausar = document.getElementById('btn-pausar-tk');
    if (btnPausar) {
        btnPausar.addEventListener('click', function() {
            var tkId = document.getElementById('oc-tk-id').value;
            document.getElementById('pau_ticket_id').value = tkId;
            document.getElementById('form-pausar-ticket').reset();
        });
    }

    var formPausar = document.getElementById('form-pausar-ticket');
    if (formPausar) {
        formPausar.addEventListener('submit', function(e) {
            e.preventDefault();
            var tkId = document.getElementById('pau_ticket_id').value;
            var comentario = document.getElementById('pau_comentario').value.trim();
            var btnSubmit = document.getElementById('btn-submit-pausar');
            
            btnSubmit.disabled = true;
            btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
            
            fetch('/tickets/api/action/', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify({ id: tkId, estado: 'PENDIENTE_PROVEEDOR', comentario: comentario })
            })
            .then(function(r) { return r.json(); })
            .then(function(res) {
                if (res.success) {
                    Swal.fire({
                        icon: 'success', title: 'Ticket Pausado',
                        text: 'El SLA se ha detenido y el motivo ha sido registrado.',
                        confirmButtonColor: '#002855'
                    }).then(() => window.location.reload());
                } else {
                    Swal.fire('Error', res.message, 'error');
                    btnSubmit.disabled = false;
                    btnSubmit.innerHTML = '<i class="fas fa-pause"></i> Confirmar Pausa';
                }
            })
            .catch(function(err) {
                Swal.fire('Error', 'Error de red', 'error');
                btnSubmit.disabled = false;
                btnSubmit.innerHTML = '<i class="fas fa-pause"></i> Confirmar Pausa';
            });
        });
    }

    // Toggle campos bitácora al hacer check
    document.getElementById('chk-crear-bitacora').addEventListener('change', function() {
        if(this.checked) {
            document.getElementById('campos-bitacora').style.display = 'block';
        } else {
            document.getElementById('campos-bitacora').style.display = 'none';
        }
    });

    // Submit Formulario Resolver
    document.getElementById('form-resolver-ticket').addEventListener('submit', function(e) {
        e.preventDefault();
        var tkId = document.getElementById('res_ticket_id').value;
        var solucion = document.getElementById('res_solucion').value.trim();
        var crearBitacora = document.getElementById('chk-crear-bitacora').checked;
        
        var payload = {
            solucion: solucion,
            crear_bitacora: crearBitacora
        };
        
        if (crearBitacora) {
            payload.tipo_registro = document.getElementById('res_tipo_registro').value;
            payload.falla_reportada = document.getElementById('res_falla_reportada').value.trim();
            payload.actividades_realizadas = document.getElementById('res_actividades').value.trim();
        }

        var btn = document.getElementById('btn-submit-resolver');
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

        fetch('/tickets/api/ticket/' + tkId + '/resolve/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
            body: JSON.stringify(payload)
        })
        .then(r => r.json())
        .then(res => {
            if (res.success) {
                $('#modalResolverTicket').modal('hide');
                Swal.fire({icon: 'success', title: 'Ticket Resuelto', text: 'Solución ' + (crearBitacora ? 'y Bitácora guardadas' : 'guardada'), timer: 1500, showConfirmButton: false});
                setTimeout(() => window.location.reload(), 1500);
            } else {
                Swal.fire('Error', res.message, 'error');
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-check"></i> Finalizar y Resolver Ticket';
            }
        }).catch(err => {
            Swal.fire('Error', 'Problema de conexión.', 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-check"></i> Finalizar y Resolver Ticket';
        });
    });

    // Tomar Ticket (Self Assign)
    var btnTomarTk = document.getElementById('btn-tomar-tk');
    if (btnTomarTk) {
        btnTomarTk.addEventListener('click', function() {
            var tkId = document.getElementById('oc-tk-id').value;
            this.disabled = true;
            this.innerHTML = '...';

            fetch('/tickets/api/ticket/' + tkId + '/take/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN }
            })
            .then(r => r.json())
            .then(res => {
                if (res.success) {
                    Swal.fire({icon: 'success', title: 'Ticket Asignado', text: 'Has tomado este ticket.', timer: 1500, showConfirmButton: false});
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    Swal.fire('Error', res.message, 'error');
                    this.disabled = false;
                    this.innerHTML = '<i class="fas fa-hand-paper"></i> Tomar Ticket';
                }
            });
        });
    }

    // Form Crear Usuario al Vuelo
    var formCrearUsuario = document.getElementById('form-crear-usuario');
    if (formCrearUsuario) {
        formCrearUsuario.addEventListener('submit', function(e) {
            e.preventDefault();
            
            var rut_val = this.rut_nuevo.value.trim();
            if (!validarRut(rut_val)) {
                Swal.fire('RUT Inválido', 'Por favor ingresa un RUT chileno válido (Ej: 12345678-9).', 'warning');
                return false;
            }

            var btn = document.getElementById('btn-submit-usuario');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';

            var payload = {
                rut: rut_val,
                nombres: this.nombres_nuevo.value,
                apellidos: this.apellidos_nuevo.value,
                cargo: this.cargo_nuevo.value,
                unidad: this.unidad_nuevo.value,
                correo: this.correo_nuevo.value
            };

            fetch('/tickets/api/search/users/create/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(res => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-save"></i> Guardar Funcionario';
                if (res.success) {
                    $('#modalCrearUsuario').modal('hide');
                    // Limpiar el form
                    formCrearUsuario.reset();
                    // Agregar y seleccionar la nueva opción en Select2
                    var newOption = new Option(res.user.text, res.user.id, true, true);
                    $('#solicitante-select').append(newOption).trigger('change');
                    Swal.fire({icon: 'success', title: 'Funcionario creado', toast: true, position: 'top-end', showConfirmButton: false, timer: 3000});
                } else {
                    Swal.fire('Error', res.message || 'Error desconocido del servidor.', 'error');
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-save"></i> Guardar Funcionario';
                Swal.fire('Error', 'No se pudo conectar con el servidor o la sesión expiró.', 'error');
                console.error(err);
            });
        });
    }

    // Validador de RUT Chileno
    function validarRut(rut) {
        if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test(rut)) return false;
        var tmp = rut.split('-');
        var digv = tmp[1]; 
        var rutNum = tmp[0];
        if (digv == 'K') digv = 'k';
        return (dv(rutNum) == digv);
    }
    
    function dv(T) {
        var M = 0, S = 1;
        for (; T; T = Math.floor(T / 10))
            S = (S + T % 10 * (9 - M++ % 6)) % 11;
        return S ? S - 1 : 'k';
    }

    // Live Validation para Modal de Usuario
    var rutTimeout = null;
    var rutInput = document.getElementById('rut_nuevo');
    var rutFeedback = document.getElementById('rut_feedback');
    if (rutInput) {
        rutInput.addEventListener('input', function(e) {
            // Limpiar y auto-formatear
            var valLimpio = this.value.replace(/[^0-9kK]/gi, '').toUpperCase();
            if (valLimpio.length > 1) {
                var cuerpo = valLimpio.slice(0, -1);
                var dv = valLimpio.slice(-1);
                this.value = cuerpo + '-' + dv;
            } else {
                this.value = valLimpio;
            }

            var val = this.value.trim();
            if (val === '') {
                this.classList.remove('is-valid', 'is-invalid');
                rutFeedback.className = 'form-text text-muted';
                rutFeedback.innerHTML = 'Ingresa el RUT con guion y dígito verificador.';
                var btnSubmit = document.getElementById('btn-submit-usuario');
                if(btnSubmit) btnSubmit.disabled = false;
                return;
            }
            if (validarRut(val)) {
                rutFeedback.className = 'form-text text-info font-weight-bold';
                rutFeedback.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Verificando disponibilidad...';
                this.classList.remove('is-invalid', 'is-valid');
                
                clearTimeout(rutTimeout);
                var inputElem = this;
                rutTimeout = setTimeout(function() {
                    fetch('/tickets/api/search/users/?q=' + val)
                    .then(r => r.json())
                    .then(res => {
                        var exists = res.results && res.results.some(u => u.rut.toUpperCase() === val.toUpperCase());
                        if (exists) {
                            inputElem.classList.remove('is-valid');
                            inputElem.classList.add('is-invalid');
                            rutFeedback.className = 'form-text text-danger font-weight-bold';
                            rutFeedback.innerHTML = '<i class="fas fa-exclamation-triangle"></i> El RUT ya se encuentra registrado.';
                            var btnSubmit = document.getElementById('btn-submit-usuario');
                            if(btnSubmit) btnSubmit.disabled = true;
                        } else {
                            inputElem.classList.remove('is-invalid');
                            inputElem.classList.add('is-valid');
                            rutFeedback.className = 'form-text text-success font-weight-bold';
                            rutFeedback.innerHTML = '<i class="fas fa-check-circle"></i> RUT Válido y Disponible';
                            var btnSubmit = document.getElementById('btn-submit-usuario');
                            if(btnSubmit) btnSubmit.disabled = false;
                        }
                    }).catch(err => {
                        inputElem.classList.add('is-valid');
                        rutFeedback.className = 'form-text text-success font-weight-bold';
                        rutFeedback.innerHTML = '<i class="fas fa-check-circle"></i> RUT Válido';
                    });
                }, 400);
            } else {
                clearTimeout(rutTimeout);
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                rutFeedback.className = 'form-text text-danger font-weight-bold';
                rutFeedback.innerHTML = '<i class="fas fa-times-circle"></i> RUT Inválido';
                var btnSubmit = document.getElementById('btn-submit-usuario');
                if(btnSubmit) btnSubmit.disabled = true;
            }
        });
    }

    var correoInput = document.getElementById('correo_nuevo');
    var correoFeedback = document.getElementById('correo_feedback');
    if (correoInput) {
        correoInput.addEventListener('input', function() {
            var val = this.value.trim();
            if (val === '') {
                this.classList.remove('is-valid', 'is-invalid');
                correoFeedback.className = 'form-text text-muted';
                correoFeedback.innerHTML = 'Opcional, pero recomendado.';
                return;
            }
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailRegex.test(val)) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                correoFeedback.className = 'form-text text-success font-weight-bold';
                correoFeedback.innerHTML = '<i class="fas fa-check-circle"></i> Correo Válido';
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
                correoFeedback.className = 'form-text text-danger font-weight-bold';
                correoFeedback.innerHTML = '<i class="fas fa-times-circle"></i> Correo Inválido';
            }
        });
    }

    // Auto-Refresh Kanban Ligero
    setInterval(function() {
        if (!document.getElementById('panel-kanban').classList.contains('active')) return;
        
        fetch('/tickets/api/sync/')
        .then(r => r.json())
        .then(res => {
            if (res.success) {
                // Verificar si hay cambios en las cantidades
                var changed = false;
                for (var estado in res.sync) {
                    var countBadge = document.getElementById('count-' + estado);
                    if (countBadge) {
                        var currentCount = parseInt(countBadge.textContent);
                        if (currentCount !== res.sync[estado].length) {
                            changed = true;
                        }
                    }
                }
                
                // Si cambiaron, podemos recargar los datos
                if (changed) {
                    // Verificamos si hay algún modal abierto (modal-open class en body)
                    if (document.body.classList.contains('modal-open')) {
                        console.log("Cambios detectados pero hay un modal abierto. Posponiendo recarga para no interrumpir al usuario...");
                    } else {
                        console.log("Cambios detectados, recargando kanban...");
                        window.location.reload();
                    }
                }
            }
        });
    }, 30000); // 30 segundos
    var devSwitcher = document.getElementById('dev-user-switcher');
    if (devSwitcher) {
        devSwitcher.addEventListener('change', function() {
            var userId = this.value;
            if (!userId) return;
            fetch('/tickets/api/dev/switch-user/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                body: JSON.stringify({ user_id: userId })
            })
            .then(r => r.json())
            .then(res => {
                if(res.success) {
                    window.location.reload();
                } else {
                    Swal.fire('Error', res.message, 'error');
                }
            });
        });
    }

});

// --- LOGICA MODAL NUEVO TICKET ---
$(document).ready(function() {
    if ($('#solicitante-select').length === 0) return; // Si no existe el select en la vista, no hacer nada

    $('#solicitante-select').select2({
        dropdownParent: $('#modalNuevoTicket'),
        ajax: {
            url: window.TICKET_CONFIG && window.TICKET_CONFIG.urls ? window.TICKET_CONFIG.urls.apiSearchUsers : '',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { q: params.term };
            },
            processResults: function (data) {
                return { results: data.results };
            }
        },
        placeholder: 'Buscar funcionario...',
        minimumInputLength: 2,
        language: {
            inputTooShort: function() { return "Por favor ingrese 2 o más caracteres"; },
            noResults: function() { 
                return "<button class='btn btn-sm btn-primary w-100' onclick='abrirModalNuevoUsuario()'><i class='fas fa-plus'></i> Añadir Funcionario</button>"; 
            },
            searching: function() { return "Buscando..."; }
        },
        escapeMarkup: function (markup) { return markup; } // Permitir HTML en los mensajes
    });
    
    // Auto-rellenar correo si el funcionario lo tiene
    $('#solicitante-select').on('select2:select', function (e) {
        var data = e.params.data;
        var inputCorreo = document.querySelector('[name="correo_contacto"]');
        if (inputCorreo) {
            inputCorreo.value = data.correo ? data.correo : '';
        }
        validateFormProgress();
    });
    $('#solicitante-select').on('change', validateFormProgress);
    
    // Enfocar campo de búsqueda al abrir modal
    $('#modalNuevoTicket').on('shown.bs.modal', function () {
        $('#solicitante-select').select2('open');
    });
    
    // Select2 para activo
    $('#activo-select').select2({
        dropdownParent: $('#modalNuevoTicket'),
        placeholder: '-- Sin equipo específico --',
        allowClear: true
    });

    $('select[name="categoria_id"], select[name="impacto"], select[name="urgencia"]').select2({
        dropdownParent: $('#modalNuevoTicket'),
        minimumResultsForSearch: Infinity,
        placeholder: '-- Seleccionar --',
        width: '100%'
    });
    $('select[name="categoria_id"]').on('change', validateFormProgress);
    
    // Validación de texto
    var descInput = document.querySelector('[name="descripcion"]');
    if(descInput) {
        descInput.addEventListener('input', validateFormProgress);
    }

    function validateFormProgress() {
        var sol = $('#solicitante-select').val();
        var cat = $('select[name="categoria_id"]').val();
        var desc = $('[name="descripcion"]').val() ? $('[name="descripcion"]').val().trim() : '';
        
        var total = 3;
        var valid = 0;
        
        // Solicitante
        var solContainer = $('#solicitante-select').next('.select2-container');
        if (sol) { valid++; solContainer.removeClass('ms-val-error').addClass('ms-val-success'); }
        else if (solContainer.hasClass('ms-val-error') || solContainer.hasClass('ms-val-success')) { solContainer.removeClass('ms-val-success ms-val-error'); }
        
        // Categoria
        var catContainer = $('select[name="categoria_id"]').next('.select2-container');
        if (cat) { valid++; catContainer.removeClass('ms-val-error').addClass('ms-val-success'); }
        else if (catContainer.hasClass('ms-val-error') || catContainer.hasClass('ms-val-success')) { catContainer.removeClass('ms-val-success ms-val-error'); }
        
        // Descripcion
        var dInput = $('[name="descripcion"]');
        if (desc.length > 0) { valid++; dInput.removeClass('ms-val-error').addClass('ms-val-success'); }
        else if (dInput.hasClass('ms-val-error') || dInput.hasClass('ms-val-success')) { dInput.removeClass('ms-val-success ms-val-error'); }
        
        var pct = (valid / total) * 100;
        var bar = document.getElementById('tk-progress-bar');
        if(bar) {
            bar.style.width = pct + '%';
        }
    }
});

window.abrirModalNuevoUsuario = function() {
    var searchTerm = $('.select2-search__field').val() || '';
    $('#solicitante-select').select2('close');
    
    document.getElementById('form-crear-usuario').reset();
    
    var rutInput = document.querySelector('input[name="rut_nuevo"]');
    var nombresInput = document.querySelector('input[name="nombres_nuevo"]');
    
    if (searchTerm.trim() !== '') {
        if (/\d/.test(searchTerm)) {
            rutInput.value = searchTerm;
        } else {
            nombresInput.value = searchTerm;
        }
    }
    
    $('#modalCrearUsuario').modal('show');
    
    setTimeout(function() {
        if (rutInput.value) {
            nombresInput.focus();
        } else {
            rutInput.focus();
        }
    }, 500);
};

// KEDB Integration
var kedbTimer = null;
$('#tk-descripcion').on('input', function() {
    var query = $(this).val();
    clearTimeout(kedbTimer);
    
    if (query.length < 5) {
        $('#kedb-container').hide();
        return;
    }
    
    kedbTimer = setTimeout(function() {
        $.ajax({
            url: window.TICKET_CONFIG && window.TICKET_CONFIG.urls ? window.TICKET_CONFIG.urls.apiSearchKedb : '',
            data: { q: query },
            success: function(res) {
                if (res.results && res.results.length > 0) {
                    var html = '';
                    res.results.forEach(function(art) {
                        html += '<div style="margin-bottom:10px; border-bottom:1px solid #bbf7d0; padding-bottom:10px;">';
                        html += '<strong style="color:#166534; font-size:0.85rem;">' + art.titulo + '</strong><br>';
                        html += '<div style="font-size:0.75rem; color:#14532d; margin-top:4px;">' + art.solucion + '</div>';
                        html += '</div>';
                    });
                    $('#kedb-results').html(html);
                    $('#kedb-container').fadeIn();
                } else {
                    $('#kedb-container').hide();
                }
            }
        });
    }, 500);

    /* ---- SORTABLE JS (DRAG & DROP) ---- */
    if (typeof Sortable !== 'undefined') {
        var columns = document.querySelectorAll('.kanban-column');
        columns.forEach(function(col) {
            new Sortable(col, {
                group: 'kanban', // set both lists to same group
                animation: 150,
                ghostClass: 'sortable-ghost',
                onEnd: function (evt) {
                    var itemEl = evt.item;  // dragged HTMLElement
                    var toList = evt.to;    // target list
                    var newStatus = toList.id.replace('column-', ''); // column-NUEVO -> NUEVO
                    var ticketId = itemEl.dataset.id;
                    
                    if (evt.from === evt.to) return; // Didn't change column

                    // Call backend to update status
                    fetch('/tickets/api/action/', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
                        body: JSON.stringify({ id: ticketId, estado: newStatus })
                    })
                    .then(r => r.json())
                    .then(res => {
                        if (!res.success) {
                            // Revert change
                            evt.from.appendChild(itemEl);
                            Swal.fire({ icon: 'error', title: 'Error', text: res.message || 'No se pudo cambiar el estado.', confirmButtonColor: '#002855' });
                        } else {
                            // Update badges and empty states
                            var fromStatus = evt.from.id.replace('column-', '');
                            var countFrom = document.getElementById('count-' + fromStatus);
                            var countTo = document.getElementById('count-' + newStatus);
                            
                            updateColumnEmptyState(evt.from, fromStatus);
                            updateColumnEmptyState(evt.to, newStatus);
                            
                            if (countFrom) countFrom.textContent = evt.from.querySelectorAll('.kanban-card').length;
                            if (countTo) countTo.textContent = evt.to.querySelectorAll('.kanban-card').length;
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        evt.from.appendChild(itemEl); // Revert
                        Swal.fire('Error', 'Error de conexión', 'error');
                    });
                },
            });
        });
    }

    /* ---- Resaltado Visual (Highlight) de URL ---- */
    const urlParams = new URLSearchParams(window.location.search);
    const hlCorrelativo = urlParams.get('hl');
    if (hlCorrelativo) {
        // Encontrar la card por correlativo
        setTimeout(() => {
            let foundCard = null;
            document.querySelectorAll('.kanban-card').forEach(card => {
                const correlativoSpan = card.querySelector('.card-correlativo');
                if (correlativoSpan && correlativoSpan.textContent.trim() === hlCorrelativo) {
                    foundCard = card;
                }
            });
            
            if (foundCard) {
                // Hacer scroll
                foundCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Efecto visual
                const originalBg = foundCard.style.backgroundColor;
                foundCard.style.transition = 'all 0.5s ease';
                foundCard.style.backgroundColor = '#fff3cd';
                foundCard.style.transform = 'scale(1.02)';
                foundCard.style.boxShadow = '0 0 15px rgba(217, 119, 6, 0.5)';
                foundCard.style.border = '2px solid #d97706';
                
                // Limpiar param de URL sin recargar
                window.history.replaceState({}, document.title, window.location.pathname);
                
                setTimeout(() => {
                    foundCard.style.transform = 'scale(1)';
                    setTimeout(() => {
                        foundCard.style.backgroundColor = originalBg;
                        foundCard.style.boxShadow = '';
                        foundCard.style.border = '';
                    }, 3000);
                }, 500);
            }
        }, 500); // Dar tiempo al render
    }

}); // fin DOMContentLoaded