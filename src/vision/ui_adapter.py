"""
UI Adapter - Dynamic UI adaptation system

This module handles:
- Detecting UI changes after game updates
- Auto-learning new button positions
- Template matching with fuzzy logic
- Multi-version UI support
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import cv2
from loguru import logger
from datetime import datetime


class UIAdapter:
    """
    Dynamically adapt to UI changes after game updates
    """

    def __init__(self, config: Dict):
        """
        Initialize UI adapter

        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.ui_database_path = Path("data/ui_database.json")
        self.templates_dir = Path("data/templates")
        self.screenshots_dir = Path("data/screenshots")

        # Create directories
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Load UI database
        self.ui_database = self._load_ui_database()

        # Current game version
        self.game_version = None

        logger.info("UI Adapter initialized")

    def _load_ui_database(self) -> Dict:
        """
        Load UI element database

        Returns:
            UI database dictionary
        """
        if self.ui_database_path.exists():
            with open(self.ui_database_path, 'r') as f:
                return json.load(f)
        else:
            # Initialize empty database
            return {
                "versions": {},
                "elements": {},
                "last_updated": None
            }

    def save_ui_database(self):
        """Save UI database to disk"""
        self.ui_database["last_updated"] = datetime.now().isoformat()

        with open(self.ui_database_path, 'w') as f:
            json.dump(self.ui_database, f, indent=2)

        logger.debug("UI database saved")

    def detect_game_version(self, screenshot: np.ndarray) -> Optional[str]:
        """
        Detect game version from screenshot

        Args:
            screenshot: Game screenshot

        Returns:
            Version string or None
        """
        # TODO: Implement version detection
        # Could use OCR on version text in settings
        # Or hash-based fingerprinting of UI elements

        # For now, return None (unknown version)
        return None

    def find_element(
        self,
        screenshot: np.ndarray,
        element_name: str,
        confidence: float = 0.8
    ) -> Optional[Tuple[int, int]]:
        """
        Find UI element with adaptive template matching

        Args:
            screenshot: Current screenshot
            element_name: Name of element to find
            confidence: Minimum confidence threshold

        Returns:
            (x, y) coordinates or None
        """
        # Check if element exists in database
        if element_name not in self.ui_database["elements"]:
            logger.warning(f"Element '{element_name}' not in database")
            return None

        element_data = self.ui_database["elements"][element_name]

        # Try all known templates for this element
        for template_info in element_data.get("templates", []):
            template_path = Path(template_info["path"])

            if not template_path.exists():
                continue

            # Load template
            template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)

            # Multi-scale template matching
            result = self._multi_scale_match(screenshot, template, confidence)

            if result:
                # Update success statistics
                template_info["last_used"] = datetime.now().isoformat()
                template_info["success_count"] = template_info.get("success_count", 0) + 1
                self.save_ui_database()

                return result

        logger.warning(f"Element '{element_name}' not found in screenshot")
        return None

    def _multi_scale_match(
        self,
        screenshot: np.ndarray,
        template: np.ndarray,
        confidence: float
    ) -> Optional[Tuple[int, int]]:
        """
        Multi-scale template matching (handles different UI scales)

        Args:
            screenshot: Source image
            template: Template image
            confidence: Minimum confidence

        Returns:
            (x, y) center coordinates or None
        """
        # Convert to grayscale
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Try different scales (0.8x to 1.2x)
        scales = [0.8, 0.9, 1.0, 1.1, 1.2]

        best_match = None
        best_confidence = 0

        for scale in scales:
            # Resize template
            width = int(gray_template.shape[1] * scale)
            height = int(gray_template.shape[0] * scale)

            if width <= 0 or height <= 0:
                continue

            resized_template = cv2.resize(gray_template, (width, height))

            # Skip if template is larger than screenshot
            if (resized_template.shape[0] > gray_screenshot.shape[0] or
                resized_template.shape[1] > gray_screenshot.shape[1]):
                continue

            # Template matching
            result = cv2.matchTemplate(
                gray_screenshot,
                resized_template,
                cv2.TM_CCOEFF_NORMED
            )

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val > best_confidence:
                best_confidence = max_val
                best_match = (
                    max_loc[0] + width // 2,
                    max_loc[1] + height // 2
                )

        if best_confidence >= confidence:
            logger.debug(f"Match found with confidence: {best_confidence:.2f}")
            return best_match

        return None

    def learn_element(
        self,
        screenshot: np.ndarray,
        element_name: str,
        bbox: Tuple[int, int, int, int],
        version: Optional[str] = None
    ):
        """
        Learn a new UI element from screenshot

        Args:
            screenshot: Screenshot containing element
            element_name: Name of element
            bbox: Bounding box (x1, y1, x2, y2)
            version: Game version (optional)
        """
        x1, y1, x2, y2 = bbox

        # Extract element from screenshot
        element_img = screenshot[y1:y2, x1:x2]

        # Generate template filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        template_filename = f"{element_name}_{timestamp}.png"
        template_path = self.templates_dir / template_filename

        # Save template
        cv2.imwrite(str(template_path), element_img)

        # Update database
        if element_name not in self.ui_database["elements"]:
            self.ui_database["elements"][element_name] = {
                "templates": [],
                "created": datetime.now().isoformat()
            }

        self.ui_database["elements"][element_name]["templates"].append({
            "path": str(template_path),
            "version": version,
            "created": datetime.now().isoformat(),
            "success_count": 0,
            "last_used": None
        })

        self.save_ui_database()
        logger.info(f"Learned new template for '{element_name}'")

    def auto_calibrate(self, screenshot: np.ndarray, known_elements: Dict[str, Tuple[int, int, int, int]]):
        """
        Auto-calibrate UI elements from a known good screenshot

        Args:
            screenshot: Screenshot with known elements
            known_elements: Dict of element_name -> bbox
        """
        logger.info("Starting auto-calibration...")

        for element_name, bbox in known_elements.items():
            self.learn_element(screenshot, element_name, bbox)

        logger.success(f"Calibrated {len(known_elements)} UI elements")

    def detect_ui_change(self, screenshot: np.ndarray) -> bool:
        """
        Detect if UI has changed (after game update)

        Args:
            screenshot: Current screenshot

        Returns:
            True if UI has changed
        """
        # Try to find critical elements
        critical_elements = [
            "city_button",
            "map_button",
            "menu_button"
        ]

        found_count = 0
        for element in critical_elements:
            if element in self.ui_database["elements"]:
                result = self.find_element(screenshot, element, confidence=0.7)
                if result:
                    found_count += 1

        # If less than 50% of critical elements found, UI likely changed
        if found_count < len(critical_elements) * 0.5:
            logger.warning("UI change detected! UI elements not found.")
            return True

        return False

    def get_element_stats(self, element_name: str) -> Dict:
        """
        Get statistics for an element

        Args:
            element_name: Element name

        Returns:
            Statistics dictionary
        """
        if element_name not in self.ui_database["elements"]:
            return {}

        element_data = self.ui_database["elements"][element_name]
        templates = element_data.get("templates", [])

        return {
            "total_templates": len(templates),
            "total_successes": sum(t.get("success_count", 0) for t in templates),
            "created": element_data.get("created"),
            "versions": list(set(t.get("version") for t in templates if t.get("version")))
        }
