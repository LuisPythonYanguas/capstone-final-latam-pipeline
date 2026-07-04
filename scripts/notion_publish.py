"""
Notion publisher for the Análisis LatAm 2025 pipeline.

Populates the board-facing Notion workspace via the Notion API:
  - "Country Profiles" database  -> 6 country entries
  - "Findings Tracker" database  -> 6 findings, each with its own linked page
  - "Informe Ejecutivo" page     -> the executive report content

This is the reproducible, scriptable counterpart to the /publish-finding skill.
It adapts to databases whether you created them by hand (per the assignment) or
let the script create them under a parent page.

USAGE (PowerShell):
  $env:NOTION_API_KEY = "secret_xxx"            # required (integration key)
  $env:NOTION_PARENT_PAGE_ID = "xxxxxxxx"       # optional: create DBs/page here if missing
  $env:GITHUB_RAW_BASE = "https://raw.githubusercontent.com/<user>/<repo>/main"  # optional: chart images
  venv/Scripts/python.exe scripts/notion_publish.py

The script never hard-codes your key. Nothing secret is committed.
"""

import os
import sys
import json
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _profile_lib import profile_country  # noqa: E402  (reuse Phase 2.5 logic)
import pandas as pd  # noqa: E402

API = "https://api.notion.com/v1"
VERSION = "2022-06-28"

KEY = os.environ.get("NOTION_API_KEY")
PARENT = os.environ.get("NOTION_PARENT_PAGE_ID")
RAW_BASE = os.environ.get("GITHUB_RAW_BASE", "").rstrip("/")

if not KEY:
    sys.exit("ERROR: set NOTION_API_KEY (your Notion integration key) first.")

H = {
    "Authorization": f"Bearer {KEY}",
    "Notion-Version": VERSION,
    "Content-Type": "application/json",
}

CLEAN = "data/latam_finanzas_clean.csv"
COUNTRIES = ["México", "Colombia", "Argentina", "Chile", "Perú", "Brasil"]

# ---------------------------------------------------------------------------
# Findings (Phase 3 stats + Phase 5 /interpret output)
# ---------------------------------------------------------------------------
FINDINGS = [
    {
        "n": 1,
        "titulo": "Comparación de ingresos por país",
        "estadistica": "Brasil lidera con ingreso mediano de $1,458 USD/mes vs. $798 en Argentina (brecha del 83%).",
        "alcance": "Muestra completa (6 países)",
        "prioridad": "Alta",
        "interpretacion": (
            "El ingreso mensual mediano varía un 83% entre países, desde $1,458 USD en "
            "Brasil hasta $798 USD en Argentina. Esta brecha implica que un programa único "
            "para toda la región resultaría irreal para los participantes de menores ingresos, "
            "especialmente en Argentina, Perú y Colombia. Recomendamos definir metas de ahorro "
            "relativas al ingreso en lugar de montos fijos, y priorizar los mercados de menor "
            "ingreso para el contenido de presupuesto básico."
        ),
        "proximos_pasos": (
            "Definir metas de ahorro relativas al ingreso (ej. 10% del ingreso) y priorizar "
            "Argentina, Perú y Colombia para el contenido de presupuesto básico."
        ),
    },
    {
        "n": 2,
        "titulo": "Edad y tasa de ahorro",
        "estadistica": "La tasa de ahorro sube de 5.7% (18-22) a 15.5% (29-32); Pearson r = 0.41.",
        "alcance": "Jóvenes de 18-25 años",
        "prioridad": "Alta",
        "interpretacion": (
            "La tasa de ahorro casi se triplica con la edad, pasando del 5.7% del ingreso "
            "entre los 18-22 años al 15.5% entre los 29-32 años (r = 0.41, p < 0.001). Esto "
            "señala que el grupo de 18-25 años —el segmento más numeroso de la muestra— es el "
            "más vulnerable financieramente y donde una intervención temprana tiene mayor "
            "impacto. Recomendamos lanzar un módulo de 'primer hábito de ahorro' dirigido a "
            "menores de 25 años, antes de que los gastos fijos reduzcan su margen."
        ),
        "proximos_pasos": (
            "Lanzar un módulo de 'primer hábito de ahorro' dirigido a menores de 25 años."
        ),
    },
    {
        "n": 3,
        "titulo": "Distribución del gasto",
        "estadistica": "Vivienda 28.5% + alimentación 23.8% = 52% del ingreso; gasto total 84.5%.",
        "alcance": "Muestra completa",
        "prioridad": "Media",
        "interpretacion": (
            "En promedio, la vivienda (28.5%) y la alimentación (23.8%) consumen el 52% del "
            "ingreso, y el gasto total alcanza el 84.5%, dejando un margen mínimo para el "
            "ahorro. Como estos dos rubros esenciales dominan el presupuesto, el contenido "
            "sobre 'pequeños gastos' tiene poco efecto frente a las decisiones estructurales "
            "de vivienda y alimentación. Recomendamos priorizar contenido sobre decisiones de "
            "vivienda y presupuesto de alimentación, donde una reducción de 2-3 puntos casi "
            "duplica la tasa de ahorro típica."
        ),
        "proximos_pasos": (
            "Priorizar contenido de decisiones de vivienda (renta ≤30%) y presupuesto de "
            "alimentación."
        ),
    },
    {
        "n": 4,
        "titulo": "Tarjetahabientes vs. no tarjetahabientes",
        "estadistica": "+16% alimentación y +17% entretenimiento con ingreso casi igual (+1.5%).",
        "alcance": "Muestra completa",
        "prioridad": "Media",
        "interpretacion": (
            "Con ingresos casi idénticos (+1.5%), quienes tienen tarjeta de crédito gastan 16% "
            "más en alimentación y 17% más en entretenimiento que quienes no la tienen. Esto "
            "indica que el gasto adicional no proviene de mayores ingresos sino del acceso al "
            "crédito, un riesgo para toda la muestra pero sobre todo para los usuarios más "
            "jóvenes con menor colchón de ahorro. Recomendamos acompañar cualquier contenido "
            "de 'acceso al crédito' con un módulo de uso responsable enfocado en categorías "
            "discrecionales como comidas fuera y entretenimiento."
        ),
        "proximos_pasos": (
            "Añadir un módulo de uso responsable del crédito enfocado en gasto discrecional."
        ),
    },
    {
        "n": 5,
        "titulo": "Uso de IA y satisfacción financiera",
        "estadistica": "Satisfacción 2.05 (bajo) vs. 3.43 (alto), r = 0.57; ingreso $747 vs. $1,750 (confundido).",
        "alcance": "Muestra completa",
        "prioridad": "Baja",
        "interpretacion": (
            "La satisfacción financiera aumenta con el uso de herramientas de IA (r = 0.57): "
            "de 2.05 en usuarios bajos (0-3 h/semana) a 3.43 en usuarios altos (11+ h/semana). "
            "Sin embargo, esta relación está confundida por el ingreso —los usuarios intensivos "
            "ganan más del doble ($1,750 vs. $747)— por lo que la IA es un marcador de "
            "profesionales de mayores ingresos, no una causa directa del bienestar financiero. "
            "Recomendamos ofrecer la alfabetización digital y de IA como habilidad de "
            "empleabilidad, sin prometer que 'usar IA' mejore las finanzas por sí solo."
        ),
        "proximos_pasos": (
            "Ofrecer alfabetización digital/IA como habilidad de empleabilidad, sin prometer "
            "mejora financiera directa."
        ),
    },
    {
        "n": 6,
        "titulo": "Carga de vivienda por país",
        "estadistica": "Argentina 34.1% y Chile 32.6% del ingreso en vivienda; Perú 24.6% (el más bajo).",
        "alcance": "Argentina y Chile",
        "prioridad": "Alta",
        "interpretacion": (
            "La carga de vivienda es más alta en Argentina (34.1%) y Chile (32.6%) —ambas por "
            "encima del umbral de asequibilidad del 30%— y más baja en Perú (24.6%). Argentina "
            "combina el menor ingreso de la región con la mayor carga de vivienda, una doble "
            "presión sobre la capacidad de ahorro de sus jóvenes profesionales. Recomendamos "
            "incluir un módulo de gestión del costo de vivienda como contenido prioritario en "
            "Argentina y Chile, donde reducir ese gasto es la palanca más efectiva para liberar "
            "capacidad de ahorro."
        ),
        "proximos_pasos": (
            "Incluir un módulo de gestión del costo de vivienda como prioridad en Argentina y Chile."
        ),
    },
]


# ---------------------------------------------------------------------------
# Notion helpers
# ---------------------------------------------------------------------------
def api(method, path, **kw):
    r = requests.request(method, f"{API}{path}", headers=H, timeout=30, **kw)
    if r.status_code >= 300:
        raise RuntimeError(f"{method} {path} -> {r.status_code}: {r.text[:400]}")
    return r.json()


def find_by_title(kind, title):
    """kind = 'database' | 'page'. Returns object id or None."""
    body = {"query": title, "filter": {"property": "object", "value": kind}}
    for res in api("POST", "/search", data=json.dumps(body)).get("results", []):
        if kind == "database":
            t = "".join(x["plain_text"] for x in res.get("title", []))
        else:
            props = res.get("properties", {})
            t = ""
            for p in props.values():
                if p.get("type") == "title":
                    t = "".join(x["plain_text"] for x in p["title"])
        if t.strip().lower() == title.strip().lower():
            return res["id"]
    return None


def create_database(title, properties):
    if not PARENT:
        sys.exit(f"'{title}' not found and NOTION_PARENT_PAGE_ID is not set — "
                 f"either create the database in Notion and share it with the integration, "
                 f"or set NOTION_PARENT_PAGE_ID so the script can create it.")
    body = {
        "parent": {"type": "page_id", "page_id": PARENT},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    }
    return api("POST", "/databases", data=json.dumps(body))["id"]


def get_db_schema(db_id):
    return api("GET", f"/databases/{db_id}")["properties"]


def prop_value(schema_entry, value):
    """Format a value for whatever property type the DB actually uses."""
    t = schema_entry["type"]
    s = str(value)
    if t == "title":
        return {"title": [{"text": {"content": s}}]}
    if t == "rich_text":
        return {"rich_text": [{"text": {"content": s}}]}
    if t == "number":
        try:
            return {"number": float(value)}
        except (TypeError, ValueError):
            return {"number": None}
    if t == "select":
        return {"select": {"name": s}}
    if t == "status":
        return {"status": {"name": s}}
    if t == "multi_select":
        return {"multi_select": [{"name": s}]}
    if t == "checkbox":
        return {"checkbox": bool(value)}
    # Fallback: store as rich_text-like note is impossible for other types; skip
    return None


def set_props(db_schema, mapping):
    """mapping: {property_name: value}. Only writes properties present in schema."""
    out = {}
    for name, value in mapping.items():
        if name in db_schema:
            pv = prop_value(db_schema[name], value)
            if pv is not None:
                out[name] = pv
    return out


# Notion block builders
def h2(text):
    return {"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def h3(text):
    return {"object": "block", "type": "heading_3",
            "heading_3": {"rich_text": [{"type": "text", "text": {"content": text}}]}}


def para(text):
    return {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": text[:1900]}}]}}


def callout(text, emoji="📊"):
    return {"object": "block", "type": "callout",
            "callout": {"icon": {"type": "emoji", "emoji": emoji},
                        "rich_text": [{"type": "text", "text": {"content": text[:1900]}}]}}


def image(url):
    return {"object": "block", "type": "image",
            "image": {"type": "external", "external": {"url": url}}}


def append_blocks(page_id, blocks):
    for i in range(0, len(blocks), 90):  # API limit 100 children/request
        api("PATCH", f"/blocks/{page_id}/children",
            data=json.dumps({"children": blocks[i:i + 90]}))


# ---------------------------------------------------------------------------
# Publish steps
# ---------------------------------------------------------------------------
def publish_country_profiles():
    print("\n== Country Profiles ==")
    db = find_by_title("database", "Country Profiles")
    if not db:
        db = create_database("Country Profiles", {
            "País": {"title": {}},
            "Muestra": {"number": {}},
            "Ingreso Mediano": {"number": {}},
            "Carga Vivienda": {"rich_text": {}},
        })
    schema = get_db_schema(db)
    df = pd.read_csv(CLEAN)
    for country in COUNTRIES:
        c = df[df["pais"] == country]
        inc = c["ingreso_mensual_usd"]
        burden = (c["gasto_vivienda_usd"] / inc * 100).mean()
        props = set_props(schema, {
            "País": country,
            "Muestra": len(c),
            "Ingreso Mediano": round(inc.median()),
            "Carga Vivienda": f"{burden:.1f}%",
        })
        api("POST", "/pages",
            data=json.dumps({"parent": {"database_id": db}, "properties": props}))
        print(f"  + {country}: muestra {len(c)}, mediana ${inc.median():,.0f}, vivienda {burden:.1f}%")


def publish_findings():
    print("\n== Findings Tracker ==")
    db = find_by_title("database", "Findings Tracker")
    if not db:
        db = create_database("Findings Tracker", {
            "Título": {"title": {}},
            "Estadística Clave": {"rich_text": {}},
            "Alcance": {"rich_text": {}},
            "Prioridad": {"select": {"options": [
                {"name": "Alta"}, {"name": "Media"}, {"name": "Baja"}]}},
            "Publicado": {"checkbox": {}},
        })
    schema = get_db_schema(db)
    for f in FINDINGS:
        props = set_props(schema, {
            "Título": f"Hallazgo {f['n']}: {f['titulo']}",
            "Estadística Clave": f["estadistica"],
            "Alcance": f["alcance"],
            "Prioridad": f["prioridad"],
            "Publicado": True,
        })
        children = [
            callout(f["estadistica"], "📊"),
            para(f["interpretacion"]),
            h3("Próximos pasos"),
            para(f["proximos_pasos"]),
        ]
        page = api("POST", "/pages", data=json.dumps({
            "parent": {"database_id": db}, "properties": props, "children": children,
        }))
        print(f"  + Hallazgo {f['n']}: {f['titulo']} [{f['prioridad']}] -> {page.get('url','')}")


def publish_report():
    print("\n== Informe Ejecutivo ==")
    page_id = find_by_title("page", "Informe Ejecutivo")
    if not page_id:
        if not PARENT:
            print("  (skipped: 'Informe Ejecutivo' page not found and no NOTION_PARENT_PAGE_ID)")
            return
        page_id = api("POST", "/pages", data=json.dumps({
            "parent": {"type": "page_id", "page_id": PARENT},
            "properties": {"title": [{"text": {"content": "Informe Ejecutivo"}}]},
        }))["id"]

    blocks = [
        h2("Datos que Hablan — Informe Ejecutivo, Futuro Digital LatAm 2025"),
        para("Bienestar Financiero de Jóvenes Profesionales en América Latina. "
             "Encuesta 2025: 500 encuestados, 6 países, edades 18-32."),
        h2("Resumen Ejecutivo"),
        para("El ingreso mediano varía 83% entre Brasil ($1,458) y Argentina ($798). "
             "El ahorro depende de la edad: 5.7% (18-22) frente a 15.5% (29-32). "
             "Vivienda y alimentación consumen el 52% del ingreso, y en Argentina la vivienda "
             "sola llega al 34%. Recomendaciones prioritarias: (1) un módulo de ahorro temprano "
             "para menores de 25 años y (2) contenido localizado por país, priorizando la carga "
             "de vivienda en Argentina y Chile."),
    ]
    # One section per finding, with chart where available
    chart_map = {
        1: "charts/01_income_by_country.png",
        2: "charts/02_age_vs_savings.png",
        3: "charts/03_spending_breakdown.png",
        4: None,
        5: "charts/04_satisfaction_by_ai_usage.png",
        6: "charts/05_housing_burden_by_country.png",
    }
    blocks.append(h2("Hallazgos"))
    for f in FINDINGS:
        blocks.append(h3(f"Hallazgo {f['n']}: {f['titulo']}"))
        blocks.append(callout(f["estadistica"], "📊"))
        blocks.append(para(f["interpretacion"]))
        chart = chart_map.get(f["n"])
        if chart and RAW_BASE:
            blocks.append(image(f"{RAW_BASE}/{chart}"))
    append_blocks(page_id, blocks)
    print(f"  + Report published to Informe Ejecutivo page (id {page_id})")
    if not RAW_BASE:
        print("  (note: set GITHUB_RAW_BASE to embed chart images from your GitHub repo)")


def main():
    print("Publishing Análisis LatAm 2025 to Notion...")
    publish_country_profiles()
    publish_findings()
    publish_report()
    print("\nDone. Open your Notion workspace to confirm 6 profiles, 6 findings, and the report.")


if __name__ == "__main__":
    main()
