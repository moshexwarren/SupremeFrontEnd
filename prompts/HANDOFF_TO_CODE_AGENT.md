# Prompt: Handoff to Coding Agent

Read these files first:

1. SKILL.md
2. WORKFLOW.md
3. DESIGN_BRAIN.md
4. PHASE_GATES.md
5. SCORECARDS.md
6. project-state/APPROVED_DESIGN_DIRECTION.md
7. project-state/TOKEN_CONTRACT.md
8. project-state/COMPONENT_RULES.md
9. project-state/FRONTEND_SCREEN_SPEC.md

Task:
Implement the specified screen using approved tokens/components and the approved direction.

Hard rules:
- no raw styling values if token exists
- no new component/variant without justification
- no generic AI SaaS patterns
- implement states
- capture screenshots
- score and revise until pass

---

# v3 Enforcement Requirements for Coding Agent

Before coding, declare:

```text
Mode tier:
Screenshot capability:
External validation path:
Final-pass eligibility:
```

After coding:

1. Render real UI screenshots.
2. Fill `project-state/SCREENSHOT_REVIEW_REPORT.md` and `project-state/LOOP_REPORT.md`.
3. Run:

```bash
python scripts/validate_skill_state.py --root . --implementation path/to/app/src
```

4. Do not provide final pass until a blind reviewer or human also approves.

Allowed final statuses only:

```text
PASS — externally validated
FAIL — revise required
BLOCKED — screenshot unavailable
SPEC COMPLETE — implementation not visually verified
DRAFT — self-score only
```

## One-shot inputs (use these at generation, do not default to the mean)
- ORGANIZING_IDEA.md — build the layout around this concept; it is the anti-slop backbone.
- REAL_CONTENT.md — lay the page out around this real copy, not placeholder structure.
- screenshots/refs/*.png — the pixel anchor; match feel to these, not to the word "modern".
- Restraint: <= 2 font families, <= 3 weights, minimal palette. Premium = subtraction.
