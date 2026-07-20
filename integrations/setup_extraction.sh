#!/usr/bin/env bash
set -euo pipefail
# Sets up reference-extraction tooling so the agent studies references instead of eyeballing.
# Run once from the project root. Records the tool in project-state/EXTRACTION_TOOL.md.

ROOT="${1:-.}"
REC="$ROOT/project-state/EXTRACTION_TOOL.md"
mkdir -p "$ROOT/project-state"

echo "Setting up Playwright (baseline extraction: render + screenshot + computed styles)..."
if command -v npm >/dev/null 2>&1; then
  npm i -D playwright >/dev/null 2>&1 || npm i -D playwright
  npx playwright install chromium
  TOOL="playwright"
else
  echo "npm not found — install Node first, or set up Hallmark/design-extract manually." >&2
  TOOL="none set up"
fi

# Optional: Hallmark / design-extract (clone per their READMEs if you use them).
# git clone https://github.com/nutlope/hallmark  # then follow its setup

cat > "$REC" <<REC2
# Extraction tool

tool: $TOOL
installed-at: $(date -u +%FT%TZ)
method: render + computed-style extraction (not eyeballing)
notes: if a reference's CSS cannot be fetched, set project-state/EXTRACTION_DEGRADED.md
REC2
echo "Recorded extraction tool in $REC"
