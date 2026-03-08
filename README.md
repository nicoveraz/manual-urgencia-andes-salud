# urgpedia — Red de Manuales de Urgencia

Plataforma de conocimiento clínico para los equipos de urgencia de la **red Andes Salud**. Arranca con la Clínica Andes Salud Puerto Montt (CASPM) y está diseñada para expandirse a las demás clínicas de la red.

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| Wiki / CMS | Wiki.js 2.5 |
| Base de datos | PostgreSQL 15 |
| Autenticación | Auth0 (SSO compartido entre clínicas) |
| Reverse proxy / SSL | Caddy 2 (Let's Encrypt automático) |
| Hosting | Oracle Cloud Free Tier — Ubuntu 22.04 |

## Dominios

| Dominio | Descripción |
|---|---|
| `urgpedia.cl` | Landing page — directorio de clínicas de la red |
| `caspm.urgpedia.cl` | Wiki.js — Manual de Urgencia CASPM Puerto Montt |
| `*.urgpedia.cl` | Futuros subdominios por clínica |

## Estructura del proyecto

```
manual-urgencia-andes-salud/
├── assets/
│   ├── urgpedia-icon.svg          # Ícono principal (fondo azul/oscuro)
│   ├── urgpedia-icon-blue.svg     # Ícono azul (fondo blanco/claro)
│   └── urgpedia-favicon.svg       # Favicon con fondo #455A64
├── landing/
│   └── index.html                 # Landing page urgpedia.cl
├── docs/
│   ├── ESTADO-ACTUAL.md           # Estado técnico completo (referencia de desarrollo)
│   └── DEPLOYMENT.md              # Guía de primer despliegue
├── scripts/
│   ├── backup.sh                  # Backup de base de datos
│   └── setup-oracle.sh            # Setup inicial Oracle Cloud
├── theme/
│   └── custom.css                 # Estilos personalizados Wiki.js
├── docker-compose.yml
└── .env.example
```

## Branding

| Asset | Uso |
|---|---|
| `urgpedia-icon.svg` | Logo en header de Wiki.js (fondo azul `#04488e`) |
| `urgpedia-icon-blue.svg` | Logo en nav de la landing (fondo blanco) |
| `urgpedia-favicon.svg` | Favicon en browser tab (autónomo, fondo `#455A64`) |

Color primario: `#04488e`

## Agregar una nueva clínica a la red

1. **Servidor**: nuevo stack Docker (wiki + wiki-db) en puerto distinto
2. **Caddy**: agregar bloque `nueva-clinica.urgpedia.cl` en `/etc/caddy/Caddyfile`
3. **Auth0**: agregar `https://nueva-clinica.urgpedia.cl/login/<AUTH0_STRATEGY_UUID>/callback` en Allowed Callback URLs
4. **Landing**: copiar bloque `.card` en `landing/index.html`, activar y actualizar datos

Ver [docs/ESTADO-ACTUAL.md](docs/ESTADO-ACTUAL.md) para el estado técnico completo.

## Roles de usuario

| Rol | Permisos |
|---|---|
| `admin` | Gestión completa del sistema |
| `editor` | Crear y editar contenido |
| `viewer` | Solo lectura |

## Inicio rápido (desarrollo local)

```bash
git clone https://github.com/nicoveraz/manual-urgencia-andes-salud.git
cd manual-urgencia-andes-salud
cp .env.example .env
# Editar .env con credenciales
docker compose up -d
# Acceder en http://localhost:3000
```

## Despliegue en producción

Ver [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) para instrucciones detalladas.

## Seguridad

- Las variables sensibles van en `.env` (no commitear)
- Scripts con PII de usuarios están en `.gitignore`
- GraphQL introspection deshabilitado en producción

## Licencia

Uso interno — Red Andes Salud · Chile
