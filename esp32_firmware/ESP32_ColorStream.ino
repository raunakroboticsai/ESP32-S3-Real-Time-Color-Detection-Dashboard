/*
 * ============================================================
 *  Project   : ESP32-S3 Object Color Detection System
 *  File      : ESP32_Stream.ino
 *  Author    : Raunak Choudhary
 *  Company   : Botics
 *  Version   : 1.0.0
 *  Date      : March 2026
 * ------------------------------------------------------------
 *  Description:
 *    ESP32-S3-WROOM camera firmware.
 *    Streams live MJPEG video over WiFi.
 *    Used by Python color detection server.
 *
 *  Hardware:
 *    - ESP32-S3-WROOM Module
 *    - OV3660 Camera Sensor
 *
 *  Arduino IDE Settings:
 *    Board         → ESP32S3 Dev Module
 *    PSRAM         → OPI PSRAM
 *    Partition     → Huge APP (3MB No OTA/1MB SPIFFS)
 *    Flash Size    → 8MB
 *    Upload Speed  → 921600
 *
 *  License   : MIT License
 *  Copyright (c) 2026 Raunak Choudhary / Botics
 * ------------------------------------------------------------
 *  GitHub    : github.com/Botics
 * ============================================================
 */

#include "esp_camera.h"

// ===========================
// Camera Model
// ===========================
#define CAMERA_MODEL_ESP32S3_EYE  // ← PEHLE DEFINE

#include "camera_pins.h"          // ← BAAD MEIN INCLUDE
#include <WiFi.h>
#include <WebServer.h>
// ===========================
// WiFi Credentials
// ===========================
const char* ssid     = "Botics";
const char* password = "12345678";

WebServer server(80);

// ===========================
// MJPEG Stream
// ===========================
#define PART_BOUNDARY "123456789000000000000987654321"

void handleStream() {
  WiFiClient client = server.client();
  client.println("HTTP/1.1 200 OK");
  client.print("Content-Type: multipart/x-mixed-replace;boundary=");
  client.println(PART_BOUNDARY);
  client.println("Access-Control-Allow-Origin: *");
  client.println();

  while (client.connected()) {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
      delay(100);
      continue;
    }

    uint8_t *jpg_buf  = NULL;
    size_t   jpg_len  = 0;
    bool     converted = false;

    if (fb->format == PIXFORMAT_JPEG) {
      jpg_buf = fb->buf;
      jpg_len = fb->len;
    } else {
      converted = frame2jpg(fb, 80, &jpg_buf, &jpg_len);
      esp_camera_fb_return(fb);
      fb = NULL;
      if (!converted) continue;
    }

    // Send MJPEG frame
    client.print("\r\n--");
    client.println(PART_BOUNDARY);
    client.println("Content-Type: image/jpeg");
    client.print("Content-Length: ");
    client.println(jpg_len);
    client.println();
    client.write(jpg_buf, jpg_len);

    if (converted) free(jpg_buf);
    if (fb) esp_camera_fb_return(fb);

    delay(30); // ~30fps
  }
}

void handleRoot() {
  String html = "<html><body style='background:#0a0a0f;color:#00f5ff;font-family:monospace;text-align:center;padding:40px'>";
  html += "<h2>ESP32-S3 Stream Server</h2>";
  html += "<p>Botics | Color Detection Project</p>";
  html += "<p>Stream: <a style='color:#22c55e' href='/stream'>/stream</a></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

// ===========================
// Setup
// ===========================
void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("=== Botics | Color Detection ===");

  // Camera Config
  camera_config_t config;
  config.ledc_channel  = LEDC_CHANNEL_0;
  config.ledc_timer    = LEDC_TIMER_0;
  config.pin_d0        = Y2_GPIO_NUM;
  config.pin_d1        = Y3_GPIO_NUM;
  config.pin_d2        = Y4_GPIO_NUM;
  config.pin_d3        = Y5_GPIO_NUM;
  config.pin_d4        = Y6_GPIO_NUM;
  config.pin_d5        = Y7_GPIO_NUM;
  config.pin_d6        = Y8_GPIO_NUM;
  config.pin_d7        = Y9_GPIO_NUM;
  config.pin_xclk      = XCLK_GPIO_NUM;
  config.pin_pclk      = PCLK_GPIO_NUM;
  config.pin_vsync     = VSYNC_GPIO_NUM;
  config.pin_href      = HREF_GPIO_NUM;
  config.pin_sccb_sda  = SIOD_GPIO_NUM;
  config.pin_sccb_scl  = SIOC_GPIO_NUM;
  config.pin_pwdn      = PWDN_GPIO_NUM;
  config.pin_reset     = RESET_GPIO_NUM;
  config.xclk_freq_hz  = 20000000;
  config.frame_size    = FRAMESIZE_QVGA;
  config.pixel_format  = PIXFORMAT_JPEG;
  config.grab_mode     = CAMERA_GRAB_LATEST;
  config.fb_location   = CAMERA_FB_IN_DRAM;
  config.jpeg_quality  = 10;
  config.fb_count      = 1;

  // Init Camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x\n", err);
    return;
  }
  Serial.println("Camera init SUCCESS!");

  // Sensor Settings for OV3660
  sensor_t *s = esp_camera_sensor_get();
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1);
    s->set_brightness(s, 1);
    s->set_saturation(s, 0);   // Normal saturation for color detection
    s->set_contrast(s, 1);     // Slight contrast boost
  }

  // WiFi Connect
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.println("================================");
  Serial.print("Stream URL: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/stream");
  Serial.println("================================");

  // Routes
  server.on("/",       handleRoot);
  server.on("/stream", handleStream);
  server.begin();
  Serial.println("Stream Server Started!");
}

// ===========================
// Loop
// ===========================
void loop() {
  server.handleClient();
}
