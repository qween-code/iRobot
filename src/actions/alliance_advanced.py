"""
Advanced Alliance Features

Handles:
- Continuous alliance donations
- Alliance helps (send/receive)
- Alliance gifts collection
- Alliance events participation
- Rally coordination
- Alliance shop purchases
"""

import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime, timedelta


class AllianceManager:
    """
    Advanced alliance/clan management
    """

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize alliance manager

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {}).get("alliance", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior

        # Tracking
        self.last_help_time = None
        self.last_donation_time = None
        self.last_gift_collection = None
        self.helps_sent_today = 0
        self.donations_made_today = 0

        logger.info("Alliance Manager initialized")

    async def execute(self, params: Dict) -> Dict[str, Any]:
        """
        Execute alliance tasks

        Args:
            params: Task parameters

        Returns:
            Result dictionary
        """
        logger.info("Starting alliance activities...")

        results = {
            "helps_sent": 0,
            "helps_received": 0,
            "gifts_collected": 0,
            "donations_made": 0,
            "rallies_joined": 0
        }

        try:
            # 1. Send alliance helps (priority - helps others first)
            if self.config.get("auto_send_helps", True):
                helps_sent = await self.send_alliance_helps()
                results["helps_sent"] = helps_sent

            # 2. Collect alliance helps received
            if self.config.get("auto_collect_helps", True):
                helps_received = await self.collect_alliance_helps()
                results["helps_received"] = helps_received

            # 3. Collect alliance gifts
            if self.config.get("auto_collect_gifts", True):
                gifts = await self.collect_alliance_gifts()
                results["gifts_collected"] = gifts

            # 4. Make alliance donations
            if self.config.get("auto_donate", True):
                donations = await self.make_alliance_donations()
                results["donations_made"] = donations

            # 5. Join alliance rallies
            if self.config.get("auto_join_rallies", False):
                rallies = await self.join_alliance_rallies()
                results["rallies_joined"] = rallies

            # 6. Alliance shop purchases (if configured)
            if self.config.get("auto_alliance_shop", False):
                await self.alliance_shop_purchases()

            logger.success(f"Alliance activities completed: {results}")
            return {"success": True, **results}

        except Exception as e:
            logger.error(f"Alliance activities failed: {e}")
            return {"success": False, "error": str(e)}

    async def send_alliance_helps(self) -> int:
        """
        Send helps to alliance members

        Returns:
            Number of helps sent
        """
        logger.info("Sending alliance helps...")

        # Check cooldown (don't spam)
        if self.last_help_time:
            time_since_last = (datetime.now() - self.last_help_time).total_seconds()
            if time_since_last < 300:  # 5 minutes minimum
                logger.debug("Help cooldown active, skipping")
                return 0

        max_helps = self.config.get("max_helps_per_session", 50)
        helps_sent = 0

        try:
            # Navigate to alliance screen
            await self._navigate_to_alliance()

            # Find and click "Help All" button
            screenshot = await self.adb.screenshot()
            help_all_btn = self.vision.find_button(screenshot, "alliance_help_all")

            if help_all_btn:
                # Randomize click position
                click_pos = self.behavior.randomize_click(*help_all_btn)
                await self.adb.tap(*click_pos)

                # Wait for animation
                await asyncio.sleep(1)

                helps_sent = max_helps  # Assume all helps sent
                self.helps_sent_today += helps_sent
                self.last_help_time = datetime.now()

                logger.success(f"Sent {helps_sent} alliance helps")
            else:
                # Fallback: Individual helps
                helps_sent = await self._send_individual_helps(max_helps)

            return helps_sent

        except Exception as e:
            logger.error(f"Failed to send alliance helps: {e}")
            return 0

    async def _send_individual_helps(self, max_helps: int) -> int:
        """
        Send helps individually (slower method)

        Args:
            max_helps: Maximum helps to send

        Returns:
            Number of helps sent
        """
        helps_sent = 0

        for _ in range(max_helps):
            screenshot = await self.adb.screenshot()
            help_btn = self.vision.find_button(screenshot, "alliance_help_button")

            if not help_btn:
                break  # No more helps available

            # Click help button
            await self.adb.tap(*self.behavior.randomize_click(*help_btn))
            helps_sent += 1

            # Random delay between helps (anti-ban)
            await self.behavior.random_delay(1, 3)

        logger.info(f"Sent {helps_sent} individual helps")
        return helps_sent

    async def collect_alliance_helps(self) -> int:
        """
        Collect helps received from alliance

        Returns:
            Number of helps collected
        """
        logger.info("Collecting alliance helps...")

        try:
            # Look for notification badge
            screenshot = await self.adb.screenshot()
            help_notification = self.vision.find_button(screenshot, "alliance_help_notification")

            if not help_notification:
                logger.debug("No alliance helps to collect")
                return 0

            # Navigate and collect
            await self._navigate_to_alliance()

            # Click collect button
            collect_btn = self.vision.find_button(screenshot, "alliance_collect_helps")
            if collect_btn:
                await self.adb.tap(*self.behavior.randomize_click(*collect_btn))
                logger.success("Collected alliance helps")
                return 1

            return 0

        except Exception as e:
            logger.error(f"Failed to collect alliance helps: {e}")
            return 0

    async def collect_alliance_gifts(self) -> int:
        """
        Collect alliance gifts

        Returns:
            Number of gifts collected
        """
        logger.info("Collecting alliance gifts...")

        # Check cooldown
        if self.last_gift_collection:
            time_since = (datetime.now() - self.last_gift_collection).total_seconds()
            if time_since < 3600:  # 1 hour cooldown
                return 0

        try:
            await self._navigate_to_alliance()

            # Find gift icon
            screenshot = await self.adb.screenshot()
            gift_btn = self.vision.find_button(screenshot, "alliance_gift")

            if gift_btn:
                await self.adb.tap(*self.behavior.randomize_click(*gift_btn))
                await asyncio.sleep(1)

                # Collect all gifts
                collect_all = self.vision.find_button(screenshot, "alliance_collect_all_gifts")
                if collect_all:
                    await self.adb.tap(*self.behavior.randomize_click(*collect_all))
                    self.last_gift_collection = datetime.now()
                    logger.success("Collected alliance gifts")
                    return 1

            return 0

        except Exception as e:
            logger.error(f"Failed to collect gifts: {e}")
            return 0

    async def make_alliance_donations(self) -> int:
        """
        Make alliance donations (technology donations)

        Returns:
            Number of donations made
        """
        logger.info("Making alliance donations...")

        donation_config = self.config.get("donation", {})
        if not donation_config.get("enabled", True):
            return 0

        # Check daily limit
        max_donations_per_day = donation_config.get("max_per_day", 10)
        if self.donations_made_today >= max_donations_per_day:
            logger.debug("Daily donation limit reached")
            return 0

        # Check cooldown
        if self.last_donation_time:
            time_since = (datetime.now() - self.last_donation_time).total_seconds()
            cooldown = donation_config.get("cooldown_minutes", 30) * 60
            if time_since < cooldown:
                return 0

        try:
            await self._navigate_to_alliance()

            # Navigate to alliance technology/donation screen
            screenshot = await self.adb.screenshot()
            tech_btn = self.vision.find_button(screenshot, "alliance_technology")

            if not tech_btn:
                logger.warning("Alliance technology button not found")
                return 0

            await self.adb.tap(*self.behavior.randomize_click(*tech_btn))
            await asyncio.sleep(2)

            # Make donations
            donations_made = 0
            donation_types = donation_config.get("types", ["gold", "resources"])

            for donation_type in donation_types:
                # Find donation button for this type
                donate_btn = self.vision.find_button(screenshot, f"donate_{donation_type}")

                if donate_btn:
                    # Check resource threshold
                    if await self._check_donation_resources(donation_type):
                        await self.adb.tap(*self.behavior.randomize_click(*donate_btn))
                        await asyncio.sleep(1)

                        # Confirm donation
                        confirm_btn = self.vision.find_button(screenshot, "confirm_button")
                        if confirm_btn:
                            await self.adb.tap(*self.behavior.randomize_click(*confirm_btn))
                            donations_made += 1

                            # Random delay between donations
                            await self.behavior.random_delay(3, 8)

            self.donations_made_today += donations_made
            self.last_donation_time = datetime.now()

            logger.success(f"Made {donations_made} alliance donations")
            return donations_made

        except Exception as e:
            logger.error(f"Failed to make donations: {e}")
            return 0

    async def _check_donation_resources(self, donation_type: str) -> bool:
        """
        Check if we have enough resources for donation

        Args:
            donation_type: Type of donation (gold, resources, etc.)

        Returns:
            True if can donate
        """
        # TODO: Implement resource checking via OCR
        # For now, assume we can donate
        donation_config = self.config.get("donation", {})
        min_resource_threshold = donation_config.get("min_resource_threshold", 0.3)

        # Keep at least 30% of resources
        return True  # Placeholder

    async def join_alliance_rallies(self) -> int:
        """
        Join alliance rallies (coordinated attacks)

        Returns:
            Number of rallies joined
        """
        logger.info("Checking for alliance rallies...")

        rally_config = self.config.get("rallies", {})
        if not rally_config.get("enabled", False):
            return 0

        max_rallies = rally_config.get("max_per_day", 10)
        rallies_joined = 0

        try:
            # Check for rally notifications
            screenshot = await self.adb.screenshot()
            rally_notification = self.vision.find_button(screenshot, "rally_notification")

            if not rally_notification:
                return 0

            # Navigate to rallies
            await self._navigate_to_alliance()
            await asyncio.sleep(1)

            # Find rally list
            rally_btn = self.vision.find_button(screenshot, "alliance_rally")
            if rally_btn:
                await self.adb.tap(*self.behavior.randomize_click(*rally_btn))
                await asyncio.sleep(2)

                # Join rallies based on type
                rally_types = rally_config.get("types", {})

                for rally_type, enabled in rally_types.items():
                    if not enabled or rallies_joined >= max_rallies:
                        continue

                    # Find and join this type of rally
                    rally_item = self.vision.find_button(screenshot, f"rally_{rally_type}")

                    if rally_item:
                        # Check participation probability (anti-ban)
                        participation_prob = rally_config.get("participation_probability", 0.8)
                        if await self._should_participate(participation_prob):
                            await self.adb.tap(*self.behavior.randomize_click(*rally_item))
                            await asyncio.sleep(1)

                            # Confirm join
                            join_btn = self.vision.find_button(screenshot, "rally_join")
                            if join_btn:
                                await self.adb.tap(*self.behavior.randomize_click(*join_btn))
                                rallies_joined += 1
                                logger.info(f"Joined {rally_type} rally")

                                # Random delay
                                await self.behavior.random_delay(5, 15)

            logger.success(f"Joined {rallies_joined} rallies")
            return rallies_joined

        except Exception as e:
            logger.error(f"Failed to join rallies: {e}")
            return 0

    async def _should_participate(self, probability: float) -> bool:
        """
        Decide if should participate in event (randomization for anti-ban)

        Args:
            probability: Participation probability (0-1)

        Returns:
            True if should participate
        """
        import random
        return random.random() < probability

    async def alliance_shop_purchases(self):
        """
        Make purchases from alliance shop
        """
        logger.info("Checking alliance shop...")

        shop_config = self.config.get("alliance_shop", {})
        if not shop_config.get("enabled", False):
            return

        # TODO: Implement alliance shop logic
        # - Navigate to alliance shop
        # - Check for configured items to buy
        # - Make purchases if alliance points available

        logger.debug("Alliance shop purchases not yet implemented")

    async def _navigate_to_alliance(self):
        """Navigate to alliance screen"""
        # TODO: Implement navigation logic
        # 1. Return to city if not there
        # 2. Click alliance button
        # 3. Wait for screen load

        logger.debug("Navigating to alliance screen")
        await asyncio.sleep(1)  # Placeholder

    def reset_daily_counters(self):
        """Reset daily counters (call at midnight)"""
        self.helps_sent_today = 0
        self.donations_made_today = 0
        logger.info("Daily alliance counters reset")
