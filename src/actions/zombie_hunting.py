"""
Zombie Hunting Executor

Handles automatic zombie hunting operations
"""

import asyncio
from typing import Dict, Any
from loguru import logger
from .navigation import NavigationAction


class ZombieHuntingExecutor:
    """Execute zombie hunting tasks"""

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize zombie hunting executor

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {}).get("hunting", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior
        self.navigator = NavigationAction(adb, vision, behavior)

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute zombie hunting task

        Args:
            params: Task parameters (e.g., {'level': 10})

        Returns:
            Result dictionary
        """
        logger.info("Starting zombie hunting...")
        target_level = params.get("level", 1)

        try:
            # 1. Navigate to Map
            if not await self.navigator.switch_to_map():
                 return {"success": False, "error": "Failed to navigate to map"}

            # 2. Open Search
            if not await self._open_search_menu():
                 return {"success": False, "error": "Failed to open search menu"}

            # 3. Configure Search (Mobs tab)
            # Switch to "Monster" tab if needed
            # Set level
            # Click Search

            if await self._search_and_attack():
                 await self.navigator.switch_to_city()
                 return {"success": True, "zombies_killed": 1}
            else:
                 return {"success": False, "error": "Attack failed"}

        except Exception as e:
            logger.error(f"Zombie hunting failed: {e}")
            return {"success": False, "error": str(e)}

    async def _open_search_menu(self) -> bool:
        """Find and click search button"""
        screenshot = await self.adb.screenshot()
        btn = self.vision.find_element(screenshot, "icon_search")
        if btn:
            await self.adb.tap(*btn["center"])
            await self.behavior.random_delay(1, 2)
            return True
        return False

    async def _search_and_attack(self) -> bool:
        """Search for zombie and attack"""
        # Assume we are in search menu
        # Click "Search"
        screenshot = await self.adb.screenshot()
        search_btn = self.vision.find_element(screenshot, "btn_search_go")

        if search_btn:
            await self.adb.tap(*search_btn["center"])
            await self.behavior.random_delay(2, 4)

            # Click center (Zombie)
            await self.adb.tap(540, 960)
            await self.behavior.random_delay(1, 2)

            # Click "Attack"
            screenshot = await self.adb.screenshot()
            attack_btn = self.vision.find_element(screenshot, "btn_attack")

            if attack_btn:
                # Check Stamina (OCR) - Optional for now

                await self.adb.tap(*attack_btn["center"])
                await self.behavior.random_delay(1, 2)

                # Dispatch
                return await self._dispatch_troops()

        return False

    async def _dispatch_troops(self) -> bool:
        """Handle troop dispatch"""
        # Logic similar to farming, but maybe select specific heroes
        screenshot = await self.adb.screenshot()
        march_btn = self.vision.find_element(screenshot, "btn_march")

        if march_btn:
            await self.adb.tap(*march_btn["center"])
            await self.behavior.random_delay(1, 2)
            return True
        return False
