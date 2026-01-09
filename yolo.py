import os
import random
import cv2
from ultralytics import YOLO
import requests
import datetime
import pytz  # For Indian timezone

# -----------------------------
# CONFIG
# -----------------------------
model = YOLO("best.pt")
custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}
image_folder = "D:\\NKB\\Projects\\EDSS\\Main\\ElephantTracker-1\\components"
SERVER_URL = "http://10.12.236.105:5000/api/events"

# -----------------------------
# IMAGE SELECTION
# -----------------------------
images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if not images:
    print("No images found in 'components' folder.")
    exit()

selected_image = random.choice(images)
image_path = os.path.join(image_folder, selected_image)
print(f"Selected image: {selected_image}")

img = cv2.imread(image_path)
results = model(img)

# -----------------------------
# PARSE DETECTIONS
# -----------------------------
detected = False
india_tz = pytz.timezone("Asia/Kolkata")  # IST timezone

for box in results[0].boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    class_name = custom_names.get(cls_id, f"class_{cls_id}")

    if conf >= 0.6:
        print(f"✅ Detected: {class_name} with {conf:.2f} confidence")
        detected = True

        # Fixed coordinates
        if class_name == "lakshmikutty":
            lat, lon = 8.8932, 76.6141
        elif class_name == "narayanankutty":
            lat, lon = 8.8932, 76.6141


        else:
            lat, lon = None, None

        if lat is not None and lon is not None:
            # IST timestamp (12-hour format for printing if needed)
            now_ist = datetime.datetime.now(india_tz)
            timestamp_iso = now_ist.strftime("%Y-%m-%dT%H:%M:%S%z")  # ISO format with IST offset
            
            print(f"🐘 Elephant ID: {class_name}")
            print(f"📍 Location: Latitude {lat}, Longitude {lon}")
            print(f"🕒 Detection Time (IST): {timestamp_iso}")

            # -----------------------------
            # SEND TO FLASK SERVER
            # -----------------------------
            data = {
                "elephant_id": class_name,
                "device_id": "cam1",
                "timestamp": timestamp_iso,  # This will be IST
                "lat": lat,
                "lon": lon
            }

            try:
                response = requests.post(SERVER_URL, json=data)
                print("🌍 Sent to server:", response.json())
            except Exception as e:
                print("❌ Error sending to server:", e)
        else:
            print("⚠️ Could not determine location.")

if not detected:
    print("🚫 No elephant detected.")
