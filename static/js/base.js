// Configuración global de CSRF para AJAX en Django
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
    const csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    // Acción de Logout mediante AJAX seguro (método POST)
    $('#logout-button').on('click', function(e) {
      e.preventDefault();
      $.ajax({
        url: window.BASE_CONFIG.logoutUrl,
        type: 'POST',
        dataType: 'json',
        success: function(response) {
          if (response.success) {
            window.location.href = response.redirect_url;
          }
        },
        error: function(xhr) {
          console.error("Error al cerrar sesión", xhr);
          window.location.href = "/login/";
        }
      });
    });

    // Control del Sidebar responsivo (Móviles y Escritorio)
    $('#sidebar-toggle, #sidebar-backdrop').on('click', function() {
      if ($(window).width() < 992) {
        $('body').toggleClass('show-sidebar');
        $('body').removeClass('sidebar-collapsed');
      } else {
        $('body').toggleClass('sidebar-collapsed');
        $('body').removeClass('show-sidebar');
      }
      adjustResponsiveFooter();
    });

    $('#logout-sidebar-link').on('click', function(e) {
      e.preventDefault();
      $('#logout-button').click();
    });

    // Ajustes responsivos dinámicos del Footer
    function adjustResponsiveFooter() {
      if ($(window).width() < 992 || $('body').hasClass('no-sidebar') || $('body').hasClass('sidebar-collapsed')) {
        $('#footer-main').css('margin-left', '0');
      } else {
        $('#footer-main').css('margin-left', '200px');
      }
    }
    $(window).on('resize', adjustResponsiveFooter);
    adjustResponsiveFooter();

    // Dev User Switcher
    $('#dev-user-switcher').on('change', function() {
      var userId = $(this).val();
      if (!userId) return;
      $.ajax({
        url: '/switch_user/',
        type: 'POST',
        data: JSON.stringify({ user_id: userId }),
        contentType: 'application/json',
        success: function(resp) {
          if (resp.success) {
            window.location.href = resp.redirect_url;
          } else {
            alert(resp.message);
          }
        },
        error: function(err) {
          alert('Error al cambiar de usuario.');
        }
      });
    });

// Utilidad global para formatear RUT
function formatearRut(input) {
    // Eliminar caracteres inválidos (deja solo números y K)
    let value = input.value.replace(/[^0-9kK]/g, '').toUpperCase();
    
    if (value.length > 1) {
        let cuerpo = value.slice(0, -1);
        let dv = value.slice(-1);
        // Limitar largo máximo del cuerpo a 8 dígitos (ej: 30.000.000 -> 8 chars)
        if (cuerpo.length > 8) {
            cuerpo = cuerpo.slice(0, 8);
        }
        input.value = cuerpo + '-' + dv;
    } else {
        input.value = value;
    }
}

// --- Notificaciones Globales de Tickets ---
function checkNotificaciones() {
    if ($('#navbarNotifDropdown').length === 0) return;
    
    $.ajax({
        url: '/tickets/api/notificaciones/',
        type: 'GET',
        success: function(response) {
            if (response.success) {
                let currentCount = parseInt($('#notif-badge').text()) || 0;
                let newCount = response.count;
                
                if (newCount > 0) {
                    $('#notif-badge').text(newCount).show();
                    
                    // Solo mostramos toast si hay NUEVOS tickets que antes no estaban
                    if (newCount > currentCount && currentCount > 0) {
                        if (typeof Swal !== 'undefined') {
                            Swal.fire({
                                toast: true,
                                position: 'top-end',
                                icon: 'info',
                                title: 'Tienes ' + (newCount - currentCount) + ' nueva(s) notificación(es)',
                                showConfirmButton: false,
                                timer: 3000
                            });
                        }
                    }
                } else {
                    $('#notif-badge').hide().text('0');
                }
                
                // Actualizar la lista en el dropdown
                let notifHtml = '';
                if (response.tickets.length > 0) {
                    response.tickets.forEach(function(t) {
                        let bgClass = t.leida ? 'bg-white' : 'bg-light';
                        let fwClass = t.leida ? 'font-weight-normal' : 'font-weight-bold';
                        let dot = t.leida ? '' : '<span style="height:8px;width:8px;background-color:#007bff;border-radius:50%;display:inline-block;margin-right:5px;"></span>';
                        let hlParam = t.correlativo !== 'Sistema' ? `?hl=${t.correlativo}` : '';
                        
                        notifHtml += `
                            <div class="dropdown-item border-bottom py-2 ${bgClass}" style="position:relative; white-space: normal; cursor:pointer;" onclick="marcarLeidaAndGo(${t.id}, '/tickets/${hlParam}')">
                                <div class="d-flex w-100 justify-content-between align-items-center">
                                    <h6 class="mb-1 ${fwClass} text-dark" style="font-size: 0.85rem;">${dot}${t.correlativo}</h6>
                                    <span class="text-muted" style="font-size: 0.65rem;">${t.fecha}</span>
                                </div>
                                <p class="mb-1 small ${fwClass} text-muted" style="font-size: 0.8rem;">${t.descripcion}</p>
                            </div>
                        `;
                    });
                    // Add mark all as read button at the end
                    if (newCount > 0) {
                        notifHtml += `
                            <div class="dropdown-divider m-0"></div>
                            <a href="#" class="dropdown-item text-center text-primary py-2 font-weight-bold" onclick="marcarTodasLeidas(event)" style="font-size: 0.85rem;">
                                Marcar todas como leídas
                            </a>
                        `;
                    }
                } else {
                    notifHtml = '<span class="dropdown-item-text text-muted small py-3 text-center d-block">No tienes notificaciones nuevas.</span>';
                }
                $('#notif-list').html(notifHtml);
            }
        },
        error: function(xhr) {
            console.error("Error al obtener notificaciones", xhr);
        }
    });
}

function marcarLeidaAndGo(notificacionId, url) {
    $.ajax({
        url: `/tickets/api/notificaciones/${notificacionId}/leida/`,
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function() {
            window.location.href = url;
        },
        error: function() {
            window.location.href = url;
        }
    });
}

function marcarTodasLeidas(e) {
    e.preventDefault();
    e.stopPropagation();
    $.ajax({
        url: '/tickets/api/notificaciones/todas-leidas/',
        type: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function() {
            checkNotificaciones();
        }
    });
}

// Helper to get CSRF token
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

$(document).ready(function() {
    // Check inicial
    checkNotificaciones();
    // Polling cada 60 segundos
    setInterval(checkNotificaciones, 60000);
});
