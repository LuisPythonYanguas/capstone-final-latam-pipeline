# Notion Setup — Análisis LatAm 2025

The Notion workspace is the only part of this pipeline that needs **your** account.
Follow these steps once, then either publish via the Notion MCP inside Claude Code
or run the reproducible `scripts/notion_publish.py`.

## 1. Create the integration (2 min)
1. Sign in / sign up at <https://notion.so>.
2. Go to <https://notion.so/my-integrations> → **New integration** → name it **LatAm Pipeline**.
3. Copy the **Internal Integration Secret** (starts with `secret_` or `ntn_`). This is your API key.

## 2. Create the workspace items
Create a page (e.g. **Análisis LatAm 2025**) containing:
- A database **Findings Tracker** — columns: `Título`, `Estadística Clave`, `Alcance`, `Prioridad`, `Publicado`
- A database **Country Profiles** — columns: `País`, `Muestra`, `Ingreso Mediano`, `Carga Vivienda`
- A blank page **Informe Ejecutivo**

## 3. Share each item with the integration
On each database and the page: **•••** menu → **Connections** → add **LatAm Pipeline**.
(If the script will create the databases for you, just share the parent page instead.)

## 4a. Publish via the reproducible script
```powershell
$env:NOTION_API_KEY = "secret_your_key_here"
# Optional — lets the script create the databases/report page if they don't exist:
$env:NOTION_PARENT_PAGE_ID = "the-32-char-id-from-the-parent-page-url"
# Optional — embeds chart images from GitHub in the report page:
$env:GITHUB_RAW_BASE = "https://raw.githubusercontent.com/LuisPythonYanguas/<repo>/main"

venv\Scripts\python.exe scripts\notion_publish.py
```
This creates the 6 Country Profiles, the 6 Findings (each with its own page), and the report.

## 4b. Or publish via the Notion MCP inside Claude Code
1. In `.claude/settings.json`, replace `YOUR_API_KEY` with your key (do **not** commit the real key).
2. Launch `claude`, run `claude mcp list` to confirm the `notion` server appears.
3. Use the `/publish-finding` skill after each analysis (Phase 3) and publish the report (Phase 6).

## Security note
Never commit your real key. `.gitignore` excludes `.env`; keep the key in an environment
variable or paste it only into your local `.claude/settings.json`.
