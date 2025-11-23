"""
Task Scheduler - Manages task priorities and scheduling

This module handles:
- Task prioritization
- Scheduling based on time/conditions
- Task queue management
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime, time as dt_time
from loguru import logger


class TaskScheduler:
    """
    Intelligent task scheduler with priority queue
    """

    def __init__(self, config: Dict, state_machine):
        """
        Initialize task scheduler

        Args:
            config: Bot configuration
            state_machine: State machine instance
        """
        self.config = config
        self.state_machine = state_machine

        # Task priorities from config
        self.priorities = config.get("automation", {}).get("task_priorities", {})

        # Enabled tasks
        self.enabled_tasks = config.get("automation", {}).get("enabled_tasks", [])

        # Task queue
        self.task_queue = []

        # Task execution history
        self.execution_history = {}

        logger.info(f"Task scheduler initialized with {len(self.enabled_tasks)} enabled tasks")

    async def get_next_task(self) -> Optional[Dict]:
        """
        Get next task to execute based on priorities and conditions

        Returns:
            Task dictionary or None if no tasks available
        """
        # Build task candidates
        candidates = []

        for task_name in self.enabled_tasks:
            if await self._should_execute_task(task_name):
                priority = self.priorities.get(task_name, 50)
                candidates.append({"name": task_name, "priority": priority})

        if not candidates:
            return None

        # Sort by priority (highest first)
        candidates.sort(key=lambda x: x["priority"], reverse=True)

        # Return highest priority task
        selected_task = candidates[0]
        logger.debug(f"Selected task: {selected_task['name']} (priority: {selected_task['priority']})")

        return selected_task

    async def _should_execute_task(self, task_name: str) -> bool:
        """
        Check if task should be executed now

        Args:
            task_name: Name of task

        Returns:
            True if task should execute, False otherwise
        """
        # Check if task is in quiet hours
        if not self._is_active_hours():
            return False

        # Check task-specific conditions
        if task_name == "resource_farming":
            return await self._should_farm()
        elif task_name == "zombie_hunting":
            return await self._should_hunt()
        elif task_name == "troop_management":
            return await self._should_manage_troops()
        elif task_name == "building_upgrades":
            return await self._should_upgrade()
        elif task_name == "alliance_activities":
            return await self._should_do_alliance()

        # Default: allow execution
        return True

    def _is_active_hours(self) -> bool:
        """
        Check if current time is within active play hours

        Returns:
            True if active, False if should be idle/sleeping
        """
        schedule_config = self.config.get("anti_ban", {}).get("play_schedule", {})

        if not schedule_config.get("enabled", False):
            return True  # No schedule restrictions

        current_hour = datetime.now().hour

        # Check sleep hours
        sleep_hours = schedule_config.get("sleep_hours", [])
        if len(sleep_hours) == 2:
            sleep_start, sleep_end = sleep_hours
            if sleep_start <= current_hour < sleep_end:
                logger.debug("Currently in sleep hours, bot idle")
                return False

        return True

    async def _should_farm(self) -> bool:
        """Check if should do resource farming"""
        farming_config = self.config.get("automation", {}).get("farming", {})

        if not farming_config.get("enabled", True):
            return False

        # Check daily attack limit
        max_attacks = farming_config.get("max_attacks_per_day", 6)
        attacks_today = self._get_executions_today("resource_farming")

        if attacks_today >= max_attacks:
            logger.debug(f"Daily farming limit reached ({attacks_today}/{max_attacks})")
            return False

        return True

    async def _should_hunt(self) -> bool:
        """Check if should do zombie hunting"""
        hunting_config = self.config.get("automation", {}).get("hunting", {})

        if not hunting_config.get("enabled", True):
            return False

        # TODO: Check stamina levels (via OCR)
        # For now, assume stamina is available
        return True

    async def _should_manage_troops(self) -> bool:
        """Check if should manage troops"""
        # TODO: Check if troops wounded or barracks idle
        return True

    async def _should_upgrade(self) -> bool:
        """Check if should do building upgrades"""
        # TODO: Check if builders idle and resources available
        return True

    async def _should_do_alliance(self) -> bool:
        """Check if should do alliance activities"""
        # TODO: Check for alliance notifications
        return True

    def _get_executions_today(self, task_name: str) -> int:
        """
        Get number of executions today for a task

        Args:
            task_name: Name of task

        Returns:
            Execution count
        """
        today = datetime.now().date()

        if task_name not in self.execution_history:
            return 0

        # Count executions from today
        count = sum(
            1
            for timestamp in self.execution_history[task_name]
            if timestamp.date() == today
        )

        return count

    def record_execution(self, task_name: str):
        """
        Record task execution

        Args:
            task_name: Name of executed task
        """
        if task_name not in self.execution_history:
            self.execution_history[task_name] = []

        self.execution_history[task_name].append(datetime.now())

        # Keep only last 100 executions
        if len(self.execution_history[task_name]) > 100:
            self.execution_history[task_name] = self.execution_history[task_name][-100:]
