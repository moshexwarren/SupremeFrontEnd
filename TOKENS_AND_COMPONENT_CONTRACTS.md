# Tokens and Component Contracts

This file defines what a real token/component contract must contain. A gate cannot pass if these sections are empty.

## Token Contract Minimum

### Color tokens

Must define at least:

```text
color-bg-page
color-bg-surface
color-bg-subtle
color-text-primary
color-text-secondary
color-text-muted
color-border-subtle
color-action-primary
color-action-primary-hover
color-focus-ring
color-error
color-success
```

Each color must include:
- value or range
- role
- usage
- do-not-use notes

Example:

```text
color-action-primary: #2F5D50
Role: primary user action
Use: primary CTA, selected-state emphasis, focus-adjacent accents
Do not use: decorative icons, every badge, large background fills unless approved
```

### Spacing tokens

Minimum:

```text
space-1: 4px
space-2: 8px
space-3: 12px
space-4: 16px
space-6: 24px
space-8: 32px
space-12: 48px
space-16: 64px
space-24: 96px
space-32: 128px
```

Must specify:
- component internal padding
- form-field gaps
- card gaps
- section gaps
- mobile adjustments

### Type tokens

Minimum roles:

```text
type-display
type-page-title
type-section-title
type-card-title
type-body
type-body-muted
type-label
type-caption
type-helper
type-error
type-button
type-input
```

Each type role must include:
- font family
- size desktop/mobile
- weight
- line height
- color token
- alignment rule

### Radius tokens

Minimum:

```text
radius-sm: 4px
radius-md: 8px
radius-lg: 12px or 16px
radius-xl: 24px
radius-pill: 999px
```

Must define which components use each radius.

### Shadow/elevation tokens

Minimum:

```text
elevation-0: none
elevation-1: subtle surface only
elevation-2: popover/active card
elevation-3: modal/overlay
```

Must include actual shadow values or state “no shadows by default”.

### Motion tokens

Minimum:

```text
motion-fast: 120–160ms
motion-base: 180–240ms
motion-slow: 280–360ms
ease-standard
ease-emphasized
```

Must define motion purpose: feedback, transition, orientation, progress. No decorative motion unless approved.

## Component Contract Minimum

Each canonical component must include:

```text
Name:
Purpose:
Use when:
Do not use when:
Anatomy:
Variants:
States:
Content rules:
Accessibility rules:
Responsive rules:
RTL/localization rules:
Tokens used:
Examples:
Anti-examples:
Slop risks:
```

## Required core components for a therapy matching product

At minimum:

1. PrimaryButton
2. SecondaryButton
3. IntakeChoiceChip
4. IntakeQuestionCard or IntakeQuestionBlock
5. TherapistMatchCard
6. TrustNote / PrivacyNote
7. FormField
8. ProgressIndicator
9. EmptyState
10. ErrorMessage

## Example: IntakeChoiceChip

```text
Name: IntakeChoiceChip
Purpose: Lets users select one or more intake answers with low anxiety.
Use when: Short answer choices in intake flow.
Do not use when: Long explanations, high-risk consent, or complex comparisons are needed.
Anatomy: label, optional helper, optional selected icon.
Variants: single-select, multi-select, selected, disabled.
States: default, hover, focus, selected, disabled, error.
Content rules: label max ~40 chars; include “Not sure yet” when relevant.
Accessibility: use button/checkbox/radio semantics; visible focus; aria-pressed or checked.
Responsive: wraps cleanly; target min 44px height where practical.
RTL: text right-aligned in Hebrew; selected icon mirrors placement.
Tokens: type-button, space-3/4, radius-pill or radius-lg, color-border-subtle, color-action-primary.
Anti-example: 20 chips in one ungrouped grid.
Slop risks: fake personalization through excessive options.
```
