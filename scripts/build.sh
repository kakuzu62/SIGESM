#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [ ! -x "$PYTHON" ]; then
  PYTHON="python"
fi

"$PYTHON" "$PROJECT_ROOT/build/build.py"
