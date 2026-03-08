#!/usr/bin/env python3
"""
Crea el menú de navegación estático para caspm.urgpedia.cl.
Actualiza la tabla 'navigation' con los ítems del menú y cambia
la configuración de nav a modo STATIC.
"""
import json, subprocess, uuid

def psql_json(sql):
    r = subprocess.run(
        ["docker", "exec", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki", "-t", "-c", sql],
        capture_output=True, text=True, check=True
    )
    return r.stdout.strip()

def psql_exec(sql_input):
    r = subprocess.run(
        ["docker", "exec", "-i", "wiki-db", "psql", "-U", "wikijs", "-d", "wiki"],
        input=sql_input.encode("utf-8"),
        capture_output=True
    )
    print("  OUT:", r.stdout.decode("utf-8").strip())
    if r.stderr.strip():
        print("  ERR:", r.stderr.decode("utf-8").strip())
    return r.returncode

def uid():
    return str(uuid.uuid4())

# Menú de navegación — orden clínico
nav_items = [
    {"id": uid(), "kind": "link", "label": "Inicio",
     "icon": "mdi-home", "targetType": "external", "target": "/es/home",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "divider", "label": "", "icon": "",
     "targetType": "", "target": "", "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Introducción",
     "icon": "mdi-book-open-variant", "targetType": "external", "target": "/es/introduccion",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "El Servicio",
     "icon": "mdi-hospital-building", "targetType": "external", "target": "/es/el-servicio",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Interconsultores",
     "icon": "mdi-account-group", "targetType": "external", "target": "/es/interconsultores/tabla",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Servicios de Apoyo",
     "icon": "mdi-flask", "targetType": "external", "target": "/es/servicios-de-apoyo",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Marco Legal",
     "icon": "mdi-gavel", "targetType": "external", "target": "/es/marco-legal",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "divider", "label": "", "icon": "",
     "targetType": "", "target": "", "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Protocolos Operativos",
     "icon": "mdi-clipboard-list", "targetType": "external", "target": "/es/protocolos-operativos",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Protocolos de Calidad",
     "icon": "mdi-shield-check", "targetType": "external", "target": "/es/protocolos-calidad",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Protocolos Clínicos",
     "icon": "mdi-stethoscope", "targetType": "external", "target": "/es/protocolos-clinicos",
     "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "divider", "label": "", "icon": "",
     "targetType": "", "target": "", "visibilityMode": "all", "visibilityGroups": None},

    {"id": uid(), "kind": "link", "label": "Calculadoras",
     "icon": "mdi-calculator", "targetType": "external", "target": "/es/calculadoras",
     "visibilityMode": "all", "visibilityGroups": None},
]

nav_config = [
    {"locale": "es", "items": nav_items},
    {"locale": "en", "items": nav_items},  # misma nav para locale en
]

config_json = json.dumps(nav_config, ensure_ascii=False)
TAG = "NAVUPDATE2026"

# 1. Actualizar tabla navigation
sql_nav = f"""
UPDATE navigation
SET config = ${TAG}${config_json}${TAG}$::json
WHERE key = 'site'
RETURNING key;
"""
print("1. Actualizando tabla navigation...")
rc = psql_exec(sql_nav)

# 2. Cambiar modo a STATIC
sql_mode = f"""
UPDATE settings
SET value = '{{"mode":"STATIC"}}'::json
WHERE key = 'nav'
RETURNING key;
"""
print("2. Cambiando modo nav a STATIC...")
rc2 = psql_exec(sql_mode)

if rc == 0 and rc2 == 0:
    print("\n✓ Navegación actualizada. Reiniciando wiki para aplicar cambios...")
    r = subprocess.run(["docker", "restart", "wiki"], capture_output=True)
    print("  Reinicio:", "OK" if r.returncode == 0 else f"ERROR {r.returncode}")
else:
    print("\n✗ Error en algún paso.")
