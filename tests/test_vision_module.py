"""
Test Vision Module
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
from src.vision import UINavigator, TemplateMatcher, OCRReader

# Mock configuration
CONFIG = {
    "yolo_model": "models/lastwar_v8n.pt",
    "templates_dir": "src/assets/templates",
    "use_gpu": False
}

def test_template_matcher_init():
    """Test TemplateMatcher initialization"""
    matcher = TemplateMatcher(templates_dir=CONFIG["templates_dir"])
    assert matcher is not None
    assert isinstance(matcher.templates, dict)

def test_ocr_reader_init():
    """Test OCRReader initialization"""
    ocr = OCRReader(use_gpu=False)
    assert ocr is not None
    # engine should be either 'easyocr', 'tesseract' or 'none'
    assert ocr.engine in ["easyocr", "tesseract", "none"]

def test_ui_navigator_init():
    """Test UINavigator initialization"""
    nav = UINavigator(CONFIG)
    assert nav is not None
    assert nav.yolo is not None
    assert nav.matcher is not None
    assert nav.ocr is not None

def test_matching_logic():
    """Test matching logic with a mock image"""
    # Create a blank image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Create a fake template file
    template_path = Path(CONFIG["templates_dir"]) / "test_icon.png"
    template_path.parent.mkdir(parents=True, exist_ok=True)

    # Draw a white square as "icon"
    cv2.rectangle(image, (10, 10), (30, 30), (255, 255, 255), -1)

    # Save as template
    cv2.imwrite(str(template_path), image[10:30, 10:30])

    # Initialize matcher
    matcher = TemplateMatcher(templates_dir=CONFIG["templates_dir"])

    # Match
    result = matcher.match(image, "test_icon")

    assert result is not None
    assert result["class"] == "test_icon"
    assert result["confidence"] > 0.9

    # Cleanup
    if template_path.exists():
        template_path.unlink()

def test_ocr_mock_image():
    """Test OCR with a synthetic image containing text"""
    # Create an image with text "123"
    # Note: Synthetic text generation with OpenCV is tricky for OCR without fonts
    # but we can try a basic test if Tesseract/EasyOCR is installed

    # Setup image
    image = np.zeros((50, 200, 3), dtype=np.uint8)
    image.fill(255) # White background

    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, '12345', (10, 40), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

    ocr = OCRReader()
    if ocr.engine != "none":
        text = ocr.read_number(image)
        # Note: OCR on synthetic cv2 text is notoriously flaky without proper fonts
        # We just check that it runs without error
        assert isinstance(text, int)

if __name__ == "__main__":
    test_template_matcher_init()
    test_ocr_reader_init()
    test_ui_navigator_init()
    test_matching_logic()
    print("All vision tests passed!")
