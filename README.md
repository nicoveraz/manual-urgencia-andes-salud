# Manual de Procedimientos - Servicio de Urgencia

Sistema de documentación para el Servicio de Urgencia de Clínica Andes Salud.

## Stack Tecnológico

- **Wiki.js 2.5** - Sistema de documentación
- **PostgreSQL 15** - Base de datos
- **Auth0** - Autenticación y gestión de usuarios
- **Oracle Cloud Free Tier** - Hosting

## Requisitos

- Docker y Docker Compose
- Cuenta en Auth0 (free tier)
- Instancia en Oracle Cloud (free tier)

## Inicio Rápido (Desarrollo Local)

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/manual-urgencia-andes-salud.git
   cd manual-urgencia-andes-salud
   ```

2. Crear archivo de configuración:
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales
   ```

3. Iniciar los servicios:
   ```bash
   docker-compose up -d
   ```

4. Acceder a Wiki.js en `http://localhost:3000`

## Estructura del Proyecto

```
manual-urgencia-andes-salud/
├── docker-compose.yml      # Configuración de servicios
├── .env.example            # Template de variables de entorno
├── assets/
│   └── logo.png            # Logo corporativo
├── theme/
│   └── custom.css          # Estilos de branding
├── scripts/
│   ├── setup-oracle.sh     # Script de setup para Oracle Cloud
│   └── backup.sh           # Script de backup de base de datos
└── docs/
    └── DEPLOYMENT.md       # Guía de despliegue en producción
```

## Configuración de Auth0

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones detalladas de configuración de Auth0.

## Roles de Usuario

| Rol | Permisos |
|-----|----------|
| `admin` | Gestión completa del sistema |
| `editor` | Crear y editar contenido |
| `viewer` | Solo lectura |

## Branding

- **Color Primario:** `#04488e`
- Los estilos personalizados están en `theme/custom.css`

## Despliegue

Consultar [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones de despliegue en Oracle Cloud.

## Backup

Ejecutar backup manual:
```bash
./scripts/backup.sh
```

## Licencia

Uso interno - Clínica Andes Salud
