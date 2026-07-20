# Merge Notes

Merged sources:

- Base: `ai-slop-resistant-frontend-skill-v5-grounded`
- Added layer: `frontend-production-skill-v2`

## Merge decision

v5 remains the base because it has stronger binding:

- project-state filechain
- content-validating validator
- reference extraction provenance
- extraction-tool setup
- screenshot hard stop
- blind-review provenance
- final status discipline
- implementation scanning

v2 contributes the missing frontier layer:

- reference-first workflow
- parallel variant generation
- human taste gate
- VLM-style reference-match review
- visual craft/reference scoring
- reviewer agents and prompts

## Canonical artifact paths

Use v5 project-state paths as canonical. v2-style `frontend-artifacts/*` templates are included for compatibility/inspiration, but final validation expects:

```text
project-state/VARIANT_BOARD.md
project-state/HUMAN_TASTE_SELECTION.md
project-state/VISUAL_REFERENCE_MATCH_REPORT.md
screenshots/desktop.png
screenshots/mobile.png
screenshots/refs/*
```

## Core v6 thesis

v5 prevented slop. v6 also fights blandness.

The loop is:

```text
real references -> distinct variants -> human choice -> rendered screenshots -> VLM/human reference match -> production validation
```
