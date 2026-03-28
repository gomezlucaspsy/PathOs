"""
Logging infrastructure for PathOs.

Provides structured logging with multiple handlers.
"""

from __future__ import annotations
import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from pathos.infrastructure.config import Settings


def configure_logging(settings: Settings) -> logging.Logger:
    """Configure logging based on settings."""
    logger = logging.getLogger("pathos")
    logger.setLevel(settings.logging.level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Formatter
    formatter = logging.Formatter(settings.logging.format)
    
    # Console handler
    if settings.logging.console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if settings.logging.file:
        log_path = Path(settings.logging.file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            settings.logging.file,
            maxBytes=10485760,  # 10MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(f"pathos.{name}")
