# detection/ocr_reader.py

import cv2
import pytesseract
from config.settings import TESSERACT_CMD

class OCRReader:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

    def read_plate(self, cropped_img):
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        text = pytesseract.image_to_string(gray, config='--psm 8')
        plate = text.strip().replace(" ", "").replace("\n", "")
        if len(plate) >= 5:
            return plate
        else:
            return None
