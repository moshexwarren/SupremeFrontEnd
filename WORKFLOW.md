# Workflow v6 — Reference/Taste Loop

## Phase 0 — Choose mode tier

Before taste/reference/build work, choose:

- Light
- Standard
- Full

Use `MODE_TIERS.md`. Declare screenshot capability and reference-match capability.

## Phase 1 — User Taste Grilling

Goal: build the design taste profile before any UI is generated.

This is a grilling, not a 5-question survey.

Rules:
- Ask one question per turn when interacting live.
- On any vague answer (“clean,” “modern,” “nice”), ask for a concrete example or anti-example.
- Continue until every axis is resolved: feel, anti-feel, layout, typography, color, key component, interaction/motion, RTL.
- Collect 2–5 references, and for each, record the one thing liked as `liked:`.

Required outputs:
- `PRODUCT_CONTEXT.md`
- `DESIGN_TASTE_PROFILE.md`
- `ANTI_TARGETS.md`
- `REAL_CONTENT.md`

## Phase 2 — Reference Discovery

Goal: collect visual anchors before generating samples.

Required outputs:
- `REFERENCE_SHORTLIST.md`
- `APPROVED_REFERENCES.md`
- real images in `screenshots/refs/`

Rules:
- Pull or accept 5–15 references.
- Group them by role: typography, forms, spacing, cards, onboarding, navigation, motion, emotional tone.
- Preserve actual screenshots or exported design images. DNA-only is not enough.
- User must approve which references are allowed to influence the system.

## Phase 3 — Reference Extraction

Goal: extract decisions, not pixels.

Required outputs:
- `EXTRACTION_TOOL.md`
- `APPROVED_REFERENCE_DNA.md`
- `DO_NOT_COPY.md`
- `SLOP_RISKS.md`

Rules:
- Set up Playwright/Hallmark/design-extract before extraction.
- Record `studied:`, `source-hash:`, or equivalent provenance markers.
- If styling cannot be fetched, set `EXTRACTION_DEGRADED.md` and cap confidence.

## Phase 4 — Design-Brain Judgment

Goal: judge extracted DNA using dense rules.

Required output:
- `DESIGN_BRAIN_JUDGMENT.md`

Must include applied judgment from:
- polish/hierarchy
- practical usability
- obviousness
- system consistency
- typography
- behavioral UX

## Phase 5 — Premium, Slop, and Organizing Idea

Required outputs:
- `PREMIUM_DEFINITION.md`
- `AI_SLOP_CLUSTER_RULES.md`
- `ORGANIZING_IDEA.md`

Must include:
- 8 premium signals
- 8 slop signals
- 5 dangerous slop clusters
- 5 do-not-use patterns
- one concrete structural organizing idea

## Phase 6 — Parallel Variant Board

Goal: generate 3–4 original directions after references are approved.

Required outputs:
- `SAMPLE_DIRECTIONS.md`
- `VARIANT_BOARD.md`

Rules:
- Generate variants that differ structurally, not cosmetically.
- Each variant must define a visual thesis, composition, type posture, color/material approach, interaction feel, emotional fit, and main risk.
- Evaluate variants on presence and distinctiveness before defect absence.
- Name the safe/median fallback to reject.

## Phase 7 — Human Taste Selection

Goal: human selects the non-median direction worth hardening.

Required outputs:
- `HUMAN_TASTE_SELECTION.md`
- `APPROVED_DESIGN_DIRECTION.md`

Pass criteria:
- Status is `APPROVED` or `APPROVED_WITH_NOTES`.
- Selected variant is named.
- The human states what gives it presence and what must not be averaged away.

## Phase 8 — Front-End Screen Spec

Required output:
- `FRONTEND_SCREEN_SPEC.md`

Must include:
- screen goal
- user state
- primary action
- selected visual direction
- token contract
- component inventory
- states
- responsive behavior
- RTL behavior if relevant
- accessibility requirements
- slop risks to avoid
- reference-match targets

## Phase 9 — Implementation

Rules:
- Reuse approved tokens/components first.
- No new token/component without justification.
- Implement real states: hover, focus, selected, disabled, loading, error, empty where relevant.
- Preserve the selected variant’s visual thesis.
- Do not sand down distinctive choices into generic SaaS defaults.

## Phase 10 — Screenshot and Reference-Match Loop

Required outputs:
- `SCREENSHOT_REVIEW_REPORT.md`
- `VISUAL_REFERENCE_MATCH_REPORT.md`
- `LOOP_REPORT.md`

Loop:
1. Render UI in a real browser.
2. Capture desktop/mobile/RTL/state screenshots.
3. Compare rendered screenshots to approved reference screenshots/designs.
4. Score reference match: mood, composition, density, hierarchy, typography, contrast, presence, non-median quality, mobile preservation, product fit.
5. Identify exact mismatches.
6. Patch implementation.
7. Repeat until reference-match and anti-slop gates pass.

## Phase 11 — External Validation

Required outputs:
- `VALIDATION_REPORT.md`
- `BLIND_REVIEW_REPORT.md` or explicit human signoff
- `FINAL_STATUS.md`

Run:

```bash
python3 scripts/validate_skill_state.py --root . --implementation path/to/app/src --require-final-pass
```

## Phase 12 — Canonization

Required outputs:
- `TOKEN_CONTRACT.md`
- `COMPONENT_RULES.md`
- `COMPONENT_CANONIZATION_LOG.md`
- `REJECTED_PATTERNS.md`

Canonize:
- tokens
- components
- variants
- layout patterns
- interaction states
- rejected slop patterns
- reference-match lessons
