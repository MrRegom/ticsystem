$(document).ready(function() {
  const $form = $('#login-form');
  const $alert = $('#login-error-alert');
  const $alertMsg = $('#login-error-message');
  const $btn = $('#btn-login-submit');
  const $btnText = $('#btn-text');
  const $btnSpinner = $('#btn-spinner');

  // ==========================================
  // Validaciones y Normalización de RUT
  // ==========================================

  function validarRut(rut) {
    if (typeof rut !== 'string') return false;
    rut = rut.replace(/\./g, '').replace(/\s+/g, '').toUpperCase();
    if (!/^\d{7,8}-[0-9K]$/.test(rut)) {
      return false;
    }
    const parts = rut.split('-');
    const cuerpo = parts[0];
    const dv = parts[1];
    
    let suma = 0;
    let multiplo = 2;
    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(cuerpo.charAt(i), 10) * multiplo;
      multiplo = (multiplo === 7) ? 2 : multiplo + 1;
    }
    const dvr = 11 - (suma % 11);
    let dvEsperado = '0';
    if (dvr === 11) dvEsperado = '0';
    else if (dvr === 10) dvEsperado = 'K';
    else dvEsperado = String(dvr);
    
    return dvEsperado === dv;
  }

  function formatRutInput(value) {
    let clean = value.replace(/[^0-9kK]/g, '').toUpperCase();
    if (clean.length === 0) return '';
    if (clean.length > 1) {
      const cuerpo = clean.slice(0, -1);
      const dv = clean.slice(-1);
      return `${cuerpo}-${dv}`;
    }
    return clean;
  }

  // Formatear dinámicamente si el usuario ingresa números
  $('#username').on('input', function() {
    const val = $(this).val();
    // Si el valor comienza con un número, asumimos que es un RUT y lo formateamos
    if (/^\d/.test(val)) {
      $(this).val(formatRutInput(val));
    }
    // Ocultar mensajes de error al escribir
    $('#username-error-required').hide();
    $('#username-error-format').hide();
  });

  $form.on('submit', function(e) {
    e.preventDefault();
    
    // Resetear alertas
    $alert.addClass('d-none');
    $form.removeClass('was-validated');
    $('#username-error-required').hide();
    $('#username-error-format').hide();

    let username = $('#username').val().trim();
    const password = $('#password').val();

    // Validación básica del lado del cliente
    let isValid = true;
    
    if (!username) {
      $('#username-error-required').show();
      isValid = false;
    } else {
      // Si parece ser un RUT (empieza con un dígito o tiene formato de RUT), validarlo
      if (/^\d/.test(username) || /^[0-9.-]+[0-9kK]$/.test(username)) {
        // Normalizar primero para la validación
        username = username.replace(/\./g, '').replace(/\s+/g, '').toUpperCase();
        if (!username.includes('-') && username.length > 1) {
          username = username.slice(0, -1) + '-' + username.slice(-1);
        }
        
        if (!validarRut(username)) {
          $('#username-error-format').show();
          isValid = false;
        }
      }
    }

    if (!password) {
      $('#password').parent().next('.invalid-feedback').show();
      isValid = false;
    }

    if (!isValid) {
      $form.addClass('was-validated');
      return;
    }

    // Cambiar estado del botón de envío
    $btn.prop('disabled', true);
    $btnText.addClass('d-none');
    $btnSpinner.removeClass('d-none');

    // Envío de la solicitud mediante AJAX
    $.ajax({
      url: '/login/',
      type: 'POST',
      contentType: 'application/json',
      headers: {
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      data: JSON.stringify({
        username: username,
        password: password
      }),
      dataType: 'json',
      success: function(response) {
        if (response.success) {
          // Redirección exitosa
          window.location.href = response.redirect_url;
        } else {
          showError(response.message || 'Error de autenticación.');
        }
      },
      error: function(xhr) {
        let msg = 'Ocurrió un error inesperado. Por favor intente más tarde.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        } else if (xhr.status === 401) {
          msg = 'RUT/Usuario o contraseña incorrectos.';
        } else if (xhr.status === 403) {
          msg = 'Cuenta deshabilitada.';
        } else if (xhr.status === 429) {
          msg = 'Acceso bloqueado por múltiples intentos fallidos (Espere 30 min).';
        }
        showError(msg);
      }
    });
  });

  function showError(message) {
    $alertMsg.text(message);
    $alert.removeClass('d-none');
    
    // Restaurar estado del botón
    $btn.prop('disabled', false);
    $btnText.removeClass('d-none');
    $btnSpinner.addClass('d-none');
  }
});
