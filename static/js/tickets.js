/* tickets.js - DataTables Server-Side + CRUD Tickets */
(function () {
  'use strict';

  var TABLA_COLORS = {
    PENDIENTE: '#ffc107',
    EN_TERRENO: '#17a2b8',
    RESUELTO: '#28a745',
  };

  var tabla;

  function initDataTable() {
    tabla = $('#tabla-tickets').DataTable({
      processing: true, serverSide: true,
      ajax: { url: '/tickets/api/', type: 'POST', dataSrc: 'data' },
      columns: [
        { data: 'id' },
        { data: 'solicitante_nombre' },
        { data: 'edificio' },
        { data: 'unidad' },
        { data: 'estado', render: function (d, t, r) { if (t === 'display' && d) { var c = r.prioridad_color || TABLA_COLORS[d] || '#6c757d'; return '<span class="badge" style="background-color:' + c + ';color:#fff;">' + d + '</span>'; } return d; } },
        { data: 'prioridad' },
        { data: 'categoria' },
        { data: 'tecnico' },
        { data: 'fecha_hora' },
        { data: 'id', orderable: false, render: function (d, t) { if (t === 'display') { return '<div class="actions-cell"><a href="#" class="action-icon ic-edit btn-editar" data-id="' + d + '" title="Editar"><i class="fas fa-edit"></i></a><a href="#" class="action-icon ic-delete btn-eliminar" data-id="' + d + '" title="Eliminar"><i class="fas fa-trash-alt"></i></a></div>'; } return d; } },
      ],
      order: [[0, 'desc']], pageLength: 25,
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
    $('#form-ticket')[0].reset();
    $('#ticket-id').val('');
    $('#ticket-error-alert').addClass('d-none').empty();
    $('#modalTicketLabel').text('Registrar Nuevo Ticket');
  }

  function showError(m) { $('#ticket-error-alert').html(m).removeClass('d-none'); }

  function getFormData() {
    return {
      id: $('#ticket-id').val() || null,
      solicitante_nombre: $('#tk-solicitante').val(),
      solicitante_rut: $('#tk-rut').val(),
      solicitante_correo: $('#tk-correo').val(),
      solicitante_anexo: $('#tk-anexo').val(),
      edificio: $('#tk-edificio').val() || null,
      piso: $('#tk-piso').val(),
      unidad: $('#tk-unidad').val() || null,
      equipo: $('#tk-equipo').val() || null,
      descripcion: $('#tk-descripcion').val(),
      prioridad: $('#tk-prioridad').val() || null,
      categoria: $('#tk-categoria').val() || null,
      tecnico: $('#tk-tecnico').val() || null,
      estado: $('#tk-estado').val(),
    };
  }

  function fillForm(d) {
    $('#ticket-id').val(d.id);
    $('#tk-solicitante').val(d.solicitante_nombre);
    $('#tk-rut').val(d.solicitante_rut);
    $('#tk-correo').val(d.solicitante_correo);
    $('#tk-anexo').val(d.solicitante_anexo);
    $('#tk-edificio').val(d.edificio);
    $('#tk-piso').val(d.piso);
    $('#tk-unidad').val(d.unidad);
    $('#tk-equipo').val(d.equipo);
    $('#tk-descripcion').val(d.descripcion);
    $('#tk-prioridad').val(d.prioridad);
    $('#tk-categoria').val(d.categoria);
    $('#tk-tecnico').val(d.tecnico);
    $('#tk-estado').val(d.estado);
    $('#modalTicketLabel').text('Editar Ticket');
  }

  function guardar() {
    var data = getFormData();
    $.ajax({ url: '/tickets/api/action/', type: data.id ? 'PUT' : 'POST', contentType: 'application/json', data: JSON.stringify(data) })
      .done(function (r) { if (r.success) { $('#modalCrearTicket').modal('hide'); Swal.fire('Éxito', r.message, 'success'); tabla.ajax.reload(null, false); } else showError(r.message); })
      .fail(function (x) { showError(x.responseJSON ? x.responseJSON.message : 'Error'); });
  }

  function editar(id) {
    resetForm();
    $.get('/tickets/api/' + id + '/').done(function (r) { if (r.success) { fillForm(r.data); $('#modalCrearTicket').modal('show'); } else Swal.fire('Error', r.message, 'error'); }).fail(function () { Swal.fire('Error', 'No se pudo cargar el ticket.', 'error'); });
  }

  function eliminar(id) {
    Swal.fire({ title: '¿Eliminar ticket?', text: 'Esta acción no se puede deshacer.', icon: 'warning', showCancelButton: true, confirmButtonText: 'Sí, eliminar', confirmButtonColor: '#dc3545' })
      .then(function (r) { if (r.isConfirmed) { $.ajax({ url: '/tickets/api/action/', type: 'DELETE', contentType: 'application/json', data: JSON.stringify({ id: id }) }).done(function (r) { if (r.success) { Swal.fire('Eliminado', r.message, 'success'); tabla.ajax.reload(null, false); } else Swal.fire({ icon:'warning', text: r.message }); }).fail(function (x) { Swal.fire({ icon:'warning', text: (x.responseJSON ? x.responseJSON.message : null) || 'El ticket está en uso y no se puede eliminar.' }); }); } });
  }

  $(function () {
    initDataTable();

    $('#modalCrearTicket').on('show.bs.modal', function (e) { if (!$(e.relatedTarget).data('id')) resetForm(); });
    $('#form-ticket').on('submit', function (e) { e.preventDefault(); guardar(); });

    $('#tabla-tickets tbody').on('click', '.btn-editar', function () { editar($(this).data('id')); });
    $('#tabla-tickets tbody').on('click', '.btn-eliminar', function () { eliminar($(this).data('id')); });
  });
})();
