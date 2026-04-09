"""
OCR Reader - Text extraction from images

Uses EasyOCR (primary) and Tesseract (fallback) to read text from game UI
"""

import numpy as np
import cv2
from typing import Optional, Union, List, Dict
from loguru import logger

# Try to import OCR engines
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR not installed")

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("Pytesseract not installed")


class OCRReader:
    """
    OCR Reader for extracting text from game UI
    """

    def __init__(self, use_gpu: bool = False, languages: List[str] = ['en']):
        """
        Initialize OCR Reader

        Args:
            use_gpu: Whether to use GPU for EasyOCR
            languages: List of languages to support
        """
        self.use_gpu = use_gpu
        self.languages = languages
        self.reader = None
        self.engine = "none"

        self._init_engine()

    def _init_engine(self):
        """Initialize the best available OCR engine"""
        if EASYOCR_AVAILABLE:
            try:
                logger.info(f"Initializing EasyOCR (GPU={self.use_gpu})...")
                self.reader = easyocr.Reader(self.languages, gpu=self.use_gpu)
                self.engine = "easyocr"
                logger.success("EasyOCR initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize EasyOCR: {e}")
                self._fallback_to_tesseract()
        elif TESSERACT_AVAILABLE:
            self._fallback_to_tesseract()
        else:
            logger.error("No OCR engine available (EasyOCR or Tesseract)")

    def _fallback_to_tesseract(self):
        """Switch to Tesseract if available"""
        if TESSERACT_AVAILABLE:
            self.engine = "tesseract"
            logger.info("Using Tesseract as OCR engine")
        else:
            self.engine = "none"
            logger.error("Tesseract also unavailable")

    def read_text(self, image: np.ndarray, region: Optional[List[int]] = None, allowlist: str = None) -> str:
        """
        Read text from an image (or specific region)

        Args:
            image: Source image
            region: Optional crop region [x, y, w, h]
            allowlist: Optional string of allowed characters (EasyOCR only)

        Returns:
            Detected text string
        """
        if self.engine == "none":
            logger.warning("OCR not initialized")
            return ""

        # Crop image if region provided
        if region:
            x, y, w, h = region
            image = image[y:y+h, x:x+w]

        # Preprocess for better accuracy
        processed_img = self._preprocess(image)

        try:
            if self.engine == "easyocr":
                return self._read_easyocr(processed_img, allowlist)
            elif self.engine == "tesseract":
                return self._read_tesseract(processed_img)
        except Exception as e:
            logger.error(f"OCR reading failed: {e}")
            return ""

        return ""

    def _read_easyocr(self, image: np.ndarray, allowlist: str = None) -> str:
        """Read using EasyOCR"""
        if not self.reader:
            return ""

        # EasyOCR expects RGB
        if len(image.shape) == 3:
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = image # already gray or similar

        results = self.reader.readtext(img_rgb, detail=0, allowlist=allowlist)
        return " ".join(results)

    def _read_tesseract(self, image: np.ndarray) -> str:
        """Read using Tesseract"""
        # Tesseract expects RGB or Gray
        text = pytesseract.image_to_string(image)
        return text.strip()

    def _preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better OCR results
        """
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # Apply thresholding to binarize (good for text)
        # Otsu's thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Sometimes inverting helps if text is white on black
        # For now, return standard threshold
        return thresh

    def read_number(self, image: np.ndarray, region: Optional[List[int]] = None) -> int:
        """
        Read a numeric value from the image

        Args:
            image: Source image
            region: Optional crop region

        Returns:
            Integer value (or 0 if failed)
        """
        text = self.read_text(image, region, allowlist="0123456789")

        # Clean text (remove non-digits)
        digits = "".join(c for c in text if c.isdigit())

        if digits:
            return int(digits)
        return 0
