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
  });

  $('#crear-rut, #editar-rut').on('blur', function() {
    const rut = $(this).val();
    if (rut && !validarRut(rut)) {
      $(this).addClass('is-invalid');
    } else {
      $(this).removeClass('is-invalid');
    }
  });


  // ==========================================
  // 2. Inicialización de DataTable (Server-Side)
  // ==========================================
  
  setupFotoInput('crear');
  setupFotoInput('editar');

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
      { data: 'cargo' },
      { data: 'grado' },
      { data: 'fecha_registro' },
      {
        data: null,
        orderable: false,
        render: function(data, type, row) {
          const $acciones = $('#dt-templates .tmpl-acciones').clone();
          
          $acciones.find('.btn-editar-usuario').attr({
            'data-id': row.id,
            'data-rut': row.rut,
            'data-nombres': row.nombres,
            'data-apellidos': row.apellidos,
            'data-email': row.email,
            'data-unidad': row.unidad,
            'data-cargo': row.cargo,
            'data-grado': row.grado,
            'data-foto-url': row.foto_url || ''
          });
          
          $acciones.find('.btn-eliminar-usuario').attr({
            'data-id': row.id,
            'data-rut': row.rut,
            'data-nombre': `${row.nombres} ${row.apellidos}`
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
  });

  $formCrear.on('submit', function(e) {
    e.preventDefault();
    $alertCrear.addClass('d-none');
    
    const rut = $('#crear-rut').val().trim();
    const email = $('#crear-email').val().trim();
    const nombres = $('#crear-nombres').val().trim();
    const apellidos = $('#crear-apellidos').val().trim();
    const unidad = $('#crear-unidad').val().trim();
    const cargo = $('#crear-cargo').val().trim();
    const grado = $('#crear-grado').val().trim();
    const contrasena = $('#crear-contrasena').val();
    const foto = $('#crear-foto')[0].files[0];

    let clientValid = true;

    if (!validarRut(rut)) {
      $('#crear-rut').addClass('is-invalid');
      clientValid = false;
    } else {
      $('#crear-rut').removeClass('is-invalid');
    }

    if (!$formCrear[0].checkValidity() || !clientValid) {
      $formCrear.addClass('was-validated');
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
    formData.append('cargo', cargo);
    formData.append('grado', grado);
    formData.append('contrasena', contrasena);
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
    const cargo = $(this).data('cargo');
    const grado = $(this).data('grado');
    const fotoUrl = $(this).data('foto-url');

    $('#editar-id').val(id);
    $('#editar-rut').val(rut).removeClass('is-invalid');
    $('#editar-nombres').val(nombres);
    $('#editar-apellidos').val(apellidos);
    $('#editar-email').val(email);
    $('#editar-unidad').val(unidad);
    $('#editar-cargo').val(cargo);
    $('#editar-grado').val(grado);
    $('#editar-contrasena').val('');

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
    const cargo = $('#editar-cargo').val().trim();
    const grado = $('#editar-grado').val().trim();
    const contrasena = $('#editar-contrasena').val();
    const foto = $('#editar-foto')[0].files[0];

    let clientValid = true;

    if (rut && (/^\d/.test(rut) || rut.length > 5)) {
      if (!validarRut(rut)) {
        $('#editar-rut').addClass('is-invalid');
        clientValid = false;
      } else {
        $('#editar-rut').removeClass('is-invalid');
      }
    } else {
      $('#editar-rut').removeClass('is-invalid');
    }

    if (!$formEditar[0].checkValidity() || !clientValid) {
      $formEditar.addClass('was-validated');
      return;
    }

    $btnEditar.prop('disabled', true);

    const formData = new FormData();
    formData.append('id', id);
    formData.append('rut', rut);
    formData.append('nombres', nombres);
    formData.append('apellidos', apellidos);
    formData.append('email', email);
    formData.append('unidad', unidad);
    formData.append('cargo', cargo);
    formData.append('grado', grado);
    formData.append('contrasena', contrasena);
    if (foto) {
      formData.append('foto', foto);
    }

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'PUT',
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
  // 5. Eliminar Funcionario / Operador
  // ==========================================

  $(document).on('click', '.btn-eliminar-usuario', function() {
    const id = $(this).data('id');
    const rut = $(this).data('rut');
    const nombreCompleto = $(this).data('nombre');

    Swal.fire({
      title: '¿Está seguro de eliminar este funcionario?',
      text: `Se revocarán todos los accesos al sistema para: ${nombreCompleto} (${rut}). Esta acción es irreversible.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar de forma definitiva',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        $.ajax({
          url: '/api/usuarios/action/',
          type: 'DELETE',
          contentType: 'application/json',
          data: JSON.stringify({
            id: id
          }),
          dataType: 'json',
          success: function(response) {
            if (response.success) {
              Swal.fire({
                icon: 'success',
                title: '¡Eliminado!',
                text: response.message,
                confirmButtonColor: '#005a9c'
              });
              table.ajax.reload();
            }
          },
          error: function(xhr) {
            let msg = 'Ocurrió un error al intentar eliminar el usuario.';
            if (xhr.responseJSON && xhr.responseJSON.message) {
              msg = xhr.responseJSON.message;
            }
            Swal.fire('Error de Permisos o Negocio', msg, 'error');
          }
        });
      }
    });
  });

});
