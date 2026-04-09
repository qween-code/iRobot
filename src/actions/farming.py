"""
Resource Farming Executor

Handles automatic resource farming operations
"""

import asyncio
from typing import Dict, Any
from loguru import logger
from .navigation import NavigationAction


class FarmingExecutor:
    """Execute resource farming tasks"""

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize farming executor

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {}).get("farming", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior
        self.navigator = NavigationAction(adb, vision, behavior)

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute farming task

        Args:
            params: Task parameters (e.g., {'resource': 'iron', 'level': 10})

        Returns:
            Result dictionary
        """
        logger.info("Starting resource farming...")
        resource_type = params.get("resource", "iron")
        target_level = params.get("level", 1)

        try:
            # 1. Navigate to world map
            if not await self.navigator.switch_to_map():
                return {"success": False, "error": "Failed to navigate to map"}

            # 2. Find and click "Search" button
            if not await self._open_search_menu():
                 return {"success": False, "error": "Failed to open search menu"}

            # 3. Select Resource Type and Level
            await self._configure_search(resource_type, target_level)

            # 4. Search and Attack
            if await self._search_and_attack():
                # 5. Return to city (optional)
                await self.navigator.switch_to_city()
                return {"success": True, "resources_farmed": 0} # Placeholder value
            else:
                 return {"success": False, "error": "No tile found or attack failed"}

        except Exception as e:
            logger.error(f"Farming failed: {e}")
            return {"success": False, "error": str(e)}

    async def _open_search_menu(self) -> bool:
        """Find and click the search (magnifying glass) button"""
        screenshot = await self.adb.screenshot()
        btn = self.vision.find_element(screenshot, "icon_search")

        if btn:
            x, y = btn["center"]
            await self.adb.tap(x, y)
            await self.behavior.random_delay(1, 2)
            return True
        return False

    async def _configure_search(self, resource_type: str, level: int):
        """Select resource type and level in search menu"""
        # This assumes the search menu is open
        screenshot = await self.adb.screenshot()

        # 1. Click Resource Tab (if needed)
        # 2. Click specific resource icon (iron, food, etc)
        res_btn = self.vision.find_element(screenshot, f"icon_select_{resource_type}")
        if res_btn:
            await self.adb.tap(*res_btn["center"])
            await self.behavior.random_delay(0.5, 1)

        # 3. Adjust level (typically plus/minus buttons or slider)
        # For simplicity, we assume we just click "Search" for now or use +/- buttons
        # TODO: Implement complex level selection logic using OCR
        pass

    async def _search_and_attack(self) -> bool:
        """Click Search, find tile, and dispatch"""
        # Click "Search" (Go) button
        screenshot = await self.adb.screenshot()
        search_btn = self.vision.find_element(screenshot, "btn_search_go")

        if search_btn:
            await self.adb.tap(*search_btn["center"])
            await self.behavior.random_delay(2, 4) # Wait for map scroll

            # Now we should be centered on a tile.
            # Click screen center to select tile
            # (Assuming the game centers on the found tile)
            await self.adb.tap(540, 960) # Center of 1080x1920
            await self.behavior.random_delay(1, 2)

            # Click "Gather"
            screenshot = await self.adb.screenshot()
            gather_btn = self.vision.find_element(screenshot, "btn_gather")
            if gather_btn:
                await self.adb.tap(*gather_btn["center"])
                await self.behavior.random_delay(1, 2)

                # Click "March" / "Deploy"
                return await self._dispatch_troops()

        return False

    async def _dispatch_troops(self) -> bool:
        """Handle troop selection and dispatch"""
        screenshot = await self.adb.screenshot()
        march_btn = self.vision.find_element(screenshot, "btn_march")

        if march_btn:
            await self.adb.tap(*march_btn["center"])
            await self.behavior.random_delay(1, 2)
            return True

        return False
