# TICsystem — Documentación Técnica Completa

> **Uso interno:** Este archivo explica el proyecto a cualquier desarrollador o IA que trabaje en él.
> **Audiencia:** Desarrolladores backend/frontend, agentes de IA, equipos de soporte.
> Está en `.agents/` (excluido del repositorio público vía `.gitignore`).

---

## 1. ¿Qué es TICsystem?

TICsystem es una **plataforma web empresarial de gestión TIC hospitalaria** para el **Hospital Provincial Marga Marga (HPMM)**, Servicio de Salud Viña del Mar - Quillota, Chile.

Reemplaza procesos manuales (papel, Excel) con un sistema centralizado:

| Módulo | Descripción |
|---|---|
| **Inventario (Equipos)** | Catálogo de activos TI con ficha QR, historial, exportación Excel/PDF |
| **Mesa de Ayuda (Tickets)** | Helpdesk Kanban con SLA, escalamiento, notificaciones y auditoría |
| **Actas** | Generación y firma digital de actas de entrega en PDF |
| **Anexos IP** | Registro de IPs, VLANs, patch panels y switch ports |
| **Reportes (BI)** | Dashboard con métricas, gráficos y exportación |
| **Mantenedores** | Estructura organizacional y física del hospital |
| **Auditoría** | Trazabilidad de cada acción del sistema |
| **Correos** | Integración SMTP para notificaciones |

---

## 2. Stack Tecnológico

```
Backend:      Django 6.0 + Python 3.12
WSGI:         Gunicorn
Base de datos: PostgreSQL 15 (Docker) / SQLite (desarrollo local)
Frontend:     HTML5 + Bootstrap 4 + Vanilla CSS (Fluent Design)
JS:           jQuery + DataTables + Select2 + SweetAlert2 + ApexCharts
PDF:          WeasyPrint
Excel:        openpyxl
QR:           qrcode[pil]
Auth:         Django Auth + django-axes (bloqueo por IP)
Servidor web: Nginx (reverse proxy)
Contenedores: Docker + Docker Compose
```

**IMPORTANTE:** Todas las librerías JS/CSS están en `static/vendor/` (sin CDN). La app funciona **100% sin internet**.

---

## 3. Arquitectura del Proyecto

```
ticsystem/
├── config/                  ← Settings Django (base, development, production)
├── core/                    ← Login, dashboard, base templates, base.html
├── equipos/                 ← Inventario de activos TI
├── tickets/                 ← Mesa de ayuda / Helpdesk
├── actas/                   ← Actas de entrega con firma digital
├── anexos/                  ← Registro de IPs y conectividad
├── mantenedores/            ← Maestros: Áreas, Unidades, Edificios, Pisos, PMAs
├── sla/                     ← Configuración de SLA y prioridades
├── reportes/                ← Módulo BI (gráficos, exportaciones)
├── auditoria/               ← Log de actividad del sistema
├── correos/                 ← Envío de e-mails (SMTP)
├── redes/                   ← Gestión de IPs de red
├── utilidades/              ← Helpers transversales
├── visor/                   ← Ficha pública de equipo (sin login, acceso QR)
├── conocimiento/            ← KEDB (base de conocimiento para tickets)
│
├── static/                  ← CSS, JS, imágenes, vendor (todo local)
│   ├── css/global-theme.css ← Sistema de diseño Fluent (.ms-* clases)
│   ├── js/                  ← Scripts por módulo
│   └── vendor/              ← Bootstrap, jQuery, FontAwesome, DataTables, Inter font...
│
├── nginx/                   ← Config Nginx producción
├── Dockerfile               ← Imagen Docker de la app
├── docker-compose.yml       ← Orquestación: web + db + nginx
├── requirements.txt         ← Dependencias Python
└── .env.example             ← Plantilla de variables de entorno
```

### Principios Arquitectónicos (OBLIGATORIOS)
- **Views** → solo orquestan, sin lógica pesada
- **Services** → lógica de negocio
- **Templates** → solo presentación, sin lógica
- **JS** → archivos separados en `static/js/`, nunca incrustado en HTML
- **CSS** → usar siempre clases `.ms-*` de `global-theme.css` (Fluent Design)
- **Modales** → siempre `border-radius: 0` (regla de diseño del proyecto)

---

## 4. Jerarquía Organizacional del Hospital

```
Institución (HPMM)
└── Edificio → Piso → Sector → PMA (rack/closet) → Equipos

Área Hospitalaria → Unidad → Recinto → Equipos
```

Los mantenedores de estos datos están en `deploy/mantenedores_dump_utf8.json`.

---

## 5. Variables de Entorno (.env)

Basado en `.env.example`. Cambiar antes de cada instalación:

```env
DATABASE_URL=postgres://ticsystem_admin:CLAVE@db:5432/ticsystem_db
DJANGO_SECRET_KEY=cambia-esto-por-clave-segura
DJANGO_ENV=production
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SECURE_SSL_REDIRECT=False
ALLOWED_HOSTS=localhost,127.0.0.1,[IP-DEL-SERVIDOR],web,ticsystem_web
DB_NAME=ticsystem_db
DB_USER=ticsystem_admin
DB_PASSWORD=CLAVE_SEGURA
```

> `.env` NUNCA va al repositorio Git.

---

## 6. Flujo de Trabajo: Desarrollo → Producción

### Desarrollo local
```bash
.venv\Scripts\activate
python manage.py runserver
```

### Subir cambios a GitHub
```bash
git add .
git commit -m "feat: descripcion"
git push origin main
```

### Actualizar producción (cambio de código)
```bash
ssh root@[IP-SERVIDOR]
cd /opt/ticsystem-prod
git pull origin main
docker compose restart web
# Si cambiaste requirements.txt:
# docker compose up -d --build
```

---

## 7. Despliegue Completo desde Cero (Nuevo Servidor)

### Prerrequisitos
- Servidor Linux (Ubuntu 22.04+), acceso root, internet disponible.

```bash
# 1. Conectarse
ssh root@[IP-DEL-SERVIDOR]

# 2. Liberar puertos (si hay Apache/Nginx preinstalado)
systemctl stop nginx   || true
systemctl disable nginx || true
systemctl stop apache2  || true
systemctl disable apache2 || true

# 3. Instalar Docker y Git
apt-get update && apt-get install -y git curl
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
apt-get install -y docker-compose-plugin

# 4. Clonar repositorio
cd /opt
git clone https://github.com/MrRegom/ticsystem.git ticsystem-prod
cd ticsystem-prod

# 5. Configurar .env
cp .env.example .env
nano .env
# → Editar ALLOWED_HOSTS con la IP real del servidor

# 6. Levantar contenedores
docker compose up -d --build
# Esperar 3-5 min. Verificar: docker ps (deben verse 3 contenedores UP)

# 7. Cargar datos del hospital (desde TU laptop, otra terminal):
scp deploy/mantenedores_dump_utf8.json root@[IP-SERVIDOR]:/root/

# Volver al servidor:
docker cp /root/mantenedores_dump_utf8.json ticsystem_web:/app/mantenedores_dump_utf8.json
docker exec ticsystem_web python manage.py loaddata mantenedores_dump_utf8.json --settings=config.settings.production

# 8. Abrir navegador: http://[IP-DEL-SERVIDOR]
# → Debe aparecer pantalla de Login de TICsystem
```

---

## 8. Contenedores Docker

| Contenedor | Rol | Puerto |
|---|---|---|
| `ticsystem_web` | Django + Gunicorn | interno 8000 |
| `ticsystem_db` | PostgreSQL 15 | interno 5432 |
| `ticsystem_nginx` | Nginx reverse proxy | **80 → 8000** |

Datos BD en `./datos_db/` | Archivos media en `./media/`

---

## 9. Roles de Usuario

| Rol | Permisos |
|---|---|
| Administrador | Acceso total, usuarios, configuración |
| Dispatcher | Asigna tickets a técnicos y grupos |
| Técnico | Atiende tickets de su grupo, registra equipos |
| Supervisor | Solo lectura de reportes y SLA |

Crear usuarios en: `/usuarios/`

---

## 10. Comandos Útiles en Producción

```bash
# Logs en tiempo real
docker compose logs -f web

# Entrar al contenedor
docker exec -it ticsystem_web bash

# Migraciones
docker exec ticsystem_web python manage.py migrate --settings=config.settings.production

# Crear superusuario
docker exec -it ticsystem_web python manage.py createsuperuser --settings=config.settings.production

# Backup de BD
docker exec ticsystem_db pg_dump -U ticsystem_admin ticsystem_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
cat backup.sql | docker exec -i ticsystem_db psql -U ticsystem_admin -d ticsystem_db

# Reiniciar todo
docker compose restart

# Apagar (sin borrar datos)
docker compose down

# Borrar TODO (¡PELIGROSO! borra la BD)
docker compose down -v
```

---

## 11. Archivos Clave para Contexto Rápido

| Archivo | Para qué sirve |
|---|---|
| `config/settings/base.py` | Apps instaladas, middleware, BD base |
| `config/settings/production.py` | Settings de producción, seguridad |
| `static/css/global-theme.css` | Sistema de diseño completo |
| `static/js/equipos.js` | Toda la lógica JS del inventario |
| `static/js/tickets-kanban.js` | Lógica del Kanban y creación de tickets |
| `deploy/mantenedores_dump_utf8.json` | Snapshot de datos del hospital |
| `deploy/TORPEDERO_SIMULACRO.md` | Guía de despliegue paso a paso |
| `docker-compose.yml` | Orquestación de los 3 contenedores |
| `Dockerfile` | Imagen Python 3.12 + dependencias |
| `nginx/nginx.conf` | Reverse proxy y archivos estáticos |

---

## 12. Hitos y Optimizaciones Recientes (Actualizado)

*   **Rediseño UX:** Se modernizó la vista `403.html` (Accesos denegados) usando el sistema de diseño corporativo Fluent, removiendo estilos básicos (subrayados) y haciendo los mensajes más amigables ("No tienes acceso...").
*   **Gestión de Permisos:** Se consolidó el rol "Coordinador de Soporte" como perfil del sistema (`is_system=True`). Se aclaró la separación de responsabilidades: los técnicos dentro de un "Grupo Resolutor" solo resuelven tickets. Para crear, asignar o cerrar tickets, el perfil del usuario debe tener el permiso explícito `GESTIONAR_TICKETS`.
*   **Integridad de Datos (Mayúsculas):** Se implementó formateo forzado a **MAYÚSCULAS** a nivel global. Los datos de usuarios y funcionarios se transforman tanto en los inputs del frontend (AJAX/JS) como a nivel de motor de Base de Datos (sobreescritura del método `save()` y señales `pre_save`).
*   **Estricto Control de RUTs y Duplicados:** 
    *   **Backend:** La base de datos ahora blinda y unifica todos los RUTs ingresados al formato estándar `XXXXXXXX-X` (sin puntos, con guion y K mayúscula). Esto erradicó el problema crítico de registros duplicados (ej. `24028352-2` vs `24.028.352-2`). Se ejecutó un script global para limpiar los duplicados históricos.
    *   **Frontend (AJAX):** Se mejoró la validación en tiempo real en `mantenedores.js` y `usuarios.js`. Al escribir el RUT, el sistema hace la conversión internamente para consultar a la API, bloqueando inmediatamente la creación si existe, sin obligar al usuario a llenar todo el formulario para enterarse del error.
    *   **Seguridad de Edición:** El campo RUT se deshabilita automáticamente al editar un registro para proteger la llave de identidad y la integridad referencial.
*   **Ergonomía de Formularios:** Se rediseñó el orden del modal de Mantenedores. El RUT fue posicionado como el primer campo (prioridad visual). La sección de "Dependencias/Ubicación" fue compactada, ubicando "Cargo" y "Unidad" en la misma línea para aprovechar el espacio.
*   **Auditoría de Arquitectura (Rendimiento Server-Side):** Se validó que el sistema está 100% optimizado para el volumen de datos de un hospital.
    *   *Funcionarios (Mantenedores):* Usa DataTables con `serverSide: true`.
    *   *Equipos (Inventario):* Usa motor AJAX propio (`eqLoadList`) con paginación real de Base de Datos.
*   **Optimizaciones de Rendimiento UI/UX en Pantallas Pequeñas:** Se diagnosticó y corrigió un colapso visual en la cuadrícula (CSS Grid) del Inventario de Equipos en pantallas de notebook (`< 1078px`). La columna de "Ubicación" (`1fr`) se reducía a 0px ocultando su contenido (Ej: "Edificio Principal"), forzando que la siguiente columna (PMA) pareciera ocupar su lugar. Se reemplazó por `minmax(150px, 1fr)` garantizando su visibilidad y activando el scroll horizontal necesario para la densidad de datos. Además, se forzó un *Cache Buster* (`v=4.5`) para propagar cambios en tiempo real.
*   **Buscador AJAX de Activos en Tickets:** Se eliminó la ineficiente carga estática (primeros 1000 registros) del selector de equipos en el Kanban de Tickets. Se reemplazó por una conexión Select2 con AJAX apuntando al nuevo endpoint `apiSearchEquipos`, asegurando que cualquier activo recién ingresado por otro usuario sea localizable de inmediato, cumpliendo estándares empresariales (Enterprise grade).
    *   *Identidades (Usuarios):* Interfaz Fluent UI con consultas directas a API restringidas y paginadas.
    *   *Protección de Trazabilidad:* La arquitectura se apoya en `on_delete=models.PROTECT`. No existe pérdida de datos al "eliminar"; el sistema obliga a un apagado lógico (Soft Delete mediante el switch "Activo") si el funcionario ya tiene historial (tickets, equipos).
