# detection/vehicle_detector.py

import cv2
from ultralytics import YOLO
from config.settings import YOLO_MODEL_PATH

class VehicleDetector:
    def __init__(self):
        self.model = YOLO(YOLO_MODEL_PATH)

    def detect_vehicles(self, frame, conf_threshold=0.5):
        results = self.model.predict(frame, conf=conf_threshold)
        detections = []

        if results[0].boxes:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                cropped = frame[y1:y2, x1:x2]
                if cropped.shape[0] > 20 and cropped.shape[1] > 60:
                    detections.append((cropped, (x1, y1, x2, y2)))

        return detections
