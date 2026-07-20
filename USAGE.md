# Usage

## Start a new project

```text
Use the SupremeFrontEnd skill.
Mode: Taste Discovery.
Product: [describe product].
Ask me the fast 10 questions first. Then produce PRODUCT_CONTEXT.md, DESIGN_TASTE_PROFILE.md, and ANTI_TARGETS.md.
Do not design UI yet.
```

## Run reference discovery

```text
Mode: Reference Discovery.
Find or organize 8 reference websites for [product/screen].
Group them by role: typography, spacing, forms, cards, onboarding, trust, motion.
Ask me to approve which ones to use.
```

## Extract references

```text
Mode: Reference Extraction.
Analyze these approved references.
Extract design DNA and token-like values.
Use the design brain to judge what is transferable.
Produce APPROVED_REFERENCE_DNA.md, DO_NOT_COPY.md, and SLOP_RISKS.md.
```

## Generate sample directions

```text
Mode: Style Synthesis.
Using the taste profile and approved reference DNA, generate 3–5 original design directions.
Each direction must specify layout, typography, color, components, interaction, premium signals, and slop risks.
Do not code yet.
```

## Build screen

```text
Mode: Front-End Build.
Use the approved design direction and token/component contracts.
Create FRONTEND_SCREEN_SPEC.md for [screen], then implement.
Do not invent new tokens/components silently.
```

## Audit and loop

```text
Mode: Audit/Loop.
Render the UI, capture desktop/mobile/RTL screenshots, score slop and premium, patch failures, and repeat until pass.
```

## Final pass

Self-score is not final.

A normal final run requires:

```bash
python3 scripts/validate_skill_state.py --root . --implementation ../app/src --require-final-pass
```

The final status must be:

```text
PASS_EXTERNALLY_VALIDATED
```

If screenshots are unavailable, write:

```text
BLOCKED_SCREENSHOT_UNAVAILABLE
```

If only specs are complete, write:

```text
SPEC_COMPLETE_UNVERIFIED
```

## One-time host setup

From the host app repository root:

```bash
bash path/to/skill/integrations/install_git_hooks.sh
```

Set custom paths if needed:

```bash
SKILL_DIR=path/to/skill IMPLEMENTATION_DIR=app bash path/to/skill/integrations/install_git_hooks.sh
```

## Manual validation from a host repo

Draft/spec validation:

```bash
python3 path/to/skill/scripts/validate_skill_state.py \
  --root path/to/skill \
  --implementation src
```

Final/deploy validation:

```bash
python3 path/to/skill/scripts/validate_skill_state.py \
  --root path/to/skill \
  --implementation src \
  --require-final-pass
```

## True blind review

Open a separate clean agent session or use yourself as reviewer. Give only the allowed packet listed in `ENFORCEMENT.md` plus screenshots. Do not let the same implementing session generate the blind-review pass.
