"""
Template Matcher - OpenCV-based image matching

Uses OpenCV template matching to find static UI elements
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from loguru import logger


class TemplateMatcher:
    """
    OpenCV-based template matcher for UI elements
    """

    def __init__(self, templates_dir: str = "src/assets/templates", threshold: float = 0.8):
        """
        Initialize Template Matcher

        Args:
            templates_dir: Directory containing template images
            threshold: Default matching threshold
        """
        self.templates_dir = Path(templates_dir)
        self.threshold = threshold
        self.templates: Dict[str, np.ndarray] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all templates from directory"""
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory not found: {self.templates_dir}")
            return

        for img_path in self.templates_dir.glob("*.png"):
            try:
                # Read image in grayscale
                template = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                if template is not None:
                    self.templates[img_path.stem] = template
                    logger.debug(f"Loaded template: {img_path.stem}")
                else:
                    logger.warning(f"Failed to load template: {img_path}")
            except Exception as e:
                logger.error(f"Error loading template {img_path}: {e}")

        logger.info(f"Loaded {len(self.templates)} templates")

    def match(self, image: np.ndarray, template_name: str, threshold: Optional[float] = None) -> Optional[Dict]:
        """
        Find a template in the image

        Args:
            image: Source image (BGR or Grayscale)
            template_name: Name of template to find
            threshold: Confidence threshold (overrides default)

        Returns:
            Dictionary with match details or None
        """
        if template_name not in self.templates:
            logger.warning(f"Template not found: {template_name}")
            return None

        template = self.templates[template_name]
        match_threshold = threshold or self.threshold

        # Convert source image to grayscale if needed
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        try:
            # Multi-scale matching could be implemented here, but starting with simple matching
            # Match template
            result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= match_threshold:
                h, w = template.shape
                top_left = max_loc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                center = (top_left[0] + w // 2, top_left[1] + h // 2)

                return {
                    "class": template_name,
                    "confidence": float(max_val),
                    "bbox": [top_left[0], top_left[1], bottom_right[0], bottom_right[1]],
                    "center": center
                }

            return None

        except Exception as e:
            logger.error(f"Matching failed for {template_name}: {e}")
            return None

    def match_all(self, image: np.ndarray, threshold: Optional[float] = None) -> List[Dict]:
        """
        Find all known templates in the image

        Args:
            image: Source image
            threshold: Confidence threshold

        Returns:
            List of matches
        """
        matches = []
        for name in self.templates:
            match = self.match(image, name, threshold)
            if match:
                matches.append(match)
        return matches
