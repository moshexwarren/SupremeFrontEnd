# Validator Requirements Checklist

Use this checklist before running `scripts/validate_skill_state.py`.

## Project-state content

- PRODUCT_CONTEXT has product category, user, problem, and language/RTL needs.
- DESIGN_TASTE_PROFILE has concrete visual/interactions preferences, not only moods.
- ANTI_TARGETS has concrete forbidden patterns.
- APPROVED_REFERENCES assigns a role to each reference.
- APPROVED_REFERENCE_DNA includes layout/type/color/spacing/component/interaction DNA.
- PREMIUM_DEFINITION defines mechanisms, not vibes.
- AI_SLOP_CLUSTER_RULES lists clusters, not isolated adjectives.
- TOKEN_CONTRACT has actual values.
- COMPONENT_RULES has states, accessibility, responsive behavior, and usage rules.
- FRONTEND_SCREEN_SPEC names primary action, states, mobile, RTL, and slop risks.
- SCREENSHOT_REVIEW_REPORT includes actual screenshot review or BLOCKED_FROM_FINAL_PASS.
- LOOP_REPORT includes itemized scores and fixes.

## Token minimums

TOKEN_CONTRACT should include at least:

- 5 semantic color roles
- 5 spacing values
- 5 type sizes or roles
- 3 radius values
- 2 shadow/elevation levels or explicit no-shadow policy

## Component minimums

COMPONENT_RULES should include:

- use case
- do-not-use case
- variants
- default/hover/focus/disabled/loading/error/empty states where relevant
- accessibility rules
- responsive behavior
- RTL behavior if relevant

## Score minimums

- slop score must be itemized and < 6
- premium score must be itemized and >= 15
- any cluster penalty must be stated
- failed items must map to fixes

## Implementation scan optional

When an implementation path is available, validator should scan for:

- raw hex values outside token files
- banned filler phrases
- arbitrary one-off values
- placeholder strings
- banned classes/pattern names
