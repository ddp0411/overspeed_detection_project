# backend.py

import cv2
import pandas as pd
from detection.vehicle_detector import VehicleDetector
from detection.ocr_reader import OCRReader
from tracking.entry_exit_tracker import EntryExitTracker
from tracking.speed_calculator import SpeedCalculator
from config.settings import USE_PHONE_CAMERA_FOR_ENTRY, ENTRY_CAMERA_URL, ENTRY_CAMERA_ID, EXIT_CAMERA_ID
import os

os.makedirs('data', exist_ok=True)

vehicle_detector = VehicleDetector()
ocr_reader = OCRReader()
tracker = EntryExitTracker()
speed_calc = SpeedCalculator()

# Initialize cameras
cap_entry = cv2.VideoCapture(ENTRY_CAMERA_URL if USE_PHONE_CAMERA_FOR_ENTRY else ENTRY_CAMERA_ID)
cap_exit = cv2.VideoCapture(EXIT_CAMERA_ID)

vehicle_records = pd.DataFrame(columns=["Plate", "Entry_Time", "Exit_Time", "Time_Taken_sec", "Speed_kmph", "Status"])

while True:
    ret_entry, frame_entry = cap_entry.read()
    ret_exit, frame_exit = cap_exit.read()

    if not ret_entry or not ret_exit:
        print("Error with camera connection")
        break

    # ENTRY CAMERA
    detections_entry = vehicle_detector.detect_vehicles(frame_entry)
    for cropped, (x1, y1, x2, y2) in detections_entry:
        plate = ocr_reader.read_plate(cropped)
        if plate:
            tracker.register_entry(plate)
            cv2.rectangle(frame_entry, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame_entry, plate, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    # EXIT CAMERA
    detections_exit = vehicle_detector.detect_vehicles(frame_exit)
    for cropped, (x1, y1, x2, y2) in detections_exit:
        plate = ocr_reader.read_plate(cropped)
        if plate and tracker.register_exit(plate):
            entry_time, exit_time = tracker.get_entry_exit_times(plate)
            speed_kmph, status = speed_calc.calculate_speed(entry_time, exit_time)
            time_taken_sec = (exit_time - entry_time).total_seconds()

            vehicle_records = vehicle_records.append({
                "Plate": plate,
                "Entry_Time": entry_time.strftime('%H:%M:%S'),
                "Exit_Time": exit_time.strftime('%H:%M:%S'),
                "Time_Taken_sec": round(time_taken_sec, 2),
                "Speed_kmph": round(speed_kmph, 2),
                "Status": status
            }, ignore_index=True)

            vehicle_records.to_csv('data/vehicle_records.csv', index=False)
            print(f"[SAVED] {plate} -> {speed_kmph:.2f} km/h | Status: {status}")

            cv2.rectangle(frame_exit, (x1, y1), (x2, y2), (0,0,255), 2)
            cv2.putText(frame_exit, plate, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Entry Camera", frame_entry)
    cv2.imshow("Exit Camera", frame_exit)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_entry.release()
cap_exit.release()
cv2.destroyAllWindows()
