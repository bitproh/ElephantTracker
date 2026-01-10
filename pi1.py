import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("last.pt")

# Class mapping
custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}

# Open camera
cap = cv2.VideoCapture(0)  # 0 = USB webcam, use 1/2 if multiple cameras

if not cap.isOpened():
    print("Error: Camera not accessible")
    exit()

print("Camera started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Run YOLO inference
    results = model(frame, conf=0.5, verbose=False)

    detected_classes = set()

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        class_name = custom_names.get(cls_id, f"class_{cls_id}")

        if class_name in custom_names.values():
            detected_classes.add(class_name)

            # Get bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Label
            label = f"{class_name} ({conf:.2f})"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Print detection status
    if detected_classes:
        for cls in detected_classes:
            print(f"Detected: {cls}")
    else:
        print("No target detected")

    # Show video
    cv2.imshow("Elephant Detection Feed", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
