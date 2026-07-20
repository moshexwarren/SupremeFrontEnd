# Changelog

## 6.0.0 — Reference/Taste Loop Edition

- Merged v5 grounded anti-slop workflow with v2 reference/variant/taste workflow.
- Added `VARIANT_BOARD.md` gate for 3–4 distinct visual directions.
- Added `HUMAN_TASTE_SELECTION.md` gate to make taste selection explicitly human-owned.
- Added `VISUAL_REFERENCE_MATCH_REPORT.md` gate for VLM/human comparison against approved visual references.
- Added `REFERENCE_MATCH_LOOP.md` and `VARIANT_AND_TASTE_GATE.md`.
- Added v2 agents, context templates, taste-pack, and screenshot/reference-match scripts.
- Updated validator with v6 checks for variant distinctiveness, human approval, and reference-match scores/provenance.
- Made real reference screenshots a hard gate when configured.
