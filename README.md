ESP32-S3 COLOR DETECTION DASHBOARD
Real-Time Computer Vision  |  Embedded Systems  |  Web Analytics
Technical Documentation & Developer Guide

ESP32-S3
Platform	OpenCV
Vision Engine	Flask
Backend	MJPEG
Streaming

1.  Project Overview
This project integrates hardware, computer vision, and web technologies into a seamless real-time pipeline. An ESP32-S3 camera module streams live MJPEG video over WiFi to a Python (Flask) backend, where OpenCV processes each frame in HSV color space to detect and annotate colored objects with bounding boxes and labels — all served to a live web dashboard.

ESP32-S3
Camera	→	WiFi
(HTTP Stream)	→	Python
(OpenCV)	→	Web Browser
(Dashboard)

2.  Key Features
Live MJPEG Streaming over WiFi
Real-time video feed from ESP32-S3 to browser with minimal latency.	Multi-Color Detection
Detects Red, Green, Blue, Yellow, Black, and White simultaneously.
Bounding Boxes & Labels
Per-object annotations rendered directly onto the video stream.	Web Dashboard
Browser-based remote monitoring — no additional software required.
HSV Color Space Processing
Lighting-robust detection using Hue-Saturation-Value thresholds.	Noise Reduction Pipeline
Gaussian blur + morphological transforms for clean detection.


3.  Technology Stack
Layer	Technology	Details
Hardware	ESP32-S3	Dual-core 240 MHz, 8MB PSRAM, OV2640/OV5640 camera
Backend	Python + Flask	REST API, MJPEG route, frame processing loop
Computer Vision	OpenCV (cv2)	HSV masking, contour detection, morphological transforms
Frontend	HTML5 + CSS3	Jinja2 templates, live stream embed, status overlays
Communication	HTTP MJPEG	Multipart JPEG stream over WiFi (2.4 GHz)

4.  Processing Pipeline
1.	Capture — ESP32-S3 streams continuous MJPEG video via its built-in HTTP web server over the local WiFi network.
2.	Preprocessing — Each frame is decoded from JPEG and converted from BGR to HSV color space for improved lighting robustness.
3.	Masking — Predefined HSV thresholds generate binary masks for each target color (Red, Green, Blue, Yellow, Black, White).
4.	Noise Reduction — GaussianBlur reduces pixel noise; morphological opening (erode then dilate) removes small false-positive blobs.
5.	Contour Detection — Contours are extracted from each mask and filtered; only those with an area exceeding 500 pixels are retained.
6.	Overlay Rendering — Bounding boxes and color labels are drawn onto the original frame using OpenCV drawing primitives.
7.	Streaming Output — Annotated frames are JPEG-encoded and served frame-by-frame via Flask's /video_feed multipart response.

5.  Installation & Setup
Step 1 — Clone the Repository
git clone https://github.com/YOUR_USERNAME/ESP32-Color-Detection-Dashboard.git
cd ESP32-Color-Detection-Dashboard

Step 2 — Install Python Dependencies
pip install -r requirements.txt

Step 3 — Flash and Configure ESP32
•	Upload the Camera Web Server firmware to your ESP32-S3 via Arduino IDE or ESP-IDF.
•	Connect the ESP32-S3 to your 2.4 GHz WiFi network.
color_server.py:

ESP32_STREAM_URL = "http://192.168.x.x/stream"

Step 4 — Run the Application
python color_server.py

Open your browser and navigate to: http://localhost:5000

6.  HSV Thresholding Configuration
Lighting conditions vary significantly across environments. Tune the HSV bounds below in color_server.py to match your setup.

Color	Lower HSV Bound	Upper HSV Bound
Red	[0, 120, 70]	[10, 255, 255]
Green	[36, 100, 100]	[86, 255, 255]
Blue	[94, 80, 2]	[126, 255, 255]
Yellow	[25, 150, 150]	[35, 255, 255]
Black	[0, 0, 0]	[180, 255, 30]
White	[0, 0, 200]	[180, 30, 255]

TIP	Modify HSV values in color_server.py based on your ambient lighting. Fluorescent vs. natural light can shift hue readings by 5–15 degrees.

7.  Hardware Requirements
Component	Specification
Microcontroller	ESP32-S3 — Dual-core Xtensa LX7, 240 MHz, 8MB PSRAM (recommended)
Camera Sensor	OV2640 or OV5640 camera module
Wireless	2.4 GHz IEEE 802.11 b/g/n WiFi
Power Supply	5V DC, minimum 2A stable supply
Host Machine	Any PC/Mac/Linux running Python 3.8+ with OpenCV

8.  Project Structure
ESP32-Color-Detection-Dashboard/
├── color_server.py        # Flask app + OpenCV processing pipeline
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Web dashboard (Jinja2 template)
└── static/
    ├── css/style.css      # Dashboard styling
    └── js/app.js          # Frontend logic

9.  Troubleshooting
Symptom	Likely Cause	Resolution
Low FPS	Weak WiFi signal or high resolution	Move ESP32 closer to router; set resolution to QVGA or CIF in firmware.
No Stream Visible	Network mismatch or wrong IP	Ensure ESP32 and host PC are on the same subnet; verify ESP32_STREAM_URL.
Colors Not Detected	Lighting mismatch	Retune HSV thresholds; avoid mixed/artificial lighting environments.
Stream Disconnects	Power instability	Use a 5V 2A rated supply; avoid USB hubs or underpowered ports.



10.  Future Roadmap
•	Edge Inference on ESP32 — Deploy a lightweight neural network using ESP-DL for on-device classification, reducing server load.
•	PID-Based Object Tracking — Implement a pan-tilt servo system with PID control to keep detected objects centered in frame.
•	WebSocket Streaming — Replace MJPEG polling with WebSockets to support multi-client streaming and lower latency.
•	CSV / Database Logging — Log detected object classes, timestamps, and confidence scores to CSV or SQLite for analytics.

Raunak Choudhary
Robotics  |  Artificial Intelligence  |  Computer Vision


