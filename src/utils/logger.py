"""Logger setup utility"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(level: str = "INFO", log_file: bool = True, colorize: bool = True):
    """
    Setup loguru logger

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Enable file logging
        colorize: Colorize console output
    """
    # Remove default handler
    logger.remove()

    # Console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level,
        colorize=colorize,
    )

    # File handler
    if log_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logger.add(
            log_dir / "bot_{time:YYYY-MM-DD}.log",
            rotation="1 day",
            retention="30 days",
            level=level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        )
