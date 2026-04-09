"""
Troop Management Executor

Handles automatic troop training, healing, and promotion
"""

import asyncio
from typing import Dict, Any
from loguru import logger
from .navigation import NavigationAction

class TroopManagementExecutor:
    """Execute troop management tasks"""

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize troop management executor
        """
        self.config = config.get("automation", {}).get("troops", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior
        self.navigator = NavigationAction(adb, vision, behavior)

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute troop management task
        """
        logger.info("Starting troop management...")
        action = params.get("action", "all") # 'heal', 'train', 'all'

        try:
            # Ensure we are in City
            if not await self.navigator.switch_to_city():
                 return {"success": False, "error": "Could not return to city"}

            success = True

            if action in ["heal", "all"]:
                if not await self._heal_troops():
                    success = False

            if action in ["train", "all"]:
                if not await self._train_troops():
                    success = False

            return {"success": success}

        except Exception as e:
            logger.error(f"Troop management failed: {e}")
            return {"success": False, "error": str(e)}

    async def _heal_troops(self) -> bool:
        """Heal wounded troops"""
        # Find Hospital
        # (This usually requires finding the building on screen, which is hard due to map size)
        # Alternative: Click "Hospital" icon in sidebar if available, or navigate via menus

        # For prototype: Assume we can find a "Hospital" bubble or icon
        screenshot = await self.adb.screenshot()
        hospital_icon = self.vision.find_element(screenshot, "building_hospital")

        if hospital_icon:
            await self.adb.tap(*hospital_icon["center"])
            await self.behavior.random_delay(1, 2)

            # Click "Heal" button inside
            # Click "Select All" logic would be here
            return True

        return False

    async def _train_troops(self) -> bool:
        """Train new troops"""
        # Similar logic for Barracks
        return True
