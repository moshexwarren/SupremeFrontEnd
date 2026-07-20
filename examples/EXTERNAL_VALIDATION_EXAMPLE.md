# External Validation Example

## Scenario

Screen: Therapli intake step 1
Mode: Full
Screenshot capability: available
Validation path: mechanical validator + blind reviewer

## Implementing agent self-score

Slop: 3
Premium: 17

This is not enough for pass.

## Mechanical validator result

```text
PASS: required project-state files populated
PASS: token contract has 7 color roles, 8 spacing values, 7 type roles, 3 radii, 2 shadows
PASS: component rules include states and accessibility
PASS: slop score itemized and < 6
PASS: premium score itemized and >= 15
WARN: implementation contains 2 raw px values in animation timing; allowed because motion token missing but should be documented
```

## Blind reviewer result

```text
Blind review result: FAIL
Slop score: 7
Premium score: 13
Cluster penalty applied: yes — cards + badges + faint text + centered hero create generic wellness-SaaS feel

Blocking issues:
1. Mobile CTA is below the fold after the first question, breaking action clarity.
2. Hebrew screenshot has cramped chip wrapping and line-height feels tight.
3. Selected state is too subtle; relies on pale border only.

Required fixes:
1. Add sticky mobile CTA after selection.
2. Increase Hebrew body line-height from 1.48 to 1.58.
3. Use selected chip fill + border + checkmark, not border only.
```

## Result

Final status: FAIL — revise required.

Even though the implementing agent self-score passed, blind review failed.

## After revision

Validator: PASS
Blind reviewer:

```text
Slop score: 2
Premium score: 17
Result: PASS
```

Final status:

```text
PASS — externally validated
```
