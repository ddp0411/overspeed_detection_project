# 🚗 Advanced Vehicle Overspeed Detection System

> Real-time Speed Violation Detection using Dual Cameras, YOLOv8, OCR, and Streamlit Dashboard

---

## 📂 Project Structure

```plaintext
overspeed_detection_project/
├── backend.py                 # Main Backend to detect vehicles and plates
├── app.py                     # Streamlit Web App
├── requirements.txt           # Required libraries
│
├── config/
│   └── settings.py             # Settings (speed limit, camera IDs, paths)
│
├── detection/
│   ├── vehicle_detector.py     # YOLOv8 vehicle and plate detection
│   └── ocr_reader.py           # OCR module using Tesseract
│
├── tracking/
│   ├── entry_exit_tracker.py   # Track entry/exit of vehicles
│   └── speed_calculator.py     # Calculate speed and status
│
├── data/
│   └── vehicle_records.csv     # Output data stored here
│   └── users.json              # Login Data of Users     
└── assets/
    └── Output Images
# 🚀 Quick Start
# 1. Install Requirements
     pip install -r requirements.txt
2. Install Tesseract OCR
     Download and install from Tesseract OCR UB Mannheim
     Update TESSERACT_CMD path in config/settings.py
3. Start Backend (Vehicle Detection)
    python backend.py
4. Start Streamlit Dashboard
    streamlit run app.py
Backend and Web app should be run in separate terminals.

✨ Features
Dual Camera Setup (Entry and Exit Points)

Real-Time YOLOv8 Vehicle Detection

Automatic License Plate Recognition

Entry/Exit Time Stamping

Speed Calculation based on Distance

Overspeed Detection and Reporting

Streamlit Interactive Dashboard

Live Auto-Refreshing Monitoring

Colored KPIs and Graphs

CSV Records Saving

📈 Dashboard Highlights
Live Table of All Detected Vehicles

Overspeeding Vehicles Highlighted in RED

Total Vehicles, Overspeeding vs Normal

Auto-Refresh every 10 seconds

Responsive Streamlit UI

🔧 Configurations
Change settings easily from config/settings.py:

Speed Limit

Distance between checkpoints

Camera IDs (0/1)

YOLO Model Path

Tesseract Path

💡 Future Improvements
SMS/Email Alerts for Overspeeding

Advanced tracking using vehicle IDs

Full IP Camera Integration

Docker Deployment

Cloud Storage for Vehicle Data
