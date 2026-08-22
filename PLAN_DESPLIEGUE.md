# Plan de Despliegue Offline (TicSystem)

Este documento detalla la estrategia de instalación de TicSystem en un entorno de red interna (Intranet hospitalaria) sin acceso a Internet, utilizando una arquitectura de contenedores (Docker).

## 1. Arquitectura Lógica (Servidor Único)
Dado que se cuenta con una sola Máquina Virtual (Debian 12/13, 8GB RAM, 800GB SSD), se aislarán dos entornos completos mediante Docker:

- **Entorno de Producción:** Puerto `80` (o `443`). Base de datos independiente. Uso exclusivo para usuarios y médicos.
- **Entorno de Testing / QA:** Puerto `8080`. Base de datos independiente. Uso exclusivo para pruebas, simulacros y validación de nuevas versiones antes de pasarlas a producción.

## 2. Requisitos Previos en el Servidor (Hospital)
El único requerimiento hacia el área de Infraestructura/TI del Hospital es que la máquina virtual sea entregada con los siguientes binarios preinstalados:
- `docker` (Docker Engine)
- `docker-compose` (Docker Compose V2)

*Nota: Si el servidor es entregado sin estos binarios y sin salida a Internet, el despliegue incluirá un paso adicional manual (Camino B) que consistirá en instalar los binarios a partir de paquetes `.deb` trasladados mediante pendrive.*

## 3. Preparación "Offline" (Antes del Día 25)
En el equipo de desarrollo (con Internet), se prepararán las "cajas fuertes" (Imágenes de Docker) que contienen absolutamente todas las dependencias del sistema.

1. **Construcción de Imágenes:** Se compilará el código de Django, configurando Python, dependencias de sistema y requerimientos (`pip install`).
2. **Exportación (Docker Save):** Se exportarán las imágenes a archivos `.tar`.
   - `ticsystem_web.tar` (Aplicación)
   - `ticsystem_db.tar` (PostgreSQL)
   - `ticsystem_nginx.tar` (Servidor Web Nginx)
3. **Empaquetado:** Se trasladarán estos archivos `.tar` junto con el archivo de orquestación `docker-compose.yml` y las variables de entorno `.env` hacia un Pendrive o a través de la red interna (FTP/SCP).

## 4. Día del Despliegue (Día 25)
Una vez dentro del servidor del Hospital, los pasos de instalación serán los siguientes:

1. **Traslado de Archivos:** Copiar los archivos `.tar` y los archivos de configuración a una carpeta, ej: `/opt/ticsystem/`.
2. **Carga de Imágenes (Sin Internet):**
   ```bash
   docker load -i ticsystem_web.tar
   docker load -i ticsystem_db.tar
   docker load -i ticsystem_nginx.tar
   ```
3. **Levantamiento del Sistema:**
   ```bash
   docker-compose up -d
   ```
4. **Validación:** El comando leerá las imágenes previamente cargadas y orquestará la red interna de contenedores. El sistema estará operativo en pocos segundos sin necesidad de descargar ninguna dependencia externa.

## 5. Simulacro
Días antes del despliegue oficial, se realizará un ensayo en un entorno local desconectado de Internet para garantizar que las imágenes `.tar` han sido generadas correctamente y se levantan sin errores.
