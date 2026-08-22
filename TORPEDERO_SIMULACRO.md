# Torpedero Definitivo: Despliegue en Servidor Nuevo

Sigue estos comandos paso a paso para simular tu instalación desde cero en el servidor del hospital.

## 1. Conexión Inicial
Abre tu terminal y conéctate al servidor (reemplaza por la IP real del hospital):
```bash
ssh root@157.245.131.99
```

## 2. Preparar el Servidor y Liberar Puertos
A veces los servidores nuevos traen un Apache o Nginx preinstalado que bloquea el puerto 80. Lo apagaremos para que nuestro Nginx de Docker pueda tomar su lugar:
```bash
systemctl stop nginx || true
systemctl disable nginx || true
systemctl stop apache2 || true
systemctl disable apache2 || true
```

## 3. Instalación de Docker y Git (Modo Online)
Instalaremos las herramientas base en el sistema limpio:
```bash
# Actualizar repositorios
apt-get update

# Instalar Git
apt-get install -y git curl

# Instalar Docker automáticamente
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
apt-get install -y docker-compose-plugin
```

## 4. Descarga del Código
Vamos a crear la carpeta del proyecto y traer el código fuente (ahora ya contiene todas las correcciones necesarias).
```bash
# Ir a la carpeta óptima
cd /opt

# Clonar tu repositorio (te pedirá tu usuario y token/clave de GitHub)
git clone https://github.com/MrRegom/ticsystem.git ticsystem-prod

# Entrar a la carpeta
cd ticsystem-prod
```

## 5. Configuración
Copiaremos el archivo de ejemplo para crear tu entorno y establecer las variables:
```bash
cp .env.example .env

# (Opcional) Si necesitas cambiar la clave de base de datos o la IP en ALLOWED_HOSTS, edita este archivo:
# nano .env
```

## 6. Levantamiento del Sistema (La Magia)
Este comando descargará las dependencias de Python (incluido el lector de QR que arreglamos), levantará la base de datos y Nginx.
```bash
docker compose up -d --build
```
> *Nota: Demorará unos minutos en descargar todo por primera vez. Cuando termine, ejecuta `docker ps` y verifica que tienes 3 contenedores (web, db, nginx) en estado "Up".*

## 7. Restauración de Base de Datos
Como partimos de cero, la base de datos está totalmente vacía. Para recuperar la configuración base, inyectaremos tu respaldo (`ticsystem_base_dump.sql`).

Desde **TU COMPUTADOR** (abre otra ventana de terminal en tu PC local), sube el archivo al servidor:
```bash
scp ticsystem_base_dump.sql root@157.245.131.99:/root/
```

Vuelve a la consola del **SERVIDOR** e inyecta los datos:
```bash
cat /root/ticsystem_base_dump.sql | docker exec -i ticsystem_db psql -U ticsystem_admin -d ticsystem_db
```
> *Nota: Si ves un par de mensajes que dicen `ERROR: role "dbuser" does not exist`, ignóralos. Es solo una advertencia sobre los dueños antiguos de las tablas, los datos (los `COPY`) sí se inyectarán correctamente.*

## 8. ¡Prueba Final!
Abre tu navegador y entra a `http://157.245.131.99`. Deberías ver la pantalla de Login de tu sistema, cargado con las áreas y perfiles de mantenedores, y listo para usarse.
