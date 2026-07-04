"""
Phase 3 — Analyse
Six statistical analyses on data/latam_finanzas_clean.csv, printed as tables.
Writes scripts/analysis_results.md so later phases can reuse the numbers.
"""

import sys
import pandas as pd
from scipy import stats

sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)

CLEAN = "data/latam_finanzas_clean.csv"
df = pd.read_csv(CLEAN)

GASTO_COLS = {
    "gasto_vivienda_usd": "Housing",
    "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport",
    "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education",
    "gasto_salud_usd": "Healthcare",
}

out = []  # markdown accumulator


def emit(text=""):
    print(text)
    out.append(text)


def emit_table(df_, floatfmt="{:.2f}"):
    md = df_.to_markdown(floatfmt=floatfmt.replace("{:", "").replace("}", ""))
    print(df_.to_string())
    out.append(md)


def header(n, title):
    line = f"\n{'=' * 70}\n{n}. {title}\n{'=' * 70}"
    print(line)
    out.append(f"\n### {n}. {title}\n")


# ======================================================================
# 1. INCOME BY COUNTRY
# ======================================================================
header(1, "INCOME BY COUNTRY")
income_by_country = (
    df.groupby("pais")["ingreso_mensual_usd"]
    .agg(median="median", mean="mean", min="min", max="max", std="std")
    .sort_values("median", ascending=False)
    .round(0)
)
emit_table(income_by_country, "{:.0f}")
emit(f"\nHighest median: {income_by_country.index[0]} "
     f"(${income_by_country.iloc[0]['median']:,.0f}); "
     f"lowest: {income_by_country.index[-1]} "
     f"(${income_by_country.iloc[-1]['median']:,.0f}).")

# ======================================================================
# 2. AGE VS. SAVINGS
# ======================================================================
header(2, "AGE VS. SAVINGS")
bins = [17, 22, 25, 28, 32]
labels = ["18-22", "23-25", "26-28", "29-32"]
df["grupo_edad"] = pd.cut(df["edad"], bins=bins, labels=labels)
df["tasa_ahorro"] = df["ahorro_mensual_usd"] / df["ingreso_mensual_usd"] * 100

age_savings = (
    df.groupby("grupo_edad", observed=True)
    .agg(
        n=("id", "count"),
        avg_savings_usd=("ahorro_mensual_usd", "mean"),
        avg_savings_rate_pct=("tasa_ahorro", "mean"),
    )
    .round(2)
)
emit_table(age_savings, "{:.2f}")

corr_age_savings, p_age = stats.pearsonr(df["edad"], df["tasa_ahorro"])
emit(f"\nPearson r (age vs. savings rate) = {corr_age_savings:.3f} "
     f"(p = {p_age:.4g})")

# ======================================================================
# 3. SPENDING BREAKDOWN (full sample)
# ======================================================================
header(3, "SPENDING BREAKDOWN (avg % of income)")
spend_rows = []
for col, label in GASTO_COLS.items():
    pct = (df[col] / df["ingreso_mensual_usd"] * 100).mean()
    spend_rows.append({"category": label, "pct_of_income": round(pct, 2)})
spending = (
    pd.DataFrame(spend_rows)
    .sort_values("pct_of_income", ascending=False)
    .set_index("category")
)
emit_table(spending, "{:.2f}")
emit(f"\nTotal expenses as % of income (avg): "
     f"{spending['pct_of_income'].sum():.1f}%")

# ======================================================================
# 4. CREDIT CARD HOLDERS VS NON-HOLDERS
# ======================================================================
header(4, "CREDIT CARD HOLDERS VS NON-HOLDERS")
metrics = {
    "avg_income": "ingreso_mensual_usd",
    "avg_food": "gasto_alimentacion_usd",
    "avg_entertainment": "gasto_entretenimiento_usd",
    "avg_savings": "ahorro_mensual_usd",
}
holders = df[df["tiene_tarjeta_credito"] == "Sí"]
non = df[df["tiene_tarjeta_credito"] == "No"]
cc_rows = []
for label, col in metrics.items():
    h, nh = holders[col].mean(), non[col].mean()
    cc_rows.append({
        "metric": label,
        "has_card": round(h, 2),
        "no_card": round(nh, 2),
        "pct_diff": round((h - nh) / nh * 100, 1),
    })
cc = pd.DataFrame(cc_rows).set_index("metric")
emit(f"Holders: {len(holders)} | Non-holders: {len(non)}\n")
emit_table(cc, "{:.2f}")

# ======================================================================
# 5. AI TOOL USAGE VS FINANCIAL SATISFACTION
# ======================================================================
header(5, "AI TOOL USAGE VS FINANCIAL SATISFACTION")
ai_bins = [-0.1, 3, 10, 100]
ai_labels = ["Low (0-3)", "Medium (4-10)", "High (11+)"]
df["grupo_ia"] = pd.cut(df["horas_herramientas_ia_semana"],
                        bins=ai_bins, labels=ai_labels)
ai_group = (
    df.groupby("grupo_ia", observed=True)
    .agg(
        n=("id", "count"),
        avg_satisfaction=("satisfaccion_financiera", "mean"),
        avg_income=("ingreso_mensual_usd", "mean"),
    )
    .round(2)
)
emit_table(ai_group, "{:.2f}")

corr_ai_sat, p_ai = stats.pearsonr(
    df["horas_herramientas_ia_semana"], df["satisfaccion_financiera"]
)
emit(f"\nPearson r (AI hours vs. satisfaction) = {corr_ai_sat:.3f} "
     f"(p = {p_ai:.4g})")

# ======================================================================
# 6. HOUSING BURDEN BY COUNTRY
# ======================================================================
header(6, "HOUSING BURDEN BY COUNTRY (avg housing as % of income)")
df["housing_burden_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
housing_burden = (
    df.groupby("pais")["housing_burden_pct"]
    .mean()
    .sort_values(ascending=False)
    .round(2)
    .to_frame("avg_housing_pct")
)
emit_table(housing_burden, "{:.2f}")

# ======================================================================
# Save markdown
# ======================================================================
with open("scripts/analysis_results.md", "w", encoding="utf-8") as f:
    f.write("# Phase 3 — Statistical Analysis Results\n")
    f.write("\n".join(out))
    f.write("\n")

print("\n" + "=" * 70)
print("Analysis complete. Results written to scripts/analysis_results.md")
print("=" * 70)
