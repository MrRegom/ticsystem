/**
 * datatables-config.js
 * Configuración global para DataTables en todo el sistema.
 * Aplica el diseño unificado "Enterprise" a todas las tablas y habilita AJAX/Server-Side defaults.
 */

if (typeof $ !== 'undefined' && $.fn.dataTable) {
    $.extend(true, $.fn.dataTable.defaults, {
        processing: true,
        language: {
            url: "/static/vendor/datatables/i18n/es-ES.json",
            search: "",
            searchPlaceholder: "Buscar por..."
        },
        // Estructura DOM personalizada que genera la barra superior automáticamente
        dom: '<"toolbar-container"<"length-wrapper"l><"search-wrapper"f>>rt<"bottom"ip><"clear">',
        initComplete: function(settings, json) {
            var api = this.api();
            var $wrapper = $(api.table().container());
            
            // Inyectar el icono de lupa en el buscador (ya que DataTables no lo hace nativamente)
            var $filter = $wrapper.find('.dataTables_filter');
            $filter.addClass('search-wrapper'); // Reutilizar la clase CSS global
            if ($filter.find('i.fa-search').length === 0) {
                $filter.prepend('<i class="fas fa-search"></i>');
            }
            
            // Reestructurar ligeramente el filter para que coincida exactamente con nuestro CSS
            var $input = $filter.find('input');
            $filter.find('label').replaceWith($input);
            $filter.append($input);
            
            // Ajustar el contenedor de select
            var $lengthWrapper = $wrapper.find('.dataTables_length');
            $lengthWrapper.wrap('<div id="custom-length-wrapper"></div>');
        }
    });
}
