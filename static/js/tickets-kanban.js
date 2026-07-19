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
                language: { url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' },
                order: [[6, 'desc']], pageLength: 25,
            });
        }
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
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">' +
                '<div style="display: flex; gap: 6px; align-items: center;">' +
                    '<span class="card-correlativo" style="background: #f1f5f9; color: #475569; padding: 2px 6px; font-size: 0.7rem; font-weight: 700;">' + t.correlativo + '</span>' +
                    '<span class="card-prio-badge" style="background:' + (t.prioridad_color || '#94a3b8') + '; color: #fff; padding: 2px 6px; font-size: 0.65rem; font-weight: 700;">' + t.prioridad + '</span>' +
                '</div>' +
                '<span style="font-size:0.65rem; color:#64748b; font-weight:600;"><i class="far fa-calendar-alt"></i> ' + (t.fecha_creacion_corta || '') + ' ' + (t.fecha_creacion_hora || '') + '</span>' +
            '</div>' +
            '<div class="card-desc" style="font-weight: 800; color: #0f172a; margin-bottom: 4px; font-size: 0.8rem; line-height: 1.2;">' + t.descripcion + '</div>' +
            '<div class="sla-timer-display" style="font-size:0.7rem; font-weight:600; margin-bottom:6px;"></div>' +
            (t.pma ? '<div class="card-pma" style="font-size:0.7rem; color:#64748b; margin-bottom:6px;"><i class="fas fa-map-marker-alt"></i> ' + t.pma + '</div>' : '') +
            '<div class="card-meta" style="font-size: 0.7rem; color: #64748b; display: flex; justify-content: space-between; align-items: center;">' +
                '<span><i class="fas fa-user"></i> ' + t.solicitante + '</span>' +
                '<span><i class="fas fa-users"></i> ' + (t.tecnico === 'Sin asignar' ? 'Sin asignar' : t.tecnico) + '</span>' +
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
                document.getElementById('oc-tk-desc').textContent = t.descripcion;
                
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

                // Lógica de visibilidad
                btnResolver.style.display = (t.estado_id !== 'RESUELTO' && t.estado_id !== 'CERRADO') ? 'inline-block' : 'none';
                if (btnPausar) {
                    btnPausar.style.display = (t.estado_id !== 'RESUELTO' && t.estado_id !== 'CERRADO' && t.estado_id !== 'PENDIENTE_PROVEEDOR') ? 'inline-block' : 'none';
                }
                if (btnTomar) {
                    btnTomar.style.display = (t.estado_id === 'NUEVO' || t.estado_id === 'ESCALADO') ? 'inline-block' : 'none';
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
                    // Para no molestar si alguien está moviendo una tarjeta, recargamos la pagina
                    // En una futura versión se puede actualizar el DOM directamente
                    console.log("Cambios detectados, recargando kanban...");
                    window.location.reload();
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
    
    // Select2 para activo y categoría
    $('#activo-select').select2({
        dropdownParent: $('#modalNuevoTicket'),
        placeholder: '-- Sin equipo específico --',
        allowClear: true
    });
    
    $('select[name="categoria_id"]').select2({
        dropdownParent: $('#modalNuevoTicket'),
        placeholder: '-- Seleccionar Categoría --'
    }).on('change', validateFormProgress);

    // Select2 para Impacto y Urgencia
    $('select[name="impacto"], select[name="urgencia"]').select2({
        dropdownParent: $('#modalNuevoTicket'),
        minimumResultsForSearch: Infinity,
        width: '100%'
    });
    
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

}); // fin DOMContentLoaded