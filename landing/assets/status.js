(function () {
  // Any HTTP response (200, 302, 404…) means the server is reachable.
  // Only a network exception (connection refused, timeout) means down.
  async function check(url) {
    try {
      var ac = new AbortController();
      var timer = setTimeout(function () { ac.abort(); }, 7000);
      await fetch(url, {
        signal: ac.signal,
        cache: 'no-store',
        redirect: 'manual',
      });
      clearTimeout(timer);
      return true;
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

  function renderTimeline(svcId, hours) {
    var container = document.getElementById('tl-' + svcId);
    if (!container || !hours || !hours.length) return;
    container.innerHTML = '';
    var BARS = 90;
    var ratio = hours.length / BARS;
    for (var i = 0; i < BARS; i++) {
      var start = Math.floor(i * ratio);
      var end   = Math.floor((i + 1) * ratio);
      var slice = hours.slice(start, end).filter(function (v) { return v !== null; });
      var bar = document.createElement('div');
      bar.className = 'tl-bar';
      if (slice.length === 0) {
        bar.classList.add('tl-nodata');
      } else {
        var avg = slice.reduce(function (a, b) { return a + b; }, 0) / slice.length;
        if (avg >= 0.9)      bar.classList.add('tl-up');
        else if (avg >= 0.1) bar.classList.add('tl-partial');
        else                 bar.classList.add('tl-down');
      }
      container.appendChild(bar);
    }
  }

  async function loadUptime() {
    try {
      var r = await fetch('/assets/uptime.json', { cache: 'no-store' });
      if (!r.ok) return;
      var data = await r.json();
      var svcs = data.services || {};
      ['urgpedia', 'caspm', 'auth0'].forEach(function (svc) {
        var s = svcs[svc] || {};
        var w = document.getElementById('up-' + svc + '-week');
        if (w) w.textContent = s.week != null ? s.week + '%' : '—';
        renderTimeline(svc, s.hours || []);
      });
    } catch (_) {}
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

    var upList = [urgpediaUp, caspmUp, auth0Up];
    var downCount = upList.filter(function (v) { return !v; }).length;
    var state = downCount === 0 ? 'ok' : (downCount < upList.length ? 'warn' : 'err');

    var ICONS = {
      ok:   '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="rgb(0,176,147)"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5l-4-4 1.41-1.41L10 13.67l6.59-6.59L18 8.5l-8 8z"/></svg>',
      warn: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#e6a817"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
      err:  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#f87171"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/></svg>',
    };

    var g  = document.getElementById('g-status');
    var l  = document.getElementById('g-label');
    var ic = document.getElementById('g-icon');
    if (g)  g.className    = 'global-status ' + state;
    if (ic) ic.innerHTML   = ICONS[state] || '';
    if (l)  l.textContent  = state === 'ok'
      ? 'Todos los sistemas operacionales'
      : state === 'warn'
        ? 'Degradación detectada'
        : 'Sistemas no disponibles';

    var ts = document.getElementById('ts');
    if (ts) ts.textContent = 'Verificado ' + new Date().toLocaleString('es-CL', {
      dateStyle: 'medium',
      timeStyle: 'short',
    });

    loadUptime();
  }

  run();
}());
