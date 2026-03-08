# Overrides de Wiki.js

Archivos personalizados que se montan como volúmenes en el contenedor `wiki`.
Esto asegura que las customizaciones **persistan** al recrear o actualizar el contenedor.

## Cómo extraer los archivos originales del contenedor actual

Antes del primer `docker compose up -d` con los nuevos volúmenes, copia los archivos
modificados desde el contenedor en ejecución:

```bash
# Extraer los archivos actuales (ya modificados) del contenedor
docker cp wiki:/wiki/server/views/login.pug ./overrides/login.pug
docker cp wiki:/wiki/server/core/servers.js ./overrides/servers.js
```

Si el contenedor ya fue recreado y perdiste los cambios, aquí están las
modificaciones que deben aplicarse:

### login.pug
No agregar un redirect JS automático a `/login/<AUTH0_STRATEGY_UUID>` desde `login.pug`.
Ese workaround compite con el callback social nativo de Wiki.js y puede dejar la
sesión en un loop de autenticación. Para saltarse la pantalla de login, usar
`Administration > Authentication > Auto Login` dentro de Wiki.js.

### servers.js
En la creación de `ApolloServer`, agregar `introspection: false`:
```javascript
this.servers.graph = new ApolloServer({
  ...graphqlSchema,
  introspection: false,
  context: ({ req, res }) => ({ req, res }),
  ...
})
```
