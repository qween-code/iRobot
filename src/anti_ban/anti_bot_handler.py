"""
Anti-Bot Modal Handler

Last War includes an anti-bot system that shows modal dialogs
when suspicious behavior is detected. This module handles:
- Detecting anti-bot modals
- Automatically closing them
- Adapting behavior to avoid triggering them
- Logging detection events for analysis

Based on research from:
- github.com/davidbourrel/BOT-for-Last-War-vice-president
  (CheckAndCloseAntiBotModal function)
- Community reports of anti-bot detection in Last War
"""

import asyncio
import time
from typing import Dict, Optional, Tuple
from datetime import datetime
from loguru import logger
import numpy as np


class AntiBotHandler:
    """
    Handle Last War's anti-bot detection system

    Last War displays modal dialogs when it suspects bot activity.
    This module detects and dismisses these modals while adapting
    bot behavior to reduce future detections.
    """

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize anti-bot handler

        Args:
            config: Anti-ban configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config
        self.adb = adb
        self.vision = vision
        self.behavior = behavior

        # Detection tracking
        self.detection_count = 0
        self.last_detection_time = None
        self.detection_history = []

        # Alert escalation thresholds
        self.warning_threshold = 3   # Yellow alert
        self.danger_threshold = 5    # Red alert - pause bot
        self.critical_threshold = 10  # Critical - stop bot

        # Known anti-bot modal templates
        self.modal_templates = [
            "anti_bot_modal",
            "captcha_dialog",
            "verification_popup",
            "security_check",
            "are_you_human",
        ]

        logger.info("Anti-Bot Handler initialized")

    async def check_and_close(self, screenshot: Optional[np.ndarray] = None) -> bool:
        """
        Check for and close anti-bot modal

        Args:
            screenshot: Current screenshot (captures new if None)

        Returns:
            True if modal was detected and closed
        """
        if screenshot is None:
            screenshot = await self.adb.screenshot()

        # Check for known anti-bot modal patterns
        for modal_template in self.modal_templates:
            modal_pos = self.vision.find_button(screenshot, modal_template)

            if modal_pos:
                logger.warning(f"Anti-bot modal detected: {modal_template}")
                await self._handle_detection(modal_template, screenshot)
                return True

        # Check for unexpected popup (generic close button detection)
        close_btn = self.vision.find_button(screenshot, "close_button")
        if close_btn:
            # Verify it's an anti-bot popup (not a regular dialog)
            if await self._is_antibot_popup(screenshot):
                logger.warning("Generic anti-bot popup detected")
                await self._handle_detection("generic_popup", screenshot)
                return True

        return False

    async def _handle_detection(self, modal_type: str, screenshot: np.ndarray):
        """
        Handle anti-bot modal detection

        Args:
            modal_type: Type of modal detected
            screenshot: Screenshot with modal
        """
        # Record detection
        self.detection_count += 1
        self.last_detection_time = datetime.now()
        self.detection_history.append({
            "type": modal_type,
            "timestamp": datetime.now().isoformat(),
            "count": self.detection_count
        })

        logger.warning(
            f"Anti-bot detection #{self.detection_count} "
            f"(type: {modal_type})"
        )

        # Save screenshot for analysis
        await self._save_detection_screenshot(screenshot, modal_type)

        # Step 1: Close the modal
        await self._close_modal(screenshot)

        # Step 2: Wait random time (look human)
        wait_time = min(30 + self.detection_count * 15, 300)  # 30s to 5min
        logger.info(f"Waiting {wait_time}s after detection...")
        await asyncio.sleep(wait_time)

        # Step 3: Escalate if too many detections
        await self._check_escalation()

    async def _close_modal(self, screenshot: np.ndarray):
        """
        Close the anti-bot modal

        Args:
            screenshot: Screenshot with modal
        """
        # Try finding close/dismiss/ok button
        close_buttons = [
            "modal_close",
            "modal_dismiss",
            "modal_ok",
            "close_button",
            "confirm_button",
        ]

        for btn_name in close_buttons:
            btn_pos = self.vision.find_button(screenshot, btn_name)
            if btn_pos:
                # Add human-like delay before clicking
                await self.behavior.random_delay(1, 3)

                # Click with variance
                click_pos = self.behavior.randomize_click(*btn_pos)
                await self.adb.tap(*click_pos)

                logger.info(f"Closed modal via '{btn_name}'")
                await asyncio.sleep(1)
                return

        # Fallback: Try pressing back button
        logger.info("No close button found, pressing back")
        await self.adb.press_back()
        await asyncio.sleep(1)

        # Fallback 2: Tap center of screen
        await self.adb.tap(540, 960)  # Approximate center
        await asyncio.sleep(1)

    async def _is_antibot_popup(self, screenshot: np.ndarray) -> bool:
        """
        Determine if a popup is an anti-bot dialog

        Uses heuristics to distinguish anti-bot modals from regular game dialogs

        Args:
            screenshot: Screenshot with popup

        Returns:
            True if likely an anti-bot popup
        """
        # Heuristic checks:
        # 1. Check if popup appeared unexpectedly (during automation)
        # 2. Check for verification-related text via OCR
        # 3. Check popup size/position (anti-bot usually center screen)

        # For now, use conservative approach
        return False  # Only flag known patterns

    async def _check_escalation(self):
        """
        Check if detection count requires escalation
        """
        if self.detection_count >= self.critical_threshold:
            logger.critical(
                f"CRITICAL: {self.detection_count} detections! "
                "Stopping bot to prevent ban."
            )
            raise AntiBotCriticalError(
                f"Too many anti-bot detections ({self.detection_count})"
            )

        elif self.detection_count >= self.danger_threshold:
            pause_minutes = 30 + (self.detection_count - self.danger_threshold) * 15
            logger.error(
                f"DANGER: {self.detection_count} detections! "
                f"Pausing for {pause_minutes} minutes."
            )
            await asyncio.sleep(pause_minutes * 60)

        elif self.detection_count >= self.warning_threshold:
            # Increase delays and randomization
            logger.warning(
                f"WARNING: {self.detection_count} detections! "
                "Increasing randomization."
            )
            self.behavior.config["action_delay_range"] = [15, 120]
            self.behavior.config["click_variance_pixels"] = 20

    async def _save_detection_screenshot(self, screenshot: np.ndarray, modal_type: str):
        """
        Save screenshot of anti-bot detection for analysis

        Args:
            screenshot: Screenshot to save
            modal_type: Type of modal detected
        """
        try:
            import cv2
            from pathlib import Path

            save_dir = Path("data/antibot_detections")
            save_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detection_{modal_type}_{timestamp}.png"
            filepath = save_dir / filename

            cv2.imwrite(str(filepath), screenshot)
            logger.info(f"Detection screenshot saved: {filepath}")

        except Exception as e:
            logger.error(f"Failed to save detection screenshot: {e}")

    def get_risk_level(self) -> str:
        """
        Get current anti-bot risk level

        Returns:
            Risk level: "safe", "low", "medium", "high", "critical"
        """
        if self.detection_count == 0:
            return "safe"
        elif self.detection_count < self.warning_threshold:
            return "low"
        elif self.detection_count < self.danger_threshold:
            return "medium"
        elif self.detection_count < self.critical_threshold:
            return "high"
        else:
            return "critical"

    def reset_counters(self):
        """Reset detection counters (call daily)"""
        self.detection_count = 0
        self.last_detection_time = None
        logger.info("Anti-bot detection counters reset")


class AntiBotCriticalError(Exception):
    """Raised when anti-bot detection reaches critical level"""
    pass
