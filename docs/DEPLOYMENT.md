# Guía de Despliegue

## 1. Configuración de Oracle Cloud

### Crear Instancia VM (Free Tier)

1. Ir a Oracle Cloud Console
2. Compute > Instances > Create Instance
3. Configuración:
   - **Shape:** VM.Standard.E2.1.Micro (Always Free)
   - **Image:** Ubuntu 22.04
   - **Boot Volume:** 50 GB
4. Descargar la clave SSH privada
5. Crear la instancia

### Configurar Networking

1. Ir a Networking > Virtual Cloud Networks
2. Seleccionar la VCN de la instancia
3. Security Lists > Default Security List
4. Agregar Ingress Rules:
   - **Puerto 80** (HTTP): Source CIDR `0.0.0.0/0`
   - **Puerto 443** (HTTPS): Source CIDR `0.0.0.0/0`
   - **Puerto 3000** (Wiki.js): Source CIDR `0.0.0.0/0` (temporal, solo para testing)

### Conectar a la Instancia

```bash
ssh -i /ruta/a/tu/clave.key ubuntu@<IP_PUBLICA>
```

## 2. Instalación del Servidor

Ejecutar en la instancia Oracle Cloud:

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Reiniciar sesión para aplicar grupos
exit
```

Reconectar y verificar:

```bash
docker --version
docker compose version
```

## 3. Desplegar Wiki.js

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/manual-urgencia-andes-salud.git
cd manual-urgencia-andes-salud

# Configurar variables de entorno
cp .env.example .env
nano .env  # Configurar DB_PASSWORD con un password seguro

# Iniciar servicios
docker compose up -d

# Verificar que los contenedores estén corriendo
docker compose ps
```

## 4. Configuración Inicial de Wiki.js

1. Acceder a `http://<IP_PUBLICA>:3000`
2. Completar el wizard de instalación:
   - Email del administrador
   - Password del administrador
   - URL del sitio

## 5. Configuración de Auth0

### Crear Aplicación en Auth0

1. Ir a [auth0.com](https://auth0.com) y crear cuenta (si no existe)
2. Applications > Create Application
3. Nombre: "Manual Urgencia Andes Salud"
4. Tipo: Regular Web Application
5. Configurar:
   - **Allowed Callback URLs:** `https://tu-dominio.com/login/oauth2/callback`
   - **Allowed Logout URLs:** `https://tu-dominio.com`
   - **Allowed Web Origins:** `https://tu-dominio.com`

### Crear Roles en Auth0

1. User Management > Roles > Create Role
2. Crear roles:
   - `admin` - Administradores del sistema
   - `editor` - Pueden editar contenido
   - `viewer` - Solo lectura

### Configurar Auth0 en Wiki.js

1. En Wiki.js, ir a Administration > Authentication
2. Agregar estrategia Auth0:
   - **Domain:** tu-tenant.auth0.com
   - **Client ID:** (copiar de Auth0)
   - **Client Secret:** (copiar de Auth0)
3. Mapear grupos de Auth0 a permisos de Wiki.js

## 6. Aplicar Branding

1. En Wiki.js, ir a Administration > Theme
2. En "Inject CSS", pegar el contenido de `theme/custom.css`
3. En Administration > General:
   - Subir logo desde `assets/logo.png`
   - Configurar favicon

## 7. SSL con Caddy (Recomendado)

Para producción, usar Caddy como reverse proxy con SSL automático:

```bash
# Instalar Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

# Configurar Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Contenido del Caddyfile:
```
tu-dominio.com {
    reverse_proxy localhost:3000
}
```

```bash
# Reiniciar Caddy
sudo systemctl restart caddy
```

## 8. Configurar Backups Automáticos

```bash
# Dar permisos de ejecución al script
chmod +x scripts/backup.sh

# Agregar cron job para backup diario
crontab -e
```

Agregar línea:
```
0 2 * * * /home/ubuntu/manual-urgencia-andes-salud/scripts/backup.sh
```

## Verificación Final

- [ ] Wiki.js accesible desde el navegador
- [ ] Login con Auth0 funcional
- [ ] Roles de usuario funcionando
- [ ] Branding aplicado correctamente
- [ ] SSL configurado (HTTPS)
- [ ] Backups automáticos programados
