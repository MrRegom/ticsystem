# Graph Report - ticsystem  (2026-07-13)

## Corpus Check
- 297 files · ~119,382 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1564 nodes · 2648 edges · 248 communities (156 shown, 92 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 283 edges (avg confidence: 0.53)
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
- AGENTS.md
- 0003_funcionario_cargo_old_alter_funcionario_cargo.py
- 0004_alter_logauditoria_options_alter_funcionario_cargo_and_more.py
- 0002_alter_bitacoraequipo_tipo_registro.py
- 0004_cargo.py
- 0005_alter_piso_edificio_alter_pma_recinto_and_more.py
- 0006_alter_categoria_grupo_resolutor_and_more.py
- xat.md
- global_users_for_impersonation
- 0003_alter_bitacoraequipo_solicitante.py

## God Nodes (most connected - your core abstractions)
1. `AuditoriaService` - 60 edges
2. `Get or create Groups` - 42 edges
3. `UsuarioService` - 34 edges
4. `Enrutar todas las categorías existentes a la Mesa de Ayuda por defecto (para que todo caiga ahí primero)` - 33 edges
5. `Command` - 31 edges
6. `get_client_ip()` - 31 edges
7. `Equipo` - 31 edges
8. `extract_validation_error()` - 28 edges
9. `Unidad` - 25 edges
10. `TicketService` - 25 edges

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

## Communities (248 total, 92 thin omitted)

### Community 0 - "UsuarioService"
Cohesion: 0.39
Nodes (3): API JSON/multipart para acciones CRUD de operadores/usuarios.     Soporta tanto, Extrae datos del request tanto de JSON como de multipart., UsuarioActionView

### Community 1 - "views.py"
Cohesion: 0.06
Nodes (39): EquipoRepository, Repositorio para Equipo y bitácoras asociadas., EquipoService, _normalizar_nombre(), Servicio para operaciones CRUD y consultas de Equipos., Crea un equipo validando FKs y unicidad de serial.         Dispara el signal pos, Caso de uso para DataTables Server-side de Equipos., Normaliza un nombre de modelo al formato usado en PHP (vistas/img/modelos/). (+31 more)

### Community 2 - "views.py"
Cohesion: 0.13
Nodes (16): Obtiene tickets abiertos para el tablero Kanban., Capa de Acceso a Datos (Repository) para el módulo de Tickets.     Aísla las con, TicketRepository, KEDBSearchApiView, LoginRequiredMixin, TemplateView, View, Devuelve el conteo de tickets y datos ligeros para el Kanban auto-refresh. (+8 more)

### Community 3 - "MantenedorService"
Cohesion: 0.04
Nodes (45): 1. ¿Por qué se asignó al grupo de inmediato al crearlo?, 2. ¿Qué pasó con los estados y el historial?, 🧪 Flujo de Prueba: El Ciclo de Vida del Ticket, Get or create Groups, PASO 1: Ingreso de la Llamada (Mesa de Ayuda), PASO 2: Recepción del Requerimiento (Técnico de Terreno), PASO 3: Ejecución en el Kanban (Drag & Drop), Planner Response (+37 more)

### Community 4 - "Acta"
Cohesion: 0.07
Nodes (27): ActaAdmin, ActaDetalleAdmin, ActaDetalleInline, Acta, ActaDetalle, Estado, Meta, Modelos del módulo de Actas de Entrega de Equipamiento.  Normalización aplicada (+19 more)

### Community 5 - "Command"
Cohesion: 0.08
Nodes (13): Command, BaseCommand, abrir_mysql(), decodificar_firma_base64(), limpiar_serial(), normalizar(), Helpers para la migracion de datos MySQL→PostgreSQL (Fase 5).  Funciones utilita, Abre conexion PyMySQL a la BD legacy (XAMPP MariaDB). (+5 more)

### Community 6 - "models.py"
Cohesion: 0.10
Nodes (19): BitacoraEquipoAdmin, BitacoraEquipoInline, BitacoraOpcionAdmin, EquipoAdmin, BitacoraEquipo, BitacoraOpcion, Equipo, Meta (+11 more)

### Community 7 - "models.py"
Cohesion: 0.13
Nodes (21): Vistas del módulo Equipos.  Siguen el patrón Clean Architecture de core.views: -, AreaHospitalaria, Cargo, Meta, Modelo, Piso, PMA, Modelos de catálogos / mantenedores del sistema TIC.  Normalización aplicada ( (+13 more)

### Community 8 - "UsuarioRepository"
Cohesion: 0.17
Nodes (9): User, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Caso de uso para DataTables Server-side de Usuarios., Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9)., Caso de uso: Crear un nuevo funcionario/operador en el sistema del hospital., Servicio de negocio para la gestión de operadores y usuarios del hospital., Caso de uso: Actualizar información de un operador, permitiendo actualizar el RU (+1 more)

### Community 9 - "Anexo"
Cohesion: 0.09
Nodes (18): AnexoAdmin, RequerimientoCambioAdmin, RequerimientoCambioInline, Anexo, Requerimiento de cambio de visor para un anexo.     Normaliza 2NF: extrae los ~1, Anexo telefónico IP. Reemplaza tabla `anexos` del esquema PHP., RequerimientoCambio, AnexoRepository (+10 more)

### Community 10 - "views.py"
Cohesion: 0.17
Nodes (11): CustomLoginView, CustomLogoutView, _get_client_ip(), View, API Server-Side para DataTables de Usuarios., Función de utilidad para extraer la IP real del cliente.     Considera entornos, API JSON para acciones CRUD de operadores/usuarios., Vista para renderizar e iniciar sesión.     Cumple con OWASP y responde solicit (+3 more)

### Community 11 - "UsuarioServiceTests"
Cohesion: 0.08
Nodes (7): AuditoriaServiceTests, CorreoServiceTests, TestCase, Pruebas unitarias para validar el registro de logs de auditoría., Pruebas unitarias para validar las reglas de negocio en UsuarioService., Pruebas unitarias para validar las reglas de negocio en CorreoService., UsuarioServiceTests

### Community 12 - "Unidad"
Cohesion: 0.11
Nodes (14): Estado, Meta, Modelos del módulo de Anexos Telefónicos IP.  Normalización aplicada (3NF): - An, Migracion de datos desde MySQL legacy (equipamiento2026) a PostgreSQL (ticsystem, Recalcula el estado del equipo según la bitácora (bitacora.modelo.php:39-91)., recalcular_estado_equipo(), Edificio, Institucion (+6 more)

### Community 13 - "models.py"
Cohesion: 0.09
Nodes (26): InfraestructuraRedAdmin, InfraestructuraRedInline, PmaAdmin, RangoIPAdmin, SlaConfiguracionAdmin, AppConfig, RedesConfig, Estado (+18 more)

### Community 14 - "admin.py"
Cohesion: 0.19
Nodes (15): AyudaRapidaAdmin, ChecklistItemAdmin, PendienteAdmin, WebAppAdmin, AyudaRapida, ChecklistItem, Estado, Meta (+7 more)

### Community 15 - "models.py"
Cohesion: 0.18
Nodes (9): Vistas del módulo Anexos. Sigue el patrón de equipos.views., LogAuditoria, AuditoriaRepository, LogAuditoria, Repositorio de datos para el modelo LogAuditoria.     Encapsula la creación e i, parse_datatables_params(), AuditoriaService, LogAuditoria (+1 more)

### Community 16 - "mantenedores.js"
Cohesion: 0.23
Nodes (18): destroySelect2(), destroyTable(), editar(), eliminar(), fillForm(), getColumns(), getFormData(), guardar() (+10 more)

### Community 17 - "views.py"
Cohesion: 0.06
Nodes (37): extract_validation_error(), get_client_ip(), normalizar_nombre(), Extrae un string legible de cualquier ValidationError (string, dict o lista)., Convierte a Title Case preservando acrónimos técnicos comunes (HP, IP, USB...)., MantenedorRepository, MantenedorRepository ==================== Capa de acceso a datos para los catálo, Retorna una lista paginada, ordenada y filtrada para DataTables server-side. (+29 more)

### Community 18 - "CredencialCorreo"
Cohesion: 0.23
Nodes (12): CredencialCorreoAdmin, GrupoCorreoAdmin, MiembroGrupoCorreoAdmin, MiembroGrupoCorreoInline, CredencialCorreo, GrupoCorreo, Meta, MiembroGrupoCorreo (+4 more)

### Community 19 - "AuditoriaService"
Cohesion: 0.06
Nodes (33): 1. El letrero rojo "Sin asignar" NO es un error, 2. ¿Dónde están los técnicos de Nivel 2?, ¿Cómo funciona ahora el flujo Enterprise?, Enrutar todas las categorías existentes a la Mesa de Ayuda por defecto (para que todo caiga ahí primero), Planner Response, Planner Response, Planner Response, Planner Response (+25 more)

### Community 20 - "UsuarioServiceTests"
Cohesion: 0.22
Nodes (9): Chat Conversation, Planner Response, Planner Response, Planner Response, Planner Response, User Input, User Input, User Input (+1 more)

### Community 21 - "admin.py"
Cohesion: 0.12
Nodes (14): ArticuloAdmin, EdificioAdmin, EstadoEquipoAdmin, InstitucionAdmin, MarcaAdmin, ModeloAdmin, ModeloAnexoAdmin, ModeloInline (+6 more)

### Community 22 - "views.py"
Cohesion: 0.17
Nodes (9): User, Servicio de negocio para la gestión de operadores y usuarios del hospital., Caso de uso: Actualizar información de un operador, permitiendo actualizar el RU, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Caso de uso para DataTables Server-side de Usuarios., Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9)., Caso de uso: Crear un nuevo funcionario/operador en el sistema del hospital. (+1 more)

### Community 23 - "Command"
Cohesion: 0.37
Nodes (6): auto_width(), Command, BaseCommand, style_header(), write_rows(), write_title()

### Community 24 - "LogAuditoria"
Cohesion: 0.10
Nodes (20): 1. El Operador de Mesa de Ayuda (Nivel 1), 1. ¿Tengo que crearle "Niveles" a los usuarios?, 2. El monitor en la oficina (Auto-Refresh), 2. El Técnico (Miembro de un Grupo Resolutor - Nivel 2), 3. ¿Cómo se entera el técnico de que le llegó un ticket? (Notificaciones), 3. El flujo de Correos Electrónicos, 4. ¿Me preocupo de los correos ahora o al último?, Base de Datos y Normas de PostgreSQL (Supabase Best Practices) (+12 more)

### Community 25 - "migrar_desde_mysql.py"
Cohesion: 0.23
Nodes (13): ArchivoAdjuntoAdmin, CategoriaAdmin, PrioridadAdmin, TicketAdmin, TicketHistorialAdmin, ArchivoAdjunto, Categoria, Prioridad (+5 more)

### Community 26 - "UsuarioRepository"
Cohesion: 0.21
Nodes (4): PerfilUsuario, User, Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado., UsuarioRepository

### Community 27 - "actas.js"
Cohesion: 0.26
Nodes (8): agregarFilaDetalle(), buildSelectOptions(), editarActa(), fillForm(), getFormData(), guardarActa(), resetForm(), showError()

### Community 28 - "equipos.js"
Cohesion: 0.28
Nodes (10): abrirBitacora(), abrirModal(), cargarBitacora(), cargarEquipo(), csrfToken(), eliminarEquipo(), guardarEquipo(), initDataTable() (+2 more)

### Community 29 - "Rol"
Cohesion: 0.22
Nodes (6): Accion, Meta, PerfilUsuario, Rol de usuario (RBAC). Reemplaza al campo texto `perfil` de tbusuarios (PHP)., Devuelve True si el rol tiene el permiso indicado (bool True)., Rol

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
Cohesion: 0.15
Nodes (12): Command, normalizar_qs(), BaseCommand, Semilla inicial de catálogos básicos para ticsystem.  Crea la institución HGF, l, Articulo, Marca, Proveedor, Tipo de artículo / categoría de equipo. Reemplaza tbarticulos.     Ej: Notebook (+4 more)

### Community 40 - "auditoria_repository.py"
Cohesion: 0.40
Nodes (3): AuditoriaRepository, LogAuditoria, Repositorio de datos para el modelo LogAuditoria.     Encapsula la creación e i

### Community 47 - "RedesConfig"
Cohesion: 0.23
Nodes (4): PerfilUsuario, User, Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado., UsuarioRepository

### Community 144 - "EstadoEquipo"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 145 - "GraficosService"
Cohesion: 0.12
Nodes (11): Retorna el número de tickets vencidos vs en tiempo., Retorna la cantidad de tickets por categoría., Tickets creados en los últimos 6 meses., Top 5 activos con más fallas históricas., Se encarga de interactuar con el ORM de forma pesada y óptima     para extraer d, ReportesRepository, GraficosService, Toma los datos crudos del Repositorio y los adapta a las estructuras     requeri (+3 more)

### Community 147 - "TicketService"
Cohesion: 0.14
Nodes (9): User, Capa de Reglas de Negocio (Service) para Tickets.     Maneja la creación, cambio, Asigna el ticket a un técnico específico o a un grupo resolutor., Genera un correlativo secuencial anual único y thread-safe.         Usa select_f, Un técnico (miembro de un grupo o en general) se auto-asigna el ticket., TicketService, TicketCommentApiView, TicketResolveApiView (+1 more)

### Community 148 - "views.py"
Cohesion: 0.13
Nodes (20): obtener_kpis_generales(), CustomLoginView, CustomLogoutView, DashboardGeneralView, FuncionarioCreateAPIView, FuncionarioSearchAPIView, LoginRequiredMixin, TemplateView (+12 more)

### Community 149 - "Writing Guidelines for Postgres References"
Cohesion: 0.12
Nodes (15): 1. Concrete Transformation Patterns, 2. Error-First Structure, 3. Quantified Impact, 4. Self-Contained Examples, 5. Semantic Naming, Code Example Standards, Comments, Impact Level Guidelines (+7 more)

### Community 150 - "UsuarioRepository"
Cohesion: 0.11
Nodes (8): AuditoriaService, LogAuditoria, Servicio de negocio para gestionar la auditoría y trazabilidad del sistema., AuditoriaServiceTests, TestCase, Pruebas unitarias para validar las reglas de negocio en UsuarioService., Pruebas unitarias para validar el registro de logs de auditoría., UsuarioServiceTests

### Community 151 - "UsuarioServiceTests"
Cohesion: 0.25
Nodes (8): audit_trail_equipo(), Devuelve un usuario 'sistema' para bitácoras automáticas.     Crea uno si no exi, Import local para evitar circular imports., Devuelve representación en texto del valor de un campo FK o plano., Crea BitacoraEquipo automático al crear/editar un equipo., timezone_localdate(), _usuario_sistema(), _valor_campo()

### Community 152 - "🏗️ Principios Arquitectónicos Obligatorios"
Cohesion: 0.18
Nodes (10): 1. Requisitos Previos, 2. Instalación, 3. Base de Datos Inicial, 4. Ejecución del Servidor, 🛠️ Despliegue en Producción, 📦 Estructura de Directorios, Guía de Inicio y Ejecución (Entorno Local), Plantilla Oficial - Hospital Dr. Gustavo Fricke (+2 more)

### Community 153 - "🏗️ Principios Arquitectónicos Obligatorios"
Cohesion: 0.18
Nodes (10): 1. Requisitos Previos, 2. Instalación, 3. Base de Datos Inicial, 4. Ejecución del Servidor, 🛠️ Despliegue en Producción, 📦 Estructura de Directorios, Guía de Inicio y Ejecución (Entorno Local), Plantilla Oficial - Hospital Dr. Gustavo Fricke (+2 more)

### Community 154 - "Section Definitions"
Cohesion: 0.20
Nodes (9): 1. Query Performance (query), 2. Connection Management (conn), 3. Security & RLS (security), 4. Schema Design (schema), 5. Concurrency & Locking (lock), 6. Data Access Patterns (data), 7. Monitoring & Diagnostics (monitor), 8. Advanced Features (advanced) (+1 more)

### Community 155 - "EquipoBitacoraView"
Cohesion: 0.33
Nodes (6): DashboardGeneralView, LoginRequiredMixin, TemplateView, Dashboard de inicio general con estadísticas agregadas del sistema., Vista para el módulo de Gestión de Usuarios., UsuariosDashboardView

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
Cohesion: 0.29
Nodes (6): Arquitectura y Patrones (Reglas Estrictas), Base de Datos, Base de Datos y Normas de PostgreSQL (Supabase Best Practices), Contexto y Estado del Proyecto (TIC System - Hospital Marga Marga), Progreso y MÃ³dulos Activos, Â¿CÃ³mo continuar el trabajo?

### Community 165 - "load_grupos.py"
Cohesion: 0.15
Nodes (10): Command, BaseCommand, Estado, GrupoResolutor, Impacto, Meta, Modelos del módulo Enterprise Helpdesk (Gestión de Incidentes).  Normalización (, Tipo (+2 more)

### Community 166 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 167 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 168 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 169 - "Command"
Cohesion: 0.40
Nodes (3): Command, BaseCommand, Semilla inicial de roles y permisos para ticsystem.  Crea los 6 roles por defect

### Community 173 - "LogAuditoriaAdmin"
Cohesion: 0.29
Nodes (4): LogAuditoriaAdmin, PerfilUsuarioInline, UserAdmin, DjangoUserAdmin

### Community 245 - "xat.md"
Cohesion: 0.50
Nodes (3): Agregar a Valeria (que es el usuario de mesa de ayuda) al grupo si no está, Crear grupo Mesa de Ayuda, Get Roles

## Knowledge Gaps
- **323 isolated node(s):** `Migration`, `Estado`, `Meta`, `TipoItem`, `Migration` (+318 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **92 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditoriaService` connect `UsuarioRepository` to `UsuarioService`, `views.py`, `Acta`, `models.py`, `Anexo`, `views.py`, `UsuarioServiceTests`, `models.py`, `views.py`, `views.py`, `EquipoBitacoraView`, `Rol`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Equipo` connect `models.py` to `views.py`, `views.py`, `Command`, `load_grupos.py`, `models.py`, `Unidad`, `models.py`, `EquipoRepository`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Unidad` connect `models.py` to `views.py`, `Acta`, `signals.py`, `models.py`, `Unidad`, `models.py`, `models.py`, `views.py`, `views.py`, `admin.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 48 inferred relationships involving `AuditoriaService` (e.g. with `ActaActionView` and `ActaDetailView`) actually correct?**
  _`AuditoriaService` has 48 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `UsuarioService` (e.g. with `UsuarioRepository` and `AuditoriaServiceTests`) actually correct?**
  _`UsuarioService` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Command` (e.g. with `Acta` and `ActaDetalle`) actually correct?**
  _`Command` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Migration`, `Estado`, `Meta` to the rest of the system?**
  _509 weakly-connected nodes found - possible documentation gaps or missing edges._