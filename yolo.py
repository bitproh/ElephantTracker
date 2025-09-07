import os
import random
import cv2
from ultralytics import YOLO
import geocoder
import requests
import datetime

# -----------------------------
# CONFIG
# -----------------------------
# Load your custom-trained model
model = YOLO("best.pt")

# Define class names (must match your training)
custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}

# Folder containing test images
image_folder = "C:\\Users\\abiaa\\Downloads\\final_year_project\\ElephantTracker\\components"

# Flask server IP (run server.py on another laptop, replace with that laptop’s IP)
SERVER_URL = "http://192.168.184.196:5000/api/events"  # <-- change IP to your server machine

# -----------------------------
# IMAGE SELECTION
# -----------------------------
images = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

if not images:
    print("No images found in 'components' folder.")
    exit()

# Randomly select one image
selected_image = random.choice(images)
image_path = os.path.join(image_folder, selected_image)
print(f"Selected image: {selected_image}")

# Load image and run inference
img = cv2.imread(image_path)
results = model(img)

# -----------------------------
# PARSE DETECTIONS
# -----------------------------
detected = False
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    class_name = custom_names.get(cls_id, f"class_{cls_id}")

    if conf >= 0.6:
        print(f"✅ Detected: {class_name} with {conf:.2f} confidence")
        detected = True

        # -----------------------------
        # GET LOCATION
        # -----------------------------
        if class_name == "lakshmikutty":
            # Example fixed coordinates (Kottayam region)
            lat, lon = 9.5100, 76.5514
        else:
            # Use current IP-based geolocation
            g = geocoder.ip('me')
            lat, lon = g.latlng if g.ok else (None, None)

        if lat is not None and lon is not None:
            print(f"📍 Location: Latitude {lat}, Longitude {lon}")

            # -----------------------------
            # SEND TO FLASK SERVER
            # -----------------------------
            data = {
                "elephant_id": class_name,
                "device_id": "cam1",   # Change if running on another laptop
                "timestamp": datetime.datetime.utcnow().isoformat(),
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
