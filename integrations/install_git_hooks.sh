#!/usr/bin/env bash
set -euo pipefail

# Installs a local git pre-commit hook that runs the AI-slop skill validator.
# Run from the repository root that contains this skill folder.
# Usage:
#   bash path/to/skill/integrations/install_git_hooks.sh
# Optional:
#   SKILL_DIR=path/to/skill IMPLEMENTATION_DIR=src bash path/to/skill/integrations/install_git_hooks.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_DIR="${SKILL_DIR:-$DEFAULT_SKILL_DIR}"
IMPLEMENTATION_DIR="${IMPLEMENTATION_DIR:-src}"
HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

if [ ! -d .git ]; then
  echo "ERROR: run this from a git repository root." >&2
  exit 1
fi
if [ ! -f "$SKILL_DIR/scripts/validate_skill_state.py" ]; then
  echo "ERROR: validator not found at $SKILL_DIR/scripts/validate_skill_state.py" >&2
  exit 1
fi

mkdir -p "$HOOK_DIR"
cat > "$HOOK_FILE" <<EOF_HOOK
#!/usr/bin/env bash
set -euo pipefail

echo "Running AI-slop front-end validation..."
python3 "$SKILL_DIR/scripts/validate_skill_state.py" --root "$SKILL_DIR" --implementation "$IMPLEMENTATION_DIR" --require-final-pass
EOF_HOOK
chmod +x "$HOOK_FILE"

echo "Installed $HOOK_FILE"
echo "Validator will block commits unless FINAL_STATUS is PASS_EXTERNALLY_VALIDATED and gates pass."
