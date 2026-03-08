#!/usr/bin/env python3
"""
Crea las páginas base del wiki de urgpedia CASPM en Wiki.js via GraphQL API.

Uso:
    # 1. Generar /tmp/wiki_token.txt con JWT válido (ver docs/ESTADO-ACTUAL.md)
    # 2. Ejecutar en el servidor:
    python3 create_wiki_pages.py

Solo crea páginas nuevas; las existentes generan "skip".
"""
import json, urllib.request, urllib.error, time

GQL = "http://localhost:3000/graphql"
TOKEN = open("/tmp/wiki_token.txt").read().strip()


def gql(query, variables=None):
    body = json.dumps(
        {"query": query, "variables": variables or {}},
        ensure_ascii=False
    ).encode("utf-8")
    req = urllib.request.Request(GQL, data=body, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json; charset=utf-8"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


CREATE = (
    "mutation($content:String!,$description:String!,$editor:String!,"
    "$isPrivate:Boolean!,$isPublished:Boolean!,$locale:String!,"
    "$path:String!,$tags:[String]!,$title:String!){"
    "pages{create(content:$content,description:$description,"
    "editor:$editor,isPrivate:$isPrivate,isPublished:$isPublished,"
    "locale:$locale,path:$path,tags:$tags,title:$title){"
    "responseResult{succeeded errorCode message}page{id path}}}}"
)

PH = "*Contenido pendiente — esta sección está en desarrollo.*"


def p(path, title, desc="", content=None):
    return {"path": path, "title": title, "description": desc,
            "content": content or f"# {title}\n\n{PH}"}


HOME = """# Manual de Urgencia · CASPM Puerto Montt

Bienvenido al manual de urgencia de la Clínica Andes Salud Puerto Montt.

## Secciones principales

| Sección | Descripción |
|---|---|
| [Introducción](/es/introduccion) | Presentación y guía de uso del manual |
| [El Servicio](/es/el-servicio) | Misión, visión, descripción y organigrama |
| [Interconsultores](/es/interconsultores/tabla) | Contactos y criterios por especialidad |
| [Servicios de Apoyo](/es/servicios-de-apoyo) | Laboratorio, imagenología, farmacia, banco de sangre |
| [Marco Legal](/es/marco-legal) | Ley de urgencia, GES, ENO, licencias |
| [Protocolos Operativos](/es/protocolos-operativos) | Triage, circuito del paciente, código rojo, traslado |
| [Protocolos de Calidad](/es/protocolos-calidad) | Seguridad del paciente, IAAS, eventos adversos |
| [Protocolos Clínicos](/es/protocolos-clinicos) | Por presentación clínica y por patología |
| [Calculadoras Clínicas](/es/calculadoras) | Herramientas interactivas con indicaciones |"""

# Orden: Intro → El Servicio → Interconsultores → Servicios de Apoyo →
#        Marco Legal → Protocolos Operativos → Protocolos de Calidad →
#        Protocolos Clínicos → Calculadoras
PAGES = [
    p("home", "Inicio", "Manual de Urgencia CASPM", HOME),

    # ── Introducción ──────────────────────────────────────────────────────────
    p("introduccion", "Introducción", "Presentación del manual",
      "# Introducción\n\n"
      "- [Bienvenida](/es/introduccion/bienvenida)\n"
      "- [Cómo usar este manual](/es/introduccion/como-usar-este-manual)\n"),
    p("introduccion/bienvenida", "Bienvenida", "Presentación del manual de urgencia"),
    p("introduccion/como-usar-este-manual", "Cómo usar este manual", "Guía de navegación y uso"),

    # ── El Servicio ───────────────────────────────────────────────────────────
    p("el-servicio", "El Servicio", "Descripción del servicio de urgencia",
      "# El Servicio\n\n"
      "- [Misión y Visión](/es/el-servicio/mision-y-vision)\n"
      "- [Descripción del Servicio](/es/el-servicio/descripcion)\n"
      "- [Organigrama](/es/el-servicio/organigrama)\n"
      "- [Horarios y Turnos](/es/el-servicio/horarios-y-turnos)\n"),
    p("el-servicio/mision-y-vision", "Misión y Visión", "Misión y visión del servicio de urgencia"),
    p("el-servicio/descripcion", "Descripción del Servicio", "Planta física, dotación, box, UPAM"),
    p("el-servicio/organigrama", "Organigrama", "Estructura organizacional del servicio"),
    p("el-servicio/horarios-y-turnos", "Horarios y Turnos", "Horarios y estructura de turnos"),

    # ── Interconsultores ──────────────────────────────────────────────────────
    p("interconsultores", "Interconsultores", "Contactos y criterios de derivación",
      "# Interconsultores\n\n→ [Tabla de Interconsultores](/es/interconsultores/tabla)\n"),
    p("interconsultores/tabla", "Tabla de Interconsultores", "Especialidad, contacto, horario y criterios",
      "# Tabla de Interconsultores\n\n"
      "| Especialidad | Profesional | Contacto | Horario | Criterios de derivación | T° respuesta |\n"
      "|---|---|---|---|---|---|\n"
      "| Medicina Interna | | | | | |\n"
      "| Cardiología | | | | | |\n"
      "| Cirugía General | | | | | |\n"
      "| Traumatología | | | | | |\n"
      "| Neurología | | | | | |\n"
      "| Psiquiatría | | | | | |\n"
      "| Ginecología | | | | | |\n"
      "| Pediatría | | | | | |\n"
      "| Oftalmología | | | | | |\n"
      "| ORL | | | | | |\n"
      "| Urología | | | | | |\n"
      "| Anestesiología | | | | | |\n\n"
      "> *Completar con datos de contacto reales del servicio.*\n"),

    # ── Servicios de Apoyo ────────────────────────────────────────────────────
    p("servicios-de-apoyo", "Servicios de Apoyo", "Laboratorio, imagenología, farmacia y otros",
      "# Servicios de Apoyo\n\n"
      "- [Laboratorio](/es/servicios-de-apoyo/laboratorio)\n"
      "- [Imagenología](/es/servicios-de-apoyo/imagenologia)\n"
      "- [Banco de Sangre](/es/servicios-de-apoyo/banco-de-sangre)\n"
      "- [Farmacia](/es/servicios-de-apoyo/farmacia)\n"
      "- [Otros](/es/servicios-de-apoyo/otros)\n"),
    p("servicios-de-apoyo/laboratorio", "Laboratorio", "Exámenes disponibles, tiempos de respuesta, valores críticos"),
    p("servicios-de-apoyo/imagenologia", "Imagenología", "Modalidades disponibles, disponibilidad nocturna y fin de semana"),
    p("servicios-de-apoyo/banco-de-sangre", "Banco de Sangre", "Productos, tiempos, protocolo de transfusión masiva"),
    p("servicios-de-apoyo/farmacia", "Farmacia", "Arsenal de urgencia, medicamentos fuera de stock"),
    p("servicios-de-apoyo/otros", "Otros Servicios", "TENS, arsenales, gases clínicos, carro de paro"),

    # ── Marco Legal ───────────────────────────────────────────────────────────
    p("marco-legal", "Marco Legal", "Normativa legal aplicable en urgencia",
      "# Marco Legal\n\n"
      "- [Ley de Urgencia](/es/marco-legal/ley-de-urgencia)\n"
      "- [Accidentes del Trabajo](/es/marco-legal/accidentes-del-trabajo)\n"
      "- [Licencias Médicas](/es/marco-legal/licencias-medicas)\n"
      "- [ENO](/es/marco-legal/eno)\n"
      "- [GES/AUGE](/es/marco-legal/ges-auge)\n"
      "- [Violencia y Maltrato](/es/marco-legal/violencia-y-maltrato)\n"
      "- [Otros Marcos Legales](/es/marco-legal/otros)\n"),
    p("marco-legal/ley-de-urgencia", "Ley de Urgencia", "Ley 19.966 — cobertura FONASA/ISAPRE"),
    p("marco-legal/accidentes-del-trabajo", "Accidentes del Trabajo", "Ley 16.744 — MUTUAL, derivación, formularios"),
    p("marco-legal/licencias-medicas", "Licencias Médicas", "Tipos A/B/C, plazos, COMPIN, formularios"),
    p("marco-legal/eno", "ENO", "Listado ENO, formulario EPIVID, plazos de denuncia"),
    p("marco-legal/ges-auge", "GES/AUGE", "Garantías con plazo en urgencia, canastas"),
    p("marco-legal/violencia-y-maltrato", "Violencia y Maltrato", "VIF, AVIF, maltrato infantil, protocolo de denuncia"),
    p("marco-legal/otros", "Otros Marcos Legales", "Consentimiento, menores sin adulto, paciente incapacitado"),

    # ── Protocolos Operativos ─────────────────────────────────────────────────
    p("protocolos-operativos", "Protocolos Operativos", "Triage, circuito del paciente, código rojo y más",
      "# Protocolos Operativos\n\n"
      "- [Triage](/es/protocolos-operativos/triage)\n"
      "- [Circuito del Paciente](/es/protocolos-operativos/circuito-del-paciente)\n"
      "- [Código Rojo](/es/protocolos-operativos/codigo-rojo)\n"
      "- [Traslado](/es/protocolos-operativos/traslado)\n"
      "- [Manejo de Camas](/es/protocolos-operativos/manejo-de-camas)\n"
      "- [Emergencias Internas](/es/protocolos-operativos/emergencias-internas)\n"),
    p("protocolos-operativos/triage", "Triage", "Escala de triage, criterios por categoría y flujo"),
    p("protocolos-operativos/circuito-del-paciente", "Circuito del Paciente", "Admisión, evaluación, tratamiento y destino"),
    p("protocolos-operativos/codigo-rojo", "Código Rojo", "Activación, roles del equipo, checklist RCP/ACLS"),
    p("protocolos-operativos/traslado", "Traslado de Pacientes", "Criterios, soporte y formularios de traslado"),
    p("protocolos-operativos/manejo-de-camas", "Manejo de Camas", "Criterios de hospitalización y gestión del flujo"),
    p("protocolos-operativos/emergencias-internas", "Emergencias Internas", "Código azul, paciente violento, incendio"),

    # ── Protocolos de Calidad ─────────────────────────────────────────────────
    p("protocolos-calidad", "Protocolos de Calidad", "Seguridad del paciente, IAAS, eventos adversos",
      "# Protocolos de Calidad\n\n"
      "- [Seguridad del Paciente](/es/protocolos-calidad/seguridad-del-paciente)\n"
      "- [IAAS](/es/protocolos-calidad/iaas)\n"
      "- [Indicadores](/es/protocolos-calidad/indicadores)\n"
      "- [Eventos Adversos](/es/protocolos-calidad/eventos-adversos)\n"
      "- [Auditoría Clínica](/es/protocolos-calidad/auditoria)\n"),
    p("protocolos-calidad/seguridad-del-paciente", "Seguridad del Paciente", "Identificación, higiene de manos, prevención de caídas"),
    p("protocolos-calidad/iaas", "IAAS", "Precauciones estándar, aislamiento, uso de EPP"),
    p("protocolos-calidad/indicadores", "Indicadores de Gestión", "Tiempos de atención, repitencia, mortalidad"),
    p("protocolos-calidad/eventos-adversos", "Notificación de Eventos Adversos", "Clasificación, notificación y análisis"),
    p("protocolos-calidad/auditoria", "Auditoría Clínica", "Revisión de fichas e indicadores de proceso"),

    # ── Protocolos Clínicos ───────────────────────────────────────────────────
    p("protocolos-clinicos", "Protocolos Clínicos", "Por presentación clínica y por patología",
      "# Protocolos Clínicos\n\n"
      "## Por presentación\n"
      "*(¿Qué veo? → qué hago)*\n\n"
      "→ [Ver protocolos por presentación](/es/protocolos-clinicos/por-presentacion)\n\n"
      "## Por patología\n"
      "*(Ya sé el diagnóstico → protocolo específico)*\n\n"
      "→ [Ver protocolos por patología](/es/protocolos-clinicos/por-patologia)\n"),
    p("protocolos-clinicos/por-presentacion", "Por Presentación Clínica", "Protocolos organizados por motivo de consulta",
      "# Por Presentación Clínica\n\n"
      "| Presentación | |\n|---|---|\n"
      "| [Dolor torácico](/es/protocolos-clinicos/por-presentacion/dolor-toracico) | |\n"
      "| [Disnea](/es/protocolos-clinicos/por-presentacion/disnea) | |\n"
      "| [Dolor abdominal](/es/protocolos-clinicos/por-presentacion/dolor-abdominal) | |\n"
      "| [Cefalea](/es/protocolos-clinicos/por-presentacion/cefalea) | |\n"
      "| [Alteración de conciencia](/es/protocolos-clinicos/por-presentacion/alteracion-de-conciencia) | |\n"
      "| [Síncope](/es/protocolos-clinicos/por-presentacion/sincope) | |\n"
      "| [Fiebre sin foco](/es/protocolos-clinicos/por-presentacion/fiebre-sin-foco) | |\n"
      "| [Trauma](/es/protocolos-clinicos/por-presentacion/trauma) | |\n"
      "| [Crisis hipertensiva](/es/protocolos-clinicos/por-presentacion/crisis-hipertensiva) | |\n"),
    p("protocolos-clinicos/por-presentacion/dolor-toracico", "Dolor Torácico", "Protocolo de evaluación y manejo del dolor torácico"),
    p("protocolos-clinicos/por-presentacion/disnea", "Disnea", "Protocolo de evaluación y manejo de la disnea"),
    p("protocolos-clinicos/por-presentacion/dolor-abdominal", "Dolor Abdominal", "Protocolo de evaluación y manejo del dolor abdominal"),
    p("protocolos-clinicos/por-presentacion/cefalea", "Cefalea", "Protocolo de evaluación y manejo de la cefalea"),
    p("protocolos-clinicos/por-presentacion/alteracion-de-conciencia", "Alteración de Conciencia", "Evaluación del paciente con alteración de conciencia"),
    p("protocolos-clinicos/por-presentacion/sincope", "Síncope", "Protocolo de evaluación del síncope"),
    p("protocolos-clinicos/por-presentacion/fiebre-sin-foco", "Fiebre sin Foco", "Evaluación de la fiebre sin foco aparente"),
    p("protocolos-clinicos/por-presentacion/trauma", "Trauma", "Evaluación primaria y secundaria del trauma"),
    p("protocolos-clinicos/por-presentacion/crisis-hipertensiva", "Crisis Hipertensiva", "Urgencia y emergencia hipertensiva"),
    p("protocolos-clinicos/por-patologia", "Por Patología", "Protocolos organizados por diagnóstico",
      "# Por Patología\n\n"
      "| Área | |\n|---|---|\n"
      "| [Cardiovascular](/es/protocolos-clinicos/por-patologia/cardiovascular) | SCA, arritmias, ICC, TEP |\n"
      "| [Respiratorio](/es/protocolos-clinicos/por-patologia/respiratorio) | NAC, EPOC, asma, neumotórax |\n"
      "| [Neurológico](/es/protocolos-clinicos/por-patologia/neurologico) | ACV, epilepsia, meningitis |\n"
      "| [Traumatología](/es/protocolos-clinicos/por-patologia/traumatologia) | Politrauma, TCE, fracturas |\n"
      "| [Digestivo](/es/protocolos-clinicos/por-patologia/digestivo) | HDA, pancreatitis, abdomen agudo |\n"
      "| [Renal y Metabólico](/es/protocolos-clinicos/por-patologia/renal-y-metabolico) | IRA, DKA, hipoglicemia |\n"
      "| [Infectología](/es/protocolos-clinicos/por-patologia/infectologia) | Sepsis, bacteriemia, ITU |\n"
      "| [Gineco-Obstetricia](/es/protocolos-clinicos/por-patologia/gineco-obstetricia) | Ectópico, metrorragia, preeclampsia |\n"
      "| [Pediatría](/es/protocolos-clinicos/por-patologia/pediatria) | Fiebre, crisis febril, bronquiolitis |\n"
      "| [Toxicología](/es/protocolos-clinicos/por-patologia/toxicologia) | Fármacos, OH, CO, organofosforados |\n"
      "| [Psiquiatría](/es/protocolos-clinicos/por-patologia/psiquiatria) | Agitación, ideación suicida |\n"
      "| [Procedimientos](/es/protocolos-clinicos/por-patologia/procedimientos) | Intubación, accesos vasculares |\n"),
    p("protocolos-clinicos/por-patologia/cardiovascular", "Cardiovascular", "SCA, arritmias, ICC descompensada, TEP"),
    p("protocolos-clinicos/por-patologia/respiratorio", "Respiratorio", "NAC, EPOC, crisis asmática, neumotórax"),
    p("protocolos-clinicos/por-patologia/neurologico", "Neurológico", "ACV, crisis epiléptica, meningitis"),
    p("protocolos-clinicos/por-patologia/traumatologia", "Traumatología", "Politrauma, TCE, fracturas específicas"),
    p("protocolos-clinicos/por-patologia/digestivo", "Digestivo", "HDA, cólico biliar, pancreatitis, abdomen agudo"),
    p("protocolos-clinicos/por-patologia/renal-y-metabolico", "Renal y Metabólico", "IRA, DKA, hipoglicemia, diselectrolitemias"),
    p("protocolos-clinicos/por-patologia/infectologia", "Infectología", "Sepsis, bacteriemia, ITU complicada"),
    p("protocolos-clinicos/por-patologia/gineco-obstetricia", "Gineco-Obstetricia", "Embarazo ectópico, metrorragia, preeclampsia"),
    p("protocolos-clinicos/por-patologia/pediatria", "Pediatría", "Fiebre pediátrica, crisis febril, bronquiolitis"),
    p("protocolos-clinicos/por-patologia/toxicologia", "Toxicología e Intoxicaciones", "Fármacos, alcohol, CO, organofosforados"),
    p("protocolos-clinicos/por-patologia/psiquiatria", "Psiquiatría", "Agitación psicomotora, ideación suicida"),
    p("protocolos-clinicos/por-patologia/procedimientos", "Procedimientos", "Intubación, acceso vascular, toracocentesis"),

    # ── Calculadoras ──────────────────────────────────────────────────────────
    p("calculadoras", "Calculadoras Clínicas", "Herramientas interactivas con indicaciones clínicas",
      "# Calculadoras Clínicas\n\n"
      "Herramientas interactivas que generan indicaciones listas para usar.\n\n"
      "| Calculadora | Descripción |\n|---|---|\n"
      "| [Analgesia y Sedación](/es/calculadoras/analgesia-y-sedacion) | Dosis según peso, EVA y alergias |\n"
      "| [Antibióticos](/es/calculadoras/antibioticos) | Selección y dosificación según foco |\n"
      "| [Fluidoterapia](/es/calculadoras/fluidoterapia) | Esquemas de reposición de volumen |\n"
      "| [Cardiovascular](/es/calculadoras/cardiovascular) | HEART, Wells TVP/TEP, antiarrítmicos |\n"
      "| [Neurológico](/es/calculadoras/neurologico) | Glasgow, NIHSS, trombolisis ACV |\n"
      "| [Severidad](/es/calculadoras/severidad) | qSOFA/SOFA, NEWS2, criterios UCI |\n"
      "| [Pediatría](/es/calculadoras/pediatria) | Peso Broselow, dosis pediátricas |\n"
      "| [Obstetricia](/es/calculadoras/obstetricia) | Edad gestacional, Bishop, SBAR |\n"),
    p("calculadoras/analgesia-y-sedacion", "Analgesia y Sedación", "Dosis según peso, EVA y alergias"),
    p("calculadoras/antibioticos", "Antibióticos", "Selección y dosificación según foco infeccioso"),
    p("calculadoras/fluidoterapia", "Fluidoterapia", "Esquemas de reposición de volumen"),
    p("calculadoras/cardiovascular", "Cardiovascular", "HEART score, Wells TVP/TEP, antiarrítmicos"),
    p("calculadoras/neurologico", "Neurológico", "Glasgow, NIHSS, criterios de trombolisis en ACV"),
    p("calculadoras/severidad", "Severidad", "qSOFA, SOFA, NEWS2, criterios ingreso UCI"),
    p("calculadoras/pediatria", "Pediatría", "Peso Broselow, dosis pediátricas por peso"),
    p("calculadoras/obstetricia", "Obstetricia", "Edad gestacional, Score de Bishop, SBAR obstétrico"),
]

ok = fail = skip = 0
for pg in PAGES:
    path = pg["path"]
    print(f"  {path} ... ", end="", flush=True)
    try:
        r = gql(CREATE, {
            "content":     pg["content"],
            "description": pg["description"],
            "editor":      "markdown",
            "isPrivate":   False,
            "isPublished": True,
            "locale":      "es",
            "path":        path,
            "tags":        [],
            "title":       pg["title"]
        })
        res = (r.get("data") or {}).get("pages", {}).get("create", {}).get("responseResult", {})
        if res.get("succeeded"):
            print("✓"); ok += 1
        else:
            code = res.get("errorCode", "?")
            msg  = res.get("message", "")
            if "already" in msg.lower() or "duplicate" in msg.lower():
                print("skip (ya existe)"); skip += 1
            else:
                print(f"FAIL {code}: {msg}"); fail += 1
    except Exception as e:
        print(f"ERR: {e}"); fail += 1
    time.sleep(0.35)

print(f"\nResultado: {ok} creadas · {skip} ya existían · {fail} fallidas")
