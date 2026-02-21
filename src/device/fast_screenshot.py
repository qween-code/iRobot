"""
Fast Screenshot Pipeline - High-speed screen capture

Uses adbnativeblitz/adbblitz for scrcpy-speed native ADB screenshots.
Falls back to py-scrcpy-client, then standard ADB screencap.

Based on research from:
- github.com/hansalemaos/adbnativeblitz
- github.com/hansalemaos/adbblitz
- github.com/leng-yue/py-scrcpy-client
"""

import asyncio
import time
from typing import Optional, Tuple
import numpy as np
from loguru import logger

# Try import fastest method first, fall back gracefully
CAPTURE_METHOD = "standard"

try:
    from adbblitz import AdbShotTCP
    CAPTURE_METHOD = "adbblitz"
    logger.info("Using adbblitz (fastest - H264 stream to NumPy)")
except ImportError:
    pass

if CAPTURE_METHOD == "standard":
    try:
        from adbnativeblitz import AdbFastScreenshots
        CAPTURE_METHOD = "adbnativeblitz"
        logger.info("Using adbnativeblitz (native fast screenshots)")
    except ImportError:
        pass

if CAPTURE_METHOD == "standard":
    try:
        import scrcpy
        CAPTURE_METHOD = "pyscrcpy"
        logger.info("Using py-scrcpy-client (scrcpy protocol)")
    except ImportError:
        pass

if CAPTURE_METHOD == "standard":
    logger.warning("No fast capture library found. Using standard ADB screencap (slow)")


class FastScreenCapture:
    """
    High-speed screen capture pipeline

    Priority order:
    1. adbblitz - H264 stream directly to NumPy (fastest, ~5ms)
    2. adbnativeblitz - Native ADB fast screenshots (~10ms)
    3. py-scrcpy-client - scrcpy protocol (~15ms)
    4. Standard ADB screencap - fallback (~200ms)
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5555, max_fps: int = 30):
        """
        Initialize fast screen capture

        Args:
            host: ADB host
            port: ADB port
            max_fps: Maximum capture FPS
        """
        self.host = host
        self.port = port
        self.max_fps = max_fps
        self.device_id = f"{host}:{port}"

        self._capture_client = None
        self._last_frame: Optional[np.ndarray] = None
        self._frame_count = 0
        self._start_time = time.time()
        self._running = False

        logger.info(f"FastScreenCapture initialized (method: {CAPTURE_METHOD})")

    async def start(self):
        """Start continuous screen capture"""
        if self._running:
            return

        self._running = True
        self._start_time = time.time()

        if CAPTURE_METHOD == "adbblitz":
            await self._start_adbblitz()
        elif CAPTURE_METHOD == "adbnativeblitz":
            await self._start_adbnativeblitz()
        elif CAPTURE_METHOD == "pyscrcpy":
            await self._start_pyscrcpy()
        else:
            logger.info("Using standard ADB screencap (on-demand)")

    async def _start_adbblitz(self):
        """Start adbblitz H264 stream capture"""
        try:
            self._capture_client = AdbShotTCP(
                device_serial=self.device_id,
                max_frame_rate=self.max_fps,
                max_video_width=1920,
                frame_buffer=4,
                lock_video_orientation=0,
            )
            logger.success("adbblitz capture started")
        except Exception as e:
            logger.error(f"adbblitz start failed: {e}")

    async def _start_adbnativeblitz(self):
        """Start adbnativeblitz native capture"""
        try:
            self._capture_client = AdbFastScreenshots(
                adb_path="adb",
                device_serial=self.device_id,
                time_interval=1 / self.max_fps,
                width=1920,
                height=1080,
            )
            logger.success("adbnativeblitz capture started")
        except Exception as e:
            logger.error(f"adbnativeblitz start failed: {e}")

    async def _start_pyscrcpy(self):
        """Start py-scrcpy-client capture"""
        try:
            client = scrcpy.Client(device=self.device_id, max_fps=self.max_fps)

            def on_frame(frame):
                if frame is not None:
                    self._last_frame = frame
                    self._frame_count += 1

            client.add_listener(scrcpy.EVENT_FRAME, on_frame)
            client.start(threaded=True)
            self._capture_client = client
            logger.success("py-scrcpy-client capture started")
        except Exception as e:
            logger.error(f"py-scrcpy-client start failed: {e}")

    async def capture(self) -> Optional[np.ndarray]:
        """
        Capture a single frame

        Returns:
            BGR numpy array or None
        """
        try:
            if CAPTURE_METHOD == "adbblitz" and self._capture_client:
                frame = self._capture_client.screenshot
                if frame is not None:
                    self._last_frame = frame
                    self._frame_count += 1
                    return frame

            elif CAPTURE_METHOD == "adbnativeblitz" and self._capture_client:
                frame = self._capture_client.screenshot
                if frame is not None:
                    self._last_frame = frame
                    self._frame_count += 1
                    return frame

            elif CAPTURE_METHOD == "pyscrcpy" and self._capture_client:
                # py-scrcpy-client uses callback, return cached frame
                return self._last_frame

            else:
                # Fallback: standard ADB screencap
                return await self._standard_screencap()

        except Exception as e:
            logger.error(f"Capture failed: {e}")
            return await self._standard_screencap()

    async def _standard_screencap(self) -> Optional[np.ndarray]:
        """
        Standard ADB screencap fallback (~200ms)

        Returns:
            BGR numpy array or None
        """
        try:
            process = await asyncio.create_subprocess_shell(
                f"adb -s {self.device_id} exec-out screencap -p",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, _ = await process.communicate()

            if stdout:
                from PIL import Image
                from io import BytesIO

                image = Image.open(BytesIO(stdout))
                img_array = np.array(image)

                # Convert RGBA to BGR for OpenCV
                if img_array.shape[2] == 4:
                    img_bgr = img_array[:, :, :3][:, :, ::-1]
                else:
                    img_bgr = img_array[:, :, ::-1]

                self._last_frame = img_bgr
                self._frame_count += 1
                return img_bgr

        except Exception as e:
            logger.error(f"Standard screencap failed: {e}")

        return None

    def get_fps(self) -> float:
        """Get current capture FPS"""
        elapsed = time.time() - self._start_time
        if elapsed > 0:
            return self._frame_count / elapsed
        return 0.0

    async def stop(self):
        """Stop screen capture"""
        self._running = False

        if CAPTURE_METHOD == "pyscrcpy" and self._capture_client:
            self._capture_client.stop()

        self._capture_client = None
        logger.info(f"Screen capture stopped (avg FPS: {self.get_fps():.1f})")
