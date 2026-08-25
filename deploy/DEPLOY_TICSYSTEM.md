# Manual Técnico de Despliegue - TICsystem

Este documento detalla el procedimiento técnico estándar para el aprovisionamiento y despliegue del ecosistema TICsystem en el servidor del Hospital Provincial Marga Marga. 

## 1. Conexión y Acceso
Acceso mediante SSH al servidor de destino:
```bash
# Inicia una conexión segura remota al servidor destino utilizando el usuario 'desa'
ssh desa@10.69.86.107
```

## 2. Preparación del Entorno
Es necesario liberar el puerto 80 deshabilitando servicios web preexistentes para evitar conflictos con el proxy reverso del sistema.
```bash
# Detiene el servicio Nginx y deshabilita su inicio automático en futuros reinicios
sudo systemctl stop nginx || true
sudo systemctl disable nginx || true

# Detiene el servicio Apache2 y deshabilita su inicio automático
sudo systemctl stop apache2 || true
sudo systemctl disable apache2 || true

# Forza el cierre inmediato de cualquier proceso colgado de Apache en memoria
sudo pkill -9 apache2 || true
```

## 3. Instalación de Dependencias (Docker)

### Escenario A: Conectividad a Internet Disponible
Si el servidor cuenta con salida a internet, proceder con la instalación automatizada de Docker:
```bash
# Actualiza la lista de repositorios del sistema e instala el cliente de descargas 'curl'
sudo apt-get update && sudo apt-get install -y curl

# Descarga el script de instalación oficial de Docker y lo ejecuta con privilegios elevados
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instala el plugin necesario para orquestar múltiples contenedores (Docker Compose)
sudo apt-get install -y docker-compose-plugin
```

### Escenario B: Entorno Aislado (Offline)
Si el servidor se encuentra en una intranet sin salida, se requiere instalar el motor de Docker manualmente mediante paquetes compilados (`.deb`) y luego inyectar las imágenes del sistema (`ticsystem_images.tar`).

**Transferencia de Archivos (Desde tu equipo local de Windows):**
```bash
# Transfiere los instaladores de Docker (.deb) y el paquete de imágenes al servidor
scp paquetes_docker/*.deb desa@10.69.86.107:/tmp/
scp ticsystem_images.tar desa@10.69.86.107:/tmp/
```

**Instalación y Carga (En el servidor destino por SSH):**
```bash
# Instala el motor de Docker forzando el uso de los paquetes locales sin requerir internet
sudo dpkg -i /tmp/*.deb

# Instruye al motor de Docker recién instalado para que extraiga y registre las imágenes
sudo docker load -i /tmp/ticsystem_images.tar
```

## 4. Obtención del Repositorio
Se requiere clonar el código fuente en el directorio de aplicaciones del servidor.
```bash
# Navega al directorio estándar para software de terceros en sistemas Linux
cd /opt

# Descarga la última versión estable del código fuente desde el repositorio oficial
sudo git clone https://github.com/MrRegom/ticsystem.git ticsystem-prod

# Ingresa al directorio recién creado
cd ticsystem-prod
```

## 5. Configuración de Variables de Entorno
Establecer las credenciales y parámetros de seguridad del proyecto. Es **CRÍTICO** configurar la IP del servidor para evitar bloqueos de seguridad por parte del firewall aplicativo (Error 400 Bad Request).

```bash
# Duplica la plantilla de variables de entorno para crear el archivo de configuración activo
sudo cp .env.example .env

# Inyecta automáticamente la IP del servidor en la lista blanca de accesos permitidos
sudo sed -i 's/^ALLOWED_HOSTS=.*/ALLOWED_HOSTS=10.69.86.107,localhost,127.0.0.1,157.245.131.99,web,ticsystem_web/' .env
```
*(Nota del Operador: Si el servidor final de producción tiene una IP distinta a 10.69.86.107, se debe reemplazar dicha IP en el comando superior, o editar el archivo manualmente utilizando `sudo nano .env`).*

## 6. Orquestación de Contenedores
Ejecutar el levantamiento de los servicios definidos en la arquitectura (Web, Celery, Redis, Postgres, Nginx).

**Si utilizó el Escenario A (Online):**
```bash
# Compila las imágenes faltantes e inicia todos los servicios en segundo plano (-d)
sudo docker compose up -d --build
```

**Si utilizó el Escenario B (Offline):**
```bash
# Etiqueta las imágenes locales cargadas para que coincidan con la nomenclatura esperada en el despliegue
sudo docker image tag ticsystem-web:latest ticsystem-prod-web:latest || true
sudo docker image tag ticsystem-celery_worker:latest ticsystem-prod-celery_worker:latest || true

# Inicia todos los servicios forzando a Docker a no intentar construir ni descargar nada de internet (--no-build)
sudo docker compose up -d --no-build
```

## 7. Inicialización de Base de Datos (Producción)
Inyección de la estructura, tablas, roles, perfiles, y mantenedores corporativos utilizando el entorno de Django.
```bash
# Ejecuta las migraciones estructurales de la base de datos
sudo docker compose exec -it web python manage.py migrate --settings=config.settings.production

# Carga la data base de mantenedores (hospital, edificios, unidades)
sudo docker compose exec -it web python manage.py loaddata mantenedores_dump_utf8.json --settings=config.settings.production

# Configura los SLA por defecto y crea los roles de sistema
sudo docker compose exec -it web python seed_sla.py
sudo docker compose exec -it web python crear_rol.py
```

## 8. Verificación
El sistema principal se encuentra operativo. 
Acceso: `http://10.69.86.107`

---


