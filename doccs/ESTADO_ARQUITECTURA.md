# Contexto y Estado del Proyecto (TIC System - Hospital Marga Marga)

> **Última actualización:** 2026-07-13
> **Entorno:** Desarrollo local (SQLite). Listo para escalar a PostgreSQL.

---

## Arquitectura y Patrones (Reglas Estrictas)

El proyecto sigue **Clean Architecture** y **SOLID** (SRP en todos los módulos):

| Capa | Responsabilidad |
|---|---|
| **Views** | Solo orquestan HTTP → Service → HTTP/JSON. Sin lógica de negocio. |
| **Services** | Toda la lógica de negocio y validaciones complejas. |
| **Repositories** | Acceso a datos y consultas ORM complejas. |
| **Models** | Solo comportamientos del dominio (3NF). Sin procesos. |
| **Templates** | Solo presentación. Sin JS ni consultas incrustadas. |
| **Static JS** | En `static/js/`. Se comunican por AJAX REST únicamente. |

Los endpoints API devuelven siempre `{ "success": true/false, "data": {…}, "message": "…" }`.

---

## Base de Datos

- **Motor actual:** SQLite (dev). Modelos 100% listos para PostgreSQL.
- **Diseño:** Tercera Forma Normal (3NF). Prohibida la redundancia.
- **Jerarquía de Ubicación:** `Institución > Edificio > Piso > (Sector/Unidad/Área) > Recinto > PMA`. El equipo apunta solo al PMA (hoja); la ruta se reconstruye on-the-fly.
- **`on_delete=PROTECT`** en todas las relaciones críticas. Nunca CASCADE ni SET_NULL en catálogos.
- **Soft Delete:** Los catálogos tienen campo `activo`. No se eliminan físicamente.
- **Auditoría Inmutable:** `LogAuditoria` registra quien, cuando, IP, valor anterior y nuevo.

---

## Normas UI / Frontend (Estrictas — NO negociables)

- **Bootstrap 4**, **SweetAlert2**, **DataTables** (server-side AJAX), **Select2**, **FontAwesome**.
- **Modales: `border-radius: 0 !important`** — Todos cuadrados, sin excepción. Regla de diseño corporativa.
- **Cabecera de modales:** Azul corporativo `modal-header-premium` (clase global en `global-theme.css`).
- Clases globales: `modal-content-premium`, `modal-header-premium`, `modal-body-clean`, `btn-primary-action`.
- **Nunca** incluir SweetAlert2, FontAwesome, DataTables en templates individuales. Van en `base.html`.
- **Nunca** incluir JS inline en templates HTML. Todo en `static/js/`.

---

## Módulos Activos

### 1. Core & Autenticación
- Login con bloqueo (django-axes). Switch de usuario para testing.
- **Auditoría transversal** (`LogAuditoria`): registra Usuario, Fecha, IP, Acción, Detalles.
- Gestión de Usuarios del sistema (CRUD DataTables AJAX).
- **API de Funcionarios** (`/api/funcionarios/search/`, `/api/funcionarios/crear/`):
  - Busca por RUT/Nombre con Select2-AJAX (mínimo 2 caracteres).
  - Si no existe, botón inline para crear funcionario "al vuelo" (modal `#modalFuncionario`).
  - Los funcionarios son personas del hospital, NO usuarios del sistema.

### 2. Mantenedores (Paramétrica)
- CRUDs completos para: Instituciones, Edificios, Pisos, Sectores, Áreas, Unidades, Recintos, PMAs.
- CRUDs para: Artículos, Marcas, Modelos (con imagen), Proveedores, SO, Estados, Cargos.
- Fallback de imagen: Modelo → Artículo → placeholder.

### 3. Inventario de Equipos (`/equipos/`)
- Listado DataTables AJAX con búsqueda y filtro por estado.
- **Formulario modal Crear/Editar** unificado (mismo modal para ambas acciones):
  - Vista previa de imagen que se actualiza automáticamente al cambiar Modelo.
  - Select2 en cascada: Piso → Unidad → Recinto → PMA.
  - Al editar, se precargan todos los campos incluyendo imagen y Unidad Clínica.
- **Pregunta de Motivo al cambiar PMA:** SweetAlert2 pregunta si es "Movimiento Real" o "Corrección de dato" antes de guardar. Evita falsos positivos en bitácora.
- **Vista Detalle** (modal read-only): datos completos, ruta topológica, fechas localizadas.
- **Historial de Auditoría** (botón reloj): log de cambios automáticos del sistema.
- **Bitácora Técnica** (botón historial) — Modal premium de ancho completo:
  - **Tarjeta superior:** foto del equipo, S/N, Estado y Ubicación (cargados por AJAX).
  - **Formulario colapsable** "REGISTRAR NUEVA ACTIVIDAD":
    - Tipo de Registro, Fecha Ingreso, Fecha Devolución (opcional), Servicio/Unidad (se preselecciona la unidad del equipo automáticamente).
    - **Solicitante:** Select2-AJAX → busca en `/api/funcionarios/search/`. Si no existe: botón "Registrar Nuevo Funcionario" → abre `#modalFuncionario` → al guardar, el funcionario nuevo queda seleccionado.
    - Falla/Motivo (lista de opciones), Actividades Realizadas.
  - **Historial de Registros:** Timeline cronológico: registros manuales (verde) y automáticos del sistema (amarillo/badge).
- **Bitácora automática (Signals):** Django Signals registran cambios de PMA, IP, estado sin intervención del técnico.

### 4. Tickets (Mesa de Ayuda) (`/tickets/`)
- Tablero Kanban con columnas por estado.
- Soporte de SLA, grupos resolutores, categorías, prioridades.
- Buscador de Solicitante con el mismo patrón Select2-AJAX que la Bitácora de Equipos.
- Creación de funcionarios al vuelo desde el formulario de ticket.

### 5. Reportes (`/reportes/`)
- App separada del core por norma de Clean Architecture.
- En desarrollo inicial.

### 6. Redes (`/redes/`)
- Módulo base creado. En planificación.

---

## Flujos Importantes Implementados

### Flujo: Registrar Mantenimiento en Bitácora de Equipo
1. Técnico presiona `fa-history` en la tabla de equipos.
2. Se abre `#modalBitacora` → AJAX carga foto, S/N, estado y ubicación del equipo.
3. Técnico presiona "REGISTRAR NUEVA ACTIVIDAD" → formulario se expande.
4. La Unidad del equipo se preselecciona automáticamente en el select de Servicio/Unidad.
5. Técnico busca solicitante (min 2 chars) → Select2-AJAX → `/api/funcionarios/search/`.
6. Si no existe: "Registrar Nuevo Funcionario" → `#modalFuncionario` → al guardar queda seleccionado.
7. Técnico completa y guarda → historial se recarga automáticamente.

### Flujo: Cambio de Ubicación de Equipo
1. Técnico presiona editar.
2. Modal carga datos del equipo (imagen, Unidad Clínica, PMA original guardado).
3. Técnico cambia el PMA.
4. Al guardar: sistema detecta PMA distinto al original.
5. SweetAlert2 pregunta: "Movimiento Real" vs "Corrección de dato".
6. La bitácora automática registra el evento con el motivo.

---

## Normas de Seguridad (OWASP)
- Bloqueo de intentos de login (django-axes).
- CSRF tokens en todos los formularios y llamadas AJAX.
- Todas las vistas requieren `LoginRequiredMixin`.
- Validaciones críticas en el backend (Services), nunca solo en el frontend.
- IPs de requests registradas en la auditoría.

---

## ¿Cómo continuar el trabajo?
1. **Nunca** insertar lógica de negocio en `views.py`.
2. **Nunca** incluir JS dentro del HTML de un template.
3. **Nunca** crear modales con bordes redondeados (norma corporativa `border-radius: 0 !important`).
4. **Siempre** incluir librerías comunes en `base.html`, no en templates individuales.
5. Usar `graphify update .` después de refactorizaciones para mantener el grafo al día.
6. Respetar clases premium globales: `modal-content-premium`, `modal-header-premium`.
