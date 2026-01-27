#!/bin/bash
#
# Script de configuración inicial para Oracle Cloud
# Manual de Procedimientos - Servicio de Urgencia
# Clínica Andes Salud
#

set -e

echo "=== Configuración del servidor Oracle Cloud ==="
echo ""

# Actualizar sistema
echo "[1/5] Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Docker
echo "[2/5] Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker instalado. Necesitarás reconectar para aplicar los permisos de grupo."
else
    echo "Docker ya está instalado."
fi

# Instalar Docker Compose
echo "[3/5] Instalando Docker Compose..."
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    sudo apt install docker-compose-plugin -y
else
    echo "Docker Compose ya está instalado."
fi

# Configurar firewall
echo "[4/5] Configurando firewall..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3000 -j ACCEPT
sudo netfilter-persistent save

# Crear directorio para backups
echo "[5/5] Creando directorios..."
mkdir -p ~/backups

echo ""
echo "=== Configuración completada ==="
echo ""
echo "Próximos pasos:"
echo "1. Reconectar SSH para aplicar permisos de Docker"
echo "2. Clonar el repositorio"
echo "3. Configurar .env"
echo "4. Ejecutar: docker compose up -d"
echo ""
