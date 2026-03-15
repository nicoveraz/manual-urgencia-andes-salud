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
    lnk("La Clínica",        "/es/el-servicio/la-clinica"),
    lnk("El Servicio",       "/es/el-servicio"),
    lnk("Cuidamos Mejor",    "/es/el-servicio/mision-y-vision"),
    lnk("Organigrama",       "/es/el-servicio/organigrama"),
    lnk("Horarios y Turnos", "/es/el-servicio/horarios-y-turnos"),

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
    lnk("↳ Decreto 34 / Condiciones Clínicas", "/es/marco-legal/ley-de-urgencia/decreto-34", ""),
    lnk("Accidentes del Trabajo","/es/marco-legal/accidentes-del-trabajo"),
    lnk("↳ Mutual",              "/es/marco-legal/accidentes-del-trabajo/mutual", ""),
    lnk("↳ IST",                 "/es/marco-legal/accidentes-del-trabajo/ist", ""),
    lnk("Licencias Médicas",     "/es/marco-legal/licencias-medicas"),
    lnk("↳ Decreto 7 / Guías Clínicas", "/es/marco-legal/licencias-medicas/decreto-7", ""),
    lnk("ENO",                   "/es/marco-legal/eno"),
    lnk("GES/AUGE",              "/es/marco-legal/ges-auge"),
    lnk("Prescripción de Medicamentos", "/es/marco-legal/prescripcion-medicamentos"),
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
    lnk("↳ Caída del Paciente",  "/es/protocolos-calidad/seguridad-del-paciente/caida", ""),
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
    lnk("Paro Cardiorrespiratorio", "/es/protocolos-clinicos/por-presentacion/paro-cardiorrespiratorio"),

    # L2 sub-grupo B: Por Patología (mdi-chevron-right = L2 toggle)
    lnk("Por Patología", "/es/protocolos-clinicos/por-patologia", "mdi-chevron-right"),
    lnk("Cardiovascular",     "/es/protocolos-clinicos/por-patologia/cardiovascular"),
    lnk("↳ Taquiarritmias",  "/es/protocolos-clinicos/por-patologia/cardiovascular/taquiarritmias", ""),
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
    # L2 sub-grupo C: Procedimientos
    lnk("Procedimientos",              "/es/protocolos-clinicos/por-patologia/procedimientos", "mdi-chevron-right"),
    lnk("Manejo de Vía Aérea",        "/es/protocolos-clinicos/por-patologia/procedimientos/manejo-via-aerea"),
    lnk("Intubación Rápida",          "/es/protocolos-clinicos/por-patologia/procedimientos/intubacion-rapida"),
    lnk("Sedación Post-Intubación",   "/es/protocolos-clinicos/por-patologia/procedimientos/sedacion-post-intubacion"),

    div(),

    # ── L1: Calculadoras ──────────────────────────────────────────────────────
    hdr("Calculadoras", "mdi-calculator"),
    lnk("Analgesia y Sedación",    "/es/calculadoras/analgesia-y-sedacion"),
    lnk("Infusiones Vasoactivas",  "/es/calculadoras/infusiones-vasoactivas"),
    lnk("Fármacos de Urgencia",    "/es/calculadoras/farmacos-de-urgencia"),
    lnk("Sangrado y Anticoag.",    "/es/calculadoras/sangrado-anticoagulacion"),
    lnk("Glicemia",                "/es/calculadoras/glicemia"),
    lnk("Ajuste TACO / Heparina",  "/es/calculadoras/ajuste-inr-ttpk"),
    lnk("Electrolitos",            "/es/calculadoras/electrolitos"),
    lnk("Antibióticos",            "/es/calculadoras/antibioticos"),
    lnk("Fluidoterapia",           "/es/calculadoras/fluidoterapia"),
    lnk("Cardiovascular",          "/es/calculadoras/cardiovascular"),
    lnk("Neurológico",             "/es/calculadoras/neurologico"),
    lnk("Severidad",               "/es/calculadoras/severidad"),
    lnk("Pediatría",               "/es/calculadoras/pediatria"),
    lnk("Obstetricia",             "/es/calculadoras/obstetricia"),
    lnk("Quemados",                "/es/calculadoras/quemados"),
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

/* Chevron L1 */
.wk-chv {
  margin-left: auto;
  font-size: 18px !important;
  transition: transform 0.25s ease;
  line-height: 1;
  opacity: 0.75;
  flex-shrink: 0;
}
.wk-chv.wk-open { transform: rotate(180deg); }

/* L2 sub-header */
.wk-sub-hdr { cursor: pointer !important; user-select: none; }
.wk-sub-hdr .v-list-item__title {
  display: flex !important; align-items: center !important; width: 100%;
}
.wk-sub-chv { transition: transform 0.25s ease; }
.wk-sub-chv.wk-open { transform: rotate(90deg); }

/* Indentación L1 sub-ítems */
.wk-sub  { padding-left: 16px !important; }
.wk-sub  .v-list-item__title { font-size: 0.82rem !important; }
.wk-sub  .v-list-item__icon  { min-width: 20px !important; }

/* Indentación L2 sub-sub-ítems */
.wk-sub2 { padding-left: 32px !important; }
.wk-sub2 .v-list-item__title { font-size: 0.78rem !important; opacity: 0.85; }
.wk-sub2 .v-list-item__icon  { min-width: 16px !important; }

/* Ítem activo: negrita + blanco + barra lateral + fondo */
.wk-active {
  background: rgba(255,255,255,0.1) !important;
  box-shadow: inset 3px 0 0 rgba(255,255,255,0.6) !important;
}
.wk-active .v-list-item__title {
  font-weight: 700 !important;
  color: #ffffff !important;
  opacity: 1 !important;
}
.wk-active .v-list-item__icon .mdi { color: #ffffff !important; opacity: 1 !important; }

/* Botón "Cerrar todo": ícono redondo en la fila de Inicio */
.wk-ctrl-btn {
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  background: none;
  cursor: pointer;
  color: rgba(255,255,255,0.45);
  width: 22px;
  height: 22px;
  min-width: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
  padding: 0;
}
.wk-ctrl-btn:hover {
  color: rgba(255,255,255,0.9);
  border-color: rgba(255,255,255,0.7);
  background: rgba(255,255,255,0.1);
}
.wk-ctrl-btn .mdi { font-size: 14px !important; line-height: 1; }
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

  function mkChv(open) {
    var i = document.createElement('i');
    i.className = 'mdi mdi-chevron-down wk-chv' + (open ? ' wk-open' : '');
    return i;
  }

  function findParentL2(l2arr, el) {
    for (var i = 0; i < l2arr.length; i++) {
      if (l2arr[i].items.indexOf(el) >= 0) return l2arr[i];
    }
    return null;
  }

  /* ── Marcar ítem activo ── */
  function markActive(nav, path) {
    nav.querySelectorAll('.wk-active').forEach(function(el) { el.classList.remove('wk-active'); });
    Array.from(nav.querySelectorAll('a.v-list-item--link')).forEach(function(el) {
      if (el.getAttribute('href') === path) el.classList.add('wk-active');
    });
  }

  /* ── Botón "Cerrar todo": ícono redondo en la fila de Inicio ── */
  function injectCtrlBtn(nav) {
    var homeLink = null;
    Array.from(nav.querySelectorAll('a.v-list-item--link')).forEach(function(el) {
      if (!homeLink && el.getAttribute('href') === '/es/home') homeLink = el;
    });
    if (!homeLink || homeLink.querySelector('.wk-ctrl-btn')) return;
    var btn = document.createElement('button');
    btn.className = 'wk-ctrl-btn';
    btn.title = 'Cerrar todos los grupos';
    btn.innerHTML = '<i class="mdi mdi-unfold-less-horizontal"></i>';
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      nav.querySelectorAll('.wk-sub, .wk-sub2').forEach(function(el) { el.style.display = 'none'; });
      nav.querySelectorAll('.wk-chv').forEach(function(el)     { el.classList.remove('wk-open'); });
      nav.querySelectorAll('.wk-sub-chv').forEach(function(el) { el.classList.remove('wk-open'); });
      ss({});
    });
    homeLink.appendChild(btn);
  }

  /* ── Inicializar acordeón ── */
  function init() {
    var nav = findNav();
    if (!nav || nav.dataset.wkInit) return !!nav;
    nav.dataset.wkInit = '1';

    var state      = gs();
    var activePath = window.location.pathname;
    var children   = Array.from(nav.children);

    /* Paso 1: agrupar por L1
       — "header" kind → DIV.v-subheader
       — "link"   kind → A.v-list-item.v-list-item--link
       — "divider" / otro → rompe grupo actual                                */
    var l1 = [], curL1 = null;
    children.forEach(function(el) {
      var isHdr = el.classList.contains('v-subheader');
      var isLnk = el.classList.contains('v-list-item') && el.classList.contains('v-list-item--link');
      if      (isHdr)           { curL1 = { hdr: el, items: [], id: 'l1_' + l1.length }; l1.push(curL1); }
      else if (isLnk && curL1)  { curL1.items.push(el); }
      else                      { curL1 = null; }
    });

    /* Paso 2: acordeón L1 */
    l1.forEach(function(g) {
      if (!g.items.length) return;

      /* Auto-expandir si algún ítem del grupo es la página activa */
      var containsActive = g.items.some(function(el) {
        return el.getAttribute && el.getAttribute('href') === activePath;
      });
      var open = state[g.id] === true || containsActive;

      g.hdr.classList.add('wk-hdr');
      var chv = mkChv(open);
      g.hdr.appendChild(chv);

      /* Paso 3: L2 sub-grupos (links con mdi-chevron-right) */
      var l2 = [], curL2 = null;
      g.items.forEach(function(el) {
        if (el.querySelector('.mdi-chevron-right')) {
          curL2 = { hdr: el, items: [], id: g.id + '_l2_' + l2.length };
          l2.push(curL2);
        } else if (curL2) {
          curL2.items.push(el);
        }
      });

      var l2Hdrs  = l2.map(function(sg) { return sg.hdr; });
      var l2Items = [].concat.apply([], l2.map(function(sg) { return sg.items; }));

      /* Paso 4: acordeón L2 */
      l2.forEach(function(sg) {
        if (!sg.items.length) return;
        var sgContainsActive = sg.items.some(function(el) {
          return el.getAttribute && el.getAttribute('href') === activePath;
        });
        var sgOpen = state[sg.id] === true || sgContainsActive;

        sg.hdr.classList.add('wk-sub-hdr');
        sg.hdr.classList.add('wk-sub');

        var icon = sg.hdr.querySelector('.mdi-chevron-right');
        if (icon) {
          icon.classList.add('wk-sub-chv');
          if (sgOpen) icon.classList.add('wk-open');
        }

        sg.items.forEach(function(el) {
          el.classList.add('wk-sub2');
          el.style.display = (open && sgOpen) ? '' : 'none';
        });
        sg.hdr.style.display = open ? '' : 'none';

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

      /* Paso 5: clases a ítems normales (fuera de L2) */
      g.items.forEach(function(el) {
        if (l2Hdrs.indexOf(el) === -1 && l2Items.indexOf(el) === -1) {
          el.classList.add('wk-sub');
        }
      });

      /* Estado inicial ítems L1 */
      g.items.forEach(function(el) {
        if (!open) {
          el.style.display = 'none';
        } else {
          if (l2Items.indexOf(el) < 0) el.style.display = '';
        }
      });

      /* Handler L1: toggle grupo */
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

    /* Marcar página activa e inyectar botón */
    markActive(nav, activePath);
    injectCtrlBtn(nav);

    return true;
  }

  var tries = 0;
  var iv = setInterval(function() { if (init() || ++tries > 60) clearInterval(iv); }, 250);

  /* Re-inicializar en navegación SPA (Vue Router pushState) */
  var _push = history.pushState;
  history.pushState = function() {
    _push.apply(history, arguments);
    setTimeout(function() {
      var nav = findNav();
      if (nav) delete nav.dataset.wkInit;
      tries = 0;
      var iv2 = setInterval(function() { if (init() || ++tries > 60) clearInterval(iv2); }, 250);
      setTimeout(wkInitCalcs, 400);
    }, 200);
  };
})();

/* ── Calculadoras de dosis ── */
(function() {
  function f(v, d) { return +(v).toFixed(d === undefined ? 1 : d); }

  function wkCalcSIR(p) {
    var rows = [
      ['Atropina',            '0.02 mg/kg · máx 0.5 mg', Math.min(f(p*0.02,2),0.5)+' mg',  'Premedicación pediátrica'],
      ['Fentanilo inducción', '1–3 mcg/kg',               f(p*1,0)+'–'+f(p*3,0)+' mcg',     'Bolo lento IV'],
      ['Etomidato estable',   '0.3 mg/kg',                f(p*0.3)+' mg',                    ''],
      ['Etomidato inestable', '0.10–0.15 mg/kg',          f(p*0.10)+'–'+f(p*0.15)+' mg',    ''],
      ['Succinilcolina',      '1–1.5 mg/kg',              f(p*1,0)+'–'+f(p*1.5,0)+' mg',    ''],
      ['Rocuronio',           '1–1.5 mg/kg',              f(p*1,0)+'–'+f(p*1.5,0)+' mg',    'Si contraindicación succinilcolina'],
    ];
    return '<table style="width:100%;border-collapse:collapse;font-size:0.92em">'
      +'<thead><tr>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:2px solid rgba(4,72,142,0.35)">Fármaco</th>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:2px solid rgba(4,72,142,0.35);opacity:0.65;font-weight:400">Rango</th>'
      +'<th style="text-align:right;padding:5px 8px;border-bottom:2px solid rgba(4,72,142,0.35)">Dosis ('+p+' kg)</th>'
      +'<th style="text-align:left;padding:5px 8px;border-bottom:2px solid rgba(4,72,142,0.35);opacity:0.65;font-weight:400">Nota</th>'
      +'</tr></thead><tbody>'
      +rows.map(function(r) {
        return '<tr style="border-bottom:1px solid rgba(128,128,128,0.12)">'
          +'<td style="padding:5px 8px">'+r[0]+'</td>'
          +'<td style="padding:5px 8px;opacity:0.6;font-size:0.88em">'+r[1]+'</td>'
          +'<td style="padding:5px 8px;font-weight:700;text-align:right;color:var(--v-primary-base,#1565c0)">'+r[2]+'</td>'
          +'<td style="padding:5px 8px;opacity:0.6;font-size:0.88em">'+r[3]+'</td>'
          +'</tr>';
      }).join('')+'</tbody></table>';
  }

  function wkCalcSed(p) {
    var fL=f(p*1), fH=f(p*2), fRL=f(fL/10), fRH=f(fH/10);
    var mL=f(p*0.03), mH=f(p*0.1);
    var weightHtml = '<table style="width:100%;border-collapse:collapse;font-size:0.92em;margin-bottom:0.8rem">'
      +'<thead><tr>'
      +'<th style="text-align:left;padding:4px 8px;border-bottom:2px solid rgba(4,72,142,0.35)">Fármaco</th>'
      +'<th style="text-align:left;padding:4px 8px;border-bottom:2px solid rgba(4,72,142,0.35);opacity:0.65;font-weight:400">Dosis/kg</th>'
      +'<th style="text-align:right;padding:4px 8px;border-bottom:2px solid rgba(4,72,142,0.35)">Dosis/h</th>'
      +'<th style="text-align:right;padding:4px 8px;border-bottom:2px solid rgba(4,72,142,0.35);color:var(--v-primary-base,#1565c0)">Vel. BIC</th>'
      +'</tr></thead><tbody>'
      +'<tr style="border-bottom:1px solid rgba(128,128,128,0.12)">'
      +'<td style="padding:4px 8px">Fentanilo <small style="opacity:0.6">(10 mcg/mL)</small></td>'
      +'<td style="padding:4px 8px;opacity:0.6;font-size:0.88em">1–2 mcg/kg/h</td>'
      +'<td style="padding:4px 8px;text-align:right">'+fL+'–'+fH+' mcg/h</td>'
      +'<td style="padding:4px 8px;text-align:right;font-weight:700;color:var(--v-primary-base,#1565c0)">'+fRL+'–'+fRH+' mL/h</td>'
      +'</tr><tr>'
      +'<td style="padding:4px 8px">Midazolam <small style="opacity:0.6">(1 mg/mL)</small></td>'
      +'<td style="padding:4px 8px;opacity:0.6;font-size:0.88em">0.03–0.1 mg/kg/h</td>'
      +'<td style="padding:4px 8px;text-align:right">'+mL+'–'+mH+' mg/h</td>'
      +'<td style="padding:4px 8px;text-align:right;font-weight:700;color:var(--v-primary-base,#1565c0)">'+mL+'–'+mH+' mL/h</td>'
      +'</tr></tbody></table>';
    var escHtml = '<table style="width:100%;border-collapse:collapse;font-size:0.88em">'
      +'<thead><tr style="border-bottom:2px solid rgba(4,72,142,0.35)">'
      +'<th style="text-align:center;padding:4px 6px;width:3em">Esc.</th>'
      +'<th style="text-align:left;padding:4px 6px">Fentanilo</th>'
      +'<th style="text-align:right;padding:4px 6px;color:var(--v-primary-base,#1565c0)">Vel.</th>'
      +'<th style="text-align:left;padding:4px 6px">Midazolam</th>'
      +'<th style="text-align:right;padding:4px 6px;color:var(--v-primary-base,#1565c0)">Vel.</th>'
      +'<th style="text-align:left;padding:4px 6px;opacity:0.65">Indicación</th>'
      +'</tr></thead><tbody>'
      +[['1','25 mcg/h','2.5 mL/h','—','—','Inicio analgesia'],
        ['2','50 mcg/h','5 mL/h','—','—','Titular SAS 2–3'],
        ['3','50 mcg/h','5 mL/h','2 mg/h','2 mL/h','SAS >2 con E2'],
        ['4','100 mcg/h','10 mL/h','5 mg/h','5 mL/h','SAS >2 con E3'],
        ['5','150 mcg/h','15 mL/h','10 mg/h','10 mL/h','Máximo'],
      ].map(function(r,i) {
        return '<tr style="border-bottom:1px solid rgba(128,128,128,0.1);'+(i%2?'':'background:rgba(4,72,142,0.04)')+'">'
          +'<td style="text-align:center;padding:4px 6px;font-weight:700">'+r[0]+'</td>'
          +'<td style="padding:4px 6px">'+r[1]+'</td>'
          +'<td style="padding:4px 6px;text-align:right;font-weight:700;color:var(--v-primary-base,#1565c0)">'+r[2]+'</td>'
          +'<td style="padding:4px 6px">'+r[3]+'</td>'
          +'<td style="padding:4px 6px;text-align:right;font-weight:700;color:var(--v-primary-base,#1565c0)">'+r[4]+'</td>'
          +'<td style="padding:4px 6px;opacity:0.65">'+r[5]+'</td>'
          +'</tr>';
      }).join('')+'</tbody></table>';
    return '<strong style="display:block;margin-bottom:0.4rem">Dosis orientativas ('+p+' kg):</strong>'
      + weightHtml
      + '<strong style="display:block;margin-bottom:0.4rem">Escalones de sedación (preparación estándar):</strong>'
      + escHtml;
  }

  function wkCalcNorepi(p) {
    var preps = [
      { name: '4 mg / 250 mL SF', conc: 16 },
      { name: '4 mg / 100 mL SF', conc: 40 },
    ];
    var doses = [0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0];
    // Máximo recomendado periférico: 0.5 mcg/kg/min
    var MAX_PERIPH = 0.5;
    var maxMcgMin  = f(MAX_PERIPH * p, 1);
    var C  = 'color:var(--v-primary-base,#1565c0)';
    var CW = 'color:#e65100';   // naranja advertencia
    // Chip resumen dosis máxima
    var chip = '<div style="display:flex;align-items:center;gap:8px;margin-bottom:0.7rem;'
      +'background:rgba(230,81,0,0.08);border:1px solid rgba(230,81,0,0.3);'
      +'border-radius:6px;padding:0.5rem 0.8rem;font-size:0.9em">'
      +'<span style="font-size:1.1em">⚠️</span>'
      +'<span>Dosis máx. recomendada para vía periférica: '
      +'<strong style="'+CW+'">'+MAX_PERIPH+' mcg/kg/min</strong>'
      +' = <strong style="'+CW+'">'+maxMcgMin+' mcg/min</strong>'
      +' ('+p+' kg)</span></div>';
    var table = '<table style="width:100%;border-collapse:collapse;font-size:0.9em">'
      +'<thead><tr style="border-bottom:2px solid rgba(4,72,142,0.35)">'
      +'<th style="text-align:left;padding:5px 8px">Dosis</th>'
      +'<th style="text-align:right;padding:5px 8px;opacity:0.6;font-weight:400">mcg/min</th>'
      +'<th style="text-align:right;padding:5px 8px;opacity:0.6;font-weight:400">mcg/h</th>'
      +preps.map(function(pr) {
        return '<th style="text-align:right;padding:5px 8px;'+C+'">'
          +pr.name+'<br><small style="font-weight:400;opacity:0.7">('+pr.conc+' mcg/mL)</small></th>';
      }).join('')
      +'</tr></thead><tbody>'
      +doses.map(function(dose, j) {
        var over   = dose > MAX_PERIPH;
        var warn   = dose === MAX_PERIPH;
        var rowBg  = over  ? 'background:rgba(230,81,0,0.07)'
                   : warn  ? 'background:rgba(230,81,0,0.04)'
                   : j%2===0 ? 'background:rgba(4,72,142,0.03)' : '';
        var mcgMin = f(dose*p, 1);
        var mcgh   = f(dose*p*60, 0);
        var dColor = over ? CW : warn ? CW : '';
        var dBold  = (dose===0.1||over||warn) ? '700' : '400';
        return '<tr style="border-bottom:1px solid rgba(128,128,128,0.1);'+rowBg+'">'
          +'<td style="padding:5px 8px;font-weight:'+dBold+';'+dColor+'">'
            +dose+' mcg/kg/min'+(over?' ⚠️':warn?' ⚑':'')+' </td>'
          +'<td style="text-align:right;padding:5px 8px;font-weight:'+dBold+';'+dColor+'">'+mcgMin+'</td>'
          +'<td style="text-align:right;padding:5px 8px;opacity:0.6;font-size:0.88em">'+mcgh+'</td>'
          +preps.map(function(pr) {
            return '<td style="text-align:right;padding:5px 8px;font-weight:700;'+(over?CW:C)+'">'
              +f(dose*p*60/pr.conc, 1)+' mL/h</td>';
          }).join('')
          +'</tr>';
      }).join('')
      +'</tbody></table>'
      +'<p style="font-size:0.82em;opacity:0.65;margin-top:0.5rem">'
      +'Concentración máxima periférica: 40 mcg/mL · Preferir acceso central si dosis > '+MAX_PERIPH+' mcg/kg/min o uso prolongado.'
      +'</p>';
    return '<strong style="display:block;margin-bottom:0.5rem">Velocidades de infusión ('+p+' kg):</strong>'
      + chip + table;
  }

  /* ── Superficie corporal quemada (Regla de 9 / Lund-Browder) ── */
  function wkCalcQuemadosSC(v) {
    var modo = v.modo || 'adulto';
    var edad = v.edad || 25;
    var REG = [
      { k:'cab',    l:'Cabeza y cuello',         r:function(e,m){ return m==='pediatrico'&&e<15?(e<=1?18:e<=4?15:e<=9?13:11):9; } },
      { k:'tant',   l:'Tronco anterior',          r:function(e,m){ return m==='pediatrico'&&e<15?13:18; } },
      { k:'tpost',  l:'Tronco posterior',         r:function(e,m){ return m==='pediatrico'&&e<15?13:18; } },
      { k:'brad',   l:'Brazo derecho (completo)', r:function(){ return 9; } },
      { k:'brai',   l:'Brazo izquierdo (completo)',r:function(){ return 9; } },
      { k:'pierd',  l:'Pierna derecha (completa)',r:function(e,m){ return m==='pediatrico'&&e<15?(e<=1?13:e<=4?14:e<=9?15:17):18; } },
      { k:'pieri',  l:'Pierna izquierda (completa)',r:function(e,m){ return m==='pediatrico'&&e<15?(e<=1?13:e<=4?14:e<=9?15:17):18; } },
      { k:'perine', l:'Genitales / periné',       r:function(){ return 1; } },
    ];
    var total = 0;
    REG.forEach(function(r){ total += parseFloat(v[r.k])||0; });
    total = Math.round(total*10)/10;
    var gran = modo==='pediatrico' ? total>=15 : total>=20;
    var sevLabel, sevC;
    if      (total<10)                              { sevLabel='Menor';              sevC='#2e7d32'; }
    else if (total<(modo==='pediatrico'?15:20))     { sevLabel='Moderada';           sevC='#e65100'; }
    else if (total<40)                              { sevLabel='Gran Quemado';        sevC='#b71c1c'; }
    else                                            { sevLabel='Gran Quemado Crítico';sevC='#b71c1c'; }
    var refRows = REG.map(function(r){
      var val=parseFloat(v[r.k])||0, ref=r.r(edad,modo);
      return '<tr style="border-bottom:1px solid rgba(128,128,128,0.08)">'
        +'<td style="padding:3px 8px;font-size:0.88em">'+r.l+'</td>'
        +'<td style="text-align:right;padding:3px 8px;font-size:0.82em;opacity:0.55">'+ref+'%</td>'
        +'<td style="text-align:right;padding:3px 8px;font-weight:700;color:'+(val>0?sevC:'inherit')+'">'+val+'%</td>'
        +'</tr>';
    }).join('');
    return '<div style="display:flex;align-items:center;gap:12px;margin-bottom:0.8rem">'
      +'<span style="font-size:2.2em;font-weight:700;color:'+sevC+'">'+total+'%</span>'
      +'<div style="flex:1"><div style="font-weight:700;color:'+sevC+'">'+sevLabel+'</div>'
      +'<div style="background:rgba(128,128,128,0.15);border-radius:4px;height:10px;overflow:hidden;margin:4px 0">'
      +'<div style="height:100%;width:'+Math.min(total,100)+'%;background:'+sevC+';border-radius:4px;transition:width 0.3s"></div></div>'
      +'<div style="font-size:0.8em;opacity:0.6">SCQ — '+(modo==='pediatrico'?'pediátrico':'adulto')+'</div>'
      +'</div></div>'
      +(gran?'<div style="background:rgba(183,28,28,0.1);border:1px solid rgba(183,28,28,0.4);'
        +'border-radius:6px;padding:0.4rem 0.8rem;font-size:0.88em;margin-bottom:0.8rem">'
        +'🔴 <strong>Criterios de Gran Quemado</strong> — UCI/UCQ · Fórmula de Parkland indicada</div>':'')
      +'<details style="cursor:pointer"><summary style="font-size:0.85em;opacity:0.65;padding:2px 0">Referencia por región ('
      +(modo==='pediatrico'?'Lund-Browder, '+edad+' a':'Regla de los 9')
      +')</summary><table style="width:100%;border-collapse:collapse;margin-top:4px">'
      +'<tr style="border-bottom:1px solid rgba(128,128,128,0.2)">'
      +'<th style="text-align:left;padding:3px 8px;font-size:0.82em">Región</th>'
      +'<th style="text-align:right;padding:3px 8px;font-weight:400;opacity:0.6;font-size:0.82em">Ref</th>'
      +'<th style="text-align:right;padding:3px 8px;font-size:0.82em">Quemado</th></tr>'
      +refRows+'</table></details>';
  }

  /* ── Volumen resucitación gran quemado (Parkland) ── */
  function wkCalcQuemadosVol(v) {
    var modo  = v.modo  || 'adulto';
    var peso  = v.peso  || 70;
    var scq   = v.scq   || 0;
    var horas = Math.min(v.horas||0, 8);
    if (scq<=0) return '<p style="opacity:0.5;font-size:0.9em;margin:0">Ingresa % SCQ para calcular.</p>';
    var park24 = 4*peso*scq;
    var park1  = park24/2;
    var park2  = park24/2;
    var hRest  = Math.max(8-horas, 0);
    var rate1  = hRest>0 ? Math.round(park1/hRest) : 0;
    var rate2  = Math.round(park2/16);
    var C = 'color:var(--v-primary-base,#1565c0)';
    var maintRow = '';
    if (modo==='pediatrico') {
      var maintDay = peso<=10 ? peso*100 : peso<=20 ? 1000+(peso-10)*50 : 1500+(peso-20)*20;
      var mh = Math.round(maintDay/24);
      maintRow = '<tr style="border-bottom:1px solid rgba(128,128,128,0.1);background:rgba(4,72,142,0.03)">'
        +'<td style="padding:5px 8px;opacity:0.75">+ Mantención (Holliday-Segar)</td>'
        +'<td style="text-align:right;padding:5px 8px;'+C+'">'+maintDay+' mL/día</td>'
        +'<td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+mh+' mL/h</td></tr>'
        +'<tr style="border-top:2px solid rgba(4,72,142,0.25)">'
        +'<td style="padding:5px 8px;font-weight:700">Total 1er período (resusc+mant)</td>'
        +'<td></td><td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+(hRest>0?rate1+mh:0)+' mL/h</td></tr>'
        +'<tr><td style="padding:5px 8px;font-weight:700">Total 2do período (resusc+mant)</td>'
        +'<td></td><td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+(rate2+mh)+' mL/h</td></tr>';
    }
    return '<table style="width:100%;border-collapse:collapse;font-size:0.92em">'
      +'<thead><tr style="border-bottom:2px solid rgba(4,72,142,0.35)">'
      +'<th style="text-align:left;padding:5px 8px">Parámetro</th>'
      +'<th style="text-align:right;padding:5px 8px;'+C+'">Volumen</th>'
      +'<th style="text-align:right;padding:5px 8px;'+C+'">Vel. BIC</th>'
      +'</tr></thead><tbody>'
      +'<tr style="border-bottom:1px solid rgba(128,128,128,0.1)">'
      +'<td style="padding:5px 8px">Total 24h (Parkland: 4×'+peso+'×'+scq+'%)</td>'
      +'<td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+Math.round(park24)+' mL</td>'
      +'<td></td></tr>'
      +'<tr style="background:rgba(4,72,142,0.03);border-bottom:1px solid rgba(128,128,128,0.1)">'
      +'<td style="padding:5px 8px">Primeras 8h desde quemadura (50%)'+(hRest<8?' — restan '+f(hRest,1)+'h':'')+'</td>'
      +'<td style="text-align:right;padding:5px 8px;'+C+'">'+Math.round(park1)+' mL</td>'
      +'<td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+(hRest>0?rate1+' mL/h':'— completado')+'</td></tr>'
      +'<tr style="border-bottom:1px solid rgba(128,128,128,0.1)">'
      +'<td style="padding:5px 8px">Siguientes 16h (50%)</td>'
      +'<td style="text-align:right;padding:5px 8px;'+C+'">'+Math.round(park2)+' mL</td>'
      +'<td style="text-align:right;padding:5px 8px;font-weight:700;'+C+'">'+rate2+' mL/h</td></tr>'
      +maintRow
      +'</tbody></table>'
      +'<p style="font-size:0.82em;opacity:0.6;margin-top:0.5rem">'
      +'Ringer Lactato · Titular diuresis: '+(modo==='pediatrico'?'niño 1 mL/kg/h':'adulto 0.5 mL/kg/h')
      +(modo==='pediatrico'?' · Mantención con DRL 5%':'')+'.</p>';
  }

  window.wkInitCalcs = function() {
    document.querySelectorAll('[data-calc]').forEach(function(el) {
      if (el.dataset.calcInit) return;
      el.dataset.calcInit = '1';
      var output = el.querySelector('[data-calc-output]');
      var type   = el.dataset.calc;
      if (!output) return;
      function collect() {
        var v = {};
        var si = el.querySelector('[data-calc-input]');
        if (si) v.p = parseFloat(si.value) || 70;
        el.querySelectorAll('input[name],select[name]').forEach(function(i) {
          v[i.name] = i.tagName==='SELECT' ? i.value : (parseFloat(i.value)||0);
        });
        return v;
      }
      function update() {
        var v = collect();
        if (type==='sir')          output.innerHTML = wkCalcSIR(v.p||70);
        if (type==='sedacion')     output.innerHTML = wkCalcSed(v.p||70);
        if (type==='norepi')       output.innerHTML = wkCalcNorepi(v.p||70);
        if (type==='quemados-sc')  output.innerHTML = wkCalcQuemadosSC(v);
        if (type==='quemados-vol') output.innerHTML = wkCalcQuemadosVol(v);
      }
      el.querySelectorAll('input,select').forEach(function(i){
        i.addEventListener('input', update);
        i.addEventListener('change', update);
      });
      update();
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', wkInitCalcs);
  } else {
    wkInitCalcs();
  }
  var _calcObs = new MutationObserver(function() { setTimeout(wkInitCalcs, 300); });
  _calcObs.observe(document.body, { childList: true, subtree: false });
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
