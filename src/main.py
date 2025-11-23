#!/usr/bin/env python3
"""
LastWarAutoBot Pro - Main Entry Point

This is the main entry point for the bot. It handles:
- Command-line argument parsing
- Configuration loading
- Bot initialization
- Graceful shutdown

Author: LastWarAutoBot Contributors
License: MIT (Educational Use Only)
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

import click
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from core.bot_controller import BotController
from utils.config_loader import load_config
from utils.logger import setup_logger


class GracefulShutdown:
    """Handle graceful shutdown on SIGINT/SIGTERM"""

    def __init__(self):
        self.shutdown_requested = False

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.warning(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_requested = True


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True),
    default="configs/default.yaml",
    help="Path to configuration file",
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["bot", "dashboard", "api"]),
    default="bot",
    help="Run mode: bot (automation), dashboard (web UI), or api (API server)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Simulate actions without executing (testing mode)",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default=None,
    help="Override log level from config",
)
def main(
    config: str,
    mode: str,
    dry_run: bool,
    debug: bool,
    log_level: Optional[str],
):
    """
    LastWarAutoBot Pro - AI-Powered Automation for Last War: Survival

    \b
    Examples:
        # Run with default config
        python src/main.py

        # Run with custom config
        python src/main.py --config configs/myconfig.yaml

        # Dry run (testing)
        python src/main.py --dry-run

        # Debug mode
        python src/main.py --debug

        # Run web dashboard
        python src/main.py --mode dashboard

    \b
    WARNING: This bot is for EDUCATIONAL PURPOSES ONLY.
    Using bots violates Last War's Terms of Service and may result in bans.
    """

    # ASCII Art Banner
    print_banner()

    # Load configuration
    try:
        bot_config = load_config(config)
        logger.info(f"Loaded configuration from: {config}")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

    # Override settings
    if debug or dry_run:
        bot_config["advanced"]["debug_mode"] = True
    if dry_run:
        bot_config["advanced"]["dry_run"] = True
        logger.warning("🔶 DRY RUN MODE: Actions will be simulated, not executed")

    # Setup logging
    log_level = log_level or bot_config.get("logging", {}).get("level", "INFO")
    setup_logger(
        level=log_level,
        log_file=bot_config.get("logging", {}).get("file_logging", True),
        colorize=bot_config.get("logging", {}).get("colorize_console", True),
    )

    # Determine mode
    if mode == "bot":
        # Run automation bot
        asyncio.run(run_bot(bot_config))
    elif mode == "dashboard":
        # Run web dashboard
        from api.app import run_dashboard

        run_dashboard(bot_config)
    elif mode == "api":
        # Run API server
        from api.rest_api import run_api_server

        run_api_server(bot_config)


async def run_bot(config: dict):
    """
    Run the automation bot

    Args:
        config: Bot configuration dictionary
    """
    # Setup graceful shutdown
    shutdown_handler = GracefulShutdown()

    # Initialize bot controller
    logger.info("Initializing bot controller...")
    bot = None

    try:
        bot = BotController(config)

        # Pre-flight checks
        logger.info("Running pre-flight checks...")
        if not await bot.preflight_check():
            logger.error("Pre-flight checks failed. Aborting.")
            return

        # Start bot
        logger.success("✅ All systems ready. Starting bot...")
        await bot.start()

        # Main loop
        while not shutdown_handler.shutdown_requested:
            await asyncio.sleep(1)

            # Check if bot stopped
            if bot.is_stopped():
                logger.info("Bot stopped naturally.")
                break

    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt received")
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
    finally:
        # Cleanup
        if bot:
            logger.info("Stopping bot gracefully...")
            await bot.stop()
            logger.success("✅ Bot stopped successfully")


def print_banner():
    """Print ASCII art banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         ██╗      █████╗ ███████╗████████╗                ║
    ║         ██║     ██╔══██╗██╔════╝╚══██╔══╝                ║
    ║         ██║     ███████║███████╗   ██║                   ║
    ║         ██║     ██╔══██║╚════██║   ██║                   ║
    ║         ███████╗██║  ██║███████║   ██║                   ║
    ║         ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝                   ║
    ║                                                           ║
    ║              WAR: SURVIVAL AUTO BOT PRO                   ║
    ║                                                           ║
    ║                  AI-Powered Automation                    ║
    ║                  YOLOv8 + OpenCV + ADB                    ║
    ║                                                           ║
    ╠═══════════════════════════════════════════════════════════╣
    ║  ⚠️  EDUCATIONAL PURPOSE ONLY - USE AT YOUR OWN RISK ⚠️   ║
    ║  Using bots violates game ToS and may result in bans     ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


if __name__ == "__main__":
    main()
