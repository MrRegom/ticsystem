#!/bin/bash
# Script de Respaldo - TicSystem
# Genera un volcado de la base de datos PostgreSQL y comprime los archivos multimedia.

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"

echo "================================================="
echo "Iniciando respaldo de TicSystem - $TIMESTAMP"
echo "================================================="

# 1. Crear directorio de backups si no existe
mkdir -p $BACKUP_DIR

# 2. Respaldo de Base de Datos (PostgreSQL)
echo "[1/2] Exportando base de datos..."
docker exec -t ticsystem_db pg_dump -U ticsystem_admin ticsystem_db -c > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

if [ $? -eq 0 ]; then
    echo "  -> Base de datos respaldada con éxito."
else
    echo "  -> ERROR al respaldar la base de datos."
fi

# 3. Respaldo de Archivos Multimedia (Imágenes, documentos, etc.)
echo "[2/2] Comprimiendo archivos multimedia..."
tar -czf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz ./media

if [ $? -eq 0 ]; then
    echo "  -> Archivos multimedia respaldados con éxito."
else
    echo "  -> ERROR al respaldar archivos multimedia."
fi

echo "================================================="
echo "Respaldo completado. Archivos guardados en: $BACKUP_DIR"
echo "- $BACKUP_DIR/db_backup_$TIMESTAMP.sql"
echo "- $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz"
echo "================================================="
