#!/bin/bash
echo "=== Pipeline Status ==="
[ -f data/latam_finanzas_clean.csv ] && echo "✓ Phase 2: Clean dataset" || echo "✗ Phase 2: Clean dataset missing"
[ -f .claude/agents/country-profiler.md ] && echo "✓ Phase 2.5: Country profiler agent" || echo "✗ Phase 2.5: Agent missing"
[ -f scripts/03_analyse.py ] && echo "✓ Phase 3: Analysis script" || echo "✗ Phase 3: Analysis script missing"
n=$(ls charts/*.png 2>/dev/null | wc -l); [ "$n" -ge 5 ] && echo "✓ Phase 4: $n/5 charts" || echo "✗ Phase 4: $n/5 charts"
[ -f analysis-report.md ] && echo "✓ Phase 6: Executive report" || echo "✗ Phase 6: Report missing"
