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
                        notifHtml += `
                            <a class="dropdown-item border-bottom py-2" href="/tickets/">
                                <div class="d-flex w-100 justify-content-between">
                                    <h6 class="mb-1 font-weight-bold text-dark" style="font-size: 0.85rem;">${t.correlativo}</h6>
                                    <span class="badge badge-warning" style="font-size: 0.65rem;">${t.estado}</span>
                                </div>
                                <p class="mb-1 small text-muted text-truncate" style="max-width: 280px;" title="${t.descripcion}">${t.descripcion}</p>
                            </a>
                        `;
                    });
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

$(document).ready(function() {
    // Check inicial
    checkNotificaciones();
    // Polling cada 60 segundos
    setInterval(checkNotificaciones, 60000);
});

