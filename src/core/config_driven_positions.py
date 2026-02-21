"""
Config-Driven Positions - JSON-based UI element positioning

Instead of hardcoded pixel positions, all UI element locations
are stored in JSON config files. This allows easy adaptation
when game updates change the UI layout.

Inspired by: github.com/NotEnoughTina/FirstLady (positions.json approach)
"""

import json
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from loguru import logger


class PositionManager:
    """
    Manage game UI element positions via JSON config

    All screen positions are externalized to JSON files,
    making the bot resilient to UI layout changes.
    """

    def __init__(self, positions_path: str = "configs/positions.json"):
        """
        Initialize position manager

        Args:
            positions_path: Path to positions JSON file
        """
        self.positions_path = Path(positions_path)
        self.positions: Dict = {}
        self.resolution = (1920, 1080)

        self._load_positions()

    def _load_positions(self):
        """Load positions from JSON file"""
        if self.positions_path.exists():
            with open(self.positions_path, 'r') as f:
                data = json.load(f)
                self.positions = data.get("elements", {})
                self.resolution = tuple(data.get("resolution", [1920, 1080]))
            logger.info(f"Loaded {len(self.positions)} UI positions")
        else:
            logger.warning(f"Positions file not found: {self.positions_path}")
            self._create_default_positions()

    def _create_default_positions(self):
        """Create default positions file"""
        default = {
            "resolution": [1920, 1080],
            "description": "UI element positions for Last War: Survival",
            "last_updated": None,
            "game_version": None,
            "elements": {
                "city_button": {"x": 120, "y": 950, "description": "City view button"},
                "map_button": {"x": 240, "y": 950, "description": "World map button"},
                "alliance_button": {"x": 360, "y": 950, "description": "Alliance button"},
                "events_button": {"x": 480, "y": 950, "description": "Events button"},
                "menu_button": {"x": 1800, "y": 50, "description": "Menu/settings button"},
                "collect_all": {"x": 960, "y": 800, "description": "Collect all resources"},
                "help_all": {"x": 1400, "y": 600, "description": "Help all alliance members"},
                "donate_button": {"x": 960, "y": 700, "description": "Alliance donation"},
                "hunt_button": {"x": 300, "y": 700, "description": "Zombie hunt button"},
                "heal_button": {"x": 600, "y": 700, "description": "Heal troops button"},
                "train_button": {"x": 900, "y": 700, "description": "Train troops button"},
                "rally_join": {"x": 960, "y": 800, "description": "Join rally button"},
                "confirm_button": {"x": 960, "y": 700, "description": "Confirm/OK button"},
                "cancel_button": {"x": 600, "y": 700, "description": "Cancel button"},
                "close_button": {"x": 1700, "y": 100, "description": "Close popup button"},
                "back_button": {"x": 100, "y": 50, "description": "Back/return button"},
            }
        }

        self.positions_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.positions_path, 'w') as f:
            json.dump(default, f, indent=2)

        self.positions = default["elements"]
        logger.info("Created default positions file")

    def get_position(self, element_name: str) -> Optional[Tuple[int, int]]:
        """
        Get position of UI element

        Args:
            element_name: Element name

        Returns:
            (x, y) coordinates or None
        """
        if element_name in self.positions:
            pos = self.positions[element_name]
            return (pos["x"], pos["y"])
        return None

    def update_position(self, element_name: str, x: int, y: int, description: str = ""):
        """
        Update/add a UI element position

        Args:
            element_name: Element name
            x: X coordinate
            y: Y coordinate
            description: Human-readable description
        """
        self.positions[element_name] = {
            "x": x,
            "y": y,
            "description": description
        }
        self._save_positions()
        logger.info(f"Updated position: {element_name} -> ({x}, {y})")

    def scale_positions(self, target_resolution: Tuple[int, int]):
        """
        Scale all positions to a different screen resolution

        Args:
            target_resolution: Target (width, height)
        """
        scale_x = target_resolution[0] / self.resolution[0]
        scale_y = target_resolution[1] / self.resolution[1]

        for name, pos in self.positions.items():
            pos["x"] = int(pos["x"] * scale_x)
            pos["y"] = int(pos["y"] * scale_y)

        self.resolution = target_resolution
        self._save_positions()
        logger.info(f"Positions scaled to {target_resolution}")

    def _save_positions(self):
        """Save positions to JSON"""
        data = {
            "resolution": list(self.resolution),
            "elements": self.positions
        }

        with open(self.positions_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all_positions(self) -> Dict:
        """Get all registered positions"""
        return self.positions.copy()

    def list_elements(self) -> List[str]:
        """List all registered element names"""
        return list(self.positions.keys())
