# screenshots/

The validator requires REAL image files here not text mentions in a report.

Expected (see `VALIDATOR_CONFIG.json > screenshot_artifacts`):
- `desktop.png` (or .jpg/.webp), min 320x320
- `mobile.png` (or .jpg/.webp), min 320x320
- add `rtl.png`, `dark.png`, etc. as your states require and add them to `required_states`.

Capture these from a real render (e.g. Playwright). If you cannot render, do not fake it set the screenshot report to BLOCKED and the final status to `BLOCKED_SCREENSHOT_UNAVAILABLE`.
