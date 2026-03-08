#!/usr/bin/env python3
"""
Acordeón de navegación de 2 niveles para Wiki.js (caspm.urgpedia.cl).

L1: secciones principales (header kind) → chevron-down rota ▼/▲
L2: sub-grupos (link con icon mdi-chevron-right) → rota ▶/▼
    Solo "Protocolos Clínicos" tiene L2 con las presentaciones y patologías.
"""
import json, subprocess, uuid, sys

# ── helpers SQL ──────────────────────────────────────────────────────────────

def psql_pipe(sql):
    r = subprocess.run(
        ["docker", "exec", "-i", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki"],
        input=sql.encode("utf-8"), capture_output=True,
    )
    out = r.stdout.decode("utf-8").strip()
    err = r.stderr.decode("utf-8").strip()
    if out: print("  →", out)
    if err: print("  ✗", err)
    return r.returncode, out

def psql_query(sql):
    r = subprocess.run(
        ["docker", "exec", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki", "-t", "-c", sql],
        capture_output=True, text=True,
    )
    return r.stdout.strip()

def uid(): return str(uuid.uuid4())

# ── Constructores de ítems ────────────────────────────────────────────────────

def lnk(label, path, icon="mdi-circle-small"):
    """Link item (sub-item o sub-header si icon=mdi-chevron-right)."""
    return {"id": uid(), "kind": "link", "label": label, "icon": icon,
            "targetType": "external", "target": path,
            "visibilityMode": "all", "visibilityGroups": None}

def hdr(label, icon="mdi-chevron-right"):
    """Header item (L1 grupo principal)."""
    return {"id": uid(), "kind": "header", "label": label, "icon": icon,
            "targetType": "", "target": "",
            "visibilityMode": "all", "visibilityGroups": None}

def div():
    return {"id": uid(), "kind": "divider", "label": "", "icon": "",
            "targetType": "", "target": "",
            "visibilityMode": "all", "visibilityGroups": None}

# ── Estructura de navegación ──────────────────────────────────────────────────
# Leyenda de iconos:
#   hdr(...)                  → L1 toggle (header kind, sin link)
#   lnk(..., "mdi-chevron-right") → L2 toggle (link que también es sub-grupo)
#   lnk(...)                  → sub-ítem normal (mdi-circle-small por defecto)

nav_items = [
    lnk("Inicio", "/es/home", "mdi-home"),
    div(),

    # ── L1: Introducción ──────────────────────────────────────────────────────
    hdr("Introducción", "mdi-book-open-variant"),
    lnk("Bienvenida",            "/es/introduccion/bienvenida"),
    lnk("Cómo usar este manual", "/es/introduccion/como-usar-este-manual"),

    # ── L1: El Servicio ───────────────────────────────────────────────────────
    hdr("El Servicio", "mdi-hospital-building"),
    lnk("El Servicio (índice)",     "/es/el-servicio"),
    lnk("Misión y Visión",          "/es/el-servicio/mision-y-vision"),
    lnk("Descripción del Servicio", "/es/el-servicio/descripcion"),
    lnk("Organigrama",              "/es/el-servicio/organigrama"),
    lnk("Horarios y Turnos",        "/es/el-servicio/horarios-y-turnos"),

    # ── L1: Interconsultores ──────────────────────────────────────────────────
    hdr("Interconsultores", "mdi-account-group"),
    lnk("Tabla de Interconsultores", "/es/interconsultores/tabla"),

    # ── L1: Servicios de Apoyo ────────────────────────────────────────────────
    hdr("Servicios de Apoyo", "mdi-flask"),
    lnk("Laboratorio",     "/es/servicios-de-apoyo/laboratorio"),
    lnk("Imagenología",    "/es/servicios-de-apoyo/imagenologia"),
    lnk("Banco de Sangre", "/es/servicios-de-apoyo/banco-de-sangre"),
    lnk("Farmacia",        "/es/servicios-de-apoyo/farmacia"),
    lnk("Otros Servicios", "/es/servicios-de-apoyo/otros"),

    # ── L1: Marco Legal ───────────────────────────────────────────────────────
    hdr("Marco Legal", "mdi-gavel"),
    lnk("Ley de Urgencia",       "/es/marco-legal/ley-de-urgencia"),
    lnk("Accidentes del Trabajo","/es/marco-legal/accidentes-del-trabajo"),
    lnk("Licencias Médicas",     "/es/marco-legal/licencias-medicas"),
    lnk("ENO",                   "/es/marco-legal/eno"),
    lnk("GES/AUGE",              "/es/marco-legal/ges-auge"),
    lnk("Violencia y Maltrato",  "/es/marco-legal/violencia-y-maltrato"),
    lnk("Otros Marcos Legales",  "/es/marco-legal/otros"),

    div(),

    # ── L1: Protocolos Operativos ─────────────────────────────────────────────
    hdr("Protocolos Operativos", "mdi-clipboard-list"),
    lnk("Triage",               "/es/protocolos-operativos/triage"),
    lnk("Circuito del Paciente","/es/protocolos-operativos/circuito-del-paciente"),
    lnk("Código Rojo",          "/es/protocolos-operativos/codigo-rojo"),
    lnk("Traslado",             "/es/protocolos-operativos/traslado"),
    lnk("Manejo de Camas",      "/es/protocolos-operativos/manejo-de-camas"),
    lnk("Emergencias Internas", "/es/protocolos-operativos/emergencias-internas"),

    # ── L1: Protocolos de Calidad ─────────────────────────────────────────────
    hdr("Protocolos de Calidad", "mdi-shield-check"),
    lnk("Seguridad del Paciente","/es/protocolos-calidad/seguridad-del-paciente"),
    lnk("IAAS",                  "/es/protocolos-calidad/iaas"),
    lnk("Indicadores",           "/es/protocolos-calidad/indicadores"),
    lnk("Eventos Adversos",      "/es/protocolos-calidad/eventos-adversos"),
    lnk("Auditoría Clínica",     "/es/protocolos-calidad/auditoria"),

    # ── L1: Protocolos Clínicos (2 niveles) ───────────────────────────────────
    hdr("Protocolos Clínicos", "mdi-stethoscope"),

    # L2 sub-grupo A: Por Presentación (mdi-chevron-right = L2 toggle)
    lnk("Por Presentación Clínica", "/es/protocolos-clinicos/por-presentacion", "mdi-chevron-right"),
    lnk("Dolor Torácico",           "/es/protocolos-clinicos/por-presentacion/dolor-toracico"),
    lnk("Disnea",                   "/es/protocolos-clinicos/por-presentacion/disnea"),
    lnk("Dolor Abdominal",          "/es/protocolos-clinicos/por-presentacion/dolor-abdominal"),
    lnk("Cefalea",                  "/es/protocolos-clinicos/por-presentacion/cefalea"),
    lnk("Alteración de Conciencia", "/es/protocolos-clinicos/por-presentacion/alteracion-de-conciencia"),
    lnk("Síncope",                  "/es/protocolos-clinicos/por-presentacion/sincope"),
    lnk("Fiebre sin Foco",          "/es/protocolos-clinicos/por-presentacion/fiebre-sin-foco"),
    lnk("Trauma",                   "/es/protocolos-clinicos/por-presentacion/trauma"),
    lnk("Crisis Hipertensiva",      "/es/protocolos-clinicos/por-presentacion/crisis-hipertensiva"),

    # L2 sub-grupo B: Por Patología (mdi-chevron-right = L2 toggle)
    lnk("Por Patología", "/es/protocolos-clinicos/por-patologia", "mdi-chevron-right"),
    lnk("Cardiovascular",     "/es/protocolos-clinicos/por-patologia/cardiovascular"),
    lnk("Respiratorio",       "/es/protocolos-clinicos/por-patologia/respiratorio"),
    lnk("Neurológico",        "/es/protocolos-clinicos/por-patologia/neurologico"),
    lnk("Traumatología",      "/es/protocolos-clinicos/por-patologia/traumatologia"),
    lnk("Digestivo",          "/es/protocolos-clinicos/por-patologia/digestivo"),
    lnk("Renal y Metabólico", "/es/protocolos-clinicos/por-patologia/renal-y-metabolico"),
    lnk("Infectología",       "/es/protocolos-clinicos/por-patologia/infectologia"),
    lnk("Gineco-Obstetricia", "/es/protocolos-clinicos/por-patologia/gineco-obstetricia"),
    lnk("Pediatría",          "/es/protocolos-clinicos/por-patologia/pediatria"),
    lnk("Toxicología",        "/es/protocolos-clinicos/por-patologia/toxicologia"),
    lnk("Psiquiatría",        "/es/protocolos-clinicos/por-patologia/psiquiatria"),
    lnk("Procedimientos",     "/es/protocolos-clinicos/por-patologia/procedimientos"),

    div(),

    # ── L1: Calculadoras ──────────────────────────────────────────────────────
    hdr("Calculadoras", "mdi-calculator"),
    lnk("Analgesia y Sedación","/es/calculadoras/analgesia-y-sedacion"),
    lnk("Antibióticos",        "/es/calculadoras/antibioticos"),
    lnk("Fluidoterapia",       "/es/calculadoras/fluidoterapia"),
    lnk("Cardiovascular",      "/es/calculadoras/cardiovascular"),
    lnk("Neurológico",         "/es/calculadoras/neurologico"),
    lnk("Severidad",           "/es/calculadoras/severidad"),
    lnk("Pediatría",           "/es/calculadoras/pediatria"),
    lnk("Obstetricia",         "/es/calculadoras/obstetricia"),
]

nav_config = [
    {"locale": "es", "items": nav_items},
    {"locale": "en", "items": nav_items},
]

# ── JS + CSS del acordeón de 2 niveles ───────────────────────────────────────

ACCORDION_INJECT = r"""
<!-- wk-accordion-start -->
<style>
/* ── Acordeón Wiki.js 2 niveles ─────────────────────────── */
/* L1 header: v-subheader ya tiene display:flex; align-items:center */
.wk-hdr { cursor: pointer !important; user-select: none; }

/* Chevron L1: mdi-chevron-down inyectado por JS; rota ▼↔▲ */
.wk-chv {
  margin-left: auto;
  font-size: 18px !important;
  transition: transform 0.25s ease;
  line-height: 1;
  opacity: 0.75;
  flex-shrink: 0;
}
.wk-chv.wk-open { transform: rotate(180deg); }

/* L2 sub-header (v-list-item--link con mdi-chevron-right) */
.wk-sub-hdr { cursor: pointer !important; user-select: none; }
.wk-sub-hdr .v-list-item__title {
  display: flex !important; align-items: center !important; width: 100%;
}
/* El ícono mdi-chevron-right rota: ▶ cerrado → ▼ abierto */
.wk-sub-chv { transition: transform 0.25s ease; }
.wk-sub-chv.wk-open { transform: rotate(90deg); }

/* Indentación y tamaño L1 sub-ítems */
.wk-sub { padding-left: 16px !important; }
.wk-sub .v-list-item__title { font-size: 0.82rem !important; }
.wk-sub .v-list-item__icon  { min-width: 20px !important; }

/* Indentación y tamaño L2 sub-sub-ítems */
.wk-sub2 { padding-left: 32px !important; }
.wk-sub2 .v-list-item__title { font-size: 0.78rem !important; opacity: 0.85; }
.wk-sub2 .v-list-item__icon  { min-width: 16px !important; }
</style>
<script>
(function () {
  'use strict';
  var SK = 'wkAcc2';
  function gs() { try { return JSON.parse(localStorage.getItem(SK)||'{}'); } catch(e) { return {}; } }
  function ss(s) { try { localStorage.setItem(SK, JSON.stringify(s)); } catch(e) {} }

  /* ── Encontrar el v-list principal del drawer ── */
  function findNav() {
    var lists = document.querySelectorAll('.v-navigation-drawer .v-list');
    var best  = null;
    lists.forEach(function(el) {
      if (el.parentElement && el.parentElement.closest('.v-list')) return;
      if (!best || el.children.length > best.children.length) best = el;
    });
    return (best && best.children.length > 3) ? best : null;
  }

  /* ── Crear elemento chevron L1 ── */
  function mkChv(open) {
    var i = document.createElement('i');
    i.className = 'mdi mdi-chevron-down wk-chv' + (open ? ' wk-open' : '');
    return i;
  }

  /* ── Helper: encontrar grupo padre L2 ── */
  function findParentL2(l2arr, el) {
    for (var i = 0; i < l2arr.length; i++) {
      if (l2arr[i].items.indexOf(el) >= 0) return l2arr[i];
    }
    return null;
  }

  /* ── Inicializar acordeón ── */
  function init() {
    var nav = findNav();
    if (!nav || nav.dataset.wkInit) return !!nav;
    nav.dataset.wkInit = '1';

    var state    = gs();
    var children = Array.from(nav.children);

    /* Paso 1: agrupar por L1
       — Wiki.js renderiza "header" kind como DIV.v-subheader (NO v-list-item)
       — "link" kind como A.v-list-item.v-list-item--link
       — "divider" kind como HR.v-divider → rompe el grupo actual             */
    var l1 = [], curL1 = null;
    children.forEach(function(el) {
      var isHdr = el.classList.contains('v-subheader');
      var isLnk = el.classList.contains('v-list-item') && el.classList.contains('v-list-item--link');
      if      (isHdr)           { curL1 = { hdr: el, items: [], id: 'l1_' + l1.length }; l1.push(curL1); }
      else if (isLnk && curL1)  { curL1.items.push(el); }
      else                      { curL1 = null; } /* divider u otro = reset */
    });

    /* Paso 2: aplicar acordeón L1 */
    l1.forEach(function(g) {
      if (!g.items.length) return;

      /* Default: CERRADO (se abre solo si el usuario lo abrió antes) */
      var open = state[g.id] === true;
      g.hdr.classList.add('wk-hdr');

      /* Inyectar chevron directo al v-subheader (ya tiene display:flex) */
      var chv = mkChv(open);
      g.hdr.appendChild(chv);

      /* Paso 3: dentro del grupo, identificar L2 sub-headers
         (links cuyo ícono izquierdo es mdi-chevron-right) */
      var l2 = [], curL2 = null;
      g.items.forEach(function(el) {
        if (el.querySelector('.mdi-chevron-right')) {
          curL2 = { hdr: el, items: [], id: g.id + '_l2_' + l2.length };
          l2.push(curL2);
        } else if (curL2) {
          curL2.items.push(el);
        }
      });

      /* Listas planas para búsqueda rápida */
      var l2Hdrs  = l2.map(function(sg) { return sg.hdr; });
      var l2Items = [].concat.apply([], l2.map(function(sg) { return sg.items; }));

      /* Paso 4: aplicar acordeón L2 */
      l2.forEach(function(sg) {
        if (!sg.items.length) return;
        /* Default: CERRADO */
        var sgOpen = state[sg.id] === true;

        sg.hdr.classList.add('wk-sub-hdr');
        sg.hdr.classList.add('wk-sub');

        /* Rotar el ícono mdi-chevron-right existente */
        var icon = sg.hdr.querySelector('.mdi-chevron-right');
        if (icon) {
          icon.classList.add('wk-sub-chv');
          if (sgOpen) icon.classList.add('wk-open');
        }

        /* Estado inicial sub-sub-ítems */
        sg.items.forEach(function(el) {
          el.classList.add('wk-sub2');
          el.style.display = (open && sgOpen) ? '' : 'none';
        });
        sg.hdr.style.display = open ? '' : 'none';

        /* Handler L2: toggle (previene navegación en estos ítems-toggle) */
        sg.hdr.addEventListener('click', function(e) {
          e.preventDefault();
          e.stopPropagation();
          var s = gs();
          var nowOpen = !(s[sg.id] === true);
          s[sg.id] = nowOpen;
          ss(s);
          if (icon) icon.classList.toggle('wk-open', nowOpen);
          sg.items.forEach(function(el) { el.style.display = nowOpen ? '' : 'none'; });
        });
      });

      /* Paso 5: ítems normales (fuera de L2) reciben clase wk-sub */
      g.items.forEach(function(el) {
        if (l2Hdrs.indexOf(el) === -1 && l2Items.indexOf(el) === -1) {
          el.classList.add('wk-sub');
        }
      });

      /* Estado inicial de todos los ítems del grupo L1 */
      g.items.forEach(function(el) {
        if (!open) {
          el.style.display = 'none';
        } else {
          /* L2 sub-sub-ítems: ya manejados arriba */
          if (l2Items.indexOf(el) < 0) el.style.display = '';
        }
      });

      /* Handler L1: toggle grupo completo */
      g.hdr.addEventListener('click', function() {
        var s = gs();
        var nowOpen = !(s[g.id] === true);
        s[g.id] = nowOpen;
        ss(s);
        chv.classList.toggle('wk-open', nowOpen);

        g.items.forEach(function(el) {
          if (!nowOpen) {
            el.style.display = 'none';
          } else {
            /* Respetar estado L2 para sub-sub-ítems */
            if (l2Items.indexOf(el) >= 0) {
              var psg = findParentL2(l2, el);
              el.style.display = (psg && s[psg.id] === true) ? '' : 'none';
            } else {
              el.style.display = '';
            }
          }
        });
      });
    });

    return true;
  }

  /* Poll hasta que el nav esté en el DOM */
  var tries = 0;
  var iv = setInterval(function() { if (init() || ++tries > 60) clearInterval(iv); }, 250);

  /* Re-inicializar en cambios de ruta (Vue Router pushState) */
  var _push = history.pushState;
  history.pushState = function() {
    _push.apply(history, arguments);
    setTimeout(function() {
      var nav = findNav();
      if (nav) delete nav.dataset.wkInit;
      tries = 0;
      var iv2 = setInterval(function() { if (init() || ++tries > 60) clearInterval(iv2); }, 250);
    }, 200);
  };
})();
</script>
<!-- wk-accordion-end -->"""

# ── Leer injectHead actual ────────────────────────────────────────────────────

print("Leyendo configuración actual...")
raw = psql_query("SELECT value FROM settings WHERE key='theming';")
try:
    theming = json.loads(raw)
    current = theming.get("injectHead", "")
except Exception as e:
    print("Error:", e); sys.exit(1)

# Eliminar inyección previa
START, END = "<!-- wk-accordion-start -->", "<!-- wk-accordion-end -->"
if START in current:
    s = current.index(START)
    e = current.index(END) + len(END)
    current = (current[:s] + current[e:]).strip()

theming["injectHead"] = current + "\n" + ACCORDION_INJECT
new_theming = json.dumps(theming, ensure_ascii=False)

# ── Aplicar en DB ─────────────────────────────────────────────────────────────

nav_json  = json.dumps(nav_config, ensure_ascii=False)
TAG = "WKACC2"

sql = f"""
UPDATE navigation SET config = ${TAG}N${nav_json}${TAG}N$::json WHERE key = 'site';
UPDATE settings   SET value  = ${TAG}T${new_theming}${TAG}T$::json WHERE key = 'theming';
UPDATE settings   SET value  = '{{"mode":"STATIC"}}'::json WHERE key = 'nav';
"""

print("Aplicando cambios...")
rc, _ = psql_pipe(sql)
if rc != 0:
    print("✗ Error"); sys.exit(1)

print("✓ DB actualizada. Reiniciando wiki...")
r = subprocess.run(["docker", "restart", "wiki"], capture_output=True)
print("Reinicio:", "OK" if r.returncode == 0 else f"ERROR {r.returncode}")

l1_count = sum(1 for x in nav_items if x["kind"] == "header")
l2_count = sum(1 for x in nav_items if x.get("icon") == "mdi-chevron-right")
lnk_count = sum(1 for x in nav_items if x["kind"] == "link" and x.get("icon") != "mdi-chevron-right")

print(f"\n✓ Listo: {l1_count} grupos L1 · {l2_count} sub-grupos L2 · {lnk_count} links")
