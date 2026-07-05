from __future__ import annotations

import logging
from pathlib import Path


def configure_logging() -> None:
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        filename="logs/sigesm.log",
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )

    logging.getLogger().info("SIGESM Enterprise iniciado.")
