# Graph Report - .  (2026-07-10)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 1051 nodes · 2105 edges · 145 communities (111 shown, 34 thin omitted)
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 254 edges (avg confidence: 0.53)
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

## God Nodes (most connected - your core abstractions)
1. `AuditoriaService` - 57 edges
2. `Command` - 31 edges
3. `UsuarioService` - 31 edges
4. `get_client_ip()` - 31 edges
5. `Equipo` - 29 edges
6. `extract_validation_error()` - 28 edges
7. `Acta` - 24 edges
8. `Piso` - 23 edges
9. `Unidad` - 23 edges
10. `Edificio` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Command` --uses--> `Acta`  [INFERRED]
  core/management/commands/migrar_desde_mysql.py → actas/models.py
- `Command` --uses--> `ActaDetalle`  [INFERRED]
  core/management/commands/migrar_desde_mysql.py → actas/models.py
- `ActasDashboardView` --uses--> `AuditoriaService`  [INFERRED]
  actas/views.py → core/services/auditoria_service.py
- `ActaListView` --uses--> `AuditoriaService`  [INFERRED]
  actas/views.py → core/services/auditoria_service.py
- `ActaActionView` --uses--> `AuditoriaService`  [INFERRED]
  actas/views.py → core/services/auditoria_service.py

## Import Cycles
- None detected.

## Communities (145 total, 34 thin omitted)

### Community 0 - "UsuarioService"
Cohesion: 0.05
Nodes (31): Actualizar acta existente., obtener_kpis_generales(), User, Servicio de negocio para la gestión de operadores y usuarios del hospital., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso para DataTables Server-side de Usuarios., Retorna el RUT en formato limpio sin puntos y con guion (ej: 12345678-9). (+23 more)

### Community 1 - "views.py"
Cohesion: 0.07
Nodes (39): EquipoRepository, Repositorio para Equipo y bitácoras asociadas., EquipoService, _normalizar_nombre(), Servicio para operaciones CRUD y consultas de Equipos., Crea un equipo validando FKs y unicidad de serial.         Dispara el signal pos, Caso de uso para DataTables Server-side de Equipos., Normaliza un nombre de modelo al formato usado en PHP (vistas/img/modelos/). (+31 more)

### Community 2 - "views.py"
Cohesion: 0.08
Nodes (33): ArchivoAdjuntoAdmin, CategoriaAdmin, PrioridadAdmin, TicketAdmin, TicketHistorialAdmin, Command, BaseCommand, Semilla de catálogos de tickets (prioridades y categorías) + SLA de mantenciones (+25 more)

### Community 3 - "MantenedorService"
Cohesion: 0.08
Nodes (22): MantenedorRepository, MantenedorRepository ==================== Capa de acceso a datos para los catálo, Retorna una lista paginada, ordenada y filtrada para DataTables server-side., Total de registros sin filtrar (recordsTotal para DataTables)., Total de registros filtrados (recordsFiltered para DataTables)., Persiste la instancia (INSERT o UPDATE). Transacción atómica., Elimina la instancia. Transacción atómica., Repositorio genérico para todos los catálogos del sistema.      Métodos de lectu (+14 more)

### Community 4 - "Acta"
Cohesion: 0.09
Nodes (19): ActaAdmin, ActaDetalleAdmin, ActaDetalleInline, Acta, ActaDetalle, Estado, Meta, Modelos del módulo de Actas de Entrega de Equipamiento.  Normalización aplicada (+11 more)

### Community 5 - "Command"
Cohesion: 0.08
Nodes (13): Command, BaseCommand, abrir_mysql(), decodificar_firma_base64(), limpiar_serial(), normalizar(), Helpers para la migracion de datos MySQL→PostgreSQL (Fase 5).  Funciones utilita, Abre conexion PyMySQL a la BD legacy (XAMPP MariaDB). (+5 more)

### Community 6 - "models.py"
Cohesion: 0.10
Nodes (21): BitacoraEquipoAdmin, BitacoraEquipoInline, BitacoraOpcionAdmin, EquipoAdmin, BitacoraEquipo, BitacoraOpcion, Equipo, Meta (+13 more)

### Community 7 - "models.py"
Cohesion: 0.14
Nodes (18): AreaHospitalaria, Meta, Modelo, Piso, PMA, Proveedor, Modelos de catálogos / mantenedores del sistema TIC.  Normalización aplicada (, Sector geográfico o de ala (ej. NORTE, SUR, A, AU, EP). (+10 more)

### Community 8 - "UsuarioRepository"
Cohesion: 0.10
Nodes (13): PerfilUsuario, User, Repositorio de datos para el modelo User de Django y su PerfilUsuario asociado., UsuarioRepository, User, Algoritmo Módulo 11 para validación de RUT chileno., Caso de uso: Eliminar un usuario del sistema (operador), impidiendo la auto-elim, Caso de uso para DataTables Server-side de Usuarios. (+5 more)

### Community 9 - "Anexo"
Cohesion: 0.13
Nodes (10): AnexoAdmin, RequerimientoCambioAdmin, RequerimientoCambioInline, Anexo, Requerimiento de cambio de visor para un anexo.     Normaliza 2NF: extrae los ~1, Anexo telefónico IP. Reemplaza tabla `anexos` del esquema PHP., RequerimientoCambio, AnexoRepository (+2 more)

### Community 10 - "views.py"
Cohesion: 0.13
Nodes (17): CustomLoginView, CustomLogoutView, DashboardGeneralView, _get_client_ip(), LoginRequiredMixin, TemplateView, View, Dashboard de inicio general con estadísticas agregadas del sistema. (+9 more)

### Community 11 - "UsuarioServiceTests"
Cohesion: 0.08
Nodes (7): AuditoriaServiceTests, CorreoServiceTests, TestCase, Pruebas unitarias para validar el registro de logs de auditoría., Pruebas unitarias para validar las reglas de negocio en UsuarioService., Pruebas unitarias para validar las reglas de negocio en CorreoService., UsuarioServiceTests

### Community 12 - "Unidad"
Cohesion: 0.13
Nodes (12): Estado, Meta, Modelos del módulo de Anexos Telefónicos IP.  Normalización aplicada (3NF): - An, Semilla inicial de catálogos básicos para ticsystem.  Crea la institución HGF, l, Edificio, Institucion, Unidad / Servicio hospitalario. Reemplaza tbunidades., Institución / sede hospitalaria (ej. HGF). Reemplaza tb_instituciones. (+4 more)

### Community 13 - "models.py"
Cohesion: 0.18
Nodes (16): InfraestructuraRedAdmin, InfraestructuraRedInline, PmaAdmin, RangoIPAdmin, SlaConfiguracionAdmin, Estado, InfraestructuraRed, Meta (+8 more)

### Community 14 - "admin.py"
Cohesion: 0.19
Nodes (15): AyudaRapidaAdmin, ChecklistItemAdmin, PendienteAdmin, WebAppAdmin, AyudaRapida, ChecklistItem, Estado, Meta (+7 more)

### Community 15 - "models.py"
Cohesion: 0.15
Nodes (7): LogAuditoriaAdmin, PerfilUsuarioInline, UserAdmin, Accion, Meta, PerfilUsuario, DjangoUserAdmin

### Community 16 - "mantenedores.js"
Cohesion: 0.23
Nodes (18): destroySelect2(), destroyTable(), editar(), eliminar(), fillForm(), getColumns(), getFormData(), guardar() (+10 more)

### Community 17 - "views.py"
Cohesion: 0.20
Nodes (11): parse_datatables_params(), IpActionView, IpDetailView, IpListView, LoginRequiredMixin, TemplateView, View, Vistas del módulo Redes / IPAM. (+3 more)

### Community 18 - "CredencialCorreo"
Cohesion: 0.23
Nodes (12): CredencialCorreoAdmin, GrupoCorreoAdmin, MiembroGrupoCorreoAdmin, MiembroGrupoCorreoInline, CredencialCorreo, GrupoCorreo, Meta, MiembroGrupoCorreo (+4 more)

### Community 19 - "AuditoriaService"
Cohesion: 0.27
Nodes (12): AnexoService, AnexoActionView, AnexoDetailView, AnexoListView, AnexosDashboardView, LoginRequiredMixin, TemplateView, View (+4 more)

### Community 20 - "UsuarioServiceTests"
Cohesion: 0.12
Nodes (5): AuditoriaServiceTests, TestCase, Pruebas unitarias para validar las reglas de negocio en UsuarioService., Pruebas unitarias para validar el registro de logs de auditoría., UsuarioServiceTests

### Community 21 - "admin.py"
Cohesion: 0.12
Nodes (14): ArticuloAdmin, EdificioAdmin, EstadoEquipoAdmin, InstitucionAdmin, MarcaAdmin, ModeloAdmin, ModeloAnexoAdmin, ModeloInline (+6 more)

### Community 22 - "views.py"
Cohesion: 0.24
Nodes (11): ActaActionView, ActaDetailView, ActaListView, ActasDashboardView, LoginRequiredMixin, TemplateView, View, API JSON para obtener detalle de un acta (para modal de edición). (+3 more)

### Community 23 - "Command"
Cohesion: 0.37
Nodes (6): auto_width(), Command, BaseCommand, style_header(), write_rows(), write_title()

### Community 24 - "LogAuditoria"
Cohesion: 0.22
Nodes (7): LogAuditoria, AuditoriaRepository, LogAuditoria, Repositorio de datos para el modelo LogAuditoria.     Encapsula la creación e i, AuditoriaService, LogAuditoria, Servicio de negocio para gestionar la auditoría y trazabilidad del sistema.

### Community 25 - "migrar_desde_mysql.py"
Cohesion: 0.17
Nodes (10): Migracion de datos desde MySQL legacy (equipamiento2026) a PostgreSQL (ticsystem, normalizar_qs(), Articulo, Marca, ModeloAnexo, Tipo de artículo / categoría de equipo. Reemplaza tbarticulos.     Ej: Notebook, Marca de equipo. Reemplaza tbmarca., Modelo de anexo telefónico IP (catálogo separado de Modelo de equipos).     Ree (+2 more)

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
Cohesion: 0.25
Nodes (8): audit_trail_equipo(), Devuelve un usuario 'sistema' para bitácoras automáticas.     Crea uno si no exi, Import local para evitar circular imports., Devuelve representación en texto del valor de un campo FK o plano., Crea BitacoraEquipo automático al crear/editar un equipo., timezone_localdate(), _usuario_sistema(), _valor_campo()

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

## Knowledge Gaps
- **48 isolated node(s):** `Migration`, `Estado`, `Meta`, `TipoItem`, `Migration` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **34 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AuditoriaService` connect `AuditoriaService` to `UsuarioService`, `views.py`, `MantenedorService`, `models.py`, `views.py`, `UsuarioServiceTests`, `models.py`, `views.py`, `UsuarioServiceTests`, `views.py`, `LogAuditoria`?**
  _High betweenness centrality (0.113) - this node is a cross-community bridge._
- **Why does `PerfilUsuario` connect `models.py` to `UsuarioService`, `migrar_desde_mysql.py`, `UsuarioRepository`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `Equipo` connect `models.py` to `views.py`, `views.py`, `signals.py`, `Command`, `models.py`, `Unidad`, `migrar_desde_mysql.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 45 inferred relationships involving `AuditoriaService` (e.g. with `ActaActionView` and `ActaDetailView`) actually correct?**
  _`AuditoriaService` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Command` (e.g. with `Acta` and `ActaDetalle`) actually correct?**
  _`Command` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `UsuarioService` (e.g. with `UsuarioRepository` and `AuditoriaServiceTests`) actually correct?**
  _`UsuarioService` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `Equipo` (e.g. with `BitacoraEquipoAdmin` and `BitacoraEquipoInline`) actually correct?**
  _`Equipo` has 4 INFERRED edges - model-reasoned connections that need verification._