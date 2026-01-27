#!/bin/bash
#
# Script de backup para Wiki.js
# Manual de Procedimientos - Servicio de Urgencia
# Clínica Andes Salud
#

set -e

# Configuración
BACKUP_DIR="${HOME}/backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wiki_backup_${TIMESTAMP}.sql"

# Crear directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"

echo "=== Backup de Wiki.js ==="
echo "Fecha: $(date)"
echo ""

# Realizar backup de PostgreSQL
echo "[1/3] Creando backup de base de datos..."
docker exec wiki-db pg_dump -U wikijs wiki > "${BACKUP_FILE}"

# Comprimir backup
echo "[2/3] Comprimiendo backup..."
gzip "${BACKUP_FILE}"

# Eliminar backups antiguos
echo "[3/3] Limpiando backups antiguos (>${RETENTION_DAYS} días)..."
find "${BACKUP_DIR}" -name "wiki_backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete

# Mostrar resultado
BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz" | cut -f1)
echo ""
echo "=== Backup completado ==="
echo "Archivo: ${BACKUP_FILE}.gz"
echo "Tamaño: ${BACKUP_SIZE}"
echo ""

# Listar backups existentes
echo "Backups disponibles:"
ls -lh "${BACKUP_DIR}"/wiki_backup_*.sql.gz 2>/dev/null || echo "No hay backups anteriores"
