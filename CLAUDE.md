# Pipeline: Análisis LatAm 2025

## Project
Repeatable financial wellness analysis pipeline for Futuro Digital LatAm.
Dataset: data/latam_finanzas_2025.csv (raw) → data/latam_finanzas_clean.csv (clean)
Report: analysis-report.md

## Python Environment
venv activated. Libraries: pandas, matplotlib, seaborn, scipy.
Scripts go in scripts/. Charts go in charts/ as PNGs.
On Windows run scripts with: venv/Scripts/python.exe scripts/<name>.py

## Naming Conventions
Scripts: 01_explore.py, 02_clean.py, 03_analyse.py, 04_visualise.py
Charts: 01_income_by_country.png through 05_housing_burden_by_country.png
Country scripts: country_mexico.py, country_colombia.py, etc.

## Notion Workspace
Integration: LatAm Pipeline
Databases: "Findings Tracker", "Country Profiles"
Report page: "Informe Ejecutivo"
Push each finding after Phase 3 analysis. Push report after Phase 6.

## Pipeline Components
Hooks: chart counter, script logger, phase validator (configured in .claude/settings.json)
Skills: /interpret (finding format), /publish-finding (Notion push)
Agent: country-profiler (parallel country analysis)
