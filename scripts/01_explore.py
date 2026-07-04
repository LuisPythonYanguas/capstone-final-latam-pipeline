"""
Phase 1 — Explore
Understand the raw dataset before touching it.

Outputs:
  1. Number of rows and columns
  2. Every column with its data type
  3. Missing values per column (most -> least)
  4. Basic statistics for numeric columns (min, max, mean, median, std)
  5. Unique values + counts for categorical columns
"""

import pandas as pd

RAW = "data/latam_finanzas_2025.csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

df = pd.read_csv(RAW)


def header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# 1. Shape ---------------------------------------------------------------
header("1. DATASET SHAPE")
print(f"Rows:    {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# 2. Columns and dtypes --------------------------------------------------
header("2. COLUMNS AND DATA TYPES")
dtypes = df.dtypes.reset_index()
dtypes.columns = ["column", "dtype"]
print(dtypes.to_string(index=False))

# 3. Missing values ------------------------------------------------------
header("3. MISSING VALUES PER COLUMN (most -> least)")
missing = df.isna().sum().sort_values(ascending=False)
missing_pct = (missing / len(df) * 100).round(2)
missing_table = pd.DataFrame({"missing": missing, "pct": missing_pct})
print(missing_table[missing_table["missing"] > 0].to_string())
if (missing == 0).all():
    print("No missing values.")

# 4. Numeric statistics --------------------------------------------------
header("4. NUMERIC COLUMN STATISTICS")
numeric_cols = df.select_dtypes(include="number").columns
stats = df[numeric_cols].agg(["min", "max", "mean", "median", "std"]).T
print(stats.round(2).to_string())

# 5. Categorical unique values ------------------------------------------
header("5. CATEGORICAL COLUMNS — UNIQUE VALUES AND COUNTS")
categorical_cols = [
    "pais", "industria", "ocupacion", "meta_financiera",
    "tiene_tarjeta_credito", "tiene_cuenta_ahorro", "tiene_deuda",
]
for col in categorical_cols:
    print(f"\n--- {col} ({df[col].nunique(dropna=True)} unique) ---")
    print(df[col].value_counts(dropna=False).to_string())

print("\n" + "=" * 70)
print("Exploration complete.")
print("=" * 70)
