# Husky Setup

Install Husky in the host app, then add a pre-commit hook that runs the validator.

```bash
npm install --save-dev husky
npx husky init
```

Then edit `.husky/pre-commit`:

```bash
#!/usr/bin/env sh
python3 path/to/skill/scripts/validate_skill_state.py \
  --root path/to/skill \
  --implementation src \
  --require-final-pass
```

Replace `path/to/skill` and `src` with your actual paths.
