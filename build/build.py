from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Build the SIGESM desktop executable with PyInstaller."""
    root = Path(__file__).resolve().parents[1]
    spec_file = root / "build" / "build.spec"
    command = [sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm", str(spec_file)]
    completed = subprocess.run(command, cwd=root, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
