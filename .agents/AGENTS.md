# Reglas Globales (CSS y JS)

- **Nunca incluir librerias comunes (como SweetAlert2 o FontAwesome) en plantillas individuales**. Usa siempre base.html.
- **Estilos Globales y Reusables**: Los estilos genericos de la interfaz de usuario (modales, botones, cabeceras) deben ir en el CSS central (e.g., static/css/global-theme.css) y no en el CSS de cada app. Usa siempre clases globales como .modal-header-premium o .modal-content-premium.

- **Modales sin bordes redondeados**: Como regla general de diseño para esta aplicación, todos los modales deben tener bordes cuadrados ( order-radius: 0). No uses bordes redondeados para modales.

- **Sistema de Diseño Global (Microsoft Fluent)**: Todos los componentes nuevos (Tablas, Listas, Botones, Inputs, Formularios) DEBEN reutilizar las clases `.ms-*` definidas en `static/css/global-theme.css`. NUNCA crees CSS redundante en las plantillas individuales ni uses `<style>` a menos que sea una excepción justificada. Mantén el estilo corporativo limpio y compacto.

- **Cero CSS Inline**: Queda ESTRICTAMENTE PROHIBIDO el uso de estilos en línea (\style=\...\\) en las plantillas HTML para la configuración de paddings, márgenes, bordes, fondos o tamaños de letra. Todos estos detalles deben delegarse a clases globales utilitarias en \global-theme.css\ (ej: \.ms-flex\, \.ms-gap-2\, \.ms-p-4\).
- **Tablas Uniformes**: Cualquier módulo que renderice una tabla (sea simple o con DataTables) DEBE heredar visualmente del diseño de Inventario a través de \global-theme.css\. Nunca introduzcas clases de bootstrap crudas para tablas ni sobreescribas el aspecto visual global de un DataTable.
