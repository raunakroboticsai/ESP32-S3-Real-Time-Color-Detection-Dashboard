# ESP32-S3-Real-Time-Color-Detection-Dashboard
A high-performance computer vision pipeline that streams live video from an ESP32-S3 camera to a Python/Flask backend for real-time color segmentation and object tracking.
ESP32-S3 Color Detection Dashboard

A real-time computer vision system that bridges embedded hardware with web-based analytics. This project uses an ESP32-S3 camera module to stream live video to a Python backend, where OpenCV performs multi-color detection and serves the processed output to a web dashboard.

Project Overview

This project integrates hardware, computer vision, and web technologies into a seamless pipeline. The ESP32-S3 streams MJPEG video over WiFi, while a Python (Flask) server processes each frame in HSV color space to detect objects based on predefined color ranges.

Key Features
Live MJPEG streaming over WiFi
Multi-color detection (Red, Green, Blue, Yellow, Black, White)
Real-time bounding boxes and labels
Browser-based dashboard for monitoring
Optimized pipeline for smooth FPS
System Architecture
ESP32-S3 Camera  →  WiFi (HTTP Stream)  →  Python (OpenCV Processing)
                →  Flask Server        →  Web Browser (Dashboard UI)
Technology Stack
Layer	Technology
Hardware	ESP32-S3 Camera Module
Backend	Python, Flask
Computer Vision	OpenCV (cv2)
Frontend	HTML5, CSS3 (Jinja2 Templates)
Communication	HTTP MJPEG Streaming
How It Works
Capture
ESP32-S3 streams video using an onboard web server.
Preprocessing
Frames are converted from BGR → HSV for better lighting robustness.
Masking
HSV thresholds generate binary masks for each color.
Contour Detection
Objects are detected and filtered based on area.
Overlay Rendering
Bounding boxes and labels are drawn.
Streaming Output
Frames are sent via Flask /video_feed.
Installation and Setup
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/ESP32-Color-Detection-Dashboard.git
cd ESP32-Color-Detection-Dashboard
2. Install Dependencies
pip install -r requirements.txt
3. Configure ESP32

Upload Camera Web Server code and update:

ESP32_STREAM_URL = "http://192.168.x.x/stream"
4. Run the Application
python color_server.py

Open:

http://localhost:5000
🔧 Advanced Configuration (HSV Thresholding)

Lighting conditions vary across environments, so HSV values may need tuning.

Color	Lower HSV	Upper HSV
Red	[0,120,70]	[10,255,255]
Green	[36,100,100]	[86,255,255]
Blue	[94,80,2]	[126,255,255]
Yellow	[25,150,150]	[35,255,255]

Tip: Modify these values in color_server.py for best results under your lighting setup.

🛠️ Hardware Requirements
Microcontroller: ESP32-S3 (Dual-core, 240MHz, 8MB PSRAM recommended)
Camera: OV2640 / OV5640
Network: 2.4 GHz WiFi
Power Supply: 5V 2A stable supply
📈 Technical Deep Dive
Noise Reduction
Uses cv2.GaussianBlur() to smooth image and reduce pixel noise.
Morphological Transformations
Opening operation (Erode → Dilate) removes small unwanted blobs.
Contour Filtering
Only contours with area > 500 pixels are considered to avoid false detection.
⚠️ Troubleshooting (FAQs)

Low FPS?

Check WiFi signal strength
Reduce resolution to QVGA/CIF

No Stream?

Ensure ESP32 and PC are on same WiFi network

Colors not detecting?

Adjust HSV values
Avoid mixed/artificial lighting
📊 Performance Optimization
HSV color space improves robustness
Morphological filtering reduces noise
480p resolution balances speed and accuracy
📁 Project Structure
ESP32-Color-Detection-Dashboard/
│
├── color_server.py
├── templates/
├── static/
├── requirements.txt
└── README.md
🚀 Future Roadmap
 Edge inference on ESP32 (ESP-DL)
 PID-based object tracking (pan-tilt system)
 Multi-client streaming (WebSockets)
 CSV logging of detected objects
Author

Raunak Choudhary
Robotics | Artificial Intelligence | Computer Vision

License

This project is open-source and available under the MIT License.
