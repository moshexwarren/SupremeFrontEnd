---
name: supreme-front-end
description: Use when a frontend interface risks generic, bland, or AI-generated aesthetics and needs explicit taste discovery, visual references, structurally distinct directions, human selection, screenshot comparison, accessibility review, or component canonization.
---

# SupremeFrontEnd

## Mission

Build original front-end UI that feels intentional, premium, usable, product-specific, and non-median by controlling design decisions through:

1. user taste profile
2. approved visual references
3. extracted reference DNA with provenance
4. preserved reference-image anchors
5. dense design-brain rules
6. project-specific premium/slop definitions
7. parallel distinct variant generation
8. human taste selection
9. implementation specs
10. rendered screenshot review
11. VLM/human reference-match comparison
12. blind review / human signoff
13. component canonization

The skill must not let the AI invent visual taste from scratch, and it must not let the AI select final taste by itself.

## v6 frontier rule

The honest frontier is not more gates alone. It is:

```text
Reference image anchors + distinct variants + human selection + visual reference-match loop.
```

Bland is not fixed by adding rules. Bland is fixed by giving the agent strong visual anchors, forcing genuinely different directions, letting a human choose the direction with presence, and then using screenshot/VLM review to keep implementation from sanding the choice down into the median.

## Operating modes

### Mode A — Taste Discovery
Use when the product has no clear design profile yet.
Output: `DESIGN_TASTE_PROFILE.md`, `ANTI_TARGETS.md`, and `PRODUCT_CONTEXT.md`.

### Mode B — Reference Discovery
Use when the user needs examples from the internet or has provided URLs/screenshots.
Output: `REFERENCE_SHORTLIST.md`, `APPROVED_REFERENCES.md`, `screenshots/refs/*`.

### Mode C — Reference Extraction
Set up and use a real extraction tool (Playwright/Hallmark/design-extract) before extracting DNA. Do not eyeball references.
Output: `EXTRACTION_TOOL.md`, `APPROVED_REFERENCE_DNA.md`, `DO_NOT_COPY.md`, `SLOP_RISKS.md`.

### Mode D — Style Synthesis
Convert taste + references + design-brain judgment into original design directions.
Output: `PREMIUM_DEFINITION.md`, `AI_SLOP_CLUSTER_RULES.md`, `ORGANIZING_IDEA.md`, `SAMPLE_DIRECTIONS.md`.

### Mode E — Variant Board
Generate 3–4 structurally distinct visual directions.
Output: `VARIANT_BOARD.md`.

Rules:
- Directions must differ in composition, density, type posture, material, interaction feel, and organizing idea.
- Do not score variants primarily on defect absence.
- Score variants on presence, distinctiveness, visual thesis, memorability, product fit, emotional accuracy, and reference fit.
- Name the safe/median/default direction that must be rejected.

### Mode F — Human Taste Gate
The human chooses the variant.
Output: `HUMAN_TASTE_SELECTION.md`, `APPROVED_DESIGN_DIRECTION.md`.

Allowed final taste statuses:
- `APPROVED`
- `APPROVED_WITH_NOTES`
- `REJECTED`
- `NEEDS_MORE_VARIANTS`

Final implementation hardening cannot begin until the selected direction is approved.

### Mode G — Front-End Build
Create screen specs and implement using approved tokens/components only.
Output: `FRONTEND_SCREEN_SPEC.md`, implementation patches.

### Mode H — Screenshot + Reference-Match Loop
Render real UI, screenshot it, compare to references, score it, revise until gates pass.
Output: `SCREENSHOT_REVIEW_REPORT.md`, `VISUAL_REFERENCE_MATCH_REPORT.md`, `LOOP_REPORT.md`.

### Mode I — Canonize
Freeze approved tokens/components/patterns and record rejected patterns.
Output: `TOKEN_CONTRACT.md`, `COMPONENT_RULES.md`, `COMPONENT_CANONIZATION_LOG.md`, `REJECTED_PATTERNS.md`.

## Hard rules

- Do not begin implementation before the design direction is approved.
- Do not let the implementing agent be the only final taste judge.
- Do not pass on screenshot existence alone; rendered screenshots must be compared against approved references.
- Do not generate variants that are only palette swaps.
- Do not optimize variant selection for safety; select for presence and product fit, then fix defects afterward.
- Do not use references by copying exact layout, brand, copy, assets, illustrations, logos, or signature interaction identity.
- Do not invent components if approved components can be reused.
- Do not pass gates by file existence. Gates require content checks.
- Do not ship UI without screenshot review.
- Do not ship UI without visual reference-match review.
- Do not ship UI with slop score ≥ 6.
- Do not ship UI with premium score < 15 unless explicitly accepted as a rough draft.
- Do not use “make it modern/premium/clean” without specifying the mechanism.

## Default anti-slop bans unless explicitly approved

- purple/blue SaaS gradient hero
- glassmorphism-by-default
- floating blobs
- fake dashboard widgets
- everything-is-a-card layout
- cards inside cards inside cards
- random icon grids
- generic feature cards
- vague CTAs like “Get Started” without context
- tiny gray text as fake premium
- heavy shadows on every surface
- decorative motion without orientation/feedback purpose
- untested Hebrew/RTL for a multilingual product

## Required output quality

Every design decision should be explainable as one of:

- supports hierarchy
- improves comprehension
- reduces cognitive load
- builds trust
- expresses product personality
- improves accessibility
- preserves system consistency
- translates approved reference DNA
- preserves the human-selected visual thesis
- keeps the screen out of the safe median

If a decision cannot be explained, remove it.

## Enforcement summary

Self-score is never final. For Standard and Full modes, final pass requires:

1. rendered screenshots;
2. real reference-image anchors;
3. a variant board with at least 3 distinct directions;
4. human taste selection marked `APPROVED` or `APPROVED_WITH_NOTES`;
5. VLM/human reference-match review;
6. mechanical validation through `scripts/validate_skill_state.py`;
7. a true separate-session blind review or human signoff;
8. `project-state/FINAL_STATUS.md` set to `PASS_EXTERNALLY_VALIDATED`; and
9. final/deploy validation passing with `--require-final-pass`.

Before executing the skill, declare:

```text
Mode tier: Light / Standard / Full
Why this tier:
Validation path: validator + human / validator + separate-session reviewer / spec-only blocked
Screenshot capability: available / unavailable
Reference-match capability: VLM / human / unavailable
Final-pass eligibility: yes / no
```

Do not say “done,” “ship-ready,” or “final pass” unless the final status is `PASS_EXTERNALLY_VALIDATED` and the validator exits 0 with `--require-final-pass`.
