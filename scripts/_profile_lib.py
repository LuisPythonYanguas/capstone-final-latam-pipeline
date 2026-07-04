"""
Shared logic for the country-profiler agent (Phase 2.5).

profile_country(name) reads data/latam_finanzas_clean.csv, filters to one
country, and returns a Markdown section string matching the agent spec.
Each scripts/country_<name>.py is a thin wrapper that calls this.
"""

import pandas as pd

CLEAN = "data/latam_finanzas_clean.csv"

GASTO_COLS = [
    ("gasto_vivienda_usd", "Vivienda / Housing"),
    ("gasto_alimentacion_usd", "Alimentación / Food"),
    ("gasto_transporte_usd", "Transporte / Transport"),
    ("gasto_entretenimiento_usd", "Entretenimiento / Entertainment"),
    ("gasto_educacion_usd", "Educación / Education"),
    ("gasto_salud_usd", "Salud / Healthcare"),
]


def profile_country(name: str) -> str:
    df = pd.read_csv(CLEAN)
    c = df[df["pais"] == name]
    if c.empty:
        raise ValueError(f"No rows found for country '{name}'")

    inc = c["ingreso_mensual_usd"]
    lines = []
    lines.append(f"## País: {name}\n")

    # 1. Sample size and age range
    lines.append(f"- **Sample size:** {len(c)} respondents")
    lines.append(f"- **Age range:** {int(c['edad'].min())}–{int(c['edad'].max())} "
                 f"(mean {c['edad'].mean():.1f})\n")

    # 2. Income
    lines.append("**Income (USD/month)**\n")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Median | ${inc.median():,.0f} |")
    lines.append(f"| Mean | ${inc.mean():,.0f} |")
    lines.append(f"| Min | ${inc.min():,.0f} |")
    lines.append(f"| Max | ${inc.max():,.0f} |")
    lines.append(f"| Std. dev. | ${inc.std():,.0f} |\n")

    # 3. Housing burden
    housing_burden = (c["gasto_vivienda_usd"] / inc * 100).mean()
    lines.append(f"**Housing burden:** average housing cost is "
                 f"**{housing_burden:.1f}%** of income.\n")

    # 4. Spending breakdown (avg % of income per category)
    lines.append("**Spending breakdown (avg % of income)**\n")
    lines.append("| Category | % of income |")
    lines.append("|---|---|")
    breakdown = []
    for col, label in GASTO_COLS:
        pct = (c[col] / inc * 100).mean()
        breakdown.append((label, pct))
    for label, pct in sorted(breakdown, key=lambda x: x[1], reverse=True):
        lines.append(f"| {label} | {pct:.1f}% |")
    lines.append("")

    # 5. Savings
    avg_savings = c["ahorro_mensual_usd"].mean()
    pct_negative = c["ahorro_negativo"].mean() * 100
    lines.append(f"**Savings:** average monthly savings **${avg_savings:,.0f}**; "
                 f"**{pct_negative:.1f}%** of respondents have negative savings.\n")

    # 6. AI tools
    avg_ai = c["horas_herramientas_ia_semana"].mean()
    avg_sat = c["satisfaccion_financiera"].mean()
    lines.append(f"**AI tools:** average **{avg_ai:.1f}** hours/week using AI tools; "
                 f"average financial satisfaction **{avg_sat:.2f} / 5**.\n")

    return "\n".join(lines)
