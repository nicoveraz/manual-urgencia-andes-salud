#!/bin/bash
#
# Script de backup para Wiki.js
# Manual de Procedimientos - Servicio de Urgencia
# Clínica Andes Salud
#
# Genera backups cifrados con AES-256 (passphrase desde variable de entorno).
# Para restaurar:
#   gpg --decrypt wiki_backup_XXXX.sql.gz.gpg | gunzip | \
#     docker exec -i wiki-db psql -U wikijs wiki
#

set -e

# Configuración
BACKUP_DIR="${HOME}/backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wiki_backup_${TIMESTAMP}.sql"

# Passphrase para cifrado — definir en .env o exportar antes de ejecutar
# Ejemplo: export BACKUP_PASSPHRASE="una-frase-larga-y-segura"
if [ -z "${BACKUP_PASSPHRASE}" ]; then
  echo "ERROR: Variable BACKUP_PASSPHRASE no definida."
  echo "Exportar antes de ejecutar: export BACKUP_PASSPHRASE='tu-passphrase-segura'"
  exit 1
fi

# Crear directorio de backups si no existe
mkdir -p "${BACKUP_DIR}"
chmod 700 "${BACKUP_DIR}"

echo "=== Backup de Wiki.js ==="
echo "Fecha: $(date)"
echo ""

# Realizar backup de PostgreSQL
echo "[1/4] Creando backup de base de datos..."
docker exec wiki-db pg_dump -U wikijs wiki > "${BACKUP_FILE}"

# Comprimir backup
echo "[2/4] Comprimiendo backup..."
gzip "${BACKUP_FILE}"

# Cifrar backup con AES-256
echo "[3/4] Cifrando backup..."
gpg --batch --yes --symmetric --cipher-algo AES256 \
    --passphrase "${BACKUP_PASSPHRASE}" \
    "${BACKUP_FILE}.gz"
# Eliminar el archivo sin cifrar
rm -f "${BACKUP_FILE}.gz"

# Eliminar backups antiguos
echo "[4/4] Limpiando backups antiguos (>${RETENTION_DAYS} días)..."
find "${BACKUP_DIR}" -name "wiki_backup_*.sql.gz.gpg" -mtime +${RETENTION_DAYS} -delete

# Mostrar resultado
BACKUP_SIZE=$(du -h "${BACKUP_FILE}.gz.gpg" | cut -f1)
echo ""
echo "=== Backup completado (cifrado AES-256) ==="
echo "Archivo: ${BACKUP_FILE}.gz.gpg"
echo "Tamaño: ${BACKUP_SIZE}"
echo ""

# Listar backups existentes
echo "Backups disponibles:"
ls -lh "${BACKUP_DIR}"/wiki_backup_*.sql.gz.gpg 2>/dev/null || echo "No hay backups anteriores"
