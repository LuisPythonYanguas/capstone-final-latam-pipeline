"""
Generate the FINAL submission cover PDF (GitHub URL + Notion placeholder).
Output: Desktop/capstone-final-submission.pdf
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

OUT = os.path.join(os.path.expanduser("~"),
                   "OneDrive", "Desktop", "capstone-final-submission.pdf")
GH = "https://github.com/LuisPythonYanguas/capstone-final-latam-pipeline"
NOTION = os.environ.get("NOTION_WORKSPACE_URL", "").strip()

NAVY = HexColor("#0f2846")
BLUE = HexColor("#2f6fb0")
SLATE = HexColor("#6c757d")
LIGHT = HexColor("#eef2f6")
GREEN = HexColor("#2a9d8f")

c = canvas.Canvas(OUT, pagesize=letter)
W, H = letter

# Header band
c.setFillColor(NAVY)
c.rect(0, H - 1.7 * inch, W, 1.7 * inch, fill=1, stroke=0)
c.setFillColor(BLUE)
c.rect(0, H - 1.78 * inch, W, 0.08 * inch, fill=1, stroke=0)
c.setFillColor(HexColor("#ffffff"))
c.setFont("Helvetica-Bold", 11)
c.drawString(1 * inch, H - 0.65 * inch, "FINAL CAPSTONE  ·  ADVANCED TRACK — PIPELINE BUILDER")
c.setFont("Helvetica-Bold", 20)
c.drawString(1 * inch, H - 1.12 * inch, "De Analista a Arquitecto")
c.setFont("Helvetica", 10.5)
c.drawString(1 * inch, H - 1.4 * inch,
             "Pipeline de Analisis Automatizado con Claude Code — Hooks · Skills · Notion MCP")

y = H - 2.25 * inch
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 14)
c.drawString(1 * inch, y, "Submission Details")


def url_box(y, label, url, filled=True):
    c.setFillColor(SLATE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * inch, y, label)
    by = y - 0.5 * inch
    bx, bw, bh = 1 * inch, W - 2 * inch, 0.44 * inch
    c.setFillColor(LIGHT)
    c.roundRect(bx, by, bw, bh, 6, fill=1, stroke=0)
    if filled:
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(bx + 0.2 * inch, by + 0.15 * inch, url)
        c.linkURL(url, (bx, by, bx + bw, by + bh), relative=0)
    else:
        c.setFillColor(SLATE)
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(bx + 0.2 * inch, by + 0.15 * inch, url)
    return by - 0.35 * inch


y -= 0.55 * inch
y = url_box(y, "GITHUB REPOSITORY", GH, filled=True)
if NOTION:
    y = url_box(y, "NOTION WORKSPACE", NOTION, filled=True)
else:
    y = url_box(y, "NOTION WORKSPACE",
                "(paste your Notion workspace URL here after publishing)", filled=False)

# Meta
y -= 0.1 * inch
for label, val in [
    ("Student / GitHub:", "LuisPythonYanguas"),
    ("Organisation:", "Futuro Digital LatAm (2025)"),
    ("Pipeline:", "3 Hooks · 2 Skills · Notion MCP · 1 Agent"),
]:
    c.setFillColor(SLATE); c.setFont("Helvetica-Bold", 10)
    c.drawString(1 * inch, y, label)
    c.setFillColor(HexColor("#000000")); c.setFont("Helvetica", 10)
    c.drawString(2.7 * inch, y, val)
    y -= 0.28 * inch

# Deliverables
y -= 0.15 * inch
c.setFillColor(NAVY); c.setFont("Helvetica-Bold", 12)
c.drawString(1 * inch, y, "Deliverables in the repository / ZIP")
y -= 0.3 * inch
c.setFillColor(HexColor("#000000")); c.setFont("Helvetica", 9.5)
items = [
    "analysis-report.md  ·  6-section executive report",
    "scripts/  ·  Python pipeline + session-log.md audit trail + notion_publish.py",
    "charts/  ·  5 professional visualisations (PNG)",
    ".claude/settings.json  ·  3 hooks (chart counter, script logger, phase validator) + Notion MCP",
    ".claude/hooks/validate-phases.sh  ·  phase validator (Stop hook)",
    ".claude/skills/interpret + publish-finding  ·  2 skills",
    ".claude/agents/country-profiler.md  ·  parallel country agent",
    "Full git commit history — one commit per phase (0 through 6)",
]
for it in items:
    c.drawString(1.15 * inch, y, u"•  " + it)
    y -= 0.26 * inch

# Footer
c.setFillColor(GREEN)
c.rect(0, 0, W, 0.35 * inch, fill=1, stroke=0)
c.setFillColor(HexColor("#ffffff")); c.setFont("Helvetica", 8)
c.drawString(1 * inch, 0.13 * inch,
             "Final Capstone — Advanced Data Analyst Pipeline  |  Futuro Digital LatAm 2025")

c.showPage()
c.save()
print("Saved:", OUT)
