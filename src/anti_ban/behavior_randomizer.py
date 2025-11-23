"""
Behavior Randomizer - Human-like behavior simulation

Implements anti-ban techniques through randomization
"""

import time
import random
import numpy as np
from typing import Tuple, List
from datetime import datetime
from loguru import logger


class BehaviorRandomizer:
    """
    Randomize bot behavior to appear human-like
    """

    def __init__(self, config: dict):
        """
        Initialize behavior randomizer

        Args:
            config: Anti-ban configuration
        """
        self.config = config
        self.session_start = time.time()
        self.actions_count = 0

        # Session settings
        self.session_duration_range = config.get("session_duration_hours", [2, 4])
        self.break_duration_range = config.get("break_duration_minutes", [30, 120])

    def random_delay(self, min_sec: float = 5, max_sec: float = 60):
        """
        Random delay with Gaussian distribution

        Args:
            min_sec: Minimum delay in seconds
            max_sec: Maximum delay in seconds
        """
        distribution = self.config.get("delay_distribution", "gaussian")

        if distribution == "gaussian":
            # Gaussian distribution
            mean = (min_sec + max_sec) / 2
            std = (max_sec - min_sec) / 6  # 99.7% within range

            delay = np.random.normal(mean, std)
            delay = np.clip(delay, min_sec, max_sec)
        else:
            # Uniform distribution
            delay = random.uniform(min_sec, max_sec)

        logger.debug(f"Delaying for {delay:.2f} seconds")
        time.sleep(delay)

    def randomize_click(self, x: int, y: int) -> Tuple[int, int]:
        """
        Add variance to click coordinates

        Args:
            x, y: Original coordinates

        Returns:
            Randomized coordinates
        """
        variance = self.config.get("click_variance_pixels", 10)

        x_offset = random.randint(-variance, variance)
        y_offset = random.randint(-variance, variance)

        return (x + x_offset, y + y_offset)

    def should_take_break(self) -> bool:
        """
        Determine if bot should take a break

        Returns:
            True if should break
        """
        session_duration = time.time() - self.session_start

        # Convert hours to seconds
        min_duration = self.session_duration_range[0] * 3600
        max_duration = self.session_duration_range[1] * 3600

        # Random session duration
        target_duration = random.uniform(min_duration, max_duration)

        if session_duration >= target_duration:
            return True

        return False

    def get_break_duration(self) -> int:
        """
        Get random break duration

        Returns:
            Break duration in seconds
        """
        min_break = self.break_duration_range[0] * 60  # minutes to seconds
        max_break = self.break_duration_range[1] * 60

        duration = random.uniform(min_break, max_break)
        self.session_start = time.time() + duration  # Reset session timer

        return int(duration)

    def bezier_curve(
        self,
        start: Tuple[int, int],
        end: Tuple[int, int],
        control_points: int = 2,
        steps: int = 20,
    ) -> List[Tuple[int, int]]:
        """
        Generate Bezier curve for natural mouse movement

        Args:
            start: Start coordinates
            end: End coordinates
            control_points: Number of control points
            steps: Number of points in curve

        Returns:
            List of coordinates along curve
        """
        # Generate random control points
        controls = []
        for _ in range(control_points):
            cx = random.randint(
                min(start[0], end[0]) - 50, max(start[0], end[0]) + 50
            )
            cy = random.randint(
                min(start[1], end[1]) - 50, max(start[1], end[1]) + 50
            )
            controls.append((cx, cy))

        # All points (start + controls + end)
        points = [start] + controls + [end]

        # Generate Bezier curve
        curve = []
        for t in np.linspace(0, 1, steps):
            point = self._bezier_point(points, t)
            curve.append((int(point[0]), int(point[1])))

        return curve

    def _bezier_point(self, points: List[Tuple[int, int]], t: float) -> Tuple[float, float]:
        """
        Calculate point on Bezier curve at parameter t

        Args:
            points: Control points
            t: Parameter (0 to 1)

        Returns:
            Point coordinates
        """
        n = len(points) - 1
        x = sum(
            self._binomial_coeff(n, i) * (1 - t) ** (n - i) * t ** i * points[i][0]
            for i in range(n + 1)
        )
        y = sum(
            self._binomial_coeff(n, i) * (1 - t) ** (n - i) * t ** i * points[i][1]
            for i in range(n + 1)
        )
        return (x, y)

    def _binomial_coeff(self, n: int, k: int) -> int:
        """Calculate binomial coefficient"""
        if k < 0 or k > n:
            return 0
        if k == 0 or k == n:
            return 1

        # Use factorial
        from math import factorial

        return factorial(n) // (factorial(k) * factorial(n - k))
