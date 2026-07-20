# Loop Until Pass Protocol

## Goal

The AI loops until the UI matches the approved direction and passes slop/premium gates. “Looks good” is not a stopping condition.

## Required loop cycle

1. Build or revise UI.
2. Render in real browser/app environment.
3. Capture screenshots:
   - desktop
   - mobile
   - RTL/Hebrew if relevant
   - key states: default, selected, loading, error, empty if relevant
4. Compare screenshots to:
   - approved design direction
   - token contract
   - component rules
   - design-brain rules
5. Score:
   - slop score
   - premium score
   - accessibility basics
   - reference fidelity without cloning
6. Identify exact failures.
7. Patch implementation.
8. Repeat.

## Screenshot review questions

- What is the first thing the eye sees?
- Is the primary action obvious?
- Does it resemble approved references in principles, not pixels?
- Are there generic AI slop clusters?
- Are components reused?
- Are tokens used consistently?
- Does mobile preserve hierarchy and action?
- Does Hebrew/RTL feel native?
- Are selected/error/loading/empty states visually clear?
- Does real content fit?

## Stop conditions

Stop only when:
- slop score < 6
- premium score >= 15
- all phase gate blockers resolved
- no reference-copy issue
- no major mobile/RTL/accessibility issue
- token/component drift resolved or documented

## Loop report template

```text
Loop number:
Screenshots reviewed:
Slop score:
Premium score:
Blocking issues:
Non-blocking issues:
Fixes applied:
Remaining risks:
Pass/fail:
Next action:
```


---

# v3 External Loop Requirement

The loop has two stages:

## Stage 1 — Implementer loop

The implementing agent may self-score and revise until it believes the UI passes.

This creates `SCREENSHOT_REVIEW_REPORT.md` and `LOOP_REPORT.md`.

## Stage 2 — External validation loop

After implementer self-pass:

1. Run `scripts/validate_skill_state.py --root <skill-or-project-root>`.
2. If implementation source exists, also run:

```bash
python scripts/validate_skill_state.py --root . --implementation path/to/app/src
```

3. Send screenshots and required project-state files to a blind reviewer using `prompts/BLIND_REVIEWER_PROMPT.md`.
4. Apply the validator/reviewer fixes.
5. Repeat until both pass.

## New stop conditions

The UI stops only when:

- implementer self-score passes
- mechanical validator passes
- blind reviewer or human signoff passes
- screenshot hard-stop is satisfied
- final status is written to `project-state/FINAL_STATUS.md`

If any external validation fails, the loop continues.


---

# v6 Reference-Match Addendum

Screenshot existence is not enough. After rendered screenshots are captured, compare them to real approved reference screenshots or design exports. The reviewer must judge composition, hierarchy, density, mood, typography posture, contrast rhythm, and presence.

Use `project-state/VISUAL_REFERENCE_MATCH_REPORT.md`. Final pass fails if the report is missing, lacks provenance, has an average below the configured threshold, or has any category below the configured minimum.

The implementer may fix defects, but the human-selected visual thesis must not be sanded down into the safe median.
