(function () {
  // Fetch a URL server-side via same-origin Caddy proxy — no CSP issues.
  // redirect: 'manual' avoids chasing backend redirects cross-origin.
  async function check(url) {
    try {
      var ac = new AbortController();
      var timer = setTimeout(function () { ac.abort(); }, 7000);
      var resp = await fetch(url, {
        signal: ac.signal,
        cache: 'no-store',
        redirect: 'manual',
      });
      clearTimeout(timer);
      // ok = 2xx; opaqueredirect = 3xx (backend up but redirecting)
      return resp.ok || resp.type === 'opaqueredirect';
    } catch (_) {
      return false;
    }
  }

  function set(id, up) {
    var el = document.getElementById(id);
    if (!el) return;
    el.className = 'status-pill ' + (up ? 'ok' : 'err');
    el.innerHTML = (up
      ? '<div class="status-dot"></div>Operacional'
      : '<div class="status-dot"></div>No disponible');
  }

  async function run() {
    var results = await Promise.all([
      check('/assets/urgpedia-favicon.svg'),  // urgpedia.cl file serving
      check('/healthz/caspm'),                 // Caddy → localhost:3000 (Wiki.js)
      check('/healthz/auth0'),                 // Caddy → Auth0 OIDC endpoint
    ]);
    var urgpediaUp = results[0];
    var caspmUp    = results[1];
    var auth0Up    = results[2];

    set('s-urgpedia', urgpediaUp);
    set('s-caspm',    caspmUp);
    set('s-auth0',    auth0Up);

    var allUp = urgpediaUp && caspmUp && auth0Up;
    var g = document.getElementById('g-status');
    var l = document.getElementById('g-label');
    if (g) g.className = 'global-status ' + (allUp ? 'ok' : 'err');
    if (l) l.textContent = allUp
      ? 'Todos los sistemas operacionales'
      : 'Degradación detectada';

    var ts = document.getElementById('ts');
    if (ts) ts.textContent = 'Verificado ' + new Date().toLocaleString('es-CL', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });
  }

  run();
}());
