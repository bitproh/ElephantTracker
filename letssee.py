import os
import random
import cv2
from ultralytics import YOLO
import geocoder
import webbrowser
import requests
import datetime

# Load your custom-trained model
model = YOLO("best.pt")

# Manually define class names
custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}

# Folder containing images
image_folder = "components"
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

# Parse detections
detected = False
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    conf = float(box.conf[0])
    class_name = custom_names.get(cls_id, f"class_{cls_id}")

    if conf >= 0.6:
        print(f"✅ Detected: {class_name} with {conf:.2f} confidence")
        detected = True
        if class_name == "lakshmikutty":
            # Get location using geocoder
            g = geocoder.ip('me')
            lat, lon = 9.5100, 76.5514

            if lat is not None and lon is not None:
                print(f"Location: Latitude {lat}, Longitude {lon}")

                # Use Open-Meteo API to get weather data
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={9.5100}&longitude={76.5514}&current_weather=true"
                response = requests.get(weather_url)
                if response.status_code == 200:
                    weather_data = response.json()
                    current_weather = weather_data.get("current_weather", {})
                    temperature = current_weather.get("temperature")
                    windspeed = current_weather.get("windspeed")
                    weather_time = current_weather.get("time")

                    print(f"Current Weather at ({lat}, {lon}):")
                    print(f"  Temperature: {temperature}°C")
                    print(f"  Wind Speed: {windspeed} km/h")
                    print(f"  Time: {weather_time}")

                    # Open Google Maps in browser
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={9.5100},{76.5514}"
                    webbrowser.open(maps_url)
                
                else:
                    print("Failed to retrieve weather data.")
        elif class_name == "narayanankutty":
            g = geocoder.ip('me')
            lat, lon = g.latlng if g.ok else (None, None)    

            if lat is not None and lon is not None:
                print(f"Location: Latitude {lat}, Longitude {lon}")

                # Use Open-Meteo API to get weather data
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={9.5100}&longitude={76.5514}&current_weather=true"
                response = requests.get(weather_url)
                if response.status_code == 200:
                    weather_data = response.json()
                    current_weather = weather_data.get("current_weather", {})
                    temperature = current_weather.get("temperature")
                    windspeed = current_weather.get("windspeed")
                    weather_time = current_weather.get("time")

                    print(f"Current Weather at ({lat}, {lon}):")
                    print(f"  Temperature: {temperature}°C")
                    print(f"  Wind Speed: {windspeed} km/h")
                    print(f"  Time: {weather_time}")

                    # Open Google Maps in browser
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={9.5100},{76.5514}"
                    webbrowser.open(maps_url)
                
                else:
                    print("Failed to retrieve weather data.")

            else:
                print("Could not determine location.")

if not detected:
    print("No elephant detected.")