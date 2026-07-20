# SupremeFrontEnd

A tool-agnostic front-end workflow for preventing both obvious AI slop **and** competent blandness.

## Install for Codex

Clone the repository into your Codex skills directory using the technical skill
ID:

```bash
git clone https://github.com/moshexwarren/SupremeFrontEnd.git ~/.codex/skills/supreme-front-end
```

Restart Codex after installation so the new skill is discovered.

## Verification

The distributed skill is checked with the official Codex validator, Python and
JavaScript syntax checks, and a credential-pattern scan. Its project-state
validator is a runtime gate: the bundled blank starter state intentionally fails
until a real project supplies product context, design decisions, component
rules, tokens, screenshots, reference comparison, and human signoff.

v5 already enforced grounding, extraction, screenshots, content-validating phase gates, blind review provenance, and validator binding. v6 adds the missing 2026 frontier layer:

```text
reference-image anchors -> 3–4 distinct variants -> human taste selection -> VLM/human reference-match loop -> production hardening
```

## What changed from v5

- Added a real **Variant Board** gate: the agent must generate 3–4 structurally distinct directions, not color swaps.
- Added a **Human Taste Selection** gate: AI may generate candidates, but human judgment chooses the direction with presence.
- Added a **Visual Reference Match** gate: rendered screenshots are scored against reference screenshots/designs, not merely checked for existence.
- Added support files from the v2 frontend-production skill: agents, context templates, taste-pack, screenshot/VLM scripts, and design-system scaffolding.
- Upgraded the Python validator to fail final pass when variant, human taste, or reference-match evidence is missing.

## Core philosophy

Rules prevent garbage. References and human selection prevent blandness.

This skill automates:

- speed
- completeness
- screenshots
- slop detection
- token/component discipline
- visual-reference mismatch detection
- validation binding

It does **not** pretend to automate taste. Taste remains a human gate.

## Main workflow

```text
1. Choose mode tier
2. Grill taste/spec until concrete
3. Collect real visual references
4. Extract reference DNA with tooling
5. Preserve reference screenshots as pixel anchors
6. Generate 3–4 distinct visual variants
7. Human selects the direction for presence/distinctiveness
8. Create buildable screen/component/token spec
9. Implement with constraints
10. Render via Playwright and capture screenshots
11. Run VLM/human reference-match review
12. Fix mismatches without cloning
13. Run accessibility/interaction/blind review
14. Run validator
15. Canonize approved components/tokens
16. Set final status only when externally validated
```

## Final-pass validator

```bash
python3 scripts/validate_skill_state.py --root . --implementation ../app/src --require-final-pass
```

Final pass requires all v5 gates plus:

- `project-state/VARIANT_BOARD.md`
- `project-state/HUMAN_TASTE_SELECTION.md`
- `project-state/VISUAL_REFERENCE_MATCH_REPORT.md`
- real rendered screenshots
- real reference screenshots or approved visual anchors

## Important new files

```text
VARIANT_AND_TASTE_GATE.md
REFERENCE_MATCH_LOOP.md
project-state/VARIANT_BOARD.md
project-state/HUMAN_TASTE_SELECTION.md
project-state/VISUAL_REFERENCE_MATCH_REPORT.md
prompts/vlm-reference-match.md
prompts/human-taste-review.md
scripts/score-reference-match.mjs
agents/variant-director.md
agents/reference-match-reviewer.md
agents/taste-gatekeeper.md
```

## Honest ceiling

The skill can force evidence, but it cannot make the final taste judgment. Human choice of the non-median direction is part of the system, not a weakness.
