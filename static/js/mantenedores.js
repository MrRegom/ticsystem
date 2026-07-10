/**
 * mantenedores.js
 * Controlador frontend para el módulo de Mantenedores (Catálogos).
 *
 * Arquitectura de capas jerárquicas soportadas:
 *   Institución → Edificio → Piso → Sector
 *   Área Hospitalaria → Unidad → Recinto → PMA
 *
 * @module MantenedoresApp
 */

var MantenedoresApp = (function ($) {

  /* ─── Estado interno ───────────────────────────────────────── */
  var tabla        = null;
  var modeloActual = '';

  /* ─── Columnas extra por modelo ────────────────────────────── */
  // pre: columnas antes del nombre (padres)
  // post: columnas después del nombre (atributos extra)
  var COLS_EXTRA = {
    edificio:        { pre: [{ data: 'institucion',      title: 'Institución' }] },
    institucion:     { post: [{ data: 'codigo',           title: 'Código' }] },
    fallas_bitacora: { post: [{ data: 'tipo',             title: 'Tipo' }] },
    modelo:          { pre: [{ data: 'marca',            title: 'Marca' }] },
    piso:            { pre: [{ data: 'edificio',         title: 'Edificio' }], 
                       post: [{ data: 'alias',             title: 'Alias' }] },
    proveedor:       { post: [{ data: 'contacto',         title: 'Contacto' },
                             { data: 'telefono',          title: 'Teléfono' },
                             { data: 'email',             title: 'Email' }] },
    sector:          { pre: [{ data: 'piso',             title: 'Piso' }] },
    unidad:          { pre: [{ data: 'area_hospitalaria',title: 'Área Hospitalaria' }] },
    recinto:         { pre: [{ data: 'piso',             title: 'Piso' },
                             { data: 'sector',            title: 'Sector' },
                             { data: 'unidad',            title: 'Unidad' }] },
    pma:             { pre: [{ data: 'recinto',          title: 'Recinto' },
                             { data: 'unidad',            title: 'Unidad' },
                             { data: 'piso',              title: 'Piso' }] }
  };

  /* Etiquetas cortas para el encabezado de la columna 'Nombre' en la tabla */
  var TABLE_NOMBRE_LABELS = {
    piso:             'Piso',
    edificio:         'Edificio',
    institucion:      'Institución',
    marca:            'Marca',
    modelo:           'Modelo',
    articulo:         'Artículo',
    proveedor:        'Proveedor',
    sistemaoperativo: 'Sistema Operativo',
    unidad:           'Unidad',
    estados:          'Estado',
    sector:           'Sector',
    area_hospitalaria:'Área',
    recinto:          'Recinto',
    pma:              'PMA'
  };

  /* ─── Campos del formulario modal por modelo ───────────────── */
  var FIELD_MAP = {
    edificio:        ['institucion'],
    estados:         ['color_hex'],
    fallas_bitacora: ['tipo'],
    institucion:     ['codigo'],
    modelo:          ['marca'],
    piso:            ['alias', 'edificio'],
    proveedor:       ['contacto', 'telefono', 'email', 'direccion'],
    sector:          ['piso'],
    unidad:          ['area_hospitalaria'],
    recinto:         ['piso', 'sector', 'unidad'],
    pma:             ['recinto']
  };

  /* Campos <select> que necesitan Select2 */
  var SELECT_FIELDS = ['institucion', 'edificio', 'marca', 'piso',
                       'sector', 'area_hospitalaria', 'unidad', 'recinto'];

  /* Todos los campos del formulario (para ocultar en resetForm) */
  var ALL_FIELDS = ['codigo', 'alias', 'tipo', 'orden', 'color_hex',
                    'institucion', 'edificio', 'marca', 'piso', 'sector',
                    'area_hospitalaria', 'unidad', 'recinto',
                    'contacto', 'telefono', 'email', 'direccion'];

  /* Textos de ayuda y contexto para la interfaz */
  var DESCRIPTIONS = {
    articulo:         'Tipos genéricos de equipos (ej. Monitor Multiparámetro, Electrocardiógrafo). Son independientes de la marca.',
    fallas_bitacora:  'Tipos de fallas predefinidas o tareas frecuentes para facilitar el registro en bitácoras de mantenimiento.',
    marca:            'Marcas o fabricantes de los equipos médicos e informáticos.',
    modelo:           'Modelos específicos asociados a una Marca.',
    modeloanexo:      'Modelos y configuraciones específicas para teléfonos y anexos IP.',
    proveedor:        'Empresas y contactos técnicos que proveen soporte, garantía o insumos.',
    sistemaoperativo: 'Sistemas operativos (ej. Windows 11, Linux) utilizados en equipos informáticos.',
    institucion:      'Instituciones o recintos base (ej. Hospital Provincial Marga Marga).',
    edificio:         'Estructuras principales que componen la Institución (ej. Edificio Principal, Edificio Administrativo).',
    piso:             'Niveles o pisos físicos de un Edificio.',
    sector:           'Zonas o alas específicas dentro de un Piso (ej. Sector Norte, Ala B).',
    area_hospitalaria:'Áreas macro o grandes divisiones del hospital (ej. Atención Cerrada, Atención Abierta).',
    unidad:           'Servicios o Unidades Clínicas (ej. UPC, Urgencia, Pabellón). Pertenecen a un Área Hospitalaria.',
    recinto:          'Salas, habitaciones o espacios físicos (ej. Box 1, Sala Espera). <b>Tienen una doble relación:</b> están en una ubicación física (Piso/Sector) y pertenecen a una Unidad Clínica.',
    pma:              'Puntos de Montaje de Activos. Representan la "toma" o ubicación exacta (en pared, cielo o red) dentro de un Recinto donde se conecta un equipo.'
  };

  /* Etiquetas del campo "nombre" por tipo de entidad */
  var NOMBRE_LABELS = {
    piso:             'Nombre del Piso (ej. Nivel 2)',
    edificio:         'Nombre del Edificio (ej. Torre Principal)',
    institucion:      'Nombre de la Institución',
    marca:            'Nombre de la Marca',
    modelo:           'Modelo Específico',
    articulo:         'Nombre del Artículo',
    proveedor:        'Razón Social / Nombre',
    sistemaoperativo: 'Nombre del SO',
    unidad:           'Nombre de la Unidad Clínica / Servicio',
    estados:          'Estado',
    sector:           'Nombre del Sector (ej. Ala Sur)',
    area_hospitalaria:'Nombre del Área Hospitalaria',
    recinto:          'Nombre del Recinto (ej. Box de Atención 1)',
    pma:              'Código PMA (ej. PMA-1234)'
  };

  /* ─── Helpers ──────────────────────────────────────────────── */

  function updateKPI() {
    if (tabla) {
      $('#kpi-total span').text(tabla.page.info().recordsTotal);
    }
  }

  function getColumns() {
    var acciones = {
      data: 'id', title: 'Acciones', orderable: false,
      className: 'text-center', width: '80px',
      render: function (d, t) {
        if (t !== 'display') { return d; }
        return '<div class="actions-cell">' +
          '<a href="#" class="action-icon ic-edit btn-editar" data-id="' + d + '" title="Editar"><i class="fas fa-pencil-alt"></i></a>' +
          '<a href="#" class="action-icon ic-delete btn-eliminar" data-id="' + d + '" title="Eliminar"><i class="fas fa-trash-alt"></i></a>' +
          '</div>';
      }
    };

    var estado = {
      data: 'activo', title: 'Estado', orderable: true,
      className: 'text-center', width: '80px',
      render: function (d, t, r) {
        if (t !== 'display') { return d; }
        var checked = d ? 'checked' : '';
        return '<div class="custom-control custom-switch d-inline-block">' +
          '<input type="checkbox" class="custom-control-input toggle-activo"' +
          ' id="act-' + r.id + '" data-id="' + r.id + '" ' + checked + '>' +
          '<label class="custom-control-label" for="act-' + r.id + '"></label>' +
          '</div>';
      }
    };

    var config = COLS_EXTRA[modeloActual] || {};
    var preCols = config.pre || [];
    var postCols = config.post || [];
    var nombreTitle = TABLE_NOMBRE_LABELS[modeloActual] || 'Nombre';

    var base = [
      { data: 'row_num', title: '#', orderable: false, className: 'text-muted', width: '40px' }
    ];

    // 1. Columnas padre (antes del nombre) - macro a micro
    base = base.concat(preCols);
    
    // 2. Columna Nombre (con el título dinámico según el catálogo)
    base.push({ data: 'nombre', title: nombreTitle, className: 'font-weight-bold', style: 'color: #0f766e;' });
    
    // 3. Columnas extra (después del nombre)
    base = base.concat(postCols);
    
    // 4. Estado y Acciones
    base.push(estado);
    base.push(acciones);

    return base;
  }

  /* ─── DataTable ────────────────────────────────────────────── */

  function destroyTable() {
    if (tabla) { tabla.destroy(); tabla = null; }
    $('#tabla-mantenedores thead').empty();
    $('#tabla-mantenedores tbody').empty();
  }

  function initDataTable() {
    destroyTable();
    if (!modeloActual) { return; }

    var cols = getColumns();
    var headerHtml = '';
    $.each(cols, function (i, c) { headerHtml += '<th>' + (c.title || '') + '</th>'; });
    $('#tabla-mantenedores thead').html('<tr>' + headerHtml + '</tr>');

    tabla = $('#tabla-mantenedores').DataTable({
      processing : true,
      serverSide : true,
      ajax: {
        url : '/mantenedores/api/',
        type: 'POST',
        data: function (d) { d.modelo = modeloActual; return d; },
        dataSrc: 'data'
      },
      columns   : cols,
      order     : [],
      pageLength: 25,
      language  : {
        search          : 'Buscar:',
        searchPlaceholder: 'Buscar...',
        lengthMenu      : 'Mostrar _MENU_ registros',
        info            : 'Mostrando _START_ a _END_ de _TOTAL_ registros',
        infoEmpty       : 'Mostrando 0 registros',
        infoFiltered    : '(filtrado de _MAX_ registros totales)',
        zeroRecords     : 'No se encontraron registros',
        loadingRecords  : 'Cargando...',
        processing      : 'Procesando...',
        paginate: {
          first   : 'Primero', last  : 'Último',
          next    : 'Siguiente', previous: 'Anterior'
        }
      },
      drawCallback: function () {
        if (!$('.card-modelo.active').data('no-create')) {
          $('#btn-nuevo').prop('disabled', false);
        }
        updateKPI();
      }
    });
  }

  /* ─── Selección de tarjeta ─────────────────────────────────── */

  function seleccionarModelo(key) {
    modeloActual = key;
    $('#mantenedor-modelo').val(key);

    $('.card-modelo').removeClass('active');
    $('.card-modelo[data-key="' + key + '"]').addClass('active');

    var label = $('.card-modelo[data-key="' + key + '"] .modelo-label').text();
    $('#tabla-titulo').html('<i class="fas fa-list mr-2"></i>Registros de ' + label);
    
    // Setear información de ayuda contextual
    $('#info-title').text('Acerca de ' + label);
    $('#info-description').html(DESCRIPTIONS[key] || 'Gestión del catálogo de ' + label + '.');
    
    $('#table-section').fadeIn(300);
    $('#alert-seleccionar').hide();

    // Hacer scroll automático a la tabla para que el usuario no se pierda
    $('html, body').animate({
      scrollTop: $("#table-section").offset().top - 80
    }, 400);

    var noCreate = $('.card-modelo[data-key="' + key + '"]').data('no-create');
    if (noCreate) {
      $('#btn-nuevo').hide();
    } else {
      $('#btn-nuevo').show().prop('disabled', true);
    }

    initDataTable();
  }

  /* ─── Formulario modal ─────────────────────────────────────── */

  function destroySelect2() {
    $.each(SELECT_FIELDS, function (i, f) {
      var $s = $('#m-' + f);
      if ($s.length && typeof $.fn.select2 === 'function' && $s.data('select2')) {
        $s.select2('destroy');
      }
    });
  }

  function initSelect2(fieldId) {
    if (typeof $.fn.select2 !== 'function') { return; }
    var $s = $('#m-' + fieldId);
    if (!$s.length || $s.data('select2')) { return; }
    function formatSelect2Result(state) {
      if (!state.id) return state.text;
      
      var text = state.text;
      var parts = text.split(/ \– | \- | \— /);
      
      if (parts.length > 1) {
        var main = parts[0];
        var sub = parts.slice(1).join(' - ');
        return $(
          '<div style="display:flex; flex-direction:column; line-height:1.3; padding:2px 0;">' +
            '<span style="color:#0f172a; font-weight:700; font-size:0.85rem;">' + main + '</span>' +
            '<span style="color:#64748b; font-size:0.75rem; font-weight:500;">' + sub + '</span>' +
          '</div>'
        );
      }
      return $('<span style="color:#0f172a; font-weight:700; font-size:0.85rem;">' + text + '</span>');
    }

    function formatSelect2Selection(state) {
      if (!state.id) return state.text;
      var text = state.text;
      var parts = text.split(/ \– | \- | \— /);
      if (parts.length > 1) {
        // En la selección (una vez elegido), mostramos Todo en una línea: Padre en gris, Hijo normal.
        return $('<span style="color:#0f172a; font-weight:600;">' + parts[0] + ' <span style="color:#64748b; font-weight:400; font-size:0.8em;">(' + parts.slice(1).join(' - ') + ')</span></span>');
      }
      return $('<span style="color:#0f172a; font-weight:600;">' + text + '</span>');
    }

    $s.select2({
      theme         : 'bootstrap4',
      width         : '100%',
      dropdownParent: $('#modalMantenedor'),
      templateResult: formatSelect2Result,
      templateSelection: formatSelect2Selection
    });
    $s.on('select2:open',  function () { $('#field-' + fieldId).addClass('focus'); });
    $s.on('select2:close', function () { $('#field-' + fieldId).removeClass('focus'); });
  }

  function resetForm() {
    destroySelect2();
    $('#form-mantenedor')[0].reset();
    $('#mantenedor-id').val('');
    $('#mantenedor-error-alert').addClass('d-none').empty();
    $('#m-activo').prop('checked', true);
    $('#label-nombre').text('Nombre');
    $('#color-swatch-preview').css('background', '#17a2b8');
    $('#modalMantenedorLabel').html('<i class="fas fa-edit mr-2"></i>Nuevo Registro');
    $.each(ALL_FIELDS, function (i, f) { $('#field-' + f).hide(); });
  }

  function showFields(modelo) {
    $('#label-nombre').text(NOMBRE_LABELS[modelo] || 'Nombre');
    
    var fields = FIELD_MAP[modelo] || [];
    var hasRelations = false;

    $.each(fields, function (i, f) {
      $('#field-' + f).show();
      if ($.inArray(f, SELECT_FIELDS) !== -1) { 
        initSelect2(f);
        hasRelations = true;
      }
    });

    // Mostrar u ocultar el panel de "Jerarquía" si hay selects padre que llenar
    if (hasRelations) {
      $('#section-relaciones').show();
    } else {
      $('#section-relaciones').hide();
    }
  }

  /* ─── Serialización del formulario ────────────────────────── */

  function getFormData() {
    var data = {
      id    : $('#mantenedor-id').val() || null,
      modelo: $('#mantenedor-modelo').val(),
      nombre: $.trim($('#m-nombre').val()),
      activo: $('#m-activo').is(':checked')
    };
    var fields = FIELD_MAP[modeloActual] || [];
    $.each(fields, function (i, f) {
      var val = $('#m-' + f).val();
      data[f] = (val !== null && val !== undefined && val !== '') ? val : null;
    });
    return data;
  }

  function fillForm(d) {
    $('#mantenedor-id').val(d.id);
    $('#m-nombre').val(d.nombre);
    $('#m-activo').prop('checked', d.activo);

    var fields = FIELD_MAP[modeloActual] || [];
    $.each(fields, function (i, f) {
      var val = d[f];
      if (val !== null && val !== undefined) {
        var $el = $('#m-' + f);
        $el.val(val);
        if ($el.is('select') && typeof $.fn.select2 === 'function' && $el.data('select2')) {
          $el.trigger('change');
        }
      }
    });

    if (modeloActual === 'estados' && d.color_hex) {
      $('#m-color_hex').val(d.color_hex);
      $('#color-swatch-preview').css('background', d.color_hex);
    }

    $('#modalMantenedorLabel').html('<i class="fas fa-edit mr-2"></i>Editar Registro');
  }

  /* ─── CRUD ─────────────────────────────────────────────────── */

  function showError(msg) {
    $('#mantenedor-error-alert').html(msg).removeClass('d-none');
  }

  function recargar() {
    if (tabla) { tabla.ajax.reload(null, false); }
  }

  function guardar() {
    var data   = getFormData();
    var method = data.id ? 'PUT' : 'POST';
    $.ajax({
      url        : '/mantenedores/api/action/',
      type       : method,
      contentType: 'application/json',
      data       : JSON.stringify(data)
    }).done(function (r) {
      if (r.success) {
        $('#modalMantenedor').modal('hide');
        Swal.fire({ icon: 'success', title: 'Éxito', text: r.message, confirmButtonColor: '#002a54' });
        recargar();
      } else {
        showError(r.message);
      }
    }).fail(function (x) {
      showError((x.responseJSON && x.responseJSON.message) || 'Error al guardar.');
    });
  }

  function editar(id) {
    resetForm();
    showFields(modeloActual);
    $.get('/mantenedores/api/' + id + '/?modelo=' + modeloActual)
      .done(function (r) {
        if (r.success) {
          fillForm(r.data);
          $('#modalMantenedor').modal('show');
        } else {
          Swal.fire({ icon: 'error', title: 'Error', text: r.message });
        }
      });
  }

  function eliminar(id) {
    Swal.fire({
      title             : '¿Eliminar registro?',
      text              : 'Esta acción no se puede deshacer.',
      icon              : 'warning',
      showCancelButton  : true,
      confirmButtonText : 'Sí, eliminar',
      cancelButtonText  : 'Cancelar',
      confirmButtonColor: '#dc3545'
    }).then(function (r) {
      if (!r.isConfirmed) { return; }
      $.ajax({
        url        : '/mantenedores/api/action/',
        type       : 'DELETE',
        contentType: 'application/json',
        data       : JSON.stringify({ id: id, modelo: modeloActual })
      }).done(function (r) {
        if (r.success) {
          Swal.fire({ icon: 'success', title: 'Eliminado', text: r.message });
          recargar();
        } else {
          Swal.fire({ icon: 'error', title: 'Error', text: r.message });
        }
      }).fail(function (x) {
        Swal.fire({ icon: 'warning', html: (x.responseJSON && x.responseJSON.message) || 'El registro está en uso.' });
      });
    });
  }

  function toggleActivo(id, activo) {
    Swal.fire({
      title             : activo ? '¿Activar registro?' : '¿Desactivar registro?',
      text              : 'El registro se ' + (activo ? 'activará' : 'desactivará') + '.',
      icon              : 'warning',
      showCancelButton  : true,
      confirmButtonText : 'Sí, ' + (activo ? 'activar' : 'desactivar'),
      cancelButtonText  : 'Cancelar',
      confirmButtonColor: '#002a54'
    }).then(function (r) {
      if (!r.isConfirmed) { recargar(); return; }
      $.ajax({
        url        : '/mantenedores/api/action/',
        type       : 'PUT',
        contentType: 'application/json',
        data       : JSON.stringify({ id: id, modelo: modeloActual, activo: activo })
      }).done(function (r) {
        if (r.success) {
          Swal.fire({ icon: 'success', title: 'Actualizado', text: r.message, timer: 1200, showConfirmButton: false });
        } else {
          Swal.fire({ icon: 'error', title: 'Error', text: r.message });
        }
        recargar();
      }).fail(function () {
        recargar();
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo actualizar.' });
      });
    });
  }

  /* ─── Inicialización de eventos ────────────────────────────── */

  function init() {
    // Clic en tarjeta de catálogo
    $(document).on('click', '.card-modelo', function () {
      seleccionarModelo($(this).data('key'));
    });

    // Botón Nuevo
    $('#btn-nuevo').on('click', function () {
      resetForm();
      showFields(modeloActual);
      $('#modalMantenedor').modal('show');
    });

    // Modal al cerrar → limpiar errores
    $('#modalMantenedor').on('hidden.bs.modal', function () {
      $('#mantenedor-error-alert').addClass('d-none').empty();
    });

    // Submit del formulario
    $('#form-mantenedor').on('submit', function (e) {
      e.preventDefault();
      guardar();
    });

    // Botones de acción en la tabla
    $(document).on('click', '.btn-editar',  function (e) { e.preventDefault(); editar($(this).data('id')); });
    $(document).on('click', '.btn-eliminar',function (e) { e.preventDefault(); eliminar($(this).data('id')); });

    // Toggle activo/inactivo
    $(document).on('change', '.toggle-activo', function () {
      toggleActivo($(this).data('id'), this.checked);
    });

    // Color picker → swatch
    $('#m-color_hex').on('input', function () {
      $('#color-swatch-preview').css('background', $(this).val());
    });

    // Auto-seleccionar primera tarjeta al cargar
    var $primera = $('.card-modelo').first();
    if ($primera.length) {
      seleccionarModelo($primera.data('key'));
    }
  }

  /* ─── Arrancar cuando el DOM esté listo ───────────────────── */
  $(document).ready(init);

  // Exponer API pública (para debugging en consola si es necesario)
  return { seleccionarModelo: seleccionarModelo, recargar: recargar };

}(jQuery));