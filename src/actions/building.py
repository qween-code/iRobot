"""
Building Executor

Handles automatic building construction and upgrades
"""

import asyncio
from typing import Dict, Any
from loguru import logger
from .navigation import NavigationAction


class BuildingExecutor:
    """Execute building tasks"""

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize building executor

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {}).get("buildings", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior
        self.navigator = NavigationAction(adb, vision, behavior)

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute building task

        Args:
            params: Task parameters

        Returns:
            Result dictionary
        """
        logger.info("Starting building upgrades...")

        try:
            # 1. Ensure in City
            if not await self.navigator.switch_to_city():
                return {"success": False, "error": "Not in city"}

            # 2. Check for idle builders (Hammer icon on sidebar)
            # This is a heuristic: usually if there is a "Zzz" or "Free" hammer, we can build.
            # We will look for "icon_idle_builder"
            screenshot = await self.adb.screenshot()
            idle_builder = self.vision.find_element(screenshot, "icon_idle_builder")

            if not idle_builder:
                logger.info("No idle builders found.")
                return {"success": True, "status": "no_idle_builders"}

            # 3. Find upgradable buildings (Green arrow icons)
            # We look for "icon_upgrade_arrow" on the screen
            # Note: This finds the first one. In reality, we might want to scroll or choose based on priority.
            upgrade_icon = self.vision.find_element(screenshot, "icon_upgrade_arrow")

            if upgrade_icon:
                logger.info("Found upgradable building")
                await self.adb.tap(*upgrade_icon["center"])
                await self.behavior.random_delay(1, 2)

                # Click "Upgrade" button in the menu
                screenshot = await self.adb.screenshot()
                btn_upgrade = self.vision.find_element(screenshot, "btn_upgrade_confirm")

                if btn_upgrade:
                    await self.adb.tap(*btn_upgrade["center"])
                    await self.behavior.random_delay(1, 2)

                    # Handle "Help" request (shaking hands) immediately after upgrade start
                    await self._click_help()

                    return {"success": True, "action": "upgrade_started"}

            logger.info("Builders idle but no upgrades found visible")
            return {"success": True, "status": "no_upgrades_visible"}

        except Exception as e:
            logger.error(f"Building upgrades failed: {e}")
            return {"success": False, "error": str(e)}

    async def _click_help(self):
        """Click the alliance help button if it appears"""
        screenshot = await self.adb.screenshot()
        help_btn = self.vision.find_element(screenshot, "icon_alliance_help_bubble")
        if help_btn:
             await self.adb.tap(*help_btn["center"])
             logger.info("Requested alliance help")
