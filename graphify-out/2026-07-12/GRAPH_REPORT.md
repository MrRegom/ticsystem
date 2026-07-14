# Graph Report - ticsystem  (2026-07-11)

## Corpus Check
- 287 files · ~110,489 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1523 nodes · 2569 edges · 238 communities (151 shown, 87 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 273 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3a4b646e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- UsuarioService
- views.py
- views.py
- MantenedorService
- Acta
- Command
- models.py
- models.py
- UsuarioRepository
- Anexo
- views.py
- UsuarioServiceTests
- Unidad
- models.py
- admin.py
- models.py
- mantenedores.js
- views.py
- CredencialCorreo
- AuditoriaService
- UsuarioServiceTests
- admin.py
- views.py
- Command
- LogAuditoria
- migrar_desde_mysql.py
- UsuarioRepository
- actas.js
- equipos.js
- Rol
- anexos.js
- redes.js
- tickets.js
- audit_trail_equipo
- AvisoVisor
- models.py
- signals.py
- auditoria_repository.py
- ActasConfig
- AnexosConfig
- CoreConfig
- EquiposConfig
- MantenedoresConfig
- Command
- RedesConfig
- base.js
- CorreosConfig
- main
- tickets-kanban.js
- CoreConfig
- main
- TicketsConfig
- UtilidadesConfig
- VisorConfig
- 0001_initial.py
- 0001_initial.py
- asgi.py
- urls.py
- wsgi.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- 0002_proveedor_rut.py
- 0001_initial.py
- asgi.py
- urls.py
- wsgi.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- 0001_initial.py
- EstadoEquipo
- GraficosService
- EquipoRepository
- TicketService
- views.py
- Writing Guidelines for Postgres References
- UsuarioRepository
- UsuarioServiceTests
- 🏗️ Principios Arquitectónicos Obligatorios
- 🏗️ Principios Arquitectónicos Obligatorios
- Section Definitions
- EquipoBitacoraView
- models.py
- graphify reference: extra exports and benchmark
- ArticuloConocimiento
- [1.2.0](https://github.com/supabase/agent-skills/compare/v1.1.1...v1.2.0) (2026-06-02)
- Frontend Design
- graphify reference: query, path, explain
- Supabase Postgres Best Practices
- Funcionario
- _resolver_imagen_modelo
- load_grupos.py
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Command
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- ConocimientoConfig
- LogAuditoriaAdmin
- ReportesConfig
- SlaConfig
- graphify.md
- extraction-spec.md
- advanced-full-text-search.md
- advanced-jsonb-indexing.md
- conn-idle-timeout.md
- conn-limits.md
- conn-pooling.md
- conn-prepared-statements.md
- data-batch-inserts.md
- data-n-plus-one.md
- data-pagination.md
- data-upsert.md
- lock-advisory.md
- lock-deadlock-prevention.md
- lock-short-transactions.md
- lock-skip-locked.md
- monitor-explain-analyze.md
- monitor-pg-stat-statements.md
- monitor-vacuum-analyze.md
- query-composite-indexes.md
- query-covering-indexes.md
- query-index-types.md
- query-missing-indexes.md
- query-partial-indexes.md
- schema-constraints.md
- schema-data-types.md
- schema-foreign-key-indexes.md
- schema-lowercase-identifiers.md
- schema-partitioning.md
- schema-primary-keys.md
- security-privileges.md
- security-rls-basics.md
- security-rls-performance.md
- _template.md
- graphify.md
- 0001_initial.py
- 0002_funcionario.py
- 0003_articulo_imagen.py
- 0001_initial.py
- 0002_ticket_creador_ticket_fecha_vencimiento_sla_and_more.py
- 0003_gruporesolutor_categoria_grupo_resolutor_and_more.py
- 0004_ticket_anexo_contacto.py
- 0005_alter_ticket_solicitante.py

## God Nodes (most connected - your core abstractions)
1. `Chat Conversation` - 69 edges
2. `AuditoriaService` - 57 edges
3. `or serve over HTTP so a whole team points at one URL (no local graphify needed):` - 36 edges
4. `Command` - 31 edges
5. `UsuarioService` - 31 edges
6. `get_client_ip()` - 31 edges
7. `Equipo` - 31 edges
8. `extract_validation_error()` - 28 edges
9. `Acta` - 24 edges
10. `Unidad` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Command` --uses--> `Acta`  [INFERRED]
  core/management/commands/migrar_desde_mysql.py → actas/models.py
- `Command` --uses--> `Acta`  [INFERRED]
  mantenedores/management/commands/normalizar_datos.py → actas/models.py
- `Command` --uses--> `ActaDetalle`  [INFERRED]
  core/management/commands/migrar_desde_mysql.py → actas/models.py
- `Command` --uses--> `ActaDetalle`  [INFERRED]
  mantenedores/management/commands/normalizar_datos.py → actas/models.py
- `ActasDashboardView` --uses--> `AuditoriaService`  [INFERRED]
  actas/views.py → core/services/auditoria_service.py

## Import Cycles
- None detected.

## Communities (238 total, 87 thin omitted)

### Community 0 - "UsuarioService"
Cohesion: 0.15
Nodes (9): Actualizar acta existente., extract_validation_error(), get_client_ip(), Extrae un string legible de cualquier ValidationError (string, dict o lista)., API JSON/multipart para acciones CRUD de operadores/usuarios.     Soporta tanto, Extrae datos del request tanto de JSON como de multipart., UsuarioActionView, Crea un equipo validando FKs y unicidad de serial.         Dispara el signal pos (+1 more)

### Community 1 - "views.py"
Cohesion: 0.16
Nodes (27): EquipoService, Servicio para operaciones CRUD y consultas de Equipos., MargaMargaImporterService, BitacoraRegistroView, EquipoActionView, EquipoCheckView, EquipoDetailReadView, EquipoDetailView (+19 more)

### Community 2 - "views.py"
Cohesion: 0.12
Nodes (17): Obtiene tickets abiertos para el tablero Kanban., Capa de Acceso a Datos (Repository) para el módulo de Tickets.     Aísla las con, TicketRepository, KEDBSearchApiView, LoginRequiredMixin, TemplateView, View, Devuelve el conteo de tickets y datos ligeros para el Kanban auto-refresh. (+9 more)

### Community 3 - "MantenedorService"
Cohesion: 0.08
Nodes (24): normalizar_codigo(), Convierte a UPPERCASE, sin espacios y sin tildes., MantenedorRepository, MantenedorRepository ==================== Capa de acceso a datos para los catálo, Retorna una lista paginada, ordenada y filtrada para DataTables server-side., Total de registros sin filtrar (recordsTotal para DataTables)., Total de registros filtrados (recordsFiltered para DataTables)., Persiste la instancia (INSERT o UPDATE). Transacción atómica. (+16 more)

### Community 4 - "Acta"
Cohesion: 0.08
Nodes (24): ActaAdmin, ActaDetalleAdmin, ActaDetalleInline, Acta, ActaDetalle, Estado, Meta, Modelos del módulo de Actas de Entrega de Equipamiento.  Normalización aplicada (+16 more)

### Community 5 - "Command"
Cohesion: 0.08
Nodes (13): Command, BaseCommand, abrir_mysql(), decodificar_firma_base64(), limpiar_serial(), normalizar(), Helpers para la migracion de datos MySQL→PostgreSQL (Fase 5).  Funciones utilita, Abre conexion PyMySQL a la BD legacy (XAMPP MariaDB). (+5 more)

### Community 6 - "models.py"
Cohesion: 0.08
Nodes (25): BitacoraEquipoAdmin, BitacoraEquipoInline, BitacoraOpcionAdmin, EquipoAdmin, BitacoraEquipo, BitacoraOpcion, Equipo, Catálogo de fallas y actividades de mantención. Reemplaza tb_bitacora_opciones. (+17 more)

### Community 7 - "models.py"
Cohesion: 0.11
Nodes (24): Meta, Modelos del módulo de Equipos (inventario TIC) y Bitácora de mantenciones.  No, Tipo, TipoRegistro, AreaHospitalaria, Articulo, Marca, Modelo (+16 more)

### Community 8 - "UsuarioRepository"
Cohesion: 0.17
Nodes (9): User, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Caso de uso para DataTables Server-side de Usuarios., Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9)., Caso de uso: Crear un nuevo funcionario/operador en el sistema del hospital., Servicio de negocio para la gestión de operadores y usuarios del hospital., Caso de uso: Actualizar información de un operador, permitiendo actualizar el RU (+1 more)

### Community 9 - "Anexo"
Cohesion: 0.12
Nodes (13): AnexoAdmin, RequerimientoCambioAdmin, RequerimientoCambioInline, Anexo, Requerimiento de cambio de visor para un anexo.     Normaliza 2NF: extrae los ~1, Anexo telefónico IP. Reemplaza tabla `anexos` del esquema PHP., RequerimientoCambio, AnexoRepository (+5 more)

### Community 10 - "views.py"
Cohesion: 0.05
Nodes (31): User, Servicio de negocio para la gestión de operadores y usuarios del hospital., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso para DataTables Server-side de Usuarios., Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9)., Caso de uso: Crear un nuevo funcionario/operador en el sistema del hospital., Caso de uso: Actualizar información de un operador, permitiendo actualizar el RU (+23 more)

### Community 11 - "UsuarioServiceTests"
Cohesion: 0.14
Nodes (5): AuditoriaServiceTests, CorreoServiceTests, TestCase, Pruebas unitarias para validar el registro de logs de auditoría., Pruebas unitarias para validar las reglas de negocio en CorreoService.

### Community 12 - "Unidad"
Cohesion: 0.11
Nodes (21): Estado, Meta, Modelos del módulo de Anexos Telefónicos IP.  Normalización aplicada (3NF): - An, Command, normalizar_qs(), BaseCommand, Semilla inicial de catálogos básicos para ticsystem.  Crea la institución HGF, l, Edificio (+13 more)

### Community 13 - "models.py"
Cohesion: 0.15
Nodes (19): Migracion de datos desde MySQL legacy (equipamiento2026) a PostgreSQL (ticsystem, VLAN de red. Reemplaza tb_vlan (esquema básico)., Vlan, InfraestructuraRedAdmin, InfraestructuraRedInline, PmaAdmin, RangoIPAdmin, SlaConfiguracionAdmin (+11 more)

### Community 14 - "admin.py"
Cohesion: 0.19
Nodes (15): AyudaRapidaAdmin, ChecklistItemAdmin, PendienteAdmin, WebAppAdmin, AyudaRapida, ChecklistItem, Estado, Meta (+7 more)

### Community 15 - "models.py"
Cohesion: 0.23
Nodes (6): PerfilUsuarioInline, UserAdmin, Accion, Meta, PerfilUsuario, DjangoUserAdmin

### Community 16 - "mantenedores.js"
Cohesion: 0.23
Nodes (18): destroySelect2(), destroyTable(), editar(), eliminar(), fillForm(), getColumns(), getFormData(), guardar() (+10 more)

### Community 17 - "views.py"
Cohesion: 0.15
Nodes (16): Vistas del módulo Anexos. Sigue el patrón de equipos.views., LogAuditoria, AuditoriaService, LogAuditoria, Servicio de negocio para gestionar la auditoría y trazabilidad del sistema., parse_datatables_params(), IpActionView, IpDetailView (+8 more)

### Community 18 - "CredencialCorreo"
Cohesion: 0.23
Nodes (12): CredencialCorreoAdmin, GrupoCorreoAdmin, MiembroGrupoCorreoAdmin, MiembroGrupoCorreoInline, CredencialCorreo, GrupoCorreo, Meta, MiembroGrupoCorreo (+4 more)

### Community 19 - "AuditoriaService"
Cohesion: 0.24
Nodes (7): AnexoActionView, AnexoDetailView, AnexoListView, AnexosDashboardView, LoginRequiredMixin, TemplateView, View

### Community 20 - "UsuarioServiceTests"
Cohesion: 0.03
Nodes (69): Chat Conversation, Planner Response, Planner Response, Planner Response, Planner Response, Planner Response, Planner Response, Planner Response (+61 more)

### Community 21 - "admin.py"
Cohesion: 0.12
Nodes (14): ArticuloAdmin, EdificioAdmin, EstadoEquipoAdmin, InstitucionAdmin, MarcaAdmin, ModeloAdmin, ModeloAnexoAdmin, ModeloInline (+6 more)

### Community 22 - "views.py"
Cohesion: 0.04
Nodes (45): 1. Creación de Funcionarios "Al vuelo" (On-the-fly), 2. Grupos Resolutores (Colas de Trabajo / Support Groups), Alternatives:, Conclusión, expose the graph as an MCP server (for repeated tool-call access), graphify-out/cache/         # optional: commit for speed, skip to keep repo small, .graphifyignore, only index src/, ignore everything else (+37 more)

### Community 23 - "Command"
Cohesion: 0.37
Nodes (6): auto_width(), Command, BaseCommand, style_header(), write_rows(), write_title()

### Community 24 - "LogAuditoria"
Cohesion: 0.24
Nodes (6): AuditoriaRepository, LogAuditoria, Repositorio de datos para el modelo LogAuditoria.     Encapsula la creación e i, AuditoriaService, LogAuditoria, Servicio de negocio para gestionar la auditoría y trazabilidad del sistema.

### Community 25 - "migrar_desde_mysql.py"
Cohesion: 0.15
Nodes (20): ArchivoAdjuntoAdmin, CategoriaAdmin, PrioridadAdmin, TicketAdmin, TicketHistorialAdmin, Semilla de catálogos de tickets (prioridades y categorías) + SLA de mantenciones, ArchivoAdjunto, Categoria (+12 more)

### Community 26 - "UsuarioRepository"
Cohesion: 0.23
Nodes (4): PerfilUsuario, User, Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado., UsuarioRepository

### Community 27 - "actas.js"
Cohesion: 0.26
Nodes (8): agregarFilaDetalle(), buildSelectOptions(), editarActa(), fillForm(), getFormData(), guardarActa(), resetForm(), showError()

### Community 28 - "equipos.js"
Cohesion: 0.35
Nodes (8): abrirModal(), cargarEquipo(), csrfToken(), eliminarEquipo(), guardarEquipo(), initDataTable(), initEvents(), verEquipoInfo()

### Community 29 - "Rol"
Cohesion: 0.20
Nodes (6): Command, BaseCommand, Semilla inicial de roles y permisos para ticsystem.  Crea los 6 roles por defect, Devuelve True si el rol tiene el permiso indicado (bool True)., Rol de usuario (RBAC). Reemplaza al campo texto `perfil` de tbusuarios (PHP)., Rol

### Community 30 - "anexos.js"
Cohesion: 0.31
Nodes (7): cargarPisos(), editar(), fillForm(), getFormData(), guardar(), resetForm(), showError()

### Community 31 - "redes.js"
Cohesion: 0.33
Nodes (7): cargarP(), editar(), err(), fill(), get(), guardar(), reset()

### Community 32 - "tickets.js"
Cohesion: 0.33
Nodes (6): editar(), fillForm(), getFormData(), guardar(), resetForm(), showError()

### Community 33 - "audit_trail_equipo"
Cohesion: 0.07
Nodes (28): Bulk Operations, Caching Strategies, Custom Actions, Custom Middleware, Database Indexing, Django Development Patterns, Django REST Framework Patterns, Low-Level Caching (+20 more)

### Community 34 - "AvisoVisor"
Cohesion: 0.32
Nodes (5): AvisoVisorAdmin, AvisoVisor, Meta, Modelos del módulo Visor TV (pantalla pública de Mesa de Ayuda).  - AvisoVisor:, Aviso para pantalla TV de Mesa de Ayuda. Reemplaza tb_avisos_visor.

### Community 35 - "models.py"
Cohesion: 0.29
Nodes (4): Accion, LogAuditoria, Meta, PerfilUsuario

### Community 37 - "signals.py"
Cohesion: 0.33
Nodes (5): liberar_ip_on_equipo_delete(), Signals del módulo Redes (IPAM sync).  Implementa la regla de sync IPAM (listaEq, Marca la IP del equipo como OCUPADO en IPAM si existe., Libera la IP en IPAM al eliminar un equipo., sync_ipam_on_equipo_save()

### Community 40 - "auditoria_repository.py"
Cohesion: 0.40
Nodes (3): AuditoriaRepository, LogAuditoria, Repositorio de datos para el modelo LogAuditoria.     Encapsula la creación e i

### Community 144 - "EstadoEquipo"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 145 - "GraficosService"
Cohesion: 0.12
Nodes (11): Retorna el número de tickets vencidos vs en tiempo., Retorna la cantidad de tickets por categoría., Tickets creados en los últimos 6 meses., Top 5 activos con más fallas históricas., Se encarga de interactuar con el ORM de forma pesada y óptima     para extraer d, ReportesRepository, GraficosService, Toma los datos crudos del Repositorio y los adapta a las estructuras     requeri (+3 more)

### Community 146 - "EquipoRepository"
Cohesion: 0.13
Nodes (5): EquipoRepository, Repositorio para Equipo y bitácoras asociadas., Caso de uso para DataTables Server-side de Equipos., Resuelve la URL de la imagen para un equipo.      Priodad:     1. Si equipo.imag, _resolver_imagen_equipo()

### Community 147 - "TicketService"
Cohesion: 0.16
Nodes (8): NotificacionService, User, Capa de Reglas de Negocio (Service) para Tickets.     Maneja la creación, cambio, Un técnico (miembro de un grupo o en general) se auto-asigna el ticket., Genera un correlativo secuencial anual único y thread-safe.         Usa select_f, TicketService, TicketCommentApiView, TicketTakeApiView

### Community 148 - "views.py"
Cohesion: 0.20
Nodes (14): obtener_kpis_generales(), CustomLoginView, CustomLogoutView, DashboardGeneralView, LoginRequiredMixin, TemplateView, View, Dashboard de inicio general con estadísticas agregadas del sistema TIC.     Ree (+6 more)

### Community 149 - "Writing Guidelines for Postgres References"
Cohesion: 0.12
Nodes (15): 1. Concrete Transformation Patterns, 2. Error-First Structure, 3. Quantified Impact, 4. Self-Contained Examples, 5. Semantic Naming, Code Example Standards, Comments, Impact Level Guidelines (+7 more)

### Community 150 - "UsuarioRepository"
Cohesion: 0.23
Nodes (4): PerfilUsuario, User, Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado., UsuarioRepository

### Community 152 - "🏗️ Principios Arquitectónicos Obligatorios"
Cohesion: 0.18
Nodes (10): 1. Requisitos Previos, 2. Instalación, 3. Base de Datos Inicial, 4. Ejecución del Servidor, 🛠️ Despliegue en Producción, 📦 Estructura de Directorios, Guía de Inicio y Ejecución (Entorno Local), Plantilla Oficial - Hospital Dr. Gustavo Fricke (+2 more)

### Community 153 - "🏗️ Principios Arquitectónicos Obligatorios"
Cohesion: 0.18
Nodes (10): 1. Requisitos Previos, 2. Instalación, 3. Base de Datos Inicial, 4. Ejecución del Servidor, 🛠️ Despliegue en Producción, 📦 Estructura de Directorios, Guía de Inicio y Ejecución (Entorno Local), Plantilla Oficial - Hospital Dr. Gustavo Fricke (+2 more)

### Community 154 - "Section Definitions"
Cohesion: 0.20
Nodes (9): 1. Query Performance (query), 2. Connection Management (conn), 3. Security & RLS (security), 4. Schema Design (schema), 5. Concurrency & Locking (lock), 6. Data Access Patterns (data), 7. Monitoring & Diagnostics (monitor), 8. Advanced Features (advanced) (+1 more)

### Community 156 - "models.py"
Cohesion: 0.22
Nodes (6): Command, BaseCommand, Meta, Modelos de SLA (Service Level Agreement). Define los tiempos de resolución basad, Matriz de SLA que cruza Impacto y Urgencia para derivar Prioridad y Tiempos., SLAMatrix

### Community 157 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 158 - "ArticuloConocimiento"
Cohesion: 0.39
Nodes (5): ArticuloConocimientoAdmin, CategoriaConocimientoAdmin, ArticuloConocimiento, CategoriaConocimiento, Meta

### Community 159 - "[1.2.0](https://github.com/supabase/agent-skills/compare/v1.1.1...v1.2.0) (2026-06-02)"
Cohesion: 0.25
Nodes (7): [1.2.0](https://github.com/supabase/agent-skills/compare/v1.1.1...v1.2.0) (2026-06-02), [1.3.0](https://github.com/supabase/agent-skills/compare/v1.2.0...v1.3.0) (2026-06-05), Bug Fixes, Bug Fixes, Changelog, Features, Features

### Community 160 - "Frontend Design"
Cohesion: 0.29
Nodes (6): Design principles, Frontend Design, Ground it in the subject, More on writing in design, Process: brainstorm, explore, plan, critique, build, critique again, Restraint and self-critique

### Community 161 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 162 - "Supabase Postgres Best Practices"
Cohesion: 0.33
Nodes (5): How to Use, References, Rule Categories by Priority, Supabase Postgres Best Practices, When to Apply

### Community 164 - "_resolver_imagen_modelo"
Cohesion: 0.33
Nodes (4): _normalizar_nombre(), Normaliza un nombre de modelo al formato usado en PHP (vistas/img/modelos/)., Resuelve la URL de la imagen para un modelo (sin equipo asociado)., _resolver_imagen_modelo()

### Community 165 - "load_grupos.py"
Cohesion: 0.33
Nodes (3): Command, BaseCommand, GrupoResolutor

### Community 166 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 167 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 168 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **317 isolated node(s):** `Migration`, `Estado`, `Meta`, `TipoItem`, `Migration` (+312 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **87 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditoriaService` connect `views.py` to `UsuarioService`, `views.py`, `MantenedorService`, `Acta`, `models.py`, `views.py`, `UsuarioServiceTests`, `models.py`, `AuditoriaService`, `views.py`, `UsuarioServiceTests`, `LogAuditoria`, `EquipoBitacoraView`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Equipo` connect `models.py` to `UsuarioService`, `views.py`, `views.py`, `Command`, `signals.py`, `models.py`, `Unidad`, `models.py`, `EquipoRepository`, `migrar_desde_mysql.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `PerfilUsuario` connect `models.py` to `Funcionario`, `UsuarioRepository`, `views.py`, `Unidad`, `models.py`, `views.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 45 inferred relationships involving `AuditoriaService` (e.g. with `ActaActionView` and `ActaDetailView`) actually correct?**
  _`AuditoriaService` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Command` (e.g. with `Acta` and `ActaDetalle`) actually correct?**
  _`Command` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `UsuarioService` (e.g. with `UsuarioRepository` and `AuditoriaServiceTests`) actually correct?**
  _`UsuarioService` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Migration`, `Estado`, `Meta` to the rest of the system?**
  _497 weakly-connected nodes found - possible documentation gaps or missing edges._