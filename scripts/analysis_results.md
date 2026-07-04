# Phase 3 — Statistical Analysis Results

### 1. INCOME BY COUNTRY

| pais      |   median |   mean |   min |   max |   std |
|:----------|---------:|-------:|------:|------:|------:|
| Brasil    |     1458 |   1388 |   300 |  2874 |   592 |
| Chile     |     1246 |   1245 |   575 |  1861 |   290 |
| México    |     1067 |   1042 |   300 |  1693 |   287 |
| Colombia  |      857 |    849 |   405 |  1363 |   189 |
| Perú      |      822 |    818 |   362 |  1342 |   208 |
| Argentina |      798 |    766 |   373 |  1343 |   204 |

Highest median: Brasil ($1,458); lowest: Argentina ($798).

### 2. AGE VS. SAVINGS

| grupo_edad   |      n |   avg_savings_usd |   avg_savings_rate_pct |
|:-------------|-------:|------------------:|-----------------------:|
| 18-22        | 162.00 |             60.80 |                   5.72 |
| 23-25        | 123.00 |             76.48 |                   8.32 |
| 26-28        |  87.00 |            120.98 |                  11.72 |
| 29-32        | 128.00 |            154.07 |                  15.52 |

Pearson r (age vs. savings rate) = 0.408 (p = 1.667e-21)

### 3. SPENDING BREAKDOWN (avg % of income)

| category      |   pct_of_income |
|:--------------|----------------:|
| Housing       |           28.54 |
| Food          |           23.83 |
| Transport     |           10.05 |
| Entertainment |            8.69 |
| Education     |            8.45 |
| Healthcare    |            4.90 |

Total expenses as % of income (avg): 84.5%

### 4. CREDIT CARD HOLDERS VS NON-HOLDERS

Holders: 284 | Non-holders: 216

| metric            |   has_card |   no_card |   pct_diff |
|:------------------|-----------:|----------:|-----------:|
| avg_income        |    1023.35 |   1008.18 |       1.50 |
| avg_food          |     258.05 |    222.30 |      16.10 |
| avg_entertainment |      94.56 |     80.67 |      17.20 |
| avg_savings       |     101.75 |     95.39 |       6.70 |

### 5. AI TOOL USAGE VS FINANCIAL SATISFACTION

| grupo_ia      |      n |   avg_satisfaction |   avg_income |
|:--------------|-------:|-------------------:|-------------:|
| Low (0-3)     |  98.00 |               2.05 |       746.75 |
| Medium (4-10) | 381.00 |               2.54 |      1045.83 |
| High (11+)    |  21.00 |               3.43 |      1750.29 |

Pearson r (AI hours vs. satisfaction) = 0.571 (p = 1.193e-44)

### 6. HOUSING BURDEN BY COUNTRY (avg housing as % of income)

| pais      |   avg_housing_pct |
|:----------|------------------:|
| Argentina |             34.09 |
| Chile     |             32.55 |
| México    |             28.15 |
| Brasil    |             26.90 |
| Colombia  |             25.41 |
| Perú      |             24.63 |
