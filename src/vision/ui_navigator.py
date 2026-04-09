"""
UI Navigator - High-level vision interface

Combines YOLO, Template Matching, and OCR to find elements and read state.
Acts as the main entry point for the bot to "see" the game.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger

from .yolo_detector import YOLODetector
from .template_matcher import TemplateMatcher
from .ocr_reader import OCRReader


class UINavigator:
    """
    Unified vision interface for the bot
    """

    def __init__(self, config: Dict):
        """
        Initialize UI Navigator

        Args:
            config: Vision configuration
        """
        self.config = config

        # Initialize subsystems
        self.yolo = YOLODetector(config)
        self.matcher = TemplateMatcher(
            templates_dir=config.get("templates_dir", "src/assets/templates"),
            threshold=config.get("match_threshold", 0.8)
        )
        self.ocr = OCRReader(
            use_gpu=config.get("use_gpu", False)
        )

    def find_element(self, image: np.ndarray, name: str, method: str = "auto") -> Optional[Dict]:
        """
        Find a UI element by name

        Args:
            image: Screenshot
            name: Name of element (class name for YOLO or filename for Template)
            method: 'auto', 'yolo', or 'template'

        Returns:
            Element dict {bbox, center, confidence} or None
        """
        result = None

        # 1. Try YOLO first (fastest and most robust for objects)
        if method in ["auto", "yolo"]:
            bbox_center = self.yolo.find_button(image, name)
            if bbox_center:
                logger.debug(f"Found '{name}' using YOLO")
                return {
                    "method": "yolo",
                    "center": bbox_center,
                    # Note: YOLO wrapper currently returns only center for find_button
                    # Ideally we should update it to return full dict
                    "confidence": 0.8  # placeholder
                }

        # 2. Try Template Matching (precise for static buttons)
        if method in ["auto", "template"] and not result:
            result = self.matcher.match(image, name)
            if result:
                logger.debug(f"Found '{name}' using Template Matching")
                result["method"] = "template"
                return result

        return None

    def find_all_elements(self, image: np.ndarray) -> List[Dict]:
        """
        Find all recognizable elements in the image

        Args:
            image: Screenshot

        Returns:
            List of detected elements
        """
        results = []

        # Get YOLO detections
        yolo_results = self.yolo.detect_elements(image)
        for res in yolo_results:
            res["method"] = "yolo"
            results.append(res)

        # Get Template matches
        # Note: This might duplicate if both methods detect the same thing
        # In a real scenario, we would implement Non-Maximum Suppression (NMS) here
        tpl_results = self.matcher.match_all(image)
        for res in tpl_results:
            res["method"] = "template"
            results.append(res)

        return results

    def get_text(self, image: np.ndarray, region: Optional[List[int]] = None) -> str:
        """
        Read text from screen or region

        Args:
            image: Screenshot
            region: [x, y, w, h]

        Returns:
            Text content
        """
        return self.ocr.read_text(image, region)

    def get_resource_amount(self, image: np.ndarray, resource_type: str) -> int:
        """
        Get amount of specific resource

        Args:
            image: Screenshot
            resource_type: 'gold', 'iron', 'food'

        Returns:
            Resource amount
        """
        # This requires knowing where the resource counters are on screen
        # We can either hardcode coordinates or find the icon then read text next to it

        # Strategy: Find resource icon -> Read text to the right of it
        icon_name = f"icon_{resource_type}"
        icon = self.find_element(image, icon_name)

        if icon:
            # Define region to right of icon
            # This is a heuristic and would need tuning based on actual UI
            cx, cy = icon["center"]
            w = 100 # approximate width of text area
            h = 30  # approximate height

            # Assuming icon is roughly 40x40
            region = [cx + 20, cy - 15, w, h]

            return self.ocr.read_number(image, region)

        return 0
