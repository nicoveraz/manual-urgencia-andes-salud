#!/usr/bin/env python3
"""
Crea navegación estática con acordeón para Wiki.js (caspm.urgpedia.cl).

1. Actualiza `navigation` con estructura header + link.
2. Inyecta JS de acordeón en injectHead.
3. Reinicia wiki.
"""
import json, subprocess, uuid, sys

# ── helpers SQL ──────────────────────────────────────────────────────────────

def psql_pipe(sql):
    r = subprocess.run(
        ["docker", "exec", "-i", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki"],
        input=sql.encode("utf-8"),
        capture_output=True,
    )
    out = r.stdout.decode("utf-8").strip()
    err = r.stderr.decode("utf-8").strip()
    if out:  print("  →", out)
    if err:  print("  ✗", err)
    return r.returncode, out

def psql_query(sql):
    r = subprocess.run(
        ["docker", "exec", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki", "-t", "-c", sql],
        capture_output=True, text=True,
    )
    return r.stdout.strip()

def uid(): return str(uuid.uuid4())

# ── 1. Estructura de navegación ───────────────────────────────────────────────

def lnk(label, path, icon="mdi-circle-small"):
    return {"id": uid(), "kind": "link", "label": label, "icon": icon,
            "targetType": "external", "target": path,
            "visibilityMode": "all", "visibilityGroups": None}

def hdr(label, icon="mdi-chevron-right"):
    return {"id": uid(), "kind": "header", "label": label, "icon": icon,
            "targetType": "", "target": "",
            "visibilityMode": "all", "visibilityGroups": None}

def div():
    return {"id": uid(), "kind": "divider", "label": "", "icon": "",
            "targetType": "", "target": "",
            "visibilityMode": "all", "visibilityGroups": None}

nav_items = [
    lnk("Inicio", "/es/home", "mdi-home"),
    div(),

    # ── Introducción
    hdr("Introducción", "mdi-book-open-variant"),
    lnk("Bienvenida",             "/es/introduccion/bienvenida"),
    lnk("Cómo usar este manual",  "/es/introduccion/como-usar-este-manual"),

    # ── El Servicio
    hdr("El Servicio", "mdi-hospital-building"),
    lnk("El Servicio (índice)",    "/es/el-servicio"),
    lnk("Misión y Visión",         "/es/el-servicio/mision-y-vision"),
    lnk("Descripción del Servicio","/es/el-servicio/descripcion"),
    lnk("Organigrama",             "/es/el-servicio/organigrama"),
    lnk("Horarios y Turnos",       "/es/el-servicio/horarios-y-turnos"),

    # ── Interconsultores
    hdr("Interconsultores", "mdi-account-group"),
    lnk("Tabla de Interconsultores", "/es/interconsultores/tabla"),

    # ── Servicios de Apoyo
    hdr("Servicios de Apoyo", "mdi-flask"),
    lnk("Laboratorio",    "/es/servicios-de-apoyo/laboratorio"),
    lnk("Imagenología",   "/es/servicios-de-apoyo/imagenologia"),
    lnk("Banco de Sangre","/es/servicios-de-apoyo/banco-de-sangre"),
    lnk("Farmacia",       "/es/servicios-de-apoyo/farmacia"),
    lnk("Otros Servicios","/es/servicios-de-apoyo/otros"),

    # ── Marco Legal
    hdr("Marco Legal", "mdi-gavel"),
    lnk("Ley de Urgencia",       "/es/marco-legal/ley-de-urgencia"),
    lnk("Accidentes del Trabajo","/es/marco-legal/accidentes-del-trabajo"),
    lnk("Licencias Médicas",     "/es/marco-legal/licencias-medicas"),
    lnk("ENO",                   "/es/marco-legal/eno"),
    lnk("GES/AUGE",              "/es/marco-legal/ges-auge"),
    lnk("Violencia y Maltrato",  "/es/marco-legal/violencia-y-maltrato"),
    lnk("Otros Marcos Legales",  "/es/marco-legal/otros"),

    div(),

    # ── Protocolos Operativos
    hdr("Protocolos Operativos", "mdi-clipboard-list"),
    lnk("Triage",              "/es/protocolos-operativos/triage"),
    lnk("Circuito del Paciente","/es/protocolos-operativos/circuito-del-paciente"),
    lnk("Código Rojo",          "/es/protocolos-operativos/codigo-rojo"),
    lnk("Traslado",             "/es/protocolos-operativos/traslado"),
    lnk("Manejo de Camas",      "/es/protocolos-operativos/manejo-de-camas"),
    lnk("Emergencias Internas", "/es/protocolos-operativos/emergencias-internas"),

    # ── Protocolos de Calidad
    hdr("Protocolos de Calidad", "mdi-shield-check"),
    lnk("Seguridad del Paciente",    "/es/protocolos-calidad/seguridad-del-paciente"),
    lnk("IAAS",                      "/es/protocolos-calidad/iaas"),
    lnk("Indicadores",               "/es/protocolos-calidad/indicadores"),
    lnk("Eventos Adversos",          "/es/protocolos-calidad/eventos-adversos"),
    lnk("Auditoría Clínica",         "/es/protocolos-calidad/auditoria"),

    # ── Protocolos Clínicos
    hdr("Protocolos Clínicos", "mdi-stethoscope"),
    lnk("Por Presentación Clínica", "/es/protocolos-clinicos/por-presentacion"),
    lnk("Por Patología",            "/es/protocolos-clinicos/por-patologia"),

    div(),

    # ── Calculadoras
    hdr("Calculadoras", "mdi-calculator"),
    lnk("Analgesia y Sedación", "/es/calculadoras/analgesia-y-sedacion"),
    lnk("Antibióticos",         "/es/calculadoras/antibioticos"),
    lnk("Fluidoterapia",        "/es/calculadoras/fluidoterapia"),
    lnk("Cardiovascular",       "/es/calculadoras/cardiovascular"),
    lnk("Neurológico",          "/es/calculadoras/neurologico"),
    lnk("Severidad",            "/es/calculadoras/severidad"),
    lnk("Pediatría",            "/es/calculadoras/pediatria"),
    lnk("Obstetricia",          "/es/calculadoras/obstetricia"),
]

nav_config = [
    {"locale": "es", "items": nav_items},
    {"locale": "en", "items": nav_items},
]

# ── 2. JavaScript de acordeón ─────────────────────────────────────────────────
# Se inyecta en injectHead. Usa Vuetify DOM classes de Wiki.js 2.x.

ACCORDION_JS = r"""
<style>
  /* Acordeón wiki — sub-ítems indentados y más pequeños */
  .wk-sub .v-list-item__title { font-size: 0.82rem !important; opacity: .9; }
  .wk-sub { padding-left: 20px !important; }
  .wk-sub .v-list-item__icon { min-width: 20px !important; }
  .wk-hdr { cursor: pointer !important; user-select: none; }
  .wk-hdr .v-list-item__title {
    display: flex !important; align-items: center;
    font-weight: 600 !important; letter-spacing: .05em;
  }
  .wk-arrow {
    margin-left: auto; display: inline-block;
    transition: transform .2s ease; font-style: normal;
    font-size: .7rem; opacity: .7; padding-left: 4px;
  }
  .wk-arrow.closed { transform: rotate(-90deg); }
</style>
<script>
(function () {
  'use strict';
  var SK = 'wkAccState';
  function gs() { try { return JSON.parse(localStorage.getItem(SK) || '{}'); } catch(e) { return {}; } }
  function ss(s) { try { localStorage.setItem(SK, JSON.stringify(s)); } catch(e) {} }

  function findNav() {
    // Buscar el v-list principal del drawer (no anidado dentro de otro v-list)
    var lists = document.querySelectorAll('.v-navigation-drawer .v-list');
    var best = null;
    lists.forEach(function (el) {
      // Omitir listas anidadas dentro de otro v-list
      if (el.parentElement && el.parentElement.closest('.v-list')) return;
      if (!best || el.children.length > best.children.length) best = el;
    });
    return best && best.children.length > 3 ? best : null;
  }

  function init() {
    var nav = findNav();
    if (!nav || nav.dataset.wkInit) return !!nav;
    nav.dataset.wkInit = '1';

    var state = gs();
    var items  = Array.from(nav.children);
    var groups = [];
    var cur    = null;

    items.forEach(function (el) {
      // Header: v-list-item sin v-list-item--link
      if (el.classList.contains('v-list-item') && !el.classList.contains('v-list-item--link')) {
        cur = { hdr: el, links: [], id: 'g' + groups.length };
        groups.push(cur);
      } else if (el.classList.contains('v-list-item') && el.classList.contains('v-list-item--link') && cur) {
        cur.links.push(el);
      } else {
        cur = null; // divider rompe la secuencia
      }
    });

    groups.forEach(function (g) {
      if (!g.links.length) return;

      // Estado inicial: abierto si no está guardado
      var open = state[g.id] !== false;

      // Marcar header
      g.hdr.classList.add('wk-hdr');

      // Agregar flecha al título
      var titleEl = g.hdr.querySelector('.v-list-item__title');
      if (titleEl) {
        var arrow = document.createElement('span');
        arrow.className = 'wk-arrow' + (open ? '' : ' closed');
        arrow.textContent = '▾';
        titleEl.appendChild(arrow);
      }

      // Marcar e inicializar sub-ítems
      g.links.forEach(function (lnk) {
        lnk.classList.add('wk-sub');
        lnk.style.display = open ? '' : 'none';
      });

      // Toggle al hacer click
      g.hdr.addEventListener('click', function () {
        var s = gs();
        var nowOpen = s[g.id] !== false;
        nowOpen = !nowOpen;
        s[g.id] = nowOpen;
        ss(s);
        var a = g.hdr.querySelector('.wk-arrow');
        if (a) a.classList.toggle('closed', !nowOpen);
        g.links.forEach(function (lnk) { lnk.style.display = nowOpen ? '' : 'none'; });
      });
    });

    return true;
  }

  // Poll hasta que el nav esté en el DOM
  var tries = 0;
  var iv = setInterval(function () { if (init() || ++tries > 60) clearInterval(iv); }, 250);

  // Re-inicializar en cada cambio de ruta (Vue Router)
  var _push = history.pushState;
  history.pushState = function () {
    _push.apply(history, arguments);
    setTimeout(function () {
      var nav = findNav();
      if (nav) { delete nav.dataset.wkInit; }
      tries = 0;
      var iv2 = setInterval(function () { if (init() || ++tries > 60) clearInterval(iv2); }, 250);
    }, 200);
  };
})();
</script>
"""

# ── 3. Leer injectHead actual y agregar JS ────────────────────────────────────

print("Leyendo injectHead actual...")
raw = psql_query("SELECT value FROM settings WHERE key='theming';")
try:
    theming = json.loads(raw)
    current_inject = theming.get("injectHead", "")
except Exception as e:
    print("Error leyendo theming:", e)
    sys.exit(1)

# Eliminar inyección previa de acordeón si existe
MARKER_START = "<!-- wk-accordion-start -->"
MARKER_END   = "<!-- wk-accordion-end -->"
if MARKER_START in current_inject:
    s = current_inject.index(MARKER_START)
    e = current_inject.index(MARKER_END) + len(MARKER_END)
    current_inject = (current_inject[:s] + current_inject[e:]).strip()

new_inject = current_inject + "\n" + MARKER_START + ACCORDION_JS + MARKER_END

theming["injectHead"] = new_inject
new_theming_json = json.dumps(theming, ensure_ascii=False)

# ── 4. Aplicar cambios en DB ──────────────────────────────────────────────────
TAG = "WKACCUPD"

nav_json = json.dumps(nav_config, ensure_ascii=False)

sql = f"""
-- Actualizar navegación
UPDATE navigation
SET config = ${TAG}N${nav_json}${TAG}N$::json
WHERE key = 'site';

-- Actualizar injectHead con JS de acordeón
UPDATE settings
SET value = ${TAG}T${new_theming_json}${TAG}T$::json
WHERE key = 'theming';

-- Asegurar modo STATIC
UPDATE settings SET value = '{{"mode":"STATIC"}}'::json WHERE key = 'nav';
"""

print("Aplicando cambios en DB...")
rc, _ = psql_pipe(sql)

if rc != 0:
    print("✗ Error al aplicar SQL")
    sys.exit(1)

print("✓ DB actualizada")
print("Reiniciando wiki...")
r = subprocess.run(["docker", "restart", "wiki"], capture_output=True)
print("Reinicio:", "OK" if r.returncode == 0 else f"ERROR {r.returncode}")

print(f"\n✓ Acordeón listo: {sum(1 for x in nav_items if x['kind']=='header')} grupos, "
      f"{sum(1 for x in nav_items if x['kind']=='link')} links.")
