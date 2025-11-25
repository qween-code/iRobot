"""
Navigation Action - Helper for game navigation
"""

import asyncio
from typing import Optional
from loguru import logger

class NavigationAction:
    """
    Helper class for navigating between game screens (City <-> World Map)
    """

    def __init__(self, adb, vision, behavior):
        """
        Initialize navigation helper

        Args:
            adb: ADB controller
            vision: UI Navigator
            behavior: Behavior randomizer
        """
        self.adb = adb
        self.vision = vision
        self.behavior = behavior

    async def switch_to_map(self) -> bool:
        """
        Switch to World Map view
        """
        logger.info("Navigating to World Map...")

        # 1. Check if already on map
        screenshot = await self.adb.screenshot()
        if self._is_on_map(screenshot):
            logger.debug("Already on World Map")
            return True

        # 2. Find "Map" button (usually bottom left icon in City view)
        # We look for the "world_map_icon" template or button
        map_btn = self.vision.find_element(screenshot, "icon_world_map")

        if map_btn:
            x, y = map_btn["center"]
            await self.adb.tap(x, y)
            await self.behavior.random_delay(2, 4) # Wait for transition
            return True
        else:
            # Fallback: Coordinates for bottom-left (common in mobile strategy games)
            # Assuming 1080x1920 portrait or landscape? Last War is vertical usually.
            # Let's assume dynamic detection is best, but if missing, fail gracefully.
            logger.warning("Could not find World Map button")
            return False

    async def switch_to_city(self) -> bool:
        """
        Switch to City view
        """
        logger.info("Returning to City...")

        screenshot = await self.adb.screenshot()
        if self._is_in_city(screenshot):
            return True

        # Find "Home" or "City" button (usually bottom left in Map view)
        city_btn = self.vision.find_element(screenshot, "icon_city")

        if city_btn:
            x, y = city_btn["center"]
            await self.adb.tap(x, y)
            await self.behavior.random_delay(2, 4)
            return True

        logger.warning("Could not find City button")
        return False

    def _is_on_map(self, screenshot) -> bool:
        """Check if current screen is World Map"""
        # Look for map-specific elements like "Search" magnifying glass or coordinates
        return self.vision.find_element(screenshot, "icon_search") is not None

    def _is_in_city(self, screenshot) -> bool:
        """Check if current screen is City"""
        # Look for city-specific elements like "Build" menu or "Alliance" help
        return self.vision.find_element(screenshot, "icon_build_menu") is not None
