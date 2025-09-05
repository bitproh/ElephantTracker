import cv2
from ultralytics import YOLO
import subprocess
import time
import webbrowser  # Import the webbrowser module
import geocoder

model = YOLO('best.pt')


custom_names = {0: 'lakshmikutty', 1: 'narayanankutty'}


cap = cv2.VideoCapture(0)

detection_start_time = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    
    results = model(frame)

    # Display the results
    for result in results:
        
        for box, cls_id in zip(result.boxes.xyxy, result.boxes.cls):
            
            box = box.int().tolist()
            
            label = custom_names[int(cls_id)]
           
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            #  label
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            if label == 'narayanankutty':
                if detection_start_time is None:
                    detection_start_time = time.time()
                else:
                    elapsed_time = time.time() - detection_start_time
                    if elapsed_time >= 2:
                        cap.release()  # Release the webcam
                        cv2.destroyAllWindows()  
                        webbrowser.open('http://127.0.0.1:5500/website/narayanankutty.html')
                        location = geocoder.ip('me')
                        print(f"Location detected - Latitude: {location.latlng[0]}, Longitude: {location.latlng[1]}")
  
                        break
                    elif elapsed_time>=2:
                        cap.release()
                        cv2.destroyAllWindows()
                        webbrowser.open('http://127.0.0.1:5500/website/lakshmikutty.html')
                        break
            else:
                detection_start_time = None

    # Show the frame
    cv2.imshow('Live Detection', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
