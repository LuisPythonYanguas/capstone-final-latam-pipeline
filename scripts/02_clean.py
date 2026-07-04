"""
Phase 2 — Clean
Produce a clean, analysis-safe version of the dataset.

Fixes:
  1. Standardise inconsistent 'industria' values (Tecnologia/tech/TECNOLOGIA -> Tecnología)
  2. Handle missing values in numeric columns (report %, apply recommendation)
  3. Flag (do NOT remove) negative 'ahorro_mensual_usd' in a boolean column
  4. Save clean CSV + print a before/after summary
"""

import sys
import pandas as pd

# Print UTF-8 cleanly even on Windows consoles
sys.stdout.reconfigure(encoding="utf-8")

RAW = "data/latam_finanzas_2025.csv"
CLEAN = "data/latam_finanzas_clean.csv"

df = pd.read_csv(RAW)
rows_before = len(df)


def header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ----------------------------------------------------------------------
# 1. Standardise 'industria'
# ----------------------------------------------------------------------
header("1. STANDARDISE 'industria'")
print("BEFORE:")
print(df["industria"].value_counts(dropna=False).to_string())

# Map every spelling/case variant to a single canonical label.
industria_map = {
    "tecnologia": "Tecnología",
    "tecnología": "Tecnología",
    "tech": "Tecnología",
}


def normalise_industria(value):
    if pd.isna(value):
        return value
    key = str(value).strip().lower()
    return industria_map.get(key, str(value).strip())


df["industria"] = df["industria"].apply(normalise_industria)

print("\nAFTER:")
print(df["industria"].value_counts(dropna=False).to_string())
tech_total = (df["industria"] == "Tecnología").sum()
print(f"\n'Tecnología' now consolidated to {tech_total} rows "
      f"(was split across Tecnología / Tecnologia / tech / TECNOLOGÍA).")

# ----------------------------------------------------------------------
# 2. Missing values in numeric columns
# ----------------------------------------------------------------------
header("2. MISSING VALUES IN NUMERIC COLUMNS")
numeric_cols = df.select_dtypes(include="number").columns
missing = df[numeric_cols].isna().sum()
missing = missing[missing > 0]

if missing.empty:
    print("No missing numeric values.")
else:
    for col in missing.index:
        pct = missing[col] / len(df) * 100
        median = df[col].median()
        print(f"{col}: {missing[col]} missing ({pct:.1f}%). "
              f"Recommendation: fill with median = {median:.2f}")
        # Median-fill: small % missing, keeps all 500 rows, robust to outliers.
        df[col] = df[col].fillna(median)
    print("\nMissing numeric values remaining:", int(df[numeric_cols].isna().sum().sum()))

# ----------------------------------------------------------------------
# 3. Flag negative savings
# ----------------------------------------------------------------------
header("3. FLAG NEGATIVE SAVINGS (kept, not removed)")
df["ahorro_negativo"] = df["ahorro_mensual_usd"] < 0
n_negative = int(df["ahorro_negativo"].sum())
print(f"Negative 'ahorro_mensual_usd' values: {n_negative} "
      f"({n_negative / len(df) * 100:.1f}%)")
print("Added boolean column 'ahorro_negativo' (True = spends more than earns).")

# ----------------------------------------------------------------------
# 4. Save + summary
# ----------------------------------------------------------------------
df.to_csv(CLEAN, index=False, encoding="utf-8")
rows_after = len(df)

header("SUMMARY")
print(f"Rows before: {rows_before}")
print(f"Rows after:  {rows_after}  (no rows dropped)")
print(f"Columns:     {df.shape[1]}  (+1: ahorro_negativo)")
print("\nChanges made:")
print("  - industria: consolidated 4 tech variants into 'Tecnología'")
print(f"  - gasto_salud_usd: filled 33 missing values with the median")
print(f"  - ahorro_negativo: new flag marking {n_negative} negative-savings rows")
print(f"\nClean dataset saved to: {CLEAN}")
