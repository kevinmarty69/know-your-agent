#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

run_step() {
  local label="$1"
  shift
  echo "[verify-all] $label"
  "$@"
}

run_step "Backend lint/type/tests" bash -lc "cd '$ROOT_DIR/apps/api' && . .venv/bin/activate && ruff check app && mypy app && pytest -q"
run_step "SDK JS test/build" bash -lc "cd '$ROOT_DIR/packages/sdk-js' && npm run test && npm run build"
run_step "SDK Python tests" bash -lc "python -m pytest -q '$ROOT_DIR/packages/sdk-python/tests'"
run_step "Examples smoke" bash -lc "bash '$ROOT_DIR/scripts/examples_smoke.sh'"

echo "[verify-all] All checks passed"
