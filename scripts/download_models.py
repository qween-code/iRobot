#!/usr/bin/env python3
"""
Download pre-trained models for LastWarAutoBot

Supports:
- Roboflow Last War dataset (522 images, pre-trained)
- YOLO26/YOLO11/YOLOv8 base models from Ultralytics
- Custom trained models from project releases
"""

import sys
from pathlib import Path
from loguru import logger


def download_roboflow_model():
    """Download Last War detection model from Roboflow"""
    try:
        from roboflow import Roboflow

        # Roboflow Last War Survival Bot dataset
        # https://universe.roboflow.com/last-war-survival-bot/last-war-survival-bot-2-vxotg
        logger.info("Downloading Roboflow Last War model...")
        logger.info("Visit: https://universe.roboflow.com/last-war-survival-bot/last-war-survival-bot-2-vxotg")
        logger.info("You need a Roboflow API key to download the model.")
        logger.info("Set ROBOFLOW_API_KEY environment variable or enter it when prompted.")

        import os
        api_key = os.environ.get("ROBOFLOW_API_KEY")
        if not api_key:
            api_key = input("Enter Roboflow API key: ").strip()

        rf = Roboflow(api_key=api_key)
        project = rf.workspace("last-war-survival-bot").project("last-war-survival-bot-2-vxotg")
        version = project.version(1)
        dataset = version.download("yolov8")

        logger.success(f"Model downloaded to: {dataset.location}")
        return dataset.location

    except ImportError:
        logger.error("Roboflow not installed. Run: pip install roboflow")
        return None
    except Exception as e:
        logger.error(f"Failed to download Roboflow model: {e}")
        return None


def download_ultralytics_base():
    """Download Ultralytics base model (YOLO26 or YOLOv8)"""
    try:
        from ultralytics import YOLO

        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)

        # Try YOLO26 first (latest)
        model_variants = [
            ("yolo26n.pt", "YOLO26 Nano (latest, edge-optimized)"),
            ("yolo11n.pt", "YOLO11 Nano"),
            ("yolov8n.pt", "YOLOv8 Nano"),
        ]

        for model_name, description in model_variants:
            try:
                logger.info(f"Downloading {description}...")
                model = YOLO(model_name)
                target_path = models_dir / model_name
                logger.success(f"Downloaded: {target_path}")
                return str(target_path)
            except Exception as e:
                logger.warning(f"Failed to download {model_name}: {e}")
                continue

        logger.error("Failed to download any Ultralytics model")
        return None

    except ImportError:
        logger.error("Ultralytics not installed. Run: pip install ultralytics")
        return None


def main():
    """Main download script"""
    logger.info("=" * 50)
    logger.info("LastWarAutoBot - Model Downloader")
    logger.info("=" * 50)

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    print("\nAvailable downloads:")
    print("1. Ultralytics base model (YOLO26/YOLO11/YOLOv8)")
    print("2. Roboflow Last War pre-trained model")
    print("3. All models")

    choice = input("\nSelect (1/2/3): ").strip()

    if choice in ("1", "3"):
        download_ultralytics_base()

    if choice in ("2", "3"):
        download_roboflow_model()

    logger.info("Download complete!")
    logger.info(f"Models saved in: {models_dir.absolute()}")


if __name__ == "__main__":
    main()
