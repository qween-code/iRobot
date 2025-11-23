"""
Event Detector - Auto-detect and participate in game events

Handles:
- Event detection (Golden Zombies, Zombie Invasion, etc.)
- Auto-participation
- Event-specific strategies
- Reward collection
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from loguru import logger
import numpy as np


class EventDetector:
    """
    Detect and participate in game events
    """

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize event detector

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config.get("automation", {}).get("events", {})
        self.adb = adb
        self.vision = vision
        self.behavior = behavior

        # Active events tracking
        self.active_events = {}
        self.event_history = []

        # Event handlers
        self.event_handlers = {
            "golden_zombies": self.handle_golden_zombies,
            "zombie_invasion": self.handle_zombie_invasion,
            "kvk": self.handle_kvk_event,
            "alliance_war": self.handle_alliance_war,
            "resource_madness": self.handle_resource_madness,
            "troop_training": self.handle_troop_training_event,
            "hero_trial": self.handle_hero_trial,
        }

        logger.info("Event Detector initialized")

    async def detect_events(self, screenshot: np.ndarray) -> List[str]:
        """
        Detect active events from screenshot

        Args:
            screenshot: Current game screenshot

        Returns:
            List of active event names
        """
        detected_events = []

        # Method 1: Look for event notification badges
        event_badge = self.vision.find_button(screenshot, "event_notification")
        if event_badge:
            # Navigate to events screen to get details
            detected_events = await self._scan_events_screen()

        # Method 2: Check for specific event UI elements
        event_indicators = [
            ("golden_zombie_icon", "golden_zombies"),
            ("invasion_icon", "zombie_invasion"),
            ("kvk_icon", "kvk"),
            ("alliance_war_icon", "alliance_war"),
        ]

        for icon_name, event_name in event_indicators:
            if self.vision.find_button(screenshot, icon_name):
                if event_name not in detected_events:
                    detected_events.append(event_name)

        # Update active events
        for event_name in detected_events:
            if event_name not in self.active_events:
                self.active_events[event_name] = {
                    "started": datetime.now(),
                    "participations": 0
                }
                logger.info(f"🎉 New event detected: {event_name}")

        # Remove ended events
        for event_name in list(self.active_events.keys()):
            if event_name not in detected_events:
                logger.info(f"Event ended: {event_name}")
                self.event_history.append({
                    "name": event_name,
                    "started": self.active_events[event_name]["started"],
                    "ended": datetime.now(),
                    "participations": self.active_events[event_name]["participations"]
                })
                del self.active_events[event_name]

        return detected_events

    async def _scan_events_screen(self) -> List[str]:
        """
        Navigate to events screen and scan for active events

        Returns:
            List of event names
        """
        try:
            # Click events button
            screenshot = await self.adb.screenshot()
            events_btn = self.vision.find_button(screenshot, "events_button")

            if not events_btn:
                return []

            await self.adb.tap(*self.behavior.randomize_click(*events_btn))
            await asyncio.sleep(2)

            # Scan for event tiles
            screenshot = await self.adb.screenshot()

            # TODO: Implement OCR or YOLO detection for event names
            # For now, use button detection

            detected = []
            # Check each known event type
            for event_name in self.event_handlers.keys():
                if self.vision.find_button(screenshot, f"event_{event_name}"):
                    detected.append(event_name)

            # Go back
            await self.adb.press_back()
            await asyncio.sleep(1)

            return detected

        except Exception as e:
            logger.error(f"Failed to scan events screen: {e}")
            return []

    async def participate_in_events(self) -> Dict[str, Any]:
        """
        Participate in all active events

        Returns:
            Results dictionary
        """
        results = {}

        for event_name in self.active_events.keys():
            # Check if event is enabled in config
            event_config = self.config.get(event_name, {})
            if not event_config.get("enabled", False):
                logger.debug(f"Event '{event_name}' disabled in config")
                continue

            # Get handler
            handler = self.event_handlers.get(event_name)
            if not handler:
                logger.warning(f"No handler for event: {event_name}")
                continue

            # Execute handler
            try:
                logger.info(f"Participating in event: {event_name}")
                result = await handler(event_config)
                results[event_name] = result

                # Update participation count
                self.active_events[event_name]["participations"] += 1

                # Random delay between events
                await self.behavior.random_delay(10, 30)

            except Exception as e:
                logger.error(f"Error in event '{event_name}': {e}")
                results[event_name] = {"success": False, "error": str(e)}

        return results

    async def handle_golden_zombies(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Golden Zombies event

        Strategy:
        - Phase 1: Hunt small golden zombies (discovery)
        - Phase 2: Join rallies for bosses

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Golden Zombies event strategy...")

        phase1_hunts = config.get("phase1_hunts", 20)
        phase2_rallies = config.get("phase2_rallies", 10)

        results = {
            "phase1_completed": 0,
            "phase2_completed": 0,
            "bosses_discovered": 0
        }

        # Phase 1: Discovery
        for i in range(phase1_hunts):
            # Find and attack small golden zombie
            # TODO: Implement actual hunting logic
            await asyncio.sleep(2)  # Placeholder
            results["phase1_completed"] += 1

            # Random delay
            await self.behavior.random_delay(5, 15)

        # Phase 2: Boss rallies
        for i in range(phase2_rallies):
            # Join rally for golden zombie boss
            # TODO: Implement rally joining logic
            await asyncio.sleep(2)  # Placeholder
            results["phase2_completed"] += 1

            await self.behavior.random_delay(10, 30)

        # Use courage medals in shop
        if config.get("use_courage_medals_shop", True):
            await self._use_courage_medals_shop()

        logger.success(f"Golden Zombies event completed: {results}")
        return {"success": True, **results}

    async def handle_zombie_invasion(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Zombie Invasion event

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Zombie Invasion event strategy...")

        results = {
            "digs_collected": 0,
            "eggs_collected": 0
        }

        # Auto-collect digs
        if config.get("auto_collect_digs", True):
            # TODO: Implement dig collection
            results["digs_collected"] = 10  # Placeholder

        # Auto-collect eggs
        if config.get("auto_collect_eggs", True):
            # TODO: Implement egg collection
            results["eggs_collected"] = 5  # Placeholder

        logger.success(f"Zombie Invasion completed: {results}")
        return {"success": True, **results}

    async def handle_kvk_event(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Kingdom vs Kingdom (KvK) event

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing KvK event strategy...")

        # KvK is high-risk for ban - be conservative
        participation_probability = config.get("participation_probability", 0.5)

        if not await self._should_participate(participation_probability):
            logger.info("Skipping KvK participation (probability)")
            return {"success": True, "skipped": True}

        # TODO: Implement KvK logic
        # - Join alliance marches
        # - Capture structures
        # - Collect rewards

        return {"success": True, "participated": True}

    async def handle_alliance_war(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Alliance War event

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Alliance War event strategy...")

        # Similar to KvK, high-risk
        # TODO: Implement alliance war logic

        return {"success": True}

    async def handle_resource_madness(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Resource Madness event (increased gathering rewards)

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Resource Madness event strategy...")

        # Prioritize farming during this event
        max_farms = config.get("max_farms", 10)

        # TODO: Trigger resource farming task multiple times
        # This would integrate with the farming module

        return {"success": True, "farms_done": max_farms}

    async def handle_troop_training_event(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Troop Training event

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Troop Training event strategy...")

        # Continuously train troops during event
        # TODO: Integrate with troop management module

        return {"success": True}

    async def handle_hero_trial(self, config: Dict) -> Dict[str, Any]:
        """
        Handle Hero Trial event

        Args:
            config: Event configuration

        Returns:
            Result dictionary
        """
        logger.info("Executing Hero Trial event strategy...")

        # Auto-complete hero trials
        # TODO: Implement hero trial logic

        return {"success": True}

    async def _use_courage_medals_shop(self):
        """Use courage medals in event shop"""
        logger.info("Using courage medals in shop...")
        # TODO: Implement shop logic
        pass

    async def _should_participate(self, probability: float) -> bool:
        """
        Decide if should participate (randomization)

        Args:
            probability: Participation probability (0-1)

        Returns:
            True if should participate
        """
        import random
        return random.random() < probability

    def get_active_events(self) -> List[str]:
        """Get list of currently active events"""
        return list(self.active_events.keys())

    def get_event_stats(self, event_name: str) -> Optional[Dict]:
        """
        Get statistics for an event

        Args:
            event_name: Event name

        Returns:
            Stats dictionary or None
        """
        if event_name in self.active_events:
            return self.active_events[event_name]
        return None
