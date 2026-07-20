# Mode Tiers

## Purpose

Not every screen needs the same ceremony.

This skill has three tiers so the workflow stays practical while preserving strictness for important UI.

## Tier 1 — Light Mode

Use for:

- settings pages
- internal admin forms
- simple utility screens
- low-traffic maintenance screens
- minor component edits

Required:

- product context
- existing token/component reuse
- compact screen spec
- basic slop/premium score
- mechanical validator if project-state files are touched

Optional:

- reference extraction
- sample directions
- blind review

Still required:

- no new visual language without documentation
- no raw values if tokens exist
- no placeholder-only forms
- no inaccessible states

## Tier 2 — Standard Mode

Use for:

- common product screens
- dashboard/list/detail pages
- therapist profile pages
- forms with moderate importance
- components likely to be reused

Required:

- taste profile or inherited product style
- reference DNA if using references
- design-brain judgment from relevant layers only
- token/component contract updates
- screenshot review desktop + mobile
- scorecards
- validator

Relevant layers may include 2–4 of the six design-brain layers, depending on screen type.

## Tier 3 — Full Mode

Use for:

- homepage
- landing page hero
- onboarding/intake
- therapist matching result
- pricing/payment
- first-run experience
- launch-critical screens
- any screen intended to define brand/taste

Required:

- user grilling
- approved references
- reference extraction
- all six design-brain layer judgments
- premium/slop definitions
- sample directions
- user signoff
- token/component contract
- full screen spec
- rendered screenshots desktop/mobile/RTL/states
- loop until pass
- mechanical validator
- blind reviewer or human signoff
- component canonization

## Tier escalation rules

Escalate to a higher tier when:

- a new visual direction is introduced
- a new component family is created
- references are being used
- user says “premium,” “homepage,” “brand,” “conversion,” or “launch”
- sensitive user data or emotional state is involved
- Hebrew/RTL is important

## Tier downgrade rules

A screen may be downgraded only when:

- it uses existing components
- it introduces no new tokens
- it introduces no new pattern
- it is not brand-defining
- it has low user-facing importance

The agent must state the chosen tier and why.
