$(document).ready(function() {
  
  // ==========================================
  // 1. Funciones de Utilidad y Validaciones de RUT
  // ==========================================

  /**
   * Valida un RUT chileno usando el algoritmo Módulo 11.
   */
  function validarRut(rut) {
    if (typeof rut !== 'string') return false;
    
    // Limpiar puntos, espacios y normalizar guion/mayúsculas
    rut = rut.replace(/\./g, '').replace(/\s+/g, '').toUpperCase();
    
    // Formato básico de RUT chileno: 7 u 8 dígitos, guion y dígito verificador (0-9 o K)
    if (!/^\d{7,8}-[0-9K]$/.test(rut)) {
      return false;
    }
    
    const parts = rut.split('-');
    const cuerpo = parts[0];
    const dv = parts[1];
    
    let suma = 0;
    let multiplo = 2;
    
    // Calcular suma ponderada
    for (let i = cuerpo.length - 1; i >= 0; i--) {
      suma += parseInt(cuerpo.charAt(i), 10) * multiplo;
      multiplo = (multiplo === 7) ? 2 : multiplo + 1;
    }
    
    // Módulo 11
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

  /**
   * Normaliza y formatea el RUT mientras el usuario escribe o al desenfocar.
   */
  function formatRutInput(value) {
    // Mantener sólo números y letra K
    let clean = value.replace(/[^0-9kK]/g, '').toUpperCase();
    if (clean.length === 0) return '';
    
    // Si tiene más de 1 carácter, separar el último como dígito verificador
    if (clean.length > 1) {
      const cuerpo = clean.slice(0, -1);
      const dv = clean.slice(-1);
      return `${cuerpo}-${dv}`;
    }
    return clean;
  }

  // Formatear dinámicamente el RUT en el input de creación y edición
  $('#crear-rut, #editar-rut').on('input', function() {
    const val = $(this).val();
    $(this).val(formatRutInput(val));
  });

  // Validar RUT dinámicamente cuando pierde el foco (blur)
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
  
  const table = $('#tabla-usuarios').DataTable({
    processing: true,
    serverSide: true,
    responsive: true,
    order: [[7, 'desc']], // Ordenar por fecha_registro desc por defecto
    pageLength: 10,
    language: {
      url: 'https://cdn.datatables.net/plug-ins/1.10.22/i18n/Spanish.json'
    },
    ajax: {
      url: '/api/usuarios/',
      type: 'POST'
    },
    columns: [
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
          // Clonar de manera segura la plantilla de acciones del DOM
          const $acciones = $('#dt-templates .tmpl-acciones').clone();
          
          // Configurar atributos data para edición
          $acciones.find('.btn-editar-usuario').attr({
            'data-id': row.id,
            'data-rut': row.rut,
            'data-nombres': row.nombres,
            'data-apellidos': row.apellidos,
            'data-email': row.email,
            'data-unidad': row.unidad,
            'data-cargo': row.cargo,
            'data-grado': row.grado
          });
          
          // Configurar atributos data para eliminación
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

  // Limpiar formulario al abrir modal
  $('[data-target="#modalCrearUsuario"]').on('click', function() {
    $formCrear[0].reset();
    $formCrear.removeClass('was-validated');
    $('#crear-rut').removeClass('is-invalid');
    $alertCrear.addClass('d-none');
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

    // Validaciones del lado del cliente
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

    // Deshabilitar botón y mostrar spinner
    $btnCrear.prop('disabled', true);
    $btnCrear.find('span').first().addClass('d-none');
    $btnCrear.find('.spinner-border').removeClass('d-none');

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        rut: rut,
        email: email,
        nombres: nombres,
        apellidos: apellidos,
        unidad: unidad,
        cargo: cargo,
        grado: grado,
        contrasena: contrasena
      }),
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
        // Restaurar estado del botón
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

  // Delegación de eventos para botón editar de la tabla
  $(document).on('click', '.btn-editar-usuario', function() {
    const id = $(this).data('id');
    const rut = $(this).data('rut');
    const nombres = $(this).data('nombres');
    const apellidos = $(this).data('apellidos');
    const email = $(this).data('email');
    const unidad = $(this).data('unidad');
    const cargo = $(this).data('cargo');
    const grado = $(this).data('grado');

    // Cargar datos en el modal
    $('#editar-id').val(id);
    $('#editar-rut').val(rut).removeClass('is-invalid');
    $('#editar-nombres').val(nombres);
    $('#editar-apellidos').val(apellidos);
    $('#editar-email').val(email);
    $('#editar-unidad').val(unidad);
    $('#editar-cargo').val(cargo);
    $('#editar-grado').val(grado);
    $('#editar-contrasena').val(''); // Vacío por defecto

    // Resetear validación visual
    $formEditar.removeClass('was-validated');
    $alertEditar.addClass('d-none');

    // Mostrar modal
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

    // Validaciones del lado del cliente
    let clientValid = true;

    // Si el RUT parece ser un RUT (empieza con un número o tiene longitud de RUT), validarlo
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

    // Deshabilitar botón
    $btnEditar.prop('disabled', true);

    $.ajax({
      url: '/api/usuarios/action/',
      type: 'PUT',
      contentType: 'application/json',
      data: JSON.stringify({
        id: id,
        rut: rut,
        nombres: nombres,
        apellidos: apellidos,
        email: email,
        unidad: unidad,
        cargo: cargo,
        grado: grado,
        contrasena: contrasena
      }),
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
          table.ajax.reload(null, false); // Recargar sin perder paginación
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

  // Delegación de eventos para botón eliminar de la tabla
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
