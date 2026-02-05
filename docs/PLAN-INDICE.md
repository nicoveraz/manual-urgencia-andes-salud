# Plan: Índice del Manual de Procedimientos - Servicio de Urgencia

## Resumen

Crear la estructura completa de contenido Markdown (~160 archivos) dentro de `content/` en el repositorio, con página principal, plantilla estándar por procedimiento, e integración de los 4 protocolos existentes. Los archivos se crearán como plantillas con frontmatter y estructura de secciones, listos para completar contenido.

---

## Estructura de Directorios

```
content/
├── home.md                                    # Página principal del manual
│
├── 01-informacion-servicio/                   # SECCIÓN 1
│   ├── index.md
│   ├── 01-descripcion-general.md
│   ├── 02-marco-legal-normativo.md
│   ├── 03-organigrama.md
│   ├── 04-dotacion-personal.md
│   ├── 05-infraestructura/
│   │   ├── index.md
│   │   ├── 01-plano-general.md
│   │   ├── 02-areas-funcionales.md
│   │   ├── 03-sala-reanimacion.md
│   │   ├── 04-boxes-atencion.md
│   │   ├── 05-sala-procedimientos.md
│   │   ├── 06-sala-observacion.md
│   │   └── 07-area-espera.md
│   ├── 06-equipamiento/
│   │   ├── index.md
│   │   ├── 01-equipamiento-critico.md
│   │   ├── 02-botiquin-urgencia.md
│   │   ├── 03-botiquin-reanimacion.md
│   │   ├── 04-carro-paro.md
│   │   ├── 05-carro-paro-pediatrico.md
│   │   ├── 06-insumos-farmacia.md
│   │   └── 07-mantenimiento-equipos.md
│   └── 07-sistemas-informaticos/
│       ├── index.md
│       ├── 01-andesmed.md
│       ├── 02-gestion-camas.md
│       ├── 03-imagenologia-laboratorio.md
│       └── 04-registro-clinico-electronico.md
│
├── 02-procedimientos-administrativos/         # SECCIÓN 2
│   ├── index.md
│   ├── 01-flujo-paciente/
│   │   ├── index.md
│   │   ├── 01-ingreso-admision.md
│   │   ├── 02-triage/
│   │   │   ├── index.md
│   │   │   ├── 01-protocolo-triage.md
│   │   │   ├── 02-categorias-triage.md
│   │   │   ├── 03-reevaluacion-triage.md
│   │   │   ├── 04-triage-pediatrico.md
│   │   │   └── 05-triage-obstetrico.md
│   │   ├── 03-asignacion-box.md
│   │   ├── 04-interconsultas.md
│   │   ├── 05-derivaciones/
│   │   │   ├── index.md
│   │   │   ├── 01-derivacion-interna.md
│   │   │   ├── 02-derivacion-externa.md
│   │   │   └── 03-derivacion-ges-auge.md
│   │   └── 06-alta-paciente/
│   │       ├── index.md
│   │       ├── 01-alta-medica.md
│   │       ├── 02-alta-administrativa.md
│   │       ├── 03-alta-voluntaria.md
│   │       └── 04-alta-por-fallecimiento.md
│   ├── 02-gestion-camas/
│   │   ├── index.md
│   │   ├── 01-capacidad-instalada.md
│   │   ├── 02-sistema-gestion-camas.md
│   │   ├── 03-protocolo-sobredemanda.md
│   │   └── 04-criterios-observacion.md
│   ├── 03-turnos-personal/
│   │   ├── index.md
│   │   ├── 01-rotativa-medicos-urgencia.md
│   │   ├── 02-turnos-especialidades/
│   │   │   ├── index.md
│   │   │   ├── 01-cirugia-general.md
│   │   │   ├── 02-cirugia-tmt-infantil.md
│   │   │   ├── 03-anestesia.md
│   │   │   ├── 04-ginecologia.md
│   │   │   ├── 05-traumatologia.md
│   │   │   ├── 06-neurocirugia.md
│   │   │   ├── 07-neurologia.md
│   │   │   ├── 08-nefrologia.md
│   │   │   ├── 09-urologia.md
│   │   │   ├── 10-endoscopia.md
│   │   │   ├── 11-hemodinamia.md
│   │   │   ├── 12-maxilofacial.md
│   │   │   └── 13-tmt-mutual.md
│   │   ├── 03-cobertura-ausencias.md
│   │   └── 04-entrega-turno.md
│   ├── 04-registro-documentacion/
│   │   ├── index.md
│   │   ├── 01-ficha-clinica.md
│   │   ├── 02-consentimiento-informado.md
│   │   ├── 03-certificados-licencias.md
│   │   ├── 04-notificacion-obligatoria.md
│   │   └── 05-evento-centinela.md
│   ├── 05-farmacia-urgencia/
│   │   ├── index.md
│   │   ├── 01-dispensacion-medicamentos.md
│   │   ├── 02-medicamentos-controlados.md
│   │   ├── 03-cadena-frio.md
│   │   └── 04-receta-retenida.md
│   └── 06-convenios-seguros/
│       ├── index.md
│       ├── 01-isapres-fonasa.md
│       ├── 02-mutual-seguridad.md
│       ├── 03-seguros-complementarios.md
│       └── 04-ley-urgencia.md
│
├── 03-procedimientos-clinicos/                # SECCIÓN 3
│   ├── index.md
│   ├── 01-evaluacion-inicial/
│   │   ├── index.md
│   │   ├── 01-abcde.md
│   │   ├── 02-historia-clinica-urgencia.md
│   │   ├── 03-examen-fisico-dirigido.md
│   │   ├── 04-solicitud-examenes.md
│   │   └── 05-escalas-scores/
│   │       ├── index.md
│   │       ├── 01-glasgow.md
│   │       ├── 02-news.md
│   │       ├── 03-sofa-qsofa.md
│   │       ├── 04-nihss.md
│   │       ├── 05-wells.md
│   │       ├── 06-curb65.md
│   │       ├── 07-heart-score.md
│   │       └── 08-escala-dolor.md
│   ├── 02-emergencias-cardiovasculares/
│   │   ├── index.md
│   │   ├── 01-paro-cardiorrespiratorio/
│   │   │   ├── index.md
│   │   │   ├── 01-acls-adulto.md              ← Ref: ACLS_Supplementary_Material.pdf
│   │   │   ├── 02-bls-adulto.md
│   │   │   ├── 03-ritmos-desfibrilables.md
│   │   │   ├── 04-ritmos-no-desfibrilables.md
│   │   │   ├── 05-cuidados-post-paro.md
│   │   │   └── 06-acls-pediatrico.md
│   │   ├── 02-sindrome-coronario-agudo.md
│   │   ├── 03-insuficiencia-cardiaca-aguda.md
│   │   ├── 04-arritmias.md
│   │   ├── 05-crisis-hipertensiva.md
│   │   ├── 06-diseccion-aortica.md
│   │   └── 07-tromboembolismo-pulmonar.md
│   ├── 03-emergencias-respiratorias/
│   │   ├── index.md
│   │   ├── 01-insuficiencia-respiratoria.md
│   │   ├── 02-crisis-asmatica.md
│   │   ├── 03-epoc-exacerbado.md
│   │   ├── 04-neumotorax.md
│   │   └── 05-manejo-via-aerea/
│   │       ├── index.md
│   │       ├── 01-secuencia-rapida-intubacion.md
│   │       ├── 02-via-aerea-dificil.md
│   │       ├── 03-cricotirotomia.md
│   │       └── 04-ventilacion-mecanica-urgencia.md
│   ├── 04-emergencias-neurologicas/
│   │   ├── index.md
│   │   ├── 01-acv-isquemico.md
│   │   ├── 02-acv-hemorragico.md
│   │   ├── 03-convulsiones-status.md
│   │   ├── 04-cefalea-aguda.md
│   │   ├── 05-sindrome-confusional.md
│   │   └── 06-meningitis.md
│   ├── 05-emergencias-traumatologicas/
│   │   ├── index.md
│   │   ├── 01-politraumatizado.md
│   │   ├── 02-tec.md
│   │   ├── 03-trauma-toracico.md
│   │   ├── 04-trauma-abdominal.md
│   │   ├── 05-fracturas-luxaciones.md
│   │   ├── 06-heridas-suturas.md
│   │   └── 07-quemaduras.md
│   ├── 06-emergencias-abdominales/
│   │   ├── index.md
│   │   ├── 01-abdomen-agudo.md
│   │   ├── 02-apendicitis.md
│   │   ├── 03-colecistitis.md
│   │   ├── 04-pancreatitis.md
│   │   ├── 05-hemorragia-digestiva.md
│   │   └── 06-obstruccion-intestinal.md
│   ├── 07-emergencias-metabolicas-toxicologicas/
│   │   ├── index.md
│   │   ├── 01-cetoacidosis-diabetica.md
│   │   ├── 02-estado-hiperosmolar.md
│   │   ├── 03-hipoglicemia.md
│   │   ├── 04-alteraciones-electroliticas.md
│   │   ├── 05-intoxicaciones/
│   │   │   ├── index.md
│   │   │   ├── 01-enfoque-general.md
│   │   │   ├── 02-intoxicacion-medicamentosa.md
│   │   │   ├── 03-intoxicacion-oh.md
│   │   │   ├── 04-intoxicacion-drogas.md
│   │   │   └── 05-intoxicacion-organofosforados.md
│   │   └── 06-anafilaxia.md
│   ├── 08-emergencias-pediatricas/
│   │   ├── index.md
│   │   ├── 01-triage-pediatrico.md
│   │   ├── 02-fiebre-pediatrica.md
│   │   ├── 03-bronquiolitis.md
│   │   ├── 04-laringitis-croup.md
│   │   ├── 05-crisis-asmatica-pediatrica.md
│   │   ├── 06-deshidratacion-pediatrica.md
│   │   ├── 07-convulsiones-pediatricas.md
│   │   ├── 08-dolor-abdominal-pediatrico.md
│   │   ├── 09-trauma-pediatrico.md
│   │   ├── 10-rcp-pediatrico-neonatal.md
│   │   └── 11-protocolo-pediatrico-urgencia.md  ← Ref: PROTOCOLO PEDIATRICO
│   ├── 09-emergencias-gineco-obstetricas/
│   │   ├── index.md
│   │   ├── 01-embarazo-ectopico.md
│   │   ├── 02-aborto.md
│   │   ├── 03-hemorragia-obstetrica.md
│   │   ├── 04-preeclampsia-eclampsia.md
│   │   └── 05-parto-inminente.md
│   ├── 10-procedimientos-invasivos/
│   │   ├── index.md
│   │   ├── 01-acceso-venoso-periferico.md
│   │   ├── 02-acceso-venoso-central.md
│   │   ├── 03-acceso-intraoseo.md
│   │   ├── 04-puncion-lumbar.md
│   │   ├── 05-toracocentesis.md
│   │   ├── 06-paracentesis.md
│   │   ├── 07-lavado-gastrico.md
│   │   ├── 08-sonda-nasogastrica.md
│   │   ├── 09-sonda-foley.md
│   │   ├── 10-reduccion-fracturas-luxaciones.md
│   │   └── 11-sedacion-procedural.md
│   ├── 11-atencion-situaciones-especiales/
│   │   ├── index.md
│   │   ├── 01-paciente-tea.md                   ← Ref: ATENCION PACIENTE TEA
│   │   ├── 02-paciente-psiquiatrico.md
│   │   ├── 03-violencia-intrafamiliar.md
│   │   ├── 04-abuso-sexual.md
│   │   ├── 05-maltrato-infantil.md
│   │   ├── 06-paciente-geriatrico.md
│   │   ├── 07-paciente-embarazada.md
│   │   └── 08-paciente-inmunosuprimido.md
│   └── 12-farmacologia-urgencia/
│       ├── index.md
│       ├── 01-drogas-reanimacion.md
│       ├── 02-analgesicos-antipireticos.md
│       ├── 03-sedacion-analgesia.md
│       ├── 04-antibioticos-urgencia.md
│       ├── 05-anticoagulantes-trombolisis.md
│       ├── 06-vasoactivos.md
│       ├── 07-broncodilatadores.md
│       ├── 08-antidotos.md
│       └── 09-dosis-pediatricas.md
│
├── 04-calidad-seguridad/                      # SECCIÓN 4
│   ├── index.md
│   ├── 01-indicadores-calidad.md
│   ├── 02-eventos-adversos.md
│   ├── 03-prevencion-iaas.md
│   ├── 04-higiene-manos.md
│   ├── 05-identificacion-paciente.md
│   ├── 06-seguridad-medicamentos.md
│   ├── 07-prevencion-caidas.md
│   ├── 08-manejo-residuos.md
│   ├── 09-protocolo-codigo-azul.md
│   ├── 10-protocolo-incendio-evacuacion.md
│   └── 11-acreditacion/
│       ├── index.md
│       ├── 01-estandares-superintendencia.md
│       └── 02-norma-tecnica-232.md              ← Ref: NORMA TÉCNICA 232
│
├── 05-anexos/                                 # SECCIÓN 5
│   ├── index.md
│   ├── 01-glosario.md
│   ├── 02-telefonos-contacto.md
│   ├── 03-protocolos-referencia/
│   │   ├── index.md
│   │   ├── 01-acls-material-soporte.md
│   │   ├── 02-norma-tecnica-232.md
│   │   ├── 03-protocolo-pediatrico.md
│   │   └── 04-protocolo-tea.md
│   ├── 04-flujogramas/
│   │   ├── index.md
│   │   ├── 01-flujo-ingreso-alta.md
│   │   ├── 02-flujo-triage.md
│   │   ├── 03-flujo-codigo-azul.md
│   │   └── 04-flujo-trauma.md
│   ├── 05-formularios-plantillas/
│   │   ├── index.md
│   │   ├── 01-checklist-carro-paro.md
│   │   ├── 02-checklist-turno.md
│   │   ├── 03-formulario-evento-adverso.md
│   │   └── 04-consentimientos.md
│   └── 06-control-versiones.md
│
└── assets/
    └── protocolos-originales/                 # PDFs originales
        ├── acls-supplementary-material.pdf
        ├── atencion-paciente-tea-urgencia.pdf
        ├── protocolo-pediatrico-urgencia.pdf
        └── norma-tecnica-232-decreto-21-ssp-2023.pdf
```

**Total: ~160 archivos Markdown**

---

## Plantilla Estándar por Procedimiento

Cada archivo .md usará esta estructura consistente:

```markdown
---
title: [Nombre del Procedimiento]
description: [Descripción breve]
published: true
tags: [sección, tipo, especialidad]
editor: markdown
---

# [Nombre del Procedimiento]

> **Código:** [SU-SEC-NNN]  |  **Versión:** 1.0
> **Vigencia:** DD/MM/AAAA  |  **Próxima revisión:** DD/MM/AAAA
> **Elaborado por:**  |  **Aprobado por:**

---

## 1. Objetivo
<!-- Propósito del procedimiento -->

## 2. Alcance
<!-- A quién aplica: médicos, enfermeros, TENS -->

## 3. Definiciones
| Término | Definición |
|---------|-----------|

## 4. Responsabilidades
| Rol | Responsabilidad |
|-----|----------------|

## 5. Materiales / Equipamiento
-

## 6. Descripción del Procedimiento
### 6.1. [Paso 1]
### 6.2. [Paso 2]

## 7. Flujograma
<!-- Diagrama Mermaid -->

## 8. Indicadores
| Indicador | Meta | Medición |
|-----------|------|----------|

## 9. Referencias

## 10. Historial de Cambios
| Versión | Fecha | Cambio | Autor |
|---------|-------|--------|-------|
| 1.0 | | Creación | |
```

**Códigos de procedimiento:** `SU-INF-NNN` (Información), `SU-ADM-NNN` (Administrativos), `SU-CLI-NNN` (Clínicos), `SU-CAL-NNN` (Calidad), `SU-ANX-NNN` (Anexos)

---

## Integración de Protocolos Existentes

Los 4 PDFs se copian a `content/assets/protocolos-originales/` y se referencian así:

| Protocolo original | Resumen en Anexos | Referencia en sección clínica |
|---|---|---|
| ACLS_Supplementary_Material.pdf | `05-anexos/03-protocolos-referencia/01-acls-material-soporte.md` | `03-procedimientos-clinicos/02-.../01-paro-cardiorrespiratorio/01-acls-adulto.md` |
| ATENCION PACIENTE TEA | `05-anexos/03-protocolos-referencia/04-protocolo-tea.md` | `03-procedimientos-clinicos/11-.../01-paciente-tea.md` |
| PROTOCOLO PEDIATRICO | `05-anexos/03-protocolos-referencia/03-protocolo-pediatrico.md` | `03-procedimientos-clinicos/08-.../11-protocolo-pediatrico-urgencia.md` |
| Norma Técnica 232 | `05-anexos/03-protocolos-referencia/02-norma-tecnica-232.md` | `01-informacion-servicio/02-marco-legal-normativo.md` y `04-calidad-seguridad/11-acreditacion/02-norma-tecnica-232.md` |

Cada procedimiento que referencia un protocolo incluirá link al resumen y al PDF original.
