(function () {
  'use strict';

  var PISOS = window.__PISOS__ || [];
  var EDIFICIOS = window.__EDIFICIOS__ || [];
  var UNIDADES = window.__UNIDADES__ || [];

  var tabla;

  function initDataTable() {
    tabla = $('#tabla-actas').DataTable({
      processing: true,
      serverSide: true,
      ajax: {
        url: '/actas/api/',
        type: 'POST',
        dataSrc: 'data',
      },
      columns: [
        { data: 'codigo' },
        { data: 'receptor' },
        {
          data: 'estado',
          render: function (data, type) {
            if (type === 'display' && data) {
              var color = '#17a2b8';
              if (data === 'borrador') color = '#ffc107';
              else if (data === 'emitido') color = '#007bff';
              else if (data === 'enviado') color = '#28a745';
              return '<span class="badge" style="background-color:' + color + ';color:#fff;">' + data + '</span>';
            }
            return data;
          },
        },
        { data: 'fecha' },
        { data: 'encargado' },
        {
          data: 'id',
          orderable: false,
          render: function (data, type) {
            if (type === 'display') {
              return '<div class="actions-cell"><a href="#" class="action-icon ic-edit btn-editar" data-id="' + data + '" title="Editar"><i class="fas fa-edit"></i></a><a href="#" class="action-icon ic-delete btn-eliminar" data-id="' + data + '" title="Eliminar"><i class="fas fa-trash-alt"></i></a></div>';
            }
            return data;
          },
        },
      ],
      order: [[3, 'desc']],
      pageLength: 25,
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
    });
  }

  function resetForm() {
    $('#form-acta')[0].reset();
    $('#acta-id').val('');
    $('#acta-error-alert').addClass('d-none').empty();
    $('#modalActaLabel').text('Registrar Nueva Acta');
    $('#detalles-tbody').empty();
  }

  function showError(msg) {
    $('#acta-error-alert').html(msg).removeClass('d-none');
  }

  function getFormData() {
    var detalles = [];
    $('#detalles-tbody tr').each(function () {
      var row = $(this);
      detalles.push({
        tipo_item: row.find('.det-tipo-item').val(),
        id_item: parseInt(row.find('.det-id-item').val()) || 0,
        articulo: row.find('.det-articulo').val(),
        serie: row.find('.det-serie').val(),
        edificio: row.find('.det-edificio').val() || null,
        piso: row.find('.det-piso').val() || null,
        unidad: row.find('.det-unidad').val() || null,
        pma_lugar: row.find('.det-pma-lugar').val(),
        estado: row.find('.det-estado-item').val(),
      });
    });
    return {
      id: $('#acta-id').val() || null,
      codigo: $('#act-codigo').val(),
      receptor_nombre: $('#act-receptor-nombre').val(),
      receptor_rut: $('#act-receptor-rut').val(),
      receptor_cargo: $('#act-receptor-cargo').val(),
      receptor_unidad: $('#act-receptor-unidad').val(),
      encargado: $('#act-encargado').val() || null,
      observaciones: $('#act-observaciones').val(),
      email_receptor: $('#act-email-receptor').val(),
      estado: $('#act-estado').val(),
      detalles: detalles,
    };
  }

  function fillForm(data) {
    $('#acta-id').val(data.id);
    $('#act-codigo').val(data.codigo);
    $('#act-receptor-nombre').val(data.receptor_nombre);
    $('#act-receptor-rut').val(data.receptor_rut);
    $('#act-receptor-cargo').val(data.receptor_cargo);
    $('#act-receptor-unidad').val(data.receptor_unidad);
    $('#act-encargado').val(data.encargado);
    $('#act-observaciones').val(data.observaciones);
    $('#act-email-receptor').val(data.email_receptor);
    $('#act-estado').val(data.estado);

    $('#detalles-tbody').empty();
    if (data.detalles) {
      data.detalles.forEach(function (d) {
        agregarFilaDetalle(d);
      });
    }
    $('#modalActaLabel').text('Editar Acta');
  }

  function buildSelectOptions(list, valueKey, labelKey, selectedValue) {
    var opts = '<option value="">Seleccione...</option>';
    list.forEach(function (item) {
      var val = item[valueKey];
      var sel = (val == selectedValue) ? ' selected' : '';
      opts += '<option value="' + val + '"' + sel + '>' + item[labelKey] + '</option>';
    });
    return opts;
  }

  function agregarFilaDetalle(d) {
    d = d || {};
    var row = '<tr>' +
      '<td><select class="form-control form-control-sm det-tipo-item">' +
        '<option value="EQUIPO"' + (d.tipo_item === 'EQUIPO' ? ' selected' : '') + '>Equipo</option>' +
        '<option value="ANEXO"' + (d.tipo_item === 'ANEXO' ? ' selected' : '') + '>Anexo</option>' +
      '</select></td>' +
      '<td><input type="number" class="form-control form-control-sm det-id-item" value="' + (d.id_item || '') + '"></td>' +
      '<td><input type="text" class="form-control form-control-sm det-articulo" value="' + (d.articulo || '') + '"></td>' +
      '<td><input type="text" class="form-control form-control-sm det-serie" value="' + (d.serie || '') + '"></td>' +
      '<td><select class="form-control form-control-sm det-edificio">' + buildSelectOptions(EDIFICIOS, 'id', 'nombre', d.edificio) + '</select></td>' +
      '<td><select class="form-control form-control-sm det-piso"><option value="">Seleccione edificio primero...</option></select></td>' +
      '<td><select class="form-control form-control-sm det-unidad">' + buildSelectOptions(UNIDADES, 'id', 'nombre', d.unidad) + '</select></td>' +
      '<td><input type="text" class="form-control form-control-sm det-pma-lugar" value="' + (d.pma_lugar || '') + '"></td>' +
      '<td><input type="text" class="form-control form-control-sm det-estado-item" value="' + (d.estado || '') + '"></td>' +
      '<td><button type="button" class="btn btn-sm btn-danger btn-eliminar-detalle"><i class="fas fa-times"></i></button></td>' +
      '</tr>';
    var $row = $(row);
    $('#detalles-tbody').append($row);

    if (d.edificio) {
      $row.find('.det-edificio').val(d.edificio).trigger('change');
      setTimeout(function () {
        $row.find('.det-piso').val(d.piso);
      }, 50);
    }
  }

  function guardarActa() {
    var data = getFormData();
    var id = data.id;
    var method = id ? 'PUT' : 'POST';

    $.ajax({
      url: '/actas/api/action/',
      type: method,
      contentType: 'application/json',
      data: JSON.stringify(data),
    })
      .done(function (res) {
        if (res.success) {
          $('#modalCrearActa').modal('hide');
          Swal.fire('Éxito', res.message, 'success');
          tabla.ajax.reload(null, false);
        } else {
          showError(res.message || 'Error desconocido.');
        }
      })
      .fail(function (xhr) {
        var msg = 'Error al guardar.';
        if (xhr.responseJSON && xhr.responseJSON.message) msg = xhr.responseJSON.message;
        showError(msg);
      });
  }

  function editarActa(id) {
    resetForm();
    $.get('/actas/api/' + id + '/')
      .done(function (res) {
        if (res.success) {
          fillForm(res.data);
          $('#modalCrearActa').modal('show');
        } else {
          Swal.fire('Error', res.message, 'error');
        }
      })
      .fail(function () {
        Swal.fire('Error', 'No se pudo cargar el acta.', 'error');
      });
  }

  function eliminarActa(id) {
    Swal.fire({
      title: '¿Eliminar acta?',
      text: 'Esta acción no se puede deshacer.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
      confirmButtonColor: '#dc3545',
    }).then(function (result) {
      if (result.isConfirmed) {
        $.ajax({
          url: '/actas/api/action/',
          type: 'DELETE',
          contentType: 'application/json',
          data: JSON.stringify({ id: id }),
        })
          .done(function (res) {
            if (res.success) {
              Swal.fire('Eliminado', res.message, 'success');
              tabla.ajax.reload(null, false);
            } else {
              Swal.fire({ icon:'warning', text: res.message });
            }
          })
          .fail(function (xhr) {
            Swal.fire({ icon:'warning', text: xhr.responseJSON && xhr.responseJSON.message || 'El acta está en uso y no se puede eliminar.' });
          });
      }
    });
  }

  function cargarPisos(edificioId, pisoSeleccionado, selectEl) {
    var $select = selectEl ? $(selectEl) : null;
    if (!edificioId) {
      if ($select) {
        $select.html('<option value="">Seleccione edificio primero...</option>');
      }
      return;
    }
    var pisosEd = PISOS.filter(function (p) { return p.edificio__id == edificioId; });
    var opts = '<option value="">Seleccione...</option>';
    pisosEd.forEach(function (p) {
      opts += '<option value="' + p.id + '"' + (p.id == pisoSeleccionado ? ' selected' : '') + '>' + p.nombre + '</option>';
    });
    if ($select) {
      $select.html(opts);
    }
  }

  $(function () {
    window.__PISOS__ = window.__PISOS__ || [];

    initDataTable();

    $('#detalles-container').on('change', '.det-edificio', function () {
      var edificioId = $(this).val();
      var $pisoSelect = $(this).closest('tr').find('.det-piso');
      cargarPisos(edificioId, null, $pisoSelect);
    });

    $('#btn-agregar-detalle').on('click', function () {
      agregarFilaDetalle(null);
    });

    $('#detalles-container').on('click', '.btn-eliminar-detalle', function () {
      $(this).closest('tr').remove();
    });

    $('#modalCrearActa').on('show.bs.modal', function (e) {
      if (!$(e.relatedTarget).data('id')) {
        resetForm();
      }
    });
    $('#btn-guardar-acta').on('click', function (e) { e.preventDefault(); guardarActa(); });
    $('#form-acta').on('submit', function (e) { e.preventDefault(); guardarActa(); });

    $('#tabla-actas tbody').on('click', '.btn-editar', function () {
      editarActa($(this).data('id'));
    });
    $('#tabla-actas tbody').on('click', '.btn-eliminar', function () {
      eliminarActa($(this).data('id'));
    });
  });
})();
