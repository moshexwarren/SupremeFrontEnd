# Content-Validating Phase Gates

A gate passes only when content requirements are met. File existence alone is not enough.

## Gate 1 — Taste Profile Gate

Required files:
- PRODUCT_CONTEXT.md
- DESIGN_TASTE_PROFILE.md
- ANTI_TARGETS.md

Required content:
- product category
- primary user
- top 3 user emotional states
- top 5 desired feelings
- top 5 anti-targets
- language/RTL requirements
- 8+ visual preferences or explicit unknowns
- 5+ interaction preferences or explicit unknowns

Fail if:
- “premium/modern/clean” appears without mechanisms
- anti-targets are vague only

## Gate 2 — Reference Approval Gate

Required files:
- REFERENCE_SHORTLIST.md
- APPROVED_REFERENCES.md

Required content:
- 5+ candidate references or explanation why fewer
- each reference assigned a role
- each approved reference has “borrow” and “do not borrow” notes

Fail if:
- multiple references are approved without layer assignment

## Gate 3 — Design DNA Gate

Required files:
- APPROVED_REFERENCE_DNA.md
- DO_NOT_COPY.md
- SLOP_RISKS.md

Required content per reference:
- layout DNA
- typography DNA
- color DNA
- spacing DNA
- component DNA
- interaction/usability DNA
- token-like values or explicit unavailable
- 5+ do-not-copy items
- 3+ slop risks

Fail if:
- output says “nice/clean/modern” without mechanisms

## Gate 4 — Style Synthesis Gate

Required files:
- DESIGN_BRAIN_JUDGMENT.md
- PREMIUM_DEFINITION.md
- AI_SLOP_CLUSTER_RULES.md
- SAMPLE_DIRECTIONS.md

Required content:
- applied judgment from all 6 design-brain layers
- 8+ premium signals
- 5+ slop clusters
- 3–5 original sample directions
- user-approved direction or explicit pending status

Fail if:
- sample directions copy references directly
- directions are only mood names without layout/type/color/component specifics

## Gate 5 — Build Spec Gate

Required files:
- TOKEN_CONTRACT.md
- COMPONENT_RULES.md
- FRONTEND_SCREEN_SPEC.md

Required content:
- token contract includes actual values/ranges, not placeholders
- component rules include states and accessibility
- screen spec includes primary action, states, mobile, RTL if relevant, slop risks

Fail if:
- raw hex/px values are used in components without token update
- new component created without usage rules

## Gate 6 — Screenshot Loop Gate

Required files:
- SCREENSHOT_REVIEW_REPORT.md
- LOOP_REPORT.md

Required content:
- desktop screenshot review
- mobile screenshot review
- RTL review if relevant
- slop score with itemized scoring
- premium score with itemized scoring
- exact fixes from each failed score
- loop count

Pass criteria:
- slop score < 6
- premium score >= 15
- no blocking accessibility issue
- no unapproved reference copying
- no unapproved component/token drift

## Gate 7 — Canonization Gate

Required files:
- COMPONENT_CANONIZATION_LOG.md
- REJECTED_PATTERNS.md

Required content:
- approved tokens/components/patterns listed
- variants documented
- rejected patterns recorded
- what to reuse next time
- what not to repeat


---

# v3 Gate 0 — Mode and Validation Declaration

Before Gate 1, create `project-state/MODE_TIER.md`.

Required content:

- selected tier: Light / Standard / Full
- reason for tier
- external validation path
- screenshot capability
- final-pass eligibility

Fail if:

- no tier is selected
- user-facing important screen is downgraded without explanation
- screenshot capability is unknown
- final-pass eligibility is claimed while screenshots are unavailable

# v3 Gate 8 — External Validation Gate

Required files:

- `project-state/VALIDATION_REPORT.md`
- `project-state/BLIND_REVIEW_REPORT.md` or explicit human signoff note
- `project-state/FINAL_STATUS.md`

Required content:

- validator command used
- validator exit code
- validator failures/warnings
- blind reviewer scores or human approval
- final allowed status

Pass criteria for Full Mode:

- mechanical validator exit code 0
- blind reviewer slop score < 6
- blind reviewer premium score >= 15
- screenshot hard-stop satisfied
- final status is `PASS — externally validated`

Fail if:

- the same implementing agent provides the only final score
- validator was not run
- screenshots were unavailable but final pass is claimed
- final status uses any phrase outside the allowed status list
