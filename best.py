import sys
import cv2
from ultralytics import YOLO

# Load your custom-trained model
model = YOLO("last.pt")

# Manually define class names
custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}

# Get image path from command-line argument
if len(sys.argv) < 2:
    print("Usage: python best.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
img = cv2.imread(image_path)

# Run inference
results = model(img)

# Check for custom classes
detected_classes = set()
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    class_name = custom_names.get(cls_id, f"class_{cls_id}")
    if class_name in custom_names.values():
        detected_classes.add(class_name)

# Show results in terminal
if detected_classes:
    for cls in detected_classes:
        print(f"Detected: {cls}")
else:
    print("No target class detected in the image.")