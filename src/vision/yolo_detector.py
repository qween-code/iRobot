"""
YOLO Detector - YOLOv8-based object detection

Uses YOLOv8 for detecting UI elements and game objects
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
import numpy as np
from loguru import logger

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    logger.warning("YOLOv8 not available, using template matching fallback")


class YOLODetector:
    """
    YOLOv8-based object detector for game UI elements
    """

    def __init__(self, config: Dict):
        """
        Initialize YOLO detector

        Args:
            config: AI configuration
        """
        self.config = config
        self.model_path = config.get("yolo_model", "models/lastwar_v8n.pt")
        self.confidence_threshold = config.get("confidence_threshold", 0.6)
        self.model = None
        self.loaded = False

        # Try to load model
        if YOLO_AVAILABLE:
            self._load_model()

    def _load_model(self):
        """Load YOLOv8 model"""
        try:
            model_file = Path(self.model_path)

            if not model_file.exists():
                logger.warning(f"YOLO model not found: {self.model_path}")
                logger.info("Please train or download a model first")
                return

            self.model = YOLO(str(model_file))
            self.loaded = True
            logger.success(f"YOLO model loaded: {self.model_path}")

        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")

    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.loaded

    def detect_elements(self, image: np.ndarray) -> List[Dict]:
        """
        Detect UI elements in image

        Args:
            image: Input image (BGR format)

        Returns:
            List of detected elements with bounding boxes
        """
        if not self.loaded:
            logger.warning("YOLO model not loaded, returning empty detections")
            return []

        try:
            # Run inference
            results = self.model(image, conf=self.confidence_threshold, verbose=False)

            # Parse detections
            detections = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    detection = {
                        "class": r.names[int(box.cls)],
                        "confidence": float(box.conf),
                        "bbox": box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                        "center": self._get_bbox_center(box.xyxy[0].tolist()),
                    }
                    detections.append(detection)

            logger.debug(f"Detected {len(detections)} elements")
            return detections

        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return []

    def find_button(self, image: np.ndarray, button_name: str) -> Optional[Tuple[int, int]]:
        """
        Find specific button by name

        Args:
            image: Input image
            button_name: Button class name

        Returns:
            Button center coordinates (x, y) or None
        """
        detections = self.detect_elements(image)

        # Find matching button
        buttons = [d for d in detections if d["class"] == button_name]

        if buttons:
            # Return highest confidence match
            best_button = max(buttons, key=lambda x: x["confidence"])
            return tuple(best_button["center"])

        return None

    def _get_bbox_center(self, bbox: List[float]) -> Tuple[int, int]:
        """
        Get center point of bounding box

        Args:
            bbox: [x1, y1, x2, y2]

        Returns:
            (x, y) center coordinates
        """
        x1, y1, x2, y2 = bbox
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        return (cx, cy)
