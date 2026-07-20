# Reference Pipeline

## Purpose

Use references to control taste without cloning. The skill must extract **design decisions**, not pixels.

## Step 0 — Set up extraction tooling (MANDATORY, do not skip)

Before collecting references, ensure a real extraction tool is available. If none is set up, set it up now — do not fall back to eyeballing.

```bash
bash integrations/setup_extraction.sh
```

This installs Playwright (render + computed-style extraction) and records the tool in `project-state/EXTRACTION_TOOL.md`. If you use Hallmark or design-extract instead, install per their README and record it in that file. The validator FAILs (`extraction tool setup`) until a real tool is recorded. If a reference's CSS cannot be fetched, set `project-state/EXTRACTION_DEGRADED.md` (caps premium).

## Step 1 — Collect references

Sources:
- user-provided URLs
- user-provided screenshots
- web search
- product category examples
- adjacent-category examples

Classify each reference by role:
- typography
- spacing/layout rhythm
- forms
- cards/results
- onboarding/intake
- navigation
- emotional tone
- motion
- trust/privacy

## Step 2 — Approve references

Before extraction, show user:

```text
Reference:
Why it may help:
Which layer it should influence:
What we will not copy:
```

User approval required before sample generation.

## Step 3 — Extract raw observations

For each reference:
- page type
- first impression
- layout/grid
- section rhythm
- type roles
- color roles
- spacing rhythm
- card/surface treatment
- button treatment
- form treatment
- navigation/orientation
- motion/interaction
- mobile behavior if visible
- accessibility strengths/risks

## Step 4 — Extract token-like values

Use design-extract or manual inspection.

Approximate allowed:
- colors as approximate hex
- type sizes as ranges
- spacing as repeated values
- radius levels
- shadow levels

Do not claim exact font if not verified. Say “font appears like...” or “font personality is...”.

## Step 5 — Convert to transferable DNA

Bad:
> uses blue gradient and nice cards

Good:
> uses neutral base, one restrained action color, flat cards with 1px borders, left-aligned type, and 64–96px section rhythm. Polish comes from restraint and alignment, not decoration.

## Step 6 — Do-not-copy list

Always list:
- exact layout
- brand colors if distinctive
- logo
- copy
- illustrations
- icons
- photography
- proprietary visual motif
- signature animation/interaction

## Step 7 — Multi-reference role assignment

If multiple references are used, assign roles:

```text
Reference A: spacing + editorial rhythm
Reference B: form clarity
Reference C: card density
Our product: color, tone, trust copy
```

Never mix all visible traits from all references.

## Reference DNA Card Template

```text
Reference:
Role:
Overall feel:
Borrow:
Do not borrow:
Layout DNA:
Typography DNA:
Color DNA:
Spacing DNA:
Component DNA:
Interaction DNA:
Usability DNA:
Token-like values:
Slop risks:
Design-brain interpretation:
Coding-agent instruction:
```
