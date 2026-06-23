"""Logging utility for Opsie services."""

import logging
import sys


def get_logger(service_name: str, log_level: str = "INFO") -> logging.Logger:
    """Unified logging factory used uniformly across all Opsie services."""
    logger = logging.getLogger(service_name)
    logger.setLevel(log_level.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            f"[%(asctime)s] %(levelname)s [{service_name}] in %(module)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
