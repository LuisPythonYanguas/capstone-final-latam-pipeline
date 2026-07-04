# De Analista a Arquitecto — Pipeline de Análisis Automatizado

Final Capstone · **Advanced Track — Pipeline Builder** · Futuro Digital LatAm, 2025

Builds on the Option B analysis and turns it into a **repeatable, self-validating pipeline**:
Hooks that validate outputs and log every step, Skills that enforce a consistent finding format,
and a Notion MCP that publishes findings to a board-facing workspace.

🔗 **Repository:** _(added after first push)_
📄 **Report:** [`analysis-report.md`](analysis-report.md)

---

## Pipeline Components

| Component | Where | What it does |
|---|---|---|
| **Hook A — Chart Counter** | `.claude/settings.json` (PostToolUse/Write) | Prints `Chart saved: … — N/5` as each PNG is written |
| **Hook B — Script Logger** | `.claude/settings.json` (PostToolUse/Bash) | Appends a timestamped line to [`session-log.md`](session-log.md) for every command |
| **Hook C — Phase Validator** | `.claude/hooks/validate-phases.sh` (Stop) | Prints a ✓/✗ checklist of expected outputs after each response |
| **Skill — /interpret** | `.claude/skills/interpret/SKILL.md` | 3-sentence Spanish finding format (fact → implication → recommendation) |
| **Skill — /publish-finding** | `.claude/skills/publish-finding/SKILL.md` | Publishes a finding to the Notion Findings Tracker |
| **Agent — country-profiler** | `.claude/agents/country-profiler.md` | One definition, six country profiles in parallel |
| **Notion MCP** | `.claude/settings.json` (`mcpServers.notion`) | Board-facing workspace: Findings Tracker, Country Profiles, Informe Ejecutivo |

## Repository Structure

```
capstone-final/
├── analysis-report.md            # Executive report (6 sections)
├── CLAUDE.md                     # Project context for Claude Code
├── session-log.md                # Audit trail (Script Logger hook)
├── .claude/
│   ├── settings.json             # 3 hooks + Notion MCP
│   ├── hooks/validate-phases.sh  # Phase validator (Stop hook)
│   ├── skills/interpret/SKILL.md
│   ├── skills/publish-finding/SKILL.md
│   └── agents/country-profiler.md
├── scripts/
│   ├── 01_explore.py … 04_visualise.py
│   ├── build_country_profiles.py, country_*.py, country_profiles.md
│   ├── interpretations.md        # Phase 5 — 6 findings in /interpret format
│   └── notion_publish.py         # Scriptable Notion publisher (Notion API)
├── charts/                       # 5 professional PNGs
└── data/                         # raw + cleaned datasets
```

## How to Reproduce

```powershell
python -m venv venv
venv\Scripts\activate
pip install pandas matplotlib seaborn scipy tabulate requests

venv\Scripts\python.exe scripts\01_explore.py
venv\Scripts\python.exe scripts\02_clean.py
venv\Scripts\python.exe scripts\build_country_profiles.py
venv\Scripts\python.exe scripts\03_analyse.py
venv\Scripts\python.exe scripts\04_visualise.py
```

To publish to Notion, see [`NOTION_SETUP.md`](NOTION_SETUP.md).

## The Phases

0. **Setup** — configure hooks, skills, Notion MCP (this repo's `.claude/`)
1. **Explore** · 2. **Clean** · 2.5. **Country Profiler Agent**
3. **Analyse + Publish** — 6 analyses, findings pushed to Notion
4. **Visualise** · 5. **Interpret** (`/interpret`) · 6. **Report + Notion**

*From analyst to architect: building the system that runs the analysis.*
