# Plantilla Oficial - Hospital Dr. Gustavo Fricke

Este repositorio contiene la **Plantilla Base Oficial (Boilerplate)** para la construcción de nuevos módulos y sistemas web institucionales del Hospital Dr. Gustavo Fricke. La arquitectura de este proyecto está diseñada bajo estrictos estándares corporativos para garantizar escalabilidad, seguridad, y mantenibilidad.

## Tecnologías Principales

*   **Backend:** Python 3.x, Django
*   **Base de Datos:** SQLite (Desarrollo) / PostgreSQL (Producción)
*   **Frontend:** Bootstrap 4, Framework UI Gobierno Digital (gob.cl), jQuery, DataTables (Server-side)
*   **Despliegue:** Nginx, Gunicorn, systemd (Sockets Unix)

---

## 🏗️ Principios Arquitectónicos Obligatorios

Cualquier nuevo desarrollo basado en esta plantilla **DEBE** adherirse a los siguientes estándares:

1.  **Clean Architecture y Patrón Multicapa:**
    *   **Views:** Exclusivamente para enrutamiento HTTP y validación inicial de peticiones. **Prohibida la lógica de negocio.**
    *   **Services:** Toda la lógica de negocio, validaciones cruzadas y coordinación reside aquí.
    *   **Repositories:** Única capa autorizada para consultas complejas o acceso directo a la capa de datos que no sea un simple ORM call básico.
    *   **Models:** Entidades de dominio. Prohibido incluir procesos pesados.
2.  **SOLID & SRP:** Cada módulo/app debe tener una responsabilidad única. (Ej: La reportería debe ir en una app separada `reportes`).
3.  **Frontend Desacoplado:**
    *   **Prohibido mezclar HTML con JavaScript.** Todo JS debe ir en archivos separados en `static/`.
    *   Todas las tablas dinámicas deben usar **DataTables con Server-Side Processing (AJAX)**. No se permite carga masiva de datos en el frontend inicial.
4.  **Seguridad (OWASP Top 10):**
    *   Implementa mitigación de fuerza bruta (`django-axes`).
    *   Protección estricta CSRF y validación de permisos por rol.

---

### Guía de Inicio y Ejecución (Entorno Local)

### 1. Requisitos Previos
*   Python 3.10+
*   Entorno Virtual (`venv`)

### 2. Instalación

Clonar la plantilla e inicializar el entorno:

```bash
# Activar entorno virtual (Windows)
.\.venv\Scripts\activate
# (Linux)
# source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Base de Datos Inicial

La plantilla requiere inicializar sus modelos bases y cuenta con un script de creación:

```bash
python manage.py makemigrations core
python manage.py migrate
```

**Credenciales de Prueba por Defecto:**
*   **RUT (Usuario):** `55555555-5`
*   **Contraseña:** `Fricke`

### 4. Ejecución del Servidor

El servidor cuenta con configuraciones por entorno (`config/settings/local.py`, `config/settings/production.py`). Por defecto, `manage.py` utiliza `local`.

```bash
python manage.py runserver
```
Accede a `http://127.0.0.1:8000`.

---

## 📦 Estructura de Directorios

```text
plantillaOficialHGF/
│
├── config/                 # (Anteriormente telecomunicaciones)
│   ├── settings/           # Settings divididos (base, local, production)
│   ├── asgi.py
│   ├── wsgi.py
│   └── urls.py             # Enrutador principal
│
├── core/                   # (Anteriormente correos) App base del framework
│   ├── templates/core/     # Templates oficiales (base.html, login.html)
│   ├── services/           # Capa de Lógica de Negocio
│   ├── repositories/       # Capa de Acceso a Datos
│   └── ...                 
│
├── deploy/                 # Scripts oficiales para infraestructura
│   ├── plantilla.service   # Systemd service para Gunicorn
│   └── nginx.conf          # Configuración del proxy reverso
│
└── static/                 # Recursos estáticos globales y JS separados
```

---

## 🛠️ Despliegue en Producción

El sistema está diseñado para ejecutarse en entornos corporativos Linux. 

1.  El servicio debe comunicarse mediante **Sockets Unix**, no puertos TCP (por razones de performance y seguridad).
2.  Gunicorn es controlado vía **systemd** utilizando el archivo proveído en `deploy/plantilla.service`.
3.  No olvidar configurar el archivo `.env` en producción. **Bajo ninguna circunstancia** se deben versionar o hardcodear credenciales en el código fuente.
