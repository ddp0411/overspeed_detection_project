# config/settings.py

# ========== CONFIG SETTINGS ==========

# Tesseract OCR Path
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# YOLOv8 Model Path
YOLO_MODEL_PATH = 'yolov8n.pt'

# Distance between Entry and Exit (meters)
DISTANCE_METERS = 300000  # 300 km

# Speed Limit (km/h)
SPEED_LIMIT = 100

# ========== CAMERA SETTINGS ==========

# Switch between Phone Camera and Webcam for Entry
USE_PHONE_CAMERA_FOR_ENTRY = True   # <<<<<< FLIP True/False here

# If using Phone, provide IP Camera URL
ENTRY_CAMERA_URL = "http://192.168.1.2:8080/video"  # Phone IP Camera URL

# If using Webcam, provide Camera ID
ENTRY_CAMERA_ID = 1

# Exit Camera always uses a Webcam
EXIT_CAMERA_ID = 0
