$(document).ready(function() {
  
  // ==========================================
  // 1. Funciones de Utilidad y Validaciones de RUT
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
    if (dvr === 11) {
      dvEsperado = '0';
    } else if (dvr === 10) {
      dvEsperado = 'K';
    } else {
      dvEsperado = String(dvr);
    }
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

  function renderFotoPreview(fotoUrl, containerId) {
    const $container = $(containerId);
    if (fotoUrl) {
      $container.html(`<img src="${fotoUrl}" style="width:100%;height:100%;object-fit:cover;">`);
    } else {
      $container.html('<i class="fas fa-user-circle" style="font-size:64px;color:#94a3b8;"></i>');
    }
  }

  function setupFotoInput(modalPrefix) {
    $(`#${modalPrefix}-foto`).on('change', function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          $(`#${modalPrefix}-foto-preview`).html(
            `<img src="${e.target.result}" style="width:100%;height:100%;object-fit:cover;">`
          );
        };
        reader.readAsDataURL(file);
      }
    });
  }

  $('#crear-rut, #editar-rut').on('input', function() {
    const val = $(this).val();
    $(this).val(formatRutInput(val));
    // Live validation
    if (val.length >= 8) {
      if (validarRut($(this).val())) {
        $(this).removeClass('is-invalid').addClass('is-valid');
      } else {
        $(this).removeClass('is-valid').addClass('is-invalid');
      }
    } else {
      $(this).removeClass('is-valid is-invalid');
    }
  });

  let lastSearchedRut = '';

  $('#crear-rut, #editar-rut').on('blur', function() {
    const $input = $(this);
    const rut = $input.val();
    const isCrear = $input.attr('id') === 'crear-rut';

    if (rut && !validarRut(rut)) {
      $input.removeClass('is-valid').addClass('is-invalid');
    } else if (rut) {
      $input.removeClass('is-invalid').addClass('is-valid');
      
      // Auto-relleno inteligente si es RUT válido y estamos creando (o editando si quieren)
      if (rut !== lastSearchedRut) {
        lastSearchedRut = rut;
        
        $.ajax({
          url: '/api/funcionarios/buscar_por_rut/',
          type: 'GET',
          data: { rut: rut },
          success: function(res) {
            if (res.success && res.data) {
              const prefix = isCrear ? '#crear-' : '#editar-';
              
              if (!$(prefix + 'nombres').val()) $(prefix + 'nombres').val(res.data.nombres);
              if (!$(prefix + 'apellidos').val()) $(prefix + 'apellidos').val(res.data.apellidos);
              if (!$(prefix + 'email').val() && res.data.correo) $(prefix + 'email').val(res.data.correo).trigger('input');
              
              if (res.data.unidad) {
                const $unidadSelect = $(prefix + 'unidad');
                // Buscar si la unidad existe en el select
                let found = false;
                $unidadSelect.find('option').each(function() {
                  if ($(this).text() === res.data.unidad || $(this).val() === res.data.unidad) {
                    $unidadSelect.val($(this).val()).trigger('change');
                    found = true;
                  }
                });
              }

              // Pequeño aviso de que se autocompletó
              Swal.fire({
                toast: true,
                position: 'top-end',
                icon: 'success',
                title: 'Datos recuperados automáticamente',
                showConfirmButton: false,
                timer: 3000
              });
            }
          }
        });
      }
    }
  });

  // Validacion de correo en tiempo real
  $('#crear-email, #editar-email').on('input blur', function() {
    const email = $(this).val().trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email.length > 0) {
      if (emailRegex.test(email)) {
        $(this).removeClass('is-invalid').addClass('is-valid');
      } else {
        $(this).removeClass('is-valid').addClass('is-invalid');
      }
    } else {
      $(this).removeClass('is-valid is-invalid');
    }
  });


  // ==========================================
  // 2. Inicialización de DataTable (Server-Side)
  // ==========================================
  
  setupFotoInput('crear');
  setupFotoInput('editar');



  $('#crear-unidad, #editar-unidad').select2({
    theme: 'bootstrap4',
    placeholder: '-- Seleccionar Unidad --',
    width: '100%'
  });

  const table = $('#tabla-usuarios').DataTable({
    processing: true,
    serverSide: true,
    responsive: true,
    order: [[8, 'desc']],
    pageLength: 10,
    language: {
      search: 'Buscar:',
      searchPlaceholder: 'Buscar...',
      lengthMenu: 'Mostrar _MENU_ registros',
      info: 'Mostrando _START_ a _END_ de _TOTAL_ registros',
      infoEmpty: 'Mostrando 0 registros',
      infoFiltered: '(filtrado de _MAX_ registros totales)',
      zeroRecords: 'No se encontraron registros',
      loadingRecords: 'Cargando...',
      processing: 'Procesando...',
      paginate: {
        first: 'Primero',
        last: 'Último',
        next: 'Siguiente',
        previous: 'Anterior',
      },
    },
    ajax: {
      url: '/api/usuarios/',
      type: 'POST'
    },
    columns: [
      {
        data: 'foto_url',
        orderable: false,
        render: function(data, type, row) {
          if (data) {
            return `<img src="${data}" style="width:32px;height:32px;border-radius:50%;object-fit:cover;">`;
          }
          return `<i class="fas fa-user-circle" style="font-size:28px;color:#94a3b8;"></i>`;
        }
      },
      { 
        data: 'rut',
        className: 'font-weight-bold text-gob-azul'
      },
      { data: 'nombres' },
      { data: 'apellidos' },
      { data: 'email' },
      { data: 'unidad' },
      { 
        data: 'grupos',
        orderable: false,
        render: function(data, type, row) {
          if (!data || data.length === 0) return '<span class="text-muted small">Sin Grupos</span>';
          return data.map(g => `<span class="badge badge-gob-azul mr-1">${g.nombre}</span>`).join('');
        }
      },
      { 
        data: 'is_active',
        render: function(data, type, row) {
          const checked = data ? 'checked' : '';
          return `
            <div class="custom-control custom-switch" style="display: flex; justify-content: center;">
              <input type="checkbox" class="custom-control-input toggle-activo" id="toggle-activo-${row.id}" 
                data-id="${row.id}" 
                data-rut="${row.rut}" 
                data-nombres="${row.nombres}" 
                data-apellidos="${row.apellidos}" 
                data-email="${row.email}" 
                data-unidad="${row.unidad}" 
                data-grupos='${JSON.stringify(row.grupos.map(g => g.id))}' 
                ${checked}>
              <label class="custom-control-label" for="toggle-activo-${row.id}" style="cursor: pointer;"></label>
            </div>
          `;
        }
      },
      {
        data: null,
        orderable: false,
        className: 'text-center',
        render: function(data, type, row) {
          const $acciones = $('#dt-templates .tmpl-acciones').clone();
          
          $acciones.find('.btn-editar-usuario').attr({
            'data-id': row.id,
            'data-rut': row.rut,
            'data-nombres': row.nombres,
            'data-apellidos': row.apellidos,
            'data-email': row.email,
            'data-unidad': row.unidad,
            'data-foto-url': row.foto_url || '',
            'data-is-active': row.is_active ? 'true' : 'false',
            'data-rol': row.rol_id || '',
            'data-grupos': JSON.stringify(row.grupos.map(g => g.id))
          });
          
          return $acciones.prop('outerHTML');
        }
      }
    ]
  });


  // ==========================================
  // 3. Crear Funcionario / Operador
  // ==========================================

  const $formCrear = $('#form-crear-usuario');
  const $alertCrear = $('#crear-error-alert');
  const $btnCrear = $('#btn-crear-submit');

  $('[data-target="#modalCrearUsuario"]').on('click', function() {
    $formCrear[0].reset();
    $formCrear.removeClass('was-validated');
    $('#crear-rut').removeClass('is-invalid');
    $alertCrear.addClass('d-none');
    renderFotoPreview('', '#crear-foto-preview');
    $('#crear-foto').val('');
    $('.crear-grupo-checkbox').prop('checked', false);
    $('#crear-activo').prop('checked', true);
  });

  $formCrear.on('submit', function(e) {
    e.preventDefault();
    $alertCrear.addClass('d-none');
    
    const rut = $('#crear-rut').val().trim();
    const email = $('#crear-email').val().trim();
    const nombres = $('#crear-nombres').val().trim();
    const apellidos = $('#crear-apellidos').val().trim();
    const unidad = $('#crear-unidad').val().trim();
    const contrasena = $('#crear-contrasena').val();
    const fotoElement = $('#crear-foto')[0];
    const foto = fotoElement ? fotoElement.files[0] : null;
    const is_active = $('#crear-activo').is(':checked');
    const grupos = [];
    $('.crear-grupo-checkbox:checked').each(function() {
      grupos.push($(this).val());
    });
    const rol = $('#crear-rol').val();

    let clientValid = true;
    let errorMsg = '';

    if (rut && !validarRut(rut)) {
      $('#crear-rut').addClass('is-invalid');
      clientValid = false;
      errorMsg = 'El RUT ingresado no es válido.';
    } else {
      $('#crear-rut').removeClass('is-invalid');
    }

    if (!$formCrear[0].checkValidity() || !clientValid) {
      $formCrear.addClass('was-validated');
      if (!errorMsg && !$('#crear-email')[0].checkValidity()) {
        errorMsg = 'El correo electrónico no es válido.';
      } else if (!errorMsg) {
        errorMsg = 'Por favor, complete correctamente todos los campos obligatorios.';
      }
      Swal.fire({
        icon: 'warning',
        title: 'Atención',
        text: errorMsg,
        confirmButtonColor: '#005a9c'
      });
      return;
    }

    $btnCrear.prop('disabled', true);
    $btnCrear.find('span').first().addClass('d-none');
    $btnCrear.find('.spinner-border').removeClass('d-none');

    const formData = new FormData();
    formData.append('rut', rut);
    formData.append('email', email);
    formData.append('nombres', nombres);
    formData.append('apellidos', apellidos);
    formData.append('unidad', unidad);
    formData.append('cargo', 'Funcionario'); // Default por ahora
    formData.append('grado', '10'); // Default por ahora
    formData.append('contrasena', contrasena);
    formData.append('is_active', is_active);
    formData.append('grupos', JSON.stringify(grupos));
    formData.append('rol', rol);
    if (foto) {
      formData.append('foto', foto);
    }

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      dataType: 'json',
      success: function(response) {
        if (response.success) {
          Swal.fire({
            icon: 'success',
            title: '¡Funcionario Creado!',
            text: response.message,
            confirmButtonColor: '#005a9c'
          });
          $('#modalCrearUsuario').modal('hide');
          $formCrear[0].reset();
          $formCrear.removeClass('was-validated');
          table.ajax.reload();
        }
      },
      error: function(xhr) {
        let msg = 'Ocurrió un error al registrar el funcionario.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        $alertCrear.text(msg).removeClass('d-none');
      },
      complete: function() {
        $btnCrear.prop('disabled', false);
        $btnCrear.find('span').first().removeClass('d-none');
        $btnCrear.find('.spinner-border').addClass('d-none');
      }
    });
  });


  // ==========================================
  // 4. Editar Funcionario / Operador
  // ==========================================

  const $formEditar = $('#form-editar-usuario');
  const $alertEditar = $('#editar-error-alert');
  const $btnEditar = $('#btn-editar-submit');

  $(document).on('click', '.btn-editar-usuario', function() {
    const id = $(this).data('id');
    const rut = $(this).data('rut');
    const nombres = $(this).data('nombres');
    const apellidos = $(this).data('apellidos');
    const email = $(this).data('email');
    const unidad = $(this).data('unidad');
    const fotoUrl = $(this).attr('data-foto-url');
    const isActive = $(this).data('is-active') === true || $(this).data('is-active') === 'true';
    const grupos = $(this).data('grupos') || [];
    const rol = $(this).data('rol') || '';

    $('#editar-id').val(id).data('is-active', isActive);
    $('#editar-rut').val(rut).attr('data-original-rut', rut);
    $('#editar-nombres').val(nombres);
    $('#editar-apellidos').val(apellidos);
    $('#editar-email').val(email);
    $('#editar-rol').val(rol);
    
    // Si la unidad no existe en el select (dato heredado), la creamos temporalmente
    if (unidad && $('#editar-unidad').find("option[value='" + unidad + "']").length === 0) {
      $('#editar-unidad').append(new Option(unidad, unidad, true, true));
    }
    $('#editar-unidad').val(unidad).trigger('change');
    $('#editar-contrasena').val('');
    
    // Set checkboxes for grupos
    $('.editar-grupo-checkbox').prop('checked', false);
    grupos.forEach(function(groupId) {
      $(`#editar-grupo-${groupId}`).prop('checked', true);
    });

    renderFotoPreview(fotoUrl, '#editar-foto-preview');
    $('#editar-foto').val('');

    $formEditar.removeClass('was-validated');
    $alertEditar.addClass('d-none');

    $('#modalEditarUsuario').modal('show');
  });

  $formEditar.on('submit', function(e) {
    e.preventDefault();
    $alertEditar.addClass('d-none');

    const id = $('#editar-id').val();
    const rut = $('#editar-rut').val().trim();
    const nombres = $('#editar-nombres').val().trim();
    const apellidos = $('#editar-apellidos').val().trim();
    const email = $('#editar-email').val().trim();
    const unidad = $('#editar-unidad').val().trim();
    const contrasena = $('#editar-contrasena').val();
    const fotoElement = $('#editar-foto')[0];
    const foto = fotoElement ? fotoElement.files[0] : null;
    const is_active = $('#editar-id').data('is-active'); 
    const rol = $('#editar-rol').val();
    const grupos = [];
    $('.editar-grupo-checkbox:checked').each(function() {
      grupos.push($(this).val());
    });

    let clientValid = true;
    let errorMsg = '';
    const originalRut = $('#editar-rut').attr('data-original-rut');

    if (rut && rut !== originalRut) {
      if (!validarRut(rut)) {
        $('#editar-rut').addClass('is-invalid');
        clientValid = false;
        errorMsg = 'El nuevo RUT ingresado no es válido.';
      } else {
        $('#editar-rut').removeClass('is-invalid');
      }
    } else {
      $('#editar-rut').removeClass('is-invalid');
    }

    if (!$formEditar[0].checkValidity() || !clientValid) {
      $formEditar.addClass('was-validated');
      if (!errorMsg && !$('#editar-email')[0].checkValidity()) {
        errorMsg = 'El correo electrónico no es válido.';
      } else if (!errorMsg) {
        errorMsg = 'Por favor, complete correctamente todos los campos obligatorios.';
      }
      Swal.fire({
        icon: 'warning',
        title: 'Error de Validación',
        text: errorMsg,
        confirmButtonColor: '#005a9c'
      });
      return;
    }

    $btnEditar.prop('disabled', true);
    $btnEditar.find('span').first().addClass('d-none');
    $btnEditar.find('.spinner-border').removeClass('d-none');

    const formData = new FormData();
    formData.append('_method', 'PUT');
    formData.append('id', id);
    formData.append('rut', rut);
    formData.append('nombres', nombres);
    formData.append('apellidos', apellidos);
    formData.append('email', email);
    formData.append('unidad', unidad);
    formData.append('cargo', 'Funcionario');
    formData.append('grado', '10');
    formData.append('is_active', is_active);
    formData.append('grupos', JSON.stringify(grupos));
    formData.append('rol', rol);
    
    if (contrasena) {
      formData.append('contrasena', contrasena);
    }
    if (foto) {
      formData.append('foto', foto);
    }

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      dataType: 'json',
      success: function(response) {
        if (response.success) {
          Swal.fire({
            icon: 'success',
            title: '¡Actualizado!',
            text: response.message,
            confirmButtonColor: '#005a9c'
          });
          $('#modalEditarUsuario').modal('hide');
          table.ajax.reload(null, false);
        }
      },
      error: function(xhr) {
        let msg = 'Ocurrió un error al actualizar los datos.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        $alertEditar.text(msg).removeClass('d-none');
      },
      complete: function() {
        $btnEditar.prop('disabled', false);
      }
    });
  });

  // ==========================================
  // 5. Toggle Rápido de Estado (Activo/Inactivo)
  // ==========================================
  
  $(document).on('change', '.toggle-activo', function() {
    const $checkbox = $(this);
    const id = $checkbox.data('id');
    const is_active = $checkbox.is(':checked');
    const rut = $checkbox.data('rut');
    const nombres = $checkbox.data('nombres');
    const apellidos = $checkbox.data('apellidos');
    const email = $checkbox.data('email');
    const unidad = $checkbox.data('unidad');
    
    let grupos = [];
    try { grupos = JSON.parse($checkbox.attr('data-grupos') || '[]'); } catch (e) {}

    const formData = new FormData();
    formData.append('id', id);
    formData.append('rut', rut);
    formData.append('nombres', nombres);
    formData.append('apellidos', apellidos);
    formData.append('email', email);
    formData.append('unidad', unidad);
    formData.append('is_active', is_active);
    formData.append('grupos', JSON.stringify(grupos));
    formData.append('_method', 'PUT');

    $checkbox.prop('disabled', true);

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      dataType: 'json',
      success: function(response) {
        if (response.success) {
          const Toast = Swal.mixin({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true,
          });
          Toast.fire({
            icon: 'success',
            title: is_active ? 'Usuario activado' : 'Usuario desactivado'
          });
        }
      },
      error: function(xhr) {
        $checkbox.prop('checked', !is_active); // revert UI
        let msg = 'Error al cambiar el estado.';
        if (xhr.responseJSON && xhr.responseJSON.message) {
          msg = xhr.responseJSON.message;
        }
        Swal.fire('Error', msg, 'error');
      },
      complete: function() {
        $checkbox.prop('disabled', false);
      }
    });
  });

  // Autocompletado de RUT usando la base de datos de Funcionarios
  let rutTimeout;
  $('#crear-rut').on('keyup', function() {
      clearTimeout(rutTimeout);
      const query = $(this).val().replace(/[^0-9kK]/g, '');
      const $input = $(this);
      
      $('.rut-autocomplete').remove();

      if (query.length >= 3) {
          rutTimeout = setTimeout(() => {
              $.get('/tickets/api/users/search/', { q: query }, function(data) {
                  if (data.results && data.results.length > 0) {
                      let html = '<div class="dropdown-menu rut-autocomplete show" style="position:absolute; width:100%; top:100%; left:0; z-index:1000; max-height:200px; overflow-y:auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">';
                      data.results.forEach(item => {
                          // item.text tiene "Nombre (RUT) - Cargo / Unidad"
                          html += `<a class="dropdown-item rut-item" href="#" data-rut="${item.rut}" data-nombres="${item.nombres}" data-apellidos="${item.apellidos}" data-correo="${item.correo}" style="padding: 10px 15px; border-bottom: 1px solid #f1f5f9;">
                                      <strong style="color: #0f766e;">${item.rut}</strong><br>
                                      <small style="color: #475569;">${item.nombres} ${item.apellidos}</small>
                                   </a>`;
                      });
                      html += '</div>';
                      
                      const $wrapper = $input.parent();
                      $wrapper.css('position', 'relative');
                      $wrapper.append(html);
                  }
              });
          }, 400);
      }
  });

  $(document).on('click', '.rut-item', function(e) {
      e.preventDefault();
      const rut = $(this).data('rut');
      const nombres = $(this).data('nombres');
      const apellidos = $(this).data('apellidos');
      const correo = $(this).data('correo');

      $('#crear-rut').val(formatRutInput(rut)).trigger('input').trigger('blur');
      $('#crear-nombres').val(nombres);
      $('#crear-apellidos').val(apellidos);
      $('#crear-email').val(correo);
      $('.rut-autocomplete').remove();
  });

  $(document).on('click', function(e) {
      if (!$(e.target).closest('.rut-autocomplete').length && !$(e.target).is('#crear-rut')) {
          $('.rut-autocomplete').remove();
      }
  });

});
