"""
Events Executor

Handles alliance activities and special events
"""

import asyncio
from typing import Dict, Any
from loguru import logger
from .navigation import NavigationAction


class EventsExecutor:
    """Execute event and alliance tasks"""

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize events executor

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior
        self.navigator = NavigationAction(adb, vision, behavior)

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute event/alliance task

        Args:
            params: Task parameters

        Returns:
            Result dictionary
        """
        logger.info("Starting alliance/event activities...")

        try:
            # 1. Ensure in City (Alliance button is in menu bar)
            if not await self.navigator.switch_to_city():
                return {"success": False, "error": "Not in city"}

            # 2. Click "Alliance" button
            # Look for "icon_alliance"
            screenshot = await self.adb.screenshot()
            alliance_btn = self.vision.find_element(screenshot, "icon_alliance")

            if alliance_btn:
                await self.adb.tap(*alliance_btn["center"])
                await self.behavior.random_delay(1, 2)

                # 3. Handle "Help" (Shaking Hands)
                await self._handle_helps()

                # 4. Handle "Gifts"
                await self._handle_gifts()

                # Close Alliance Menu (return to city)
                # Usually a close button or back press
                await self.adb.press_back()

                return {"success": True}

            return {"success": False, "error": "Alliance button not found"}

        except Exception as e:
            logger.error(f"Alliance/event activities failed: {e}")
            return {"success": False, "error": str(e)}

    async def _handle_helps(self):
        """Click 'Help' button inside alliance menu"""
        # Look for "Help" icon/tab
        screenshot = await self.adb.screenshot()
        help_tab = self.vision.find_element(screenshot, "tab_alliance_help")

        if help_tab:
            await self.adb.tap(*help_tab["center"])
            await self.behavior.random_delay(1, 2)

            # Click "Help All" (usually a big button)
            screenshot = await self.adb.screenshot()
            help_all = self.vision.find_element(screenshot, "btn_help_all")
            if help_all:
                await self.adb.tap(*help_all["center"])
                logger.info("Clicked Help All")
                await self.behavior.random_delay(0.5, 1)

    async def _handle_gifts(self):
        """Collect alliance gifts"""
        # Look for "Gifts" tab
        screenshot = await self.adb.screenshot()
        gifts_tab = self.vision.find_element(screenshot, "tab_alliance_gifts")

        if gifts_tab:
            await self.adb.tap(*gifts_tab["center"])
            await self.behavior.random_delay(1, 2)

            # Click "Claim All"
            screenshot = await self.adb.screenshot()
            claim_all = self.vision.find_element(screenshot, "btn_claim_all")
            if claim_all:
                await self.adb.tap(*claim_all["center"])
                logger.info("Claimed Alliance Gifts")
                await self.behavior.random_delay(0.5, 1)
