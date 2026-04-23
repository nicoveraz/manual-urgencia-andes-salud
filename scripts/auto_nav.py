#!/usr/bin/env python3
"""
auto_nav.py — sincroniza el sidebar de Wiki.js desde las páginas publicadas.

Consulta pages table vía psql, agrupa por prefijo de path, genera nav accordion
(usa el inject wk-accordion de create_nav_accordion.py, que ya vive en injectHead).

Uso:
  python3 auto_nav.py            # re-sincroniza + reinicia wiki
  python3 auto_nav.py --dry      # imprime nav sin aplicar

Configuración: edita SECTIONS para mapear prefijos → grupos L1 y sub-grupos L2.
"""
import json, subprocess, uuid, sys, re, hashlib, os

# ── Config ────────────────────────────────────────────────────────────────────
# (path_prefix, label, icon, [sub_groups] | None)
# sub_groups = [(sub_prefix, sub_label), ...] — para secciones con L2
SECTIONS = [
    ("/es/introduccion",         "Introducción",          "mdi-book-open-variant", None),
    ("/es/el-servicio",          "El Servicio",           "mdi-hospital-building", None),
    ("/es/interconsultores",     "Interconsultores",      "mdi-account-group",     None),
    ("/es/servicios-de-apoyo",   "Servicios de Apoyo",    "mdi-flask",             None),
    ("/es/marco-legal",          "Marco Legal",           "mdi-gavel",             None),
    ("/es/protocolos-operativos","Protocolos Operativos", "mdi-clipboard-list",    None),
    ("/es/protocolos-calidad",   "Protocolos de Calidad", "mdi-shield-check",      None),
    ("/es/protocolos-clinicos",  "Protocolos Clínicos",   "mdi-stethoscope", [
        # Order matters: more specific prefixes FIRST so nested groups win.
        ("/es/protocolos-clinicos/por-patologia/procedimientos", "Procedimientos"),
        ("/es/protocolos-clinicos/por-presentacion",             "Por Presentación Clínica"),
        ("/es/protocolos-clinicos/por-patologia",                "Por Patología"),
        ("/es/protocolos-clinicos/adulto",                       "Adulto — Decreto 34"),
        ("/es/protocolos-clinicos/pediatrico",                   "Pediátrico / Neonatal — Decreto 34"),
    ]),
    ("/es/calculadoras",         "Calculadoras",          "mdi-calculator",        None),
]

HOME_PATH  = "/es/home"
LOCALE     = "es"
HASH_FILE  = "/tmp/.auto_nav_hash"

# ── Helpers ───────────────────────────────────────────────────────────────────
def uid(): return str(uuid.uuid4())

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

def psql_pipe(sql):
    r = subprocess.run(
        ["docker", "exec", "-i", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki"],
        input=sql.encode("utf-8"), capture_output=True,
    )
    if r.stdout: print("  →", r.stdout.decode().strip())
    if r.stderr: print("  ✗", r.stderr.decode().strip())
    return r.returncode

def psql_query(sql):
    r = subprocess.run(
        ["docker", "exec", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki",
         "-t", "-A", "-F", "\t", "-c", sql],
        capture_output=True, text=True,
    )
    return r.stdout.strip()

# ── Fetch published pages ─────────────────────────────────────────────────────
def fetch_pages():
    # Wiki.js 2.x: pages.path is WITHOUT locale prefix; locale is separate column
    # DISTINCT ON(path) guards against accidental duplicate rows
    sql = (f"SELECT DISTINCT ON(path) path, title FROM pages "
           f"WHERE \"localeCode\"='{LOCALE}' AND \"isPublished\"=true "
           f"ORDER BY path, id;")
    out = psql_query(sql)
    seen = set()
    pages = []
    for line in out.split("\n"):
        if not line: continue
        parts = line.split("\t")
        if len(parts) < 2: continue
        path, title = parts[0].strip(), parts[1].strip()
        full = f"/{LOCALE}/{path.lstrip('/')}"
        if full in seen: continue
        seen.add(full)
        pages.append((full, title))
    return pages

# ── Natural sort (§1 before §10) ──────────────────────────────────────────────
def natural_key(title):
    return [int(p) if p.isdigit() else p.lower()
            for p in re.split(r"(\d+)", title or "")]

# ── Build nav ─────────────────────────────────────────────────────────────────
def build_nav(pages):
    items = [lnk("Inicio", HOME_PATH, "mdi-home"), div()]
    used = set([HOME_PATH])

    # Section-index pages (path == L1 prefix, e.g. /es/introduccion) are
    # redundant inside their own section — the L1 header already represents
    # them. Mark them as used so they don't appear as list items.
    section_indexes = {s[0] for s in SECTIONS}
    for p in pages:
        if p[0] in section_indexes:
            used.add(p[0])

    for prefix, label, icon, subs in SECTIONS:
        section_pages = [p for p in pages
                         if p[0].startswith(prefix + "/") or p[0] == prefix]
        section_pages = [p for p in section_pages if p[0] not in used]
        if not section_pages:
            continue

        items.append(hdr(label, icon))

        if subs:
            sub_prefixes = [s[0] for s in subs]
            orphans = [p for p in section_pages
                       if not any(p[0] == sp or p[0].startswith(sp + "/") for sp in sub_prefixes)]
            orphans.sort(key=lambda p: natural_key(p[1]))
            for path, title in orphans:
                items.append(lnk(title, path))
                used.add(path)

            for sub_prefix, sub_label in subs:
                sub_pages = [p for p in section_pages
                             if (p[0] == sub_prefix or p[0].startswith(sub_prefix + "/"))
                             and p[0] not in used]
                if not sub_pages: continue
                items.append(lnk(sub_label, sub_prefix, "mdi-chevron-right"))
                used.add(sub_prefix)
                sub_items = [p for p in sub_pages if p[0] != sub_prefix]
                sub_items.sort(key=lambda p: natural_key(p[1]))
                for path, title in sub_items:
                    items.append(lnk(title, path))
                    used.add(path)
        else:
            section_pages.sort(key=lambda p: natural_key(p[1]))
            for path, title in section_pages:
                items.append(lnk(title, path))
                used.add(path)

        items.append(div())

    if items and items[-1]["kind"] == "divider":
        items.pop()
    return items

# ── Hash (skip UPDATE + restart when nav unchanged) ──────────────────────────
def nav_hash(items):
    # Hash only label+target+kind+icon+order (ignore uuid — re-rolled each run)
    canon = [(i["kind"], i.get("label", ""), i.get("target", ""), i.get("icon", ""))
             for i in items]
    return hashlib.sha256(json.dumps(canon).encode("utf-8")).hexdigest()

def load_prev_hash():
    try:
        with open(HASH_FILE) as f: return f.read().strip()
    except Exception: return ""

def save_hash(h):
    try:
        with open(HASH_FILE, "w") as f: f.write(h)
    except Exception as e: print(f"  ✗ cache write: {e}")

# ── Apply ─────────────────────────────────────────────────────────────────────
def apply_nav(items):
    nav_config = [
        {"locale": "es", "items": items},
        {"locale": "en", "items": items},
    ]
    nav_json = json.dumps(nav_config, ensure_ascii=False)
    TAG = "WKAUTONAV"
    sql = f"""
UPDATE navigation SET config = ${TAG}N${nav_json}${TAG}N$::json WHERE key='site';
UPDATE settings   SET value  = '{{"mode":"STATIC"}}'::json WHERE key='nav';
"""
    print("Aplicando nav...")
    rc = psql_pipe(sql)
    if rc != 0:
        print("✗ Falló UPDATE"); sys.exit(1)
    print("✓ Nav actualizado.")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    dry = "--dry" in sys.argv
    print("Leyendo páginas...")
    pages = fetch_pages()
    print(f"  {len(pages)} páginas publicadas en locale='{LOCALE}'")
    items = build_nav(pages)
    l1 = sum(1 for i in items if i["kind"] == "header")
    l2 = sum(1 for i in items if i.get("icon") == "mdi-chevron-right")
    lk = sum(1 for i in items if i["kind"] == "link" and i.get("icon") != "mdi-chevron-right")
    print(f"  {l1} L1 · {l2} L2 · {lk} links")

    if dry:
        print("\n─── NAV PREVIEW (--dry) ───")
        for i in items:
            if i["kind"] == "divider":
                print("  ───")
            elif i["kind"] == "header":
                print(f"\n▼ {i['label']}")
            else:
                indent = "    " if i["icon"] == "mdi-chevron-right" else "      "
                print(f"{indent}• {i['label']}  [{i['target']}]")
        return

    force = "--force" in sys.argv
    cur_hash  = nav_hash(items)
    prev_hash = load_prev_hash()
    if cur_hash == prev_hash and not force:
        print("✓ Nav sin cambios. Skip UPDATE + restart.")
        return
    if prev_hash and not force:
        print(f"  Cambios detectados ({prev_hash[:8]} → {cur_hash[:8]})")

    apply_nav(items)
    save_hash(cur_hash)
    subprocess.run(["docker", "restart", "wiki"], capture_output=True)
    print("✓ Wiki reiniciado.")

if __name__ == "__main__":
    main()
