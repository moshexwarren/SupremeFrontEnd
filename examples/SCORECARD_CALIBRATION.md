# Scorecard Calibration Example

## Screen A: Bad AI intake

Description:
- centered purple gradient hero
- headline: “Unlock your personalized wellness journey”
- three floating cards
- 18 ungrouped pastel choice chips
- low-contrast helper text
- CTA: “Get Started”
- no progress
- no privacy note
- no clear selected state

Slop score:
- generic SaaS language: 2
- decorative noise: 2
- hierarchy weakness: 1
- spacing randomness: 1
- card overuse: 2
- effects overuse: 2
- vague copy: 2
- unclear path: 1
- component inconsistency: 1
- real-content fragility: 2
Subtotal: 16
Cluster penalty: +3 purple SaaS soup
Total: 19

Premium score:
- restraint: 0
- clarity: 1
- emotional fit: 0
- component consistency: 1
- typography quality: 0
- spacing rhythm: 1
- real-content handling: 0
- accessibility: 0
- mobile/RTL: 0
- trust/specificity: 0
Total: 3

Verdict: fail.

## Screen B: Good guided intake

Description:
- neutral page background
- compact page title: “Let’s find the right kind of support”
- question block: “What are you looking for help with?”
- grouped choice chips: emotional stress, relationships, parenting, religious/cultural fit, not sure yet
- progress: “Question 1 of 5”
- privacy note: “Your answers are used only to suggest a fit.”
- CTA: “Continue to preferences”
- selected state: border + fill + check icon + aria state
- mobile chip wrap tested
- Hebrew version right-aligned

Slop score:
- generic language: 0
- decorative noise: 0
- hierarchy: 0
- spacing: 0
- card overuse: 0
- effects: 0
- vague copy: 0
- unclear path: 0
- inconsistency: 1
- content fragility: 1
Total: 2

Premium score:
- restraint: 2
- clarity: 2
- emotional fit: 2
- component consistency: 1
- typography: 2
- spacing: 2
- content handling: 1
- accessibility: 2
- mobile/RTL: 2
- trust/specificity: 2
Total: 18

Verdict: pass.
