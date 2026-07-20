# Project State Filechain

These files are runtime-filled by the agent as the workflow progresses.

The filechain is deliberately separate from the static skill files. Static files define the method; project-state files store the current project's taste, references, contracts, loops, and final status.

## Phase 0 — Mode and validation

```text
project-state/MODE_TIER.md
```

Must define Light / Standard / Full mode, screenshot capability, and external validation path.

## Phase 1 — Product and taste

```text
project-state/PRODUCT_CONTEXT.md
project-state/DESIGN_TASTE_PROFILE.md
project-state/ANTI_TARGETS.md
```

## Phase 2 — Reference discovery and approval

```text
project-state/REFERENCE_SHORTLIST.md
project-state/APPROVED_REFERENCES.md
```

## Phase 3 — Reference extraction

```text
project-state/APPROVED_REFERENCE_DNA.md
project-state/DO_NOT_COPY.md
project-state/SLOP_RISKS.md
```

## Phase 4 — Design synthesis

```text
project-state/DESIGN_BRAIN_JUDGMENT.md
project-state/PREMIUM_DEFINITION.md
project-state/AI_SLOP_CLUSTER_RULES.md
project-state/SAMPLE_DIRECTIONS.md
project-state/APPROVED_DESIGN_DIRECTION.md
```

## Phase 5 — Build contract

```text
project-state/TOKEN_CONTRACT.md
project-state/COMPONENT_RULES.md
project-state/FRONTEND_SCREEN_SPEC.md
```

## Phase 6 — Screenshot loop

```text
project-state/SCREENSHOT_REVIEW_REPORT.md
project-state/LOOP_REPORT.md
```

## Phase 7 — External validation

```text
project-state/VALIDATION_REPORT.md
project-state/BLIND_REVIEW_REPORT.md
project-state/FINAL_STATUS.md
```

## Phase 8 — Canonization

```text
project-state/COMPONENT_CANONIZATION_LOG.md
project-state/REJECTED_PATTERNS.md
```

## Required sequence

The agent should not skip ahead. Each later file should reference earlier decisions.

Example:

- `FRONTEND_SCREEN_SPEC.md` should reference `APPROVED_DESIGN_DIRECTION.md` and `TOKEN_CONTRACT.md`.
- `SCREENSHOT_REVIEW_REPORT.md` should score against `FRONTEND_SCREEN_SPEC.md`.
- `VALIDATION_REPORT.md` should record the validator command and result.
- `FINAL_STATUS.md` should cite validator + blind review/human approval status.

## Filechain integrity rules

- No project-state file may contain only placeholders.
- “Premium/modern/clean” must be accompanied by mechanisms.
- Any new token/component must be reflected in the appropriate contract.
- Any rejected pattern must be recorded so the AI does not repeat it.
- Final pass cannot be claimed from self-score alone.
