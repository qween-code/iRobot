"""
Game Version Detector

Detects game updates and version changes
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import numpy as np
from loguru import logger


class GameVersionDetector:
    """
    Detect game version and updates
    """

    def __init__(self):
        """Initialize game version detector"""
        self.version_db_path = Path("data/game_versions.json")
        self.version_db = self._load_version_db()

        self.current_version = None
        self.last_check = None

        logger.info("Game Version Detector initialized")

    def _load_version_db(self) -> Dict:
        """Load version database"""
        if self.version_db_path.exists():
            with open(self.version_db_path, 'r') as f:
                return json.load(f)
        else:
            return {
                "versions": [],
                "current": None,
                "last_updated": None
            }

    def save_version_db(self):
        """Save version database"""
        self.version_db["last_updated"] = datetime.now().isoformat()

        self.version_db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.version_db_path, 'w') as f:
            json.dump(self.version_db, f, indent=2)

    def detect_version(self, screenshot: np.ndarray) -> Optional[str]:
        """
        Detect game version from screenshot

        Methods:
        1. UI fingerprinting (hash of key UI elements)
        2. OCR version text (if visible in settings)
        3. APK version (via adb)

        Args:
            screenshot: Game screenshot

        Returns:
            Version string or None
        """
        # Method 1: UI Fingerprinting
        ui_fingerprint = self._generate_ui_fingerprint(screenshot)

        # Check if this fingerprint exists in database
        for version_info in self.version_db["versions"]:
            if version_info["fingerprint"] == ui_fingerprint:
                logger.info(f"Detected known version: {version_info['name']}")
                self.current_version = version_info["name"]
                return version_info["name"]

        # Unknown version - create new entry
        new_version = f"v{datetime.now().strftime('%Y%m%d_%H%M')}"
        logger.warning(f"Unknown game version detected, assigned: {new_version}")

        self.version_db["versions"].append({
            "name": new_version,
            "fingerprint": ui_fingerprint,
            "detected_at": datetime.now().isoformat(),
            "ui_changed": True  # Mark as UI changed
        })

        self.current_version = new_version
        self.save_version_db()

        return new_version

    def _generate_ui_fingerprint(self, screenshot: np.ndarray) -> str:
        """
        Generate UI fingerprint from screenshot

        Uses key areas of UI to create a hash

        Args:
            screenshot: Screenshot

        Returns:
            Fingerprint hash
        """
        # Extract key UI regions (buttons, menus, etc.)
        # For simplicity, use a resized version of entire screenshot
        resized = self._resize_for_fingerprint(screenshot)

        # Convert to bytes and hash
        image_bytes = resized.tobytes()
        fingerprint = hashlib.sha256(image_bytes).hexdigest()[:16]

        return fingerprint

    def _resize_for_fingerprint(self, screenshot: np.ndarray, size: int = 64) -> np.ndarray:
        """
        Resize screenshot for fingerprinting

        Args:
            screenshot: Original screenshot
            size: Target size (e.g., 64x64)

        Returns:
            Resized image
        """
        import cv2

        # Convert to grayscale
        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Resize
        resized = cv2.resize(gray, (size, size), interpolation=cv2.INTER_AREA)

        return resized

    async def check_for_update(self, adb_controller) -> bool:
        """
        Check if game has been updated (via APK version)

        Args:
            adb_controller: ADB controller instance

        Returns:
            True if update detected
        """
        try:
            # Get APK version
            package = "com.fungame.lastwar"
            version_code = await adb_controller.shell(
                f"dumpsys package {package} | grep versionCode"
            )

            if version_code:
                # Parse version code
                # Example output: "versionCode=123456789"
                version = version_code.strip()

                # Check if version changed
                last_version = self.version_db.get("last_apk_version")

                if last_version and last_version != version:
                    logger.warning(f"Game update detected! {last_version} -> {version}")
                    self.version_db["last_apk_version"] = version
                    self.save_version_db()
                    return True
                elif not last_version:
                    # First time
                    self.version_db["last_apk_version"] = version
                    self.save_version_db()

            return False

        except Exception as e:
            logger.error(f"Failed to check for update: {e}")
            return False

    def mark_ui_stable(self):
        """Mark current UI version as stable (no more changes expected)"""
        if self.current_version:
            for version_info in self.version_db["versions"]:
                if version_info["name"] == self.current_version:
                    version_info["ui_changed"] = False
                    version_info["stable_since"] = datetime.now().isoformat()

            self.save_version_db()
            logger.info(f"Marked version {self.current_version} as stable")

    def is_ui_changed(self) -> bool:
        """
        Check if UI has changed recently

        Returns:
            True if UI changed
        """
        if not self.current_version:
            return False

        for version_info in self.version_db["versions"]:
            if version_info["name"] == self.current_version:
                return version_info.get("ui_changed", False)

        return False
