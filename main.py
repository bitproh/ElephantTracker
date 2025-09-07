import cv2
import os
from datetime import datetime
from ultralytics import YOLO
import subprocess

# Load COCO-trained YOLOv8 model
model = YOLO('yolov8n.pt')  # Replace with your actual model path

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Failed to access webcam")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    results = model(frame)

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name.lower() == "elephant":
            # Save image
            folder_path = os.path.join("static", "images", "elephant")
            os.makedirs(folder_path, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"elephant_{timestamp}.jpg"
            filepath = os.path.join(folder_path, filename)
            cv2.imwrite(filepath, frame)

            print(f"Elephant detected — saved to {filepath}")

            # Release camera and close OpenCV window
            cap.release()
            cv2.destroyAllWindows()

            # Call best.py and pass image path
            subprocess.run(["python", "best.py", filepath])
            exit()

    cv2.imshow("Elephant Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()