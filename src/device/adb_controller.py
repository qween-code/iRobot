"""
ADB Controller - Android Debug Bridge interface

Handles all device communication via ADB
"""

import asyncio
import base64
from typing import Tuple, Optional
from loguru import logger
import numpy as np
from PIL import Image
from io import BytesIO


class ADBController:
    """
    ADB controller for Android device communication
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5555):
        """
        Initialize ADB controller

        Args:
            host: ADB host address
            port: ADB port
        """
        self.host = host
        self.port = port
        self.device_id = f"{host}:{port}"
        self.connected = False

    async def connect(self) -> bool:
        """
        Connect to ADB device

        Returns:
            True if connected successfully
        """
        try:
            # Connect to device
            result = await self._run_adb_command(f"connect {self.device_id}")

            if "connected" in result.lower() or "already connected" in result.lower():
                self.connected = True
                logger.success(f"Connected to ADB device: {self.device_id}")
                return True
            else:
                logger.error(f"Failed to connect to ADB: {result}")
                return False

        except Exception as e:
            logger.error(f"ADB connection error: {e}")
            return False

    async def disconnect(self):
        """Disconnect from ADB device"""
        if self.connected:
            await self._run_adb_command(f"disconnect {self.device_id}")
            self.connected = False
            logger.info("Disconnected from ADB")

    async def screenshot(self) -> np.ndarray:
        """
        Capture screenshot from device

        Returns:
            Screenshot as numpy array (BGR format for OpenCV)
        """
        try:
            # Use screencap to get screenshot
            result = await self.shell("screencap -p")

            # Convert to image
            image = Image.open(BytesIO(result.encode('latin1')))

            # Convert to numpy array (RGB -> BGR for OpenCV)
            img_array = np.array(image)
            img_bgr = img_array[:, :, ::-1]  # RGB to BGR

            return img_bgr

        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            raise

    async def tap(self, x: int, y: int):
        """
        Tap at coordinates

        Args:
            x: X coordinate
            y: Y coordinate
        """
        await self.shell(f"input tap {x} {y}")
        logger.debug(f"Tapped at ({x}, {y})")

    async def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500):
        """
        Swipe from one point to another

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Swipe duration in milliseconds
        """
        await self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
        logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")

    async def text(self, text: str):
        """
        Input text

        Args:
            text: Text to input
        """
        # Escape special characters
        escaped_text = text.replace(" ", "%s")
        await self.shell(f"input text {escaped_text}")

    async def press_key(self, keycode: int):
        """
        Press a key

        Args:
            keycode: Android keycode
        """
        await self.shell(f"input keyevent {keycode}")

    async def press_back(self):
        """Press back button"""
        await self.press_key(4)  # KEYCODE_BACK

    async def press_home(self):
        """Press home button"""
        await self.press_key(3)  # KEYCODE_HOME

    async def shell(self, command: str) -> str:
        """
        Execute shell command on device

        Args:
            command: Shell command

        Returns:
            Command output
        """
        result = await self._run_adb_command(f"-s {self.device_id} shell {command}")
        return result

    async def _run_adb_command(self, args: str) -> str:
        """
        Run ADB command

        Args:
            args: ADB command arguments

        Returns:
            Command output
        """
        try:
            process = await asyncio.create_subprocess_shell(
                f"adb {args}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                if error_msg:
                    raise Exception(f"ADB command failed: {error_msg}")

            return stdout.decode().strip()

        except Exception as e:
            logger.error(f"ADB command error: {e}")
            raise
