# Final Status

Set exactly one status before validation.

Allowed statuses are defined in `VALIDATOR_CONFIG.json`:

- PASS_EXTERNALLY_VALIDATED
- FAIL_REVISE_REQUIRED
- BLOCKED_SCREENSHOT_UNAVAILABLE
- SPEC_COMPLETE_UNVERIFIED
- DRAFT_SELF_SCORE_ONLY

Current status:

DRAFT_SELF_SCORE_ONLY

## Evidence required for PASS_EXTERNALLY_VALIDATED

- Validator run with `--require-final-pass` exits `0`.
- Desktop/mobile screenshots are referenced in `SCREENSHOT_REVIEW_REPORT.md`.
- Blind reviewer report was produced in a clean separate context.
- Blind reviewer report says pass.
- Slop and premium thresholds pass according to `VALIDATOR_CONFIG.json`.
