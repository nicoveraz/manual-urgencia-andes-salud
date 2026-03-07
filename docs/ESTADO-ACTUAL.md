# Estado Actual del Proyecto — urgpedia

> Referencia técnica para sesiones de desarrollo en Claude Code.
> Última actualización: 2026-03-07

---

## 1. Infraestructura

| Elemento | Valor |
|---|---|
| Servidor | Oracle Cloud · Ubuntu 22.04 |
| IP pública | `146.235.242.103` |
| SSH key | `~/Downloads/ssh-key-2026-01-27.key` |
| Reverse proxy | Caddy 2 · `/etc/caddy/Caddyfile` |
| SSL | Let's Encrypt automático vía Caddy |

**Contenedores Docker:**

| Contenedor | Imagen | Puerto | Descripción |
|---|---|---|---|
| `wiki` | requarks/wiki:2 | 3000 | Wiki.js |
| `wiki-db` | postgres:15 | — (interno) | PostgreSQL 15 |

---

## 2. Dominios y routing

**Caddyfile actual** (`/etc/caddy/Caddyfile`):

```caddy
urgpedia.cl {
    root * /srv/urgpedia
    file_server
}

caspm.urgpedia.cl {
    @root path /
    redir @root /login/81ff3df8-2a3f-4073-b335-38d113f6da22 302
    reverse_proxy localhost:3000
}
```

| URL | Resultado |
|---|---|
| `urgpedia.cl` | Landing page estática desde `/srv/urgpedia/` |
| `caspm.urgpedia.cl/` | Redirect 302 → Auth0 login |
| `caspm.urgpedia.cl/*` | Wiki.js (reverse proxy a localhost:3000) |

> **Pendiente DNS**: agregar registro `A urgpedia.cl → 146.235.242.103` en el registrador de dominio.

---

## 3. Autenticación — Auth0

| Parámetro | Valor |
|---|---|
| Tenant | `dev-0zpeshonra8ull1d.us.auth0.com` |
| Aplicación | Regular Web Application |
| Strategy UUID (Wiki.js) | `81ff3df8-2a3f-4073-b335-38d113f6da22` |
| Callback configurado | `https://caspm.urgpedia.cl/login/callback` |

**Para agregar una nueva clínica:**
Ir a Auth0 Dashboard → Applications → Allowed Callback URLs → agregar `https://nueva-clinica.urgpedia.cl/login/callback`.

El SSO es transparente: un usuario autenticado en cualquier subdominio no necesita volver a hacer login en otro.

---

## 4. Wiki.js — archivos modificados en el contenedor

Los siguientes archivos dentro del contenedor `wiki` fueron modificados directamente:

### `/wiki/server/views/login.pug`
Agrega redirect JS a Auth0 cuando no hay password-change flow activo:
```pug
block head
  if !changePwdContinuationToken
    script.
      window.location.replace('/login/81ff3df8-2a3f-4073-b335-38d113f6da22');
```
> Nota: el redirect principal ya lo hace Caddy. Este JS es un fallback.

### `/wiki/server/core/servers.js`
GraphQL introspection deshabilitado (seguridad):
```javascript
this.servers.graph = new ApolloServer({
  ...graphqlSchema,
  introspection: false,   // ← agregado
  context: ({ req, res }) => ({ req, res }),
  ...
})
```

**Advertencia**: los cambios en el contenedor se pierden si se recrea el contenedor. Considerar montar los archivos como volúmenes o hacer imagen custom.

---

## 5. Wiki.js — configuración en base de datos

Acceso: `docker exec wiki-db psql -U wikijs wikijs`

### Search engine
```sql
-- PostgreSQL full-text activo con diccionario español
SELECT key, "isEnabled", config FROM "searchEngines" WHERE "isEnabled" = true;
-- Resultado: postgres | true | {"dictLanguage":"spanish"}
```
> ⚠️ **Pendiente**: reconstruir índice de búsqueda.
> Admin → Search Engine → Rebuild Index

### Comments
```sql
SELECT key, "isEnabled" FROM "commentProviders" WHERE key = 'default';
-- Resultado: default | true
```

### Theming (logoUrl y favicon)
```sql
SELECT value->>'logoUrl', value->>'injectHead' FROM settings WHERE key = 'theming';
```
- `logoUrl`: URL raw GitHub de `assets/urgpedia-icon.svg`
- `injectHead`: script JS que reemplaza los `<link rel="icon">` del HTML por `urgpedia-favicon.svg`

---

## 6. Assets de marca

| Archivo | Uso | Fondo óptimo |
|---|---|---|
| `urgpedia-icon.svg` | Header Wiki.js · hero landing page | Azul `#04488e` / oscuro |
| `urgpedia-icon-blue.svg` | Nav landing page | Blanco / gris claro |
| `urgpedia-favicon.svg` | Favicon browser tab | Cualquiera (autónomo) |

**Diseño**: Material Design "cognition" icon (silueta de cabeza, espiral removida) + cruz médica knockout (transparente, toma el color del fondo).

URLs raw GitHub:
```
https://raw.githubusercontent.com/nicoveraz/manual-urgencia-andes-salud/main/assets/urgpedia-icon.svg
https://raw.githubusercontent.com/nicoveraz/manual-urgencia-andes-salud/main/assets/urgpedia-icon-blue.svg
https://raw.githubusercontent.com/nicoveraz/manual-urgencia-andes-salud/main/assets/urgpedia-favicon.svg
```

---

## 7. Landing page

- **Repo**: `landing/index.html`
- **Servidor**: `/srv/urgpedia/index.html`
- **Tecnología**: HTML + CSS puro (sin frameworks, sin build step)
- **Íconos**: referencias a GitHub raw URLs de `assets/`

**Deploy al servidor:**
```bash
sudo curl -fsSL \
  'https://raw.githubusercontent.com/nicoveraz/manual-urgencia-andes-salud/main/landing/index.html' \
  -o /srv/urgpedia/index.html
```

**Para agregar una nueva clínica en la landing:**
Copiar el bloque `.card.coming-soon`, eliminar la clase `coming-soon`, y actualizar:
- `href` → URL del nuevo subdominio
- `h3` → Nombre de la clínica
- `.card-location` → Ciudad, región
- `.card-desc` → Descripción
- `.badge` → cambiar a `badge-active` con texto "Activo"

---

## 8. Seguridad

| Medida | Estado |
|---|---|
| GraphQL introspection | ✅ Deshabilitado |
| Firewall Oracle Cloud | ✅ Solo puertos 22, 80, 443 |
| PostgreSQL expuesto | ✅ No (solo acceso interno Docker) |
| PII en Git | ✅ Nunca commiteado (en `.gitignore`) |
| Auth0 SSO | ✅ Configurado |

**Archivos sensibles en `.gitignore`:**
```
scripts/create-users-auth0.py
scripts/*-users-*.py
*.csv
```

> `scripts/create-users-auth0.py` contiene nombres y emails de médicos (PII) y la contraseña temporal. **Nunca commitear**.

---

## 9. Tareas pendientes

- [ ] **DNS**: agregar registro `A urgpedia.cl → 146.235.242.103` en registrador de dominio
- [ ] **Search index**: Admin → Search Engine → Rebuild Index (tras cambio de `db` a `postgres`)
- [ ] **Login.pug**: evaluar si el JS redirect sigue siendo necesario (Caddy ya redirige `/`)
- [ ] **Nueva clínica**: nuevo stack Docker + subdominio en Caddy + callback Auth0 + card en landing
- [ ] **Volúmenes Docker**: considerar montar login.pug y servers.js como volúmenes para persistir customizaciones

---

## 10. Comandos frecuentes

```bash
# ── SERVIDOR ────────────────────────────────────────
ssh -i ~/Downloads/ssh-key-2026-01-27.key ubuntu@146.235.242.103

# ── DOCKER ──────────────────────────────────────────
docker ps                          # Ver contenedores corriendo
docker logs wiki --tail 50         # Logs Wiki.js
docker restart wiki                # Reiniciar Wiki.js

# ── BASE DE DATOS ────────────────────────────────────
docker exec wiki-db psql -U wikijs wikijs

# ── CADDY ───────────────────────────────────────────
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
cat /etc/caddy/Caddyfile

# ── LANDING PAGE ────────────────────────────────────
sudo curl -fsSL \
  'https://raw.githubusercontent.com/nicoveraz/manual-urgencia-andes-salud/main/landing/index.html' \
  -o /srv/urgpedia/index.html

# ── EDITAR ARCHIVOS EN CONTENEDOR ───────────────────
# (escribir primero en /tmp, luego docker cp)
docker cp /tmp/archivo.pug wiki:/wiki/server/views/archivo.pug
```

---

## 11. Historial de decisiones relevantes

| Decisión | Motivo |
|---|---|
| Auth0 en lugar de login local | SSO corporativo, gestión centralizada de usuarios |
| Redirect en Caddy (no solo JS) | Server-side, más rápido, no depende de JS |
| `@root path /` en Caddy | `redir /` usa prefijo y redirige todo; `path /` es exact match |
| PostgreSQL full-text search | Mejor calidad para contenido médico en español |
| SVG inline → `<img>` con URL GitHub | Un solo source de verdad para los assets de marca |
| GraphQL introspection deshabilitado | Evita exposición del schema de la API |
| Archivos PII en `.gitignore` | `create-users-auth0.py` nunca fue commiteado (verificado) |
