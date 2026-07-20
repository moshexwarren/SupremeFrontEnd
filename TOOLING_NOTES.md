# Tooling Notes

## Tool-agnostic principle

The skill describes what must happen. Tools are interchangeable.

## Helpful tools

### Hallmark-style design study
Use for URL/screenshot design DNA extraction, hierarchy/layout/component analysis, and avoiding pixel clones.

### design-extract-style token extraction
Use for colors, spacing, type sizes, radius, shadows, CSS variables, and Tailwind clues.

### Browser automation / Playwright
Use for rendering real UI, screenshots, mobile viewport checks, console errors, and interaction states.

### Figma
Use for sample direction boards, user signoff, and token/component reference.

## Claude Code / Codex guidance

Put this skill folder in project context. Tell the agent:

```text
Read SKILL.md first.
Use WORKFLOW.md for phase order.
Use PHASE_GATES.md as hard gates.
Use DESIGN_BRAIN.md for judgment.
Use SCORECARDS.md for calibration.
Use ENFORCEMENT.md for final-pass rules.
Do not implement until the required prior files pass content gates.
```

## No tools available

If no screenshot/browser tools are available, the skill can still:

- ask questions
- organize references
- produce design briefs
- create token/component contracts
- generate implementation specs

But it must mark screenshot review as pending, not passed. Final status should be `BLOCKED_SCREENSHOT_UNAVAILABLE` or `SPEC_COMPLETE_UNVERIFIED`, not `PASS_EXTERNALLY_VALIDATED`.

## Mechanical validator

Run from the skill/project root:

```bash
python3 scripts/validate_skill_state.py --root .
```

With app source scanning:

```bash
python3 scripts/validate_skill_state.py --root . --implementation ../app/src
```

JSON output:

```bash
python3 scripts/validate_skill_state.py --root . --implementation ../app/src --json
```

Final/deploy mode:

```bash
python3 scripts/validate_skill_state.py --root . --implementation ../app/src --require-final-pass
```

## Binding outside agent goodwill

Highest-value setup:

1. Put this skill folder inside the repo.
2. Install the git hook with `integrations/install_git_hooks.sh`.
3. Add the `predeploy` script from `integrations/package-json-scripts.example.json`.
4. Run blind review in a second clean agent session or review screenshots yourself.

Without steps 2–4, the skill remains discipline-prompting rather than binding.
