"""
State Machine - Decision engine for bot actions

This module implements the AI decision-making logic:
- Game state analysis
- Priority-based task selection
- Action execution
"""

from typing import Dict, Any, Optional
from loguru import logger


class StateMachine:
    """
    State machine for bot decision making
    """

    def __init__(self, config: Dict, adb, vision, behavior):
        """
        Initialize state machine

        Args:
            config: Bot configuration
            adb: ADB controller
            vision: Vision module
            behavior: Behavior randomizer
        """
        self.config = config
        self.adb = adb
        self.vision = vision
        self.behavior = behavior

        self.current_state = "idle"
        self.game_state = {}

        # Task executors (will be loaded dynamically)
        self.executors = {}
        self._load_executors()

    def _load_executors(self):
        """Load task executor modules"""
        from actions.farming import FarmingExecutor
        from actions.zombie_hunting import ZombieHuntingExecutor
        from actions.troop_management import TroopManagementExecutor
        from actions.building import BuildingExecutor
        from actions.events import EventsExecutor

        self.executors = {
            "resource_farming": FarmingExecutor(self.config, self.adb, self.vision, self.behavior),
            "zombie_hunting": ZombieHuntingExecutor(self.config, self.adb, self.vision, self.behavior),
            "troop_management": TroopManagementExecutor(self.config, self.adb, self.vision, self.behavior),
            "building_upgrades": BuildingExecutor(self.config, self.adb, self.vision, self.behavior),
            "alliance_activities": EventsExecutor(self.config, self.adb, self.vision, self.behavior),
        }

    async def execute_task(self, task_name: str, params: Dict) -> Dict[str, Any]:
        """
        Execute a task

        Args:
            task_name: Name of task to execute
            params: Task parameters

        Returns:
            Result dictionary with success status and data
        """
        logger.info(f"Executing task: {task_name}")

        # Get executor
        executor = self.executors.get(task_name)
        if not executor:
            return {"success": False, "error": f"Unknown task: {task_name}"}

        try:
            # Update game state before task
            await self.update_game_state()

            # Execute task
            result = await executor.execute(params)

            return result

        except Exception as e:
            logger.exception(f"Error executing task {task_name}: {e}")
            return {"success": False, "error": str(e)}

    async def update_game_state(self):
        """
        Update current game state by analyzing screen

        This uses OCR and YOLO detection to understand:
        - Current screen/menu
        - Resource levels
        - Troop status
        - Notifications
        """
        try:
            screenshot = await self.adb.screenshot()

            # Detect UI elements using UINavigator
            # Note: UINavigator.find_all_elements returns a combined list from YOLO + Template
            elements = self.vision.find_all_elements(screenshot)

            # Update state
            self.game_state = {
                "screen": self._identify_screen(elements),
                "resources": {},  # TODO: Use self.vision.get_resource_amount()
                "troops": {},  # TODO
                "notifications": self._detect_notifications(elements),
            }

            logger.debug(f"Game state updated: {self.game_state}")

        except Exception as e:
            logger.error(f"Failed to update game state: {e}")

    def _identify_screen(self, elements: list) -> str:
        """
        Identify current screen based on detected elements

        Args:
            elements: List of detected UI elements

        Returns:
            Screen name (e.g., 'city', 'map', 'menu')
        """
        element_names = [e.get("class") for e in elements]

        if "icon_search" in element_names and "icon_coords" in element_names:
            return "map"
        elif "icon_build_menu" in element_names or "building_hq" in element_names:
            return "city"
        elif "btn_close" in element_names:
            return "menu"

        return "unknown"

    def _detect_notifications(self, elements: list) -> list:
        """
        Detect notification badges/alerts

        Args:
            elements: List of detected UI elements

        Returns:
            List of notifications
        """
        notifications = []
        for e in elements:
            if "badge_red" in e.get("class", ""):
                notifications.append(e)
        return notifications

    async def decide_next_action(self) -> Optional[str]:
        """
        AI-based decision for next action based on current game state

        Returns:
            Task name or None
        """
        await self.update_game_state()

        # Check for emergency notifications first (e.g. Alliance Help)
        if self._has_alliance_help():
             return "alliance_activities"

        # Priority-based decision tree
        if self._resources_near_cap():
            return "building_upgrades"

        if self._troops_wounded():
            # Only prioritize healing if significant wounded
            return "troop_management"

        if self._stamina_available():
            return "zombie_hunting"

        if self._attacks_remaining():
            return "resource_farming"

        return "building_upgrades" # Default to building checks if nothing else

    def _has_alliance_help(self) -> bool:
        """Check for alliance help request"""
        # Look for shaking hands icon
        return any("icon_alliance_help" == n.get("class") for n in self.game_state.get("notifications", []))

    def _resources_near_cap(self) -> bool:
        """Check if resources near capacity"""
        # Check logic: resource amount > 80% of cap
        # Since we don't track cap yet, we can use a simpler heuristic
        # If any resource is "red" (game indicates full), return True
        # For now, let's assume False to prioritize other tasks
        return False

    def _troops_wounded(self) -> bool:
        """Check if troops need healing"""
        # Look for "Hospital" having a notification badge
        # In update_game_state, we find elements.
        # Ideally we would check for "icon_hospital_plus" or similar
        return False # Placeholder

    def _stamina_available(self) -> bool:
        """Check if stamina available for hunting"""
        # OCR stamina value
        # This requires reading the stamina bar
        # For now, we can check if we have failed a hunt recently due to stamina
        # Or blindly return True and let the executor handle the "No Stamina" popup
        return True

    def _attacks_remaining(self) -> bool:
        """Check if daily attacks remaining"""
        # This state should be tracked in a database/file, not just vision
        # For now, assume yes
        return True
