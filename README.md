
## ESP32-S3 Color Detection Dashboard

A real-time computer vision system that bridges embedded hardware with web-based analytics. This project uses an ESP32-S3 camera module to stream live video to a Python backend, where OpenCV performs multi-color detection and serves the processed output to a web dashboard.

## Project Overview

This project integrates hardware, computer vision, and web technologies into a seamless pipeline. The ESP32-S3 streams MJPEG video over WiFi, while a Python (Flask) server processes each frame in HSV color space to detect objects based on predefined color ranges.
<div align="center">

# ESP32-S3 Color Detection Dashboard

### Real-Time Computer Vision · Embedded Systems · Web Analytics

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![ESP32](https://img.shields.io/badge/ESP32--S3-240MHz-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> A real-time computer vision system that bridges embedded hardware with web-based analytics.  
> The ESP32-S3 streams live video over WiFi → Python + OpenCV detects colors → results stream to a live web dashboard.

</div>

---

## 📌 Table of Contents

- [Overview](#-project-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#️-technology-stack)
- [How It Works](#-how-it-works)
- [Installation & Setup](#-installation--setup)
- [HSV Configuration](#-advanced-configuration-hsv-thresholding)
- [Hardware Requirements](#️-hardware-requirements)
- [Project Structure](#-project-structure)
- [Troubleshooting](#️-troubleshooting)
- [Performance Optimization](#-performance-optimization)
- [Future Roadmap](#-future-roadmap)
- [Author](#-author)

---

##  Project Overview

This project integrates **hardware, computer vision, and web technologies** into a seamless real-time pipeline.

The **ESP32-S3 camera module** streams MJPEG video over WiFi to a **Python (Flask) backend**, where OpenCV processes each frame in **HSV color space** to detect and annotate colored objects — served live to a browser dashboard with zero additional software.

---

##  Key Features

| Feature | Description |
|---|---|
|  **Live MJPEG Streaming** | Real-time video feed from ESP32-S3 to browser over WiFi |
|  **Multi-Color Detection** | Detects Red, Green, Blue, Yellow, Black & White simultaneously |
|  **Bounding Boxes & Labels** | Per-object annotations rendered directly onto the video stream |
|  **Web Dashboard** | Browser-based remote monitoring — no extra software needed |
|  **HSV Color Space** | Lighting-robust detection using Hue-Saturation-Value thresholds |
|  **Noise Reduction Pipeline** | Gaussian blur + morphological transforms for clean detection |

---

##  System Architecture

```
┌─────────────────┐        ┌──────────────────┐        ┌─────────────────────┐
│   ESP32-S3      │        │  Python Backend  │        │   Web Browser       │
│   Camera Module │──WiFi─▶│  Flask + OpenCV  │──HTTP─▶│   Live Dashboard    │
│   MJPEG Stream  │        │  HSV Processing  │        │   /video_feed       │
└─────────────────┘        └──────────────────┘        └─────────────────────┘
```

**Data Flow:**
```
Capture → Preprocess → HSV Mask → Contour Filter → Annotate → Stream → Browser
```

---

##  Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Hardware** | ESP32-S3 (OV2640/OV5640) | Video capture & WiFi streaming |
| **Backend** | Python + Flask | Frame processing & HTTP server |
| **Computer Vision** | OpenCV (cv2) | HSV masking, contour detection |
| **Frontend** | HTML5 + CSS3 (Jinja2) | Live dashboard UI |
| **Communication** | HTTP MJPEG | Multipart JPEG stream over WiFi |

---

##  How It Works

1. **Capture** — ESP32-S3 streams continuous MJPEG video via its HTTP web server
2. **Preprocessing** — Frames are decoded and converted from `BGR → HSV` for lighting robustness
3. **Masking** — Predefined HSV thresholds generate binary masks for each target color
4. **Noise Reduction** — `GaussianBlur` + morphological opening (erode → dilate) removes false blobs
5. **Contour Detection** — Contours are extracted and filtered; only those with **area > 500 px** are retained
6. **Overlay Rendering** — Bounding boxes and color labels are drawn with OpenCV primitives
7. **Streaming Output** — Annotated frames are JPEG-encoded and served via Flask's `/video_feed`

---

##  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ESP32-Color-Detection-Dashboard.git
cd ESP32-Color-Detection-Dashboard
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the ESP32

- Upload the **Camera Web Server** firmware via Arduino IDE or ESP-IDF
- Connect ESP32-S3 to your **2.4 GHz WiFi** network
- Note the assigned **IP address**

Update the stream URL in `color_server.py`:

```python
ESP32_STREAM_URL = "http://192.168.x.x/stream"
```

### 4. Run the Application

```bash
python color_server.py
```

Open your browser: **http://localhost:5000**

---

##  Advanced Configuration (HSV Thresholding)

Lighting conditions vary, so HSV tuning is often required.

| Color | Lower HSV | Upper HSV |
|---|---|---|
| 🔴 Red | `[0, 120, 70]` | `[10, 255, 255]` |
| 🟢 Green | `[36, 100, 100]` | `[86, 255, 255]` |
| 🔵 Blue | `[94, 80, 2]` | `[126, 255, 255]` |
| 🟡 Yellow | `[25, 150, 150]` | `[35, 255, 255]` |
| ⚫ Black | `[0, 0, 0]` | `[180, 255, 30]` |
| ⚪ White | `[0, 0, 200]` | `[180, 30, 255]` |

> ** Tip:** Fluorescent vs. natural light can shift hue readings by 5–15°. Always tune in your actual deployment environment.

---

##  Hardware Requirements

| Component | Specification |
|---|---|
| **Microcontroller** | ESP32-S3 — Dual-core Xtensa LX7, 240 MHz, **8MB PSRAM** recommended |
| **Camera** | OV2640 or OV5640 |
| **Network** | 2.4 GHz IEEE 802.11 b/g/n WiFi |
| **Power Supply** | 5V DC, minimum **2A** stable supply |
| **Host Machine** | Python 3.8+ with OpenCV |

---

##  Project Structure

```
ESP32-Color-Detection-Dashboard/
│
├── color_server.py          # Flask app + OpenCV processing pipeline
├── requirements.txt         # Python dependencies
│
├── templates/
│   └── index.html           # Web dashboard (Jinja2 template)
│
└── static/
    ├── css/
    │   └── style.css        # Dashboard styling
    └── js/
        └── app.js           # Frontend logic
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| **Low FPS** | Weak WiFi / high resolution | Move ESP32 closer to router; reduce to QVGA or CIF |
| **No stream visible** | Wrong IP or network mismatch | Verify `ESP32_STREAM_URL`; ensure same subnet |
| **Colors not detected** | Lighting mismatch | Retune HSV values; avoid mixed/artificial lighting |
| **Stream disconnects** | Power instability | Use a rated 5V 2A supply; avoid underpowered USB ports |

---

## Performance Optimization

- **HSV color space** — more robust to lighting changes than BGR/RGB
- **Morphological filtering** — eliminates small noise blobs before contour detection
- **480p resolution** — optimal balance between detection accuracy and processing speed
- **Contour area threshold** — filters out sub-500px artifacts for cleaner output

---

## Future Roadmap

- [ ] Edge inference on ESP32 via ESP-DL for on-device classification
- [ ] PID-based pan-tilt servo system for object tracking
- [ ] WebSocket streaming for multi-client support
- [ ] CSV / database logging of detected colors and timestamps

---

## Author

<div align="center">

**Raunak Choudhary**  
*Robotics · Artificial Intelligence · Computer Vision*


4. Neeche **"Commit changes"** click karo

**Sirf ek kaam baaki hai** — `YOUR_USERNAME` ki jagah apna actual GitHub username daal do, 2 jagah aata hai!
