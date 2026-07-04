"""
Phase 4 — Visualise
Five professional charts saved as PNGs in charts/.

All charts: clear title, labelled axes, professional palette, source note.
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap

sys.stdout.reconfigure(encoding="utf-8")

CLEAN = "data/latam_finanzas_clean.csv"
df = pd.read_csv(CLEAN)

SOURCE = ("Source: Encuesta de Bienestar Financiero LatAm 2025, "
          "Futuro Digital LatAm")

# Professional palette
NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
CORAL = "#e76f51"
GOLD = "#e9c46a"
SLATE = "#6c757d"
COUNTRY_COLORS = {
    "México": "#264653", "Colombia": "#2a9d8f", "Argentina": "#e9c46a",
    "Chile": "#f4a261", "Perú": "#e76f51", "Brasil": "#8ab17d",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 110,
})


def add_source(fig):
    fig.text(0.01, 0.01, SOURCE, fontsize=7.5, color=SLATE, style="italic")


def save(fig, path):
    add_source(fig)
    fig.savefig(path, bbox_inches="tight", dpi=150, facecolor="white")
    plt.close(fig)
    print(f"  saved {path}")


# ----------------------------------------------------------------------
# 1. Income by country — horizontal box plot, sorted by median (highest top)
# ----------------------------------------------------------------------
order = (df.groupby("pais")["ingreso_mensual_usd"].median()
         .sort_values().index.tolist())  # ascending -> highest ends on top
fig, ax = plt.subplots(figsize=(9, 5.5))
data = [df[df["pais"] == c]["ingreso_mensual_usd"].values for c in order]
bp = ax.boxplot(data, orientation="horizontal", patch_artist=True, widths=0.6,
                medianprops=dict(color="black", linewidth=1.5))
for patch, c in zip(bp["boxes"], order):
    patch.set_facecolor(COUNTRY_COLORS.get(c, NAVY))
    patch.set_alpha(0.85)
ax.set_yticklabels(order)
ax.set_xlabel("Monthly income (USD)")
ax.set_ylabel("Country")
ax.set_title("Monthly Income Distribution by Country",
             fontsize=14, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
save(fig, "charts/01_income_by_country.png")

# ----------------------------------------------------------------------
# 2. Age vs. savings — scatter, colour by country, linear trend line
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))
for c in COUNTRY_COLORS:
    sub = df[df["pais"] == c]
    ax.scatter(sub["edad"], sub["ahorro_mensual_usd"],
               s=28, alpha=0.7, color=COUNTRY_COLORS[c], label=c,
               edgecolors="white", linewidths=0.3)
# Trend line
m, b = np.polyfit(df["edad"], df["ahorro_mensual_usd"], 1)
xs = np.array([df["edad"].min(), df["edad"].max()])
ax.plot(xs, m * xs + b, color=NAVY, linewidth=2.2, linestyle="--",
        label=f"Trend (slope ${m:.1f}/yr)")
ax.axhline(0, color=SLATE, linewidth=0.8, alpha=0.6)
ax.set_xlabel("Age (years)")
ax.set_ylabel("Monthly savings (USD)")
ax.set_title("Age vs. Monthly Savings", fontsize=14, fontweight="bold", pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"${y:,.0f}"))
ax.legend(fontsize=8, ncol=2, frameon=False, loc="upper left")
save(fig, "charts/02_age_vs_savings.png")

# ----------------------------------------------------------------------
# 3. Spending breakdown — horizontal bar, avg % of income, sorted desc
# ----------------------------------------------------------------------
gasto_cols = {
    "gasto_vivienda_usd": "Housing", "gasto_alimentacion_usd": "Food",
    "gasto_transporte_usd": "Transport", "gasto_entretenimiento_usd": "Entertainment",
    "gasto_educacion_usd": "Education", "gasto_salud_usd": "Healthcare",
}
pcts = {label: (df[col] / df["ingreso_mensual_usd"] * 100).mean()
        for col, label in gasto_cols.items()}
sp = pd.Series(pcts).sort_values()
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(sp.index, sp.values, color=TEAL, alpha=0.9)
for bar, v in zip(bars, sp.values):
    ax.text(v + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{v:.1f}%", va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("Average % of income")
ax.set_title("Average Spending Breakdown (% of income)",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlim(0, sp.max() * 1.15)
save(fig, "charts/03_spending_breakdown.png")

# ----------------------------------------------------------------------
# 4. Satisfaction by AI usage group — bar chart with value labels
# ----------------------------------------------------------------------
ai_bins = [-0.1, 3, 10, 100]
ai_labels = ["Low\n(0-3 h/wk)", "Medium\n(4-10 h/wk)", "High\n(11+ h/wk)"]
df["grupo_ia"] = pd.cut(df["horas_herramientas_ia_semana"],
                        bins=ai_bins, labels=ai_labels)
sat = df.groupby("grupo_ia", observed=True)["satisfaccion_financiera"].mean()
counts = df.groupby("grupo_ia", observed=True)["id"].count()
fig, ax = plt.subplots(figsize=(8, 5.5))
colors4 = [GOLD, TEAL, NAVY]
bars = ax.bar(range(len(sat)), sat.values, color=colors4, alpha=0.9, width=0.6)
for i, (bar, v) in enumerate(zip(bars, sat.values)):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 0.05,
            f"{v:.2f}", ha="center", fontsize=12, fontweight="bold")
    ax.text(bar.get_x() + bar.get_width() / 2, 0.12,
            f"n={counts.iloc[i]}", ha="center", fontsize=9, color="white")
ax.set_xticks(range(len(sat)))
ax.set_xticklabels(sat.index)
ax.set_ylabel("Average financial satisfaction (1–5)")
ax.set_ylim(0, 5)
ax.set_title("Financial Satisfaction by AI Tool Usage",
             fontsize=14, fontweight="bold", pad=12)
save(fig, "charts/04_satisfaction_by_ai_usage.png")

# ----------------------------------------------------------------------
# 5. Housing burden by country — horizontal bar, red(high)->green(low)
# ----------------------------------------------------------------------
df["housing_burden_pct"] = df["gasto_vivienda_usd"] / df["ingreso_mensual_usd"] * 100
hb = (df.groupby("pais")["housing_burden_pct"].mean()
      .sort_values(ascending=True))  # lowest bottom, highest top after barh
cmap = LinearSegmentedColormap.from_list("rg", ["#2a9d8f", "#e9c46a", "#e76f51"])
norm = (hb.values - hb.values.min()) / (hb.values.max() - hb.values.min())
colors5 = [cmap(x) for x in norm]
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(hb.index, hb.values, color=colors5)
for bar, v in zip(bars, hb.values):
    ax.text(v + 0.2, bar.get_y() + bar.get_height() / 2,
            f"{v:.1f}%", va="center", fontsize=10, fontweight="bold")
ax.set_xlabel("Average housing cost as % of income")
ax.set_title("Housing Burden by Country (red = high, green = low)",
             fontsize=14, fontweight="bold", pad=12)
ax.set_xlim(0, hb.max() * 1.15)
save(fig, "charts/05_housing_burden_by_country.png")

print("\nAll 5 charts generated in charts/")
