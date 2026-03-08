/* urgpedia CASPM — Service Worker v1 */
var CACHE = 'urgpedia-caspm-v1';
var OFFLINE = '/offline.html';
/* Rutas que no deben cachearse (auth, API, GraphQL) */
var SKIP_PATHS = ['/login/', '/logout', '/a/', '/graphql', '/_assets/'];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll([OFFLINE]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys
          .filter(function (k) { return k !== CACHE; })
          .map(function (k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function (e) {
  var url = e.request.url;

  /* Solo same-origin */
  if (!url.startsWith(self.location.origin)) return;

  /* Excluir rutas de auth y API */
  var path = new URL(url).pathname;
  if (SKIP_PATHS.some(function (p) { return path.startsWith(p); })) return;

  /* Navegación (HTML): network-first, fallback a caché o offline */
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request)
        .then(function (r) {
          var clone = r.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
          return r;
        })
        .catch(function () {
          return caches.match(e.request).then(function (cached) {
            return cached || caches.match(OFFLINE);
          });
        })
    );
    return;
  }

  /* Assets estáticos: cache-first */
  e.respondWith(
    caches.match(e.request).then(function (cached) {
      if (cached) return cached;
      return fetch(e.request).then(function (r) {
        if (r.ok) {
          var clone = r.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, clone); });
        }
        return r;
      });
    })
  );
});
