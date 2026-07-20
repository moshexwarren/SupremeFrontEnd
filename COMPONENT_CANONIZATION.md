# Component Canonization

## Purpose

Once a component, token, or layout pattern works, freeze it so future agents do not redesign it.

## Canonization trigger

Canonize after:
- user approval
- screenshot review pass
- slop score < 6
- premium score >= 15
- component states verified
- accessibility basics verified
- mobile/RTL verified if relevant

## Canonization log entry

```text
Component/token/pattern name:
Date:
Where approved:
Purpose:
Tokens used:
Allowed variants:
States:
Accessibility rules:
Responsive rules:
RTL rules:
Content rules:
Examples:
Anti-examples:
Do not change without:
```

## Rejected patterns log

Record patterns the user rejected, including subtle variants.

Example:

```text
Rejected: pastel blob wellness background
Reason: feels generic/soft wellness, not serious therapy guidance
Avoid in: hero, intake, empty states
Possible acceptable version: none unless user explicitly requests softer wellness direction
```

## Future-agent rule

Before creating any new UI pattern, the agent must check:

1. Does a canonical component already solve this?
2. Can an existing variant solve this?
3. Is a new component justified by a recurring need?
4. Can it be documented immediately?

No silent component invention.
