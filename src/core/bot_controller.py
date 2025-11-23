"""
Bot Controller - Main orchestration logic

This module controls the entire bot lifecycle:
- Task scheduling
- State management
- Error handling
- Performance monitoring
"""

import asyncio
from typing import Dict, List, Optional

from loguru import logger

from src.core.state_machine import StateMachine
from src.core.task_scheduler import TaskScheduler
from src.device.adb_controller import ADBController
from src.device.emulator_manager import EmulatorManager
from src.vision.yolo_detector import YOLODetector
from src.anti_ban.behavior_randomizer import BehaviorRandomizer
from src.utils.metrics import MetricsCollector


class BotController:
    """
    Main bot controller orchestrating all components
    """

    def __init__(self, config: Dict):
        """
        Initialize bot controller

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.running = False
        self.stopped = False

        # Initialize components
        logger.info("Initializing bot components...")

        # Device control
        self.emulator_manager = EmulatorManager(config.get("emulator", {}))
        self.adb = ADBController(
            config["emulator"]["adb_host"], config["emulator"]["adb_port"]
        )

        # Computer vision
        self.vision = YOLODetector(config.get("ai", {}))

        # Anti-ban
        self.behavior = BehaviorRandomizer(config.get("anti_ban", {}))

        # State machine & scheduler
        self.state_machine = StateMachine(config, self.adb, self.vision, self.behavior)
        self.scheduler = TaskScheduler(config, self.state_machine)

        # Metrics
        self.metrics = MetricsCollector()

        logger.success("Bot components initialized successfully")

    async def preflight_check(self) -> bool:
        """
        Run pre-flight checks before starting

        Returns:
            True if all checks pass, False otherwise
        """
        logger.info("Running pre-flight checks...")

        checks = [
            ("ADB Connection", self._check_adb),
            ("Emulator Status", self._check_emulator),
            ("Game Running", self._check_game_running),
            ("Vision Models", self._check_vision_models),
        ]

        for check_name, check_func in checks:
            logger.info(f"Checking: {check_name}...")
            if not await check_func():
                logger.error(f"❌ {check_name} check failed")
                return False
            logger.success(f"✅ {check_name} check passed")

        logger.success("All pre-flight checks passed!")
        return True

    async def _check_adb(self) -> bool:
        """Check ADB connection"""
        try:
            return await self.adb.connect()
        except Exception as e:
            logger.error(f"ADB connection failed: {e}")
            return False

    async def _check_emulator(self) -> bool:
        """Check emulator status"""
        try:
            return await self.emulator_manager.is_running()
        except Exception as e:
            logger.error(f"Emulator check failed: {e}")
            return False

    async def _check_game_running(self) -> bool:
        """Check if game is running"""
        try:
            # Check for game package
            package = "com.fungame.lastwar"  # Last War package name
            result = await self.adb.shell(f"pidof {package}")
            return bool(result.strip())
        except Exception as e:
            logger.error(f"Game check failed: {e}")
            return False

    async def _check_vision_models(self) -> bool:
        """Check if vision models are loaded"""
        try:
            return self.vision.is_loaded()
        except Exception as e:
            logger.error(f"Vision model check failed: {e}")
            return False

    async def start(self):
        """Start the bot"""
        if self.running:
            logger.warning("Bot is already running")
            return

        logger.info("Starting bot...")
        self.running = True
        self.stopped = False

        # Send start notification
        await self._notify("bot_start", "Bot started successfully")

        try:
            # Main bot loop
            while self.running:
                # Check if should take break (anti-ban)
                if self.behavior.should_take_break():
                    break_duration = self.behavior.get_break_duration()
                    logger.info(f"Taking human-like break for {break_duration / 60:.1f} minutes")
                    await asyncio.sleep(break_duration)
                    continue

                # Get next task from scheduler
                task = await self.scheduler.get_next_task()

                if task:
                    logger.info(f"Executing task: {task['name']}")
                    await self._execute_task(task)
                else:
                    # No tasks, idle for a bit
                    logger.debug("No tasks scheduled, idling...")
                    await asyncio.sleep(60)

                # Random delay between tasks (anti-ban)
                await self.behavior.random_delay(5, 30)

        except Exception as e:
            logger.exception(f"Error in main bot loop: {e}")
            await self._notify("error", f"Bot error: {e}")
        finally:
            self.stopped = True
            await self._notify("bot_stop", "Bot stopped")

    async def _execute_task(self, task: Dict):
        """
        Execute a single task

        Args:
            task: Task dictionary with name and parameters
        """
        task_name = task["name"]
        task_params = task.get("params", {})

        try:
            # Record start time
            start_time = asyncio.get_event_loop().time()

            # Execute via state machine
            result = await self.state_machine.execute_task(task_name, task_params)

            # Record metrics
            duration = asyncio.get_event_loop().time() - start_time
            self.metrics.record_task(task_name, duration, result)

            if result.get("success"):
                logger.success(f"Task '{task_name}' completed successfully")
            else:
                logger.warning(f"Task '{task_name}' failed: {result.get('error')}")

        except Exception as e:
            logger.exception(f"Error executing task '{task_name}': {e}")
            self.metrics.record_error(task_name, str(e))

    async def stop(self):
        """Stop the bot gracefully"""
        logger.info("Stopping bot...")
        self.running = False

        # Wait for current task to finish (max 30 seconds)
        timeout = 30
        while not self.stopped and timeout > 0:
            await asyncio.sleep(1)
            timeout -= 1

        # Cleanup
        await self.adb.disconnect()
        logger.info("Bot stopped")

    def is_stopped(self) -> bool:
        """Check if bot is stopped"""
        return self.stopped

    async def _notify(self, event: str, message: str):
        """
        Send notification

        Args:
            event: Event type (bot_start, bot_stop, error, etc.)
            message: Notification message
        """
        # TODO: Implement notification logic (Telegram, Discord, etc.)
        logger.debug(f"Notification [{event}]: {message}")
