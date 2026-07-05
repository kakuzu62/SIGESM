from __future__ import annotations

from sigesm.bootstrap import build_application
from sigesm.presentation.qt.app import run_qt_application


def main() -> int:
    application = build_application()
    return run_qt_application(application)


if __name__ == "__main__":
    raise SystemExit(main())
