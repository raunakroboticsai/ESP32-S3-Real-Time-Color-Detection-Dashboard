# ============================================================
#  Project   : ESP32-S3 Object Color Detection System
#  Author    : Raunak Choudhary
#  Company   : Botics
#  Version   : 1.0.0
#  Date      : March 2026
# ------------------------------------------------------------
#  License   : MIT License
#  Copyright (c) 2026 Raunak Choudhary / Botics
# ------------------------------------------------------------
#  GitHub    : github.com/Botics
# ============================================================

import cv2
import numpy as np
from flask import Flask, Response, jsonify
import threading
import time

# ===========================
# CHANGE THIS TO YOUR ESP32 IP
# ===========================
ESP32_STREAM_URL = "http://192.168.137.212/stream"

# ===========================
# Flask App
# ===========================
app = Flask(__name__)

current_frame    = None
frame_lock       = threading.Lock()
detected_colors  = []  # List of all detected colors in frame

# ===========================
# Color Ranges in HSV
# ===========================
COLOR_RANGES = {
    "RED": [
        (np.array([0, 120, 70]),   np.array([10, 255, 255])),
        (np.array([170, 120, 70]), np.array([180, 255, 255])),
    ],
    "GREEN":  [(np.array([35, 80, 50]),  np.array([85, 255, 255]))],
    "BLUE":   [(np.array([100, 80, 50]), np.array([130, 255, 255]))],
    "YELLOW": [(np.array([20, 100, 100]),np.array([35, 255, 255]))],
    "BLACK":  [(np.array([0, 0, 0]),     np.array([180, 255, 50]))],
    "WHITE":  [(np.array([0, 0, 200]),   np.array([180, 30, 255]))],
}

# Box colors for drawing (BGR)
BOX_COLORS = {
    "RED":    (0, 0, 255),
    "GREEN":  (0, 255, 0),
    "BLUE":   (255, 100, 0),
    "YELLOW": (0, 255, 255),
    "BLACK":  (80, 80, 80),
    "WHITE":  (220, 220, 220),
}

# ===========================
# Color Detection Function
# ===========================
def detect_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    results = []

    for color_name, ranges in COLOR_RANGES.items():
        # Create mask for this color
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lower, upper) in ranges:
            mask |= cv2.inRange(hsv, lower, upper)

        # Clean up mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:  # Minimum area filter
                x, y, w, h = cv2.boundingRect(cnt)
                results.append({
                    "color": color_name,
                    "x": x, "y": y,
                    "w": w, "h": h,
                    "area": int(area)
                })

    # Sort by area (largest first)
    results.sort(key=lambda r: r["area"], reverse=True)
    return results

# ===========================
# Draw detections on frame
# ===========================
def draw_detections(frame, detections):
    h, w = frame.shape[:2]

    for det in detections:
        color_name = det["color"]
        box_color  = BOX_COLORS.get(color_name, (255, 255, 255))
        x, y, bw, bh = det["x"], det["y"], det["w"], det["h"]

        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + bw, y + bh), box_color, 3)

        # Draw corner accents
        corner_len = 20
        thickness  = 4
        # Top-left
        cv2.line(frame, (x, y), (x + corner_len, y), box_color, thickness)
        cv2.line(frame, (x, y), (x, y + corner_len), box_color, thickness)
        # Top-right
        cv2.line(frame, (x+bw, y), (x+bw - corner_len, y), box_color, thickness)
        cv2.line(frame, (x+bw, y), (x+bw, y + corner_len), box_color, thickness)
        # Bottom-left
        cv2.line(frame, (x, y+bh), (x + corner_len, y+bh), box_color, thickness)
        cv2.line(frame, (x, y+bh), (x, y+bh - corner_len), box_color, thickness)
        # Bottom-right
        cv2.line(frame, (x+bw, y+bh), (x+bw - corner_len, y+bh), box_color, thickness)
        cv2.line(frame, (x+bw, y+bh), (x+bw, y+bh - corner_len), box_color, thickness)

        # Label background
        label      = color_name
        font_scale = 0.8
        thickness2 = 2
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness2)
        label_y = y - 10 if y - 10 > th else y + bh + th + 10
        cv2.rectangle(frame, (x, label_y - th - 6), (x + tw + 10, label_y + 4), (0, 0, 0), -1)
        cv2.rectangle(frame, (x, label_y - th - 6), (x + tw + 10, label_y + 4), box_color, 2)
        cv2.putText(frame, label, (x + 5, label_y),
                    cv2.FONT_HERSHEY_DUPLEX, font_scale, box_color, thickness2)

    # Top status bar
    cv2.rectangle(frame, (0, 0), (w, 50), (0, 0, 0), -1)
    if detections:
        names = list(dict.fromkeys([d["color"] for d in detections]))  # unique
        status = "DETECTED: " + " | ".join(names)
        cv2.putText(frame, status, (10, 34),
                    cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 245, 255), 2)
    else:
        cv2.putText(frame, "NO COLOR DETECTED", (10, 34),
                    cv2.FONT_HERSHEY_DUPLEX, 0.75, (100, 100, 100), 2)

    # Watermark
    cv2.putText(frame, "Botics | Color Detection", (w - 230, h - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (60, 60, 60), 1)

    return frame

# ===========================
# ESP32 Stream Thread
# ===========================
def read_esp32_stream():
    global current_frame, detected_colors

    while True:
        print(f"Connecting to ESP32: {ESP32_STREAM_URL}")
        cap = cv2.VideoCapture(ESP32_STREAM_URL)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not cap.isOpened():
            print("Cannot connect! Retrying in 3s...")
            time.sleep(3)
            continue

        print("ESP32 Connected!")

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Frame lost! Reconnecting...")
                break

            frame = cv2.flip(frame, 1)

            # Detect colors
            detections    = detect_colors(frame)
            detected_colors = detections

            # Draw on frame
            frame = draw_detections(frame, detections)

            # Save frame
            with frame_lock:
                _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                current_frame = jpeg.tobytes()

        cap.release()
        time.sleep(2)

# ===========================
# Flask Routes
# ===========================
def generate_frames():
    while True:
        with frame_lock:
            frame = current_frame
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/colors')
def colors():
    unique = []
    seen   = set()
    for d in detected_colors:
        if d["color"] not in seen:
            seen.add(d["color"])
            unique.append({
                "color": d["color"],
                "area":  d["area"]
            })
    return jsonify({"detected": unique, "count": len(unique)})

# ===========================
# Main
# ===========================
if __name__ == '__main__':
    t = threading.Thread(target=read_esp32_stream, daemon=True)
    t.start()

    print("\n" + "="*50)
    print("  COLOR DETECTION SERVER STARTED!")
    print("="*50)
    print(f"  ESP32 Stream : {ESP32_STREAM_URL}")
    print(f"  Web Page     : http://localhost:5000")
    print("="*50 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
