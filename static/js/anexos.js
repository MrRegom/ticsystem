/* anexos.js - DataTables Server-Side + CRUD Anexos */
(function () {
  'use strict';
  let tabla;

  function initDataTable() {
    tabla = $('#tabla-anexos').DataTable({
      processing: true, serverSide: true,
      ajax: { url: '/anexos/api/', type: 'POST', dataSrc: 'data' },
      columns: [
        { data: 'numero_anexo' }, { data: 'marca' }, { data: 'modelo' },
        { data: 'edificio' }, { data: 'piso' }, { data: 'unidad' },
        { data: 'estado', render: function(d,t,r){ if(t==='display'&&d){ var c=d==='Activo'?'success':'secondary'; return '<span class="badge badge-'+c+'">'+d+'</span>'; } return d; } },
        { data: 'serial_number' }, { data: 'ip' }, { data: 'pma_lugar' },
        { data: 'id', orderable: false, render: function(d,t){ if(t==='display'){ return '<div class="actions-cell"><a href="#" class="action-icon ic-edit btn-editar" data-id="'+d+'" title="Editar"><i class="fas fa-edit"></i></a><a href="#" class="action-icon ic-delete btn-eliminar" data-id="'+d+'" title="Eliminar"><i class="fas fa-trash-alt"></i></a></div>'; } return d; } },
      ],
      order: [[0, 'asc']], pageLength: 25,
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
    $('#form-anexo')[0].reset();
    $('#anexo-id').val('');
    $('#anexo-error-alert').addClass('d-none').empty();
    $('#modalAnexoLabel').text('Registrar Nuevo Anexo');
    $('#ax-piso').html('<option value="">Seleccione edificio...</option>');
  }

  function showError(m) { $('#anexo-error-alert').html(m).removeClass('d-none'); }

  function getFormData() {
    return {
      id: $('#anexo-id').val() || null,
      numero_anexo: $('#ax-numero').val(), marca: $('#ax-marca').val(), modelo: $('#ax-modelo').val(),
      edificio: $('#ax-edificio').val() || null, piso: $('#ax-piso').val() || null,
      unidad: $('#ax-unidad').val() || null, serial_number: $('#ax-serial').val(),
      ip: $('#ax-ip').val(), estado: $('#ax-estado').val(), pma_lugar: $('#ax-pma').val(),
      grupo: $('#ax-grupo').val(), proveedor: $('#ax-proveedor').val() || null,
      comentario: $('#ax-comentario').val(),
    };
  }

  function fillForm(d) {
    $('#anexo-id').val(d.id);
    $('#ax-numero').val(d.numero_anexo); $('#ax-marca').val(d.marca); $('#ax-modelo').val(d.modelo);
    $('#ax-edificio').val(d.edificio).trigger('change'); $('#ax-unidad').val(d.unidad);
    $('#ax-serial').val(d.serial_number); $('#ax-ip').val(d.ip); $('#ax-estado').val(d.estado);
    $('#ax-pma').val(d.pma_lugar); $('#ax-grupo').val(d.grupo); $('#ax-proveedor').val(d.proveedor);
    $('#ax-comentario').val(d.comentario);
    if (d.edificio) cargarPisos(d.edificio, d.piso);
    $('#modalAnexoLabel').text('Editar Anexo');
  }

  function cargarPisos(edId, sel) {
    if (!edId) { $('#ax-piso').html('<option value="">Seleccione edificio...</option>'); return; }
    var pisos = (window.__PISOS__||[]).filter(function(p){return p.edificio__id==edId;});
    var opts = '<option value="">Seleccione...</option>';
    pisos.forEach(function(p){ opts += '<option value="'+p.id+'"'+(p.id==sel?' selected':'')+'>'+p.nombre+'</option>'; });
    $('#ax-piso').html(opts);
  }

  function guardar() {
    var data = getFormData();
    $.ajax({ url: '/anexos/api/action/', type: data.id ? 'PUT' : 'POST', contentType: 'application/json', data: JSON.stringify(data) })
      .done(function(r){ if(r.success){ $('#modalCrearAnexo').modal('hide'); Swal.fire('Éxito',r.message,'success'); tabla.ajax.reload(null,false); } else showError(r.message); })
      .fail(function(x){ showError(x.responseJSON?.message||'Error'); });
  }

  function editar(id) {
    resetForm();
    $.get('/anexos/api/'+id+'/').done(function(r){ if(r.success){ fillForm(r.data); $('#modalCrearAnexo').modal('show'); } });
  }

  function eliminar(id) {
    Swal.fire({ title:'¿Eliminar anexo?', text:'No se puede deshacer.', icon:'warning', showCancelButton:true, confirmButtonText:'Sí, eliminar', confirmButtonColor:'#dc3545' })
      .then(function(r){ if(r.isConfirmed){ $.ajax({ url:'/anexos/api/action/', type:'DELETE', contentType:'application/json', data:JSON.stringify({id:id}) }).done(function(r){ if(r.success){ Swal.fire('Eliminado',r.message,'success'); tabla.ajax.reload(null,false); } else Swal.fire({ icon:'warning', text:r.message }); }).fail(function(x){ Swal.fire({ icon:'warning', text: (x.responseJSON && x.responseJSON.message) || 'El anexo está en uso y no se puede eliminar.' }); }); } });
  }

  $(function(){
    initDataTable();
    $('#ax-edificio').on('change', function(){ cargarPisos($(this).val()); });
    $('#modalCrearAnexo').on('show.bs.modal', function(e){ if(!$(e.relatedTarget).data('id')) resetForm(); });
    $('#form-anexo').on('submit', function(e){ e.preventDefault(); guardar(); });
    $('#tabla-anexos tbody').on('click','.btn-editar',function(){ editar($(this).data('id')); });
    $('#tabla-anexos tbody').on('click','.btn-eliminar',function(){ eliminar($(this).data('id')); });
  });
})();
