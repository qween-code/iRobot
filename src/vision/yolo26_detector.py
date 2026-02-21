"""
YOLO26 Detector - Next-gen object detection

Supports YOLO26 (2026), YOLO11 (2024), YOLOv8 (2023) with fallback chain.
Optimized for edge/mobile game UI detection.

Based on research:
- YOLO26: NMS-free, DFL-free, edge-optimized (arxiv.org/abs/2509.25164)
- Roboflow Last War dataset: 522 images pre-trained model
- VNIS UI dataset: 21 UI element classes
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
    logger.warning("Ultralytics not available - YOLO detection disabled")


class YOLO26Detector:
    """
    Next-gen YOLO detector with model fallback chain

    Priority: YOLO26 → YOLO11 → YOLOv8 → Template Matching
    """

    # Supported model generations
    MODEL_PRIORITY = ["yolo26", "yolo11", "yolov8"]

    def __init__(self, config: Dict):
        """
        Initialize YOLO26 detector

        Args:
            config: AI configuration
        """
        self.config = config
        self.model = None
        self.model_type = None
        self.loaded = False

        # Model paths (try in order)
        self.model_paths = {
            "yolo26": config.get("yolo26_model", "models/lastwar_yolo26n.pt"),
            "yolo11": config.get("yolo11_model", "models/lastwar_yolo11n.pt"),
            "yolov8": config.get("yolo_model", "models/lastwar_v8n.pt"),
        }

        # Detection settings
        self.confidence_threshold = config.get("confidence_threshold", 0.6)
        self.nms_threshold = config.get("nms_threshold", 0.45)

        # Class mappings for game UI elements
        self.class_names = {
            0: "collect_button",
            1: "attack_button",
            2: "hunt_button",
            3: "heal_button",
            4: "train_button",
            5: "upgrade_button",
            6: "alliance_button",
            7: "events_button",
            8: "map_button",
            9: "city_button",
            10: "close_button",
            11: "confirm_button",
            12: "cancel_button",
            13: "zombie_tile",
            14: "resource_tile",
            15: "player_base",
            16: "notification_badge",
            17: "stamina_bar",
            18: "resource_bar",
            19: "hero_icon",
            20: "anti_bot_modal",
        }

        if YOLO_AVAILABLE:
            self._load_best_model()

    def _load_best_model(self):
        """Load best available YOLO model"""
        for model_type in self.MODEL_PRIORITY:
            model_path = self.model_paths.get(model_type)

            if not model_path:
                continue

            model_file = Path(model_path)
            if not model_file.exists():
                logger.debug(f"{model_type} model not found: {model_path}")
                continue

            try:
                self.model = YOLO(str(model_file))
                self.model_type = model_type
                self.loaded = True
                logger.success(f"Loaded {model_type} model: {model_path}")

                # Log model info
                if model_type == "yolo26":
                    logger.info("YOLO26: NMS-free, DFL-free, edge-optimized")
                elif model_type == "yolo11":
                    logger.info("YOLO11: Enhanced CSPNet, anchor-free")
                else:
                    logger.info("YOLOv8: Anchor-free, C2f module")

                return

            except Exception as e:
                logger.error(f"Failed to load {model_type}: {e}")
                continue

        logger.warning("No YOLO model loaded - using template matching fallback")

    def is_loaded(self) -> bool:
        """Check if any model is loaded"""
        return self.loaded

    def detect_elements(self, image: np.ndarray) -> List[Dict]:
        """
        Detect UI elements in image

        Args:
            image: Input image (BGR format)

        Returns:
            List of detected elements
        """
        if not self.loaded:
            return []

        try:
            results = self.model(
                image,
                conf=self.confidence_threshold,
                iou=self.nms_threshold,
                verbose=False,
            )

            detections = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls)
                    cls_name = self.class_names.get(
                        cls_id, r.names.get(cls_id, f"class_{cls_id}")
                    )

                    bbox = box.xyxy[0].tolist()
                    detection = {
                        "class": cls_name,
                        "class_id": cls_id,
                        "confidence": float(box.conf),
                        "bbox": bbox,
                        "center": self._bbox_center(bbox),
                        "area": self._bbox_area(bbox),
                    }
                    detections.append(detection)

            logger.debug(f"Detected {len(detections)} elements via {self.model_type}")
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
            (x, y) center or None
        """
        detections = self.detect_elements(image)
        matches = [d for d in detections if d["class"] == button_name]

        if matches:
            best = max(matches, key=lambda x: x["confidence"])
            return tuple(best["center"])

        return None

    def find_all(self, image: np.ndarray, element_name: str) -> List[Dict]:
        """
        Find all instances of an element

        Args:
            image: Input image
            element_name: Element class name

        Returns:
            List of detections
        """
        detections = self.detect_elements(image)
        return [d for d in detections if d["class"] == element_name]

    def export_for_edge(self, format: str = "onnx") -> Optional[str]:
        """
        Export model for edge/mobile deployment

        Args:
            format: Export format (onnx, tflite, coreml, tensorrt)

        Returns:
            Path to exported model or None
        """
        if not self.loaded:
            return None

        try:
            export_path = self.model.export(format=format)
            logger.success(f"Model exported to {format}: {export_path}")
            return str(export_path)
        except Exception as e:
            logger.error(f"Model export failed: {e}")
            return None

    @staticmethod
    def _bbox_center(bbox: List[float]) -> Tuple[int, int]:
        """Get bounding box center"""
        x1, y1, x2, y2 = bbox
        return (int((x1 + x2) / 2), int((y1 + y2) / 2))

    @staticmethod
    def _bbox_area(bbox: List[float]) -> float:
        """Get bounding box area"""
        x1, y1, x2, y2 = bbox
        return abs(x2 - x1) * abs(y2 - y1)
