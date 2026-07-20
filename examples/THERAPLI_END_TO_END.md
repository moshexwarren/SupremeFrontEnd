# End-to-End Example: Therapli Intake Screen

This example shows the skill’s intended depth. It is not a placeholder.

## Phase 1 — Taste profile

Product: Therapli, a therapy matching product.

User emotional states:
- uncertain about what kind of therapist they need
- private/sensitive about sharing personal issues
- wants guidance without feeling judged

Desired feelings:
- calm
- competent
- human
- guided
- trustworthy

Anti-targets:
- generic wellness pastel blob site
- purple SaaS AI gradient
- clinical hospital portal
- gimmicky chatbot
- fake luxury minimalism

Language:
- Hebrew and English required
- RTL must feel native, not mirrored late

## Phase 2 — References

Approved references:

1. Reference A — editorial health app onboarding
Role: spacing, calm progression, progress cues
Borrow: step rhythm, trust note placement
Do not borrow: exact colors, illustrations

2. Reference B — premium booking/concierge service
Role: card restraint and CTA hierarchy
Borrow: low-noise cards, strong primary action
Do not borrow: luxury tone, tiny gray text

3. Reference C — form-heavy product with excellent labels
Role: input/chip clarity
Borrow: persistent labels, helper text style, selected states
Do not borrow: dense enterprise layout

## Phase 3 — Extracted DNA

Layout DNA:
- one focused question per screen
- centered container max ~680px desktop
- left/right aligned by locale
- progress visible above question
- privacy note near CTA

Typography DNA:
- calm product sans
- page title 30–36px desktop, 24–28px mobile
- body 16–18px, line-height 1.5
- labels 14–16px, 500/600 weight
- muted text readable, not below safe contrast

Color DNA:
- warm neutral background
- white or subtle surface
- one deep calm action color
- border-subtle for chips/cards
- selected chip uses light action tint + action border + check

Spacing DNA:
- page top 64–96 desktop, 32–48 mobile
- question/title stack 8–16
- chip gap 8–12
- CTA block gap 24–32
- section/form gap 40–64

Component DNA:
- IntakeQuestionBlock
- IntakeChoiceChip
- ProgressIndicator
- PrivacyNote
- PrimaryButton
- SecondaryBackButton

## Phase 4 — Design-brain judgment

Polish:
- hierarchy should come from focused question + spacing, not decoration
- no floating cards or icon grid

Practical UI:
- chips require clear selected state
- button label must describe outcome: “Continue to preferences”

Obviousness:
- user must understand this is an intake flow, not a marketing page
- progress and back action visible

System:
- chips and buttons must be canonical components
- no new chip variant per question

Typography:
- Hebrew right-aligned with equivalent hierarchy
- body text max width controlled

Behavioral UX:
- limit options to 6–8 visible; include “Not sure yet”
- progress reduces anxiety

## Phase 5 — Premium/slop definition

Premium means:
- calm guidance
- clear choices
- privacy reassurance
- no hype
- native RTL
- compact but not rushed

Slop risks:
- pastel wellness cliche
- too many chips
- chatbot pretending to be human
- vague “journey” language
- no selected state

## Phase 6 — Sample directions

### Direction 1: Warm Human Guide
Layout: focused question flow, warm neutral background, large but calm type.
Components: rounded chips, privacy note, simple progress.
Risk: may become too soft/wellness if colors too pastel.

### Direction 2: Premium Concierge Matching
Layout: sparse, high-touch, card-like intake panel, refined type.
Components: subdued chips, strong CTA, crisp progress.
Risk: fake premium if text too tiny or whitespace too huge.

### Direction 3: Calm Clinical Trust
Layout: clean, white, more healthcare-adjacent, high clarity.
Components: simple forms, visible privacy, minimal decoration.
Risk: may feel cold or institutional.

Approved: Direction 1 with restraint from Direction 2.

## Phase 7 — Screen spec

Screen: Intake question 1

Three-second message:
“You are answering a few private questions so the product can suggest a therapist fit.”

Primary action:
Continue to preferences

Components:
- ProgressIndicator
- IntakeQuestionBlock
- IntakeChoiceChip
- PrivacyNote
- PrimaryButton
- SecondaryButton

States:
- no selection: CTA disabled with helper “Choose at least one, or select Not sure yet.”
- selected: chip tint + check + aria-pressed
- loading: button “Saving...”
- error: “Choose at least one option before continuing.”

RTL:
- container direction RTL
- Hebrew text right-aligned
- check icon moves to right side of chip
- progress reads naturally in Hebrew

## Phase 8 — Token contract excerpt

```text
color-bg-page: #F7F4EF
color-bg-surface: #FFFFFF
color-text-primary: #1F2421
color-text-secondary: #4F5A55
color-text-muted: #6F7A75
color-border-subtle: #DAD7CF
color-action-primary: #2F5D50
color-action-primary-hover: #244A40
color-action-tint: #E7F0EC
color-focus-ring: rgba(47,93,80,.35)

space-2: 8px
space-3: 12px
space-4: 16px
space-6: 24px
space-8: 32px
space-12: 48px
space-16: 64px

radius-md: 10px
radius-lg: 16px
radius-pill: 999px

type-page-title: 34px/1.15 600
type-section-title: 24px/1.2 600
type-body: 16px/1.55 400
type-label: 14px/1.35 500
type-button: 15px/1 600
```

## Phase 9 — First screenshot review

Findings:
- title hierarchy good
- chips too many in one block: 10 visible
- privacy note too low, not near sensitive question
- mobile CTA below long chip list
- selected state clear
- Hebrew line-height slightly cramped

Slop score:
- generic copy 0
- decorative noise 0
- hierarchy 0
- spacing 1
- card overuse 0
- effects 0
- vague copy 0
- unclear path 1
- inconsistency 0
- content fragility 1
Total: 3

Premium score:
- restraint 2
- clarity 2
- emotional fit 2
- component consistency 2
- typography 1
- spacing 1
- real-content 1
- accessibility 2
- mobile/RTL 1
- trust/specificity 2
Total: 16

Pass? Conditional. Fix mobile CTA and Hebrew line-height.

## Phase 10 — Revision

Fixes:
- reduce first question to 6 common options + “Not sure yet”
- move privacy note below question and above choices
- make mobile CTA sticky within bottom safe area only after selection
- increase Hebrew body line-height from 1.48 to 1.58

## Phase 11 — Second review

Slop score: 2
Premium score: 18
Mobile: pass
RTL: pass
Accessibility: pass

## Phase 12 — Canonization

Canonized:
- IntakeChoiceChip
- ProgressIndicator
- PrivacyNote
- PrimaryButton
- intake screen spacing rhythm

Rejected:
- pastel blob background
- 10+ chip grids in first question
- vague “journey” copy
- selected state by border-only
