import cv2
from ultralytics import YOLO
import time
import requests
from datetime import datetime, timezone, timedelta
import RPi.GPIO as GPIO

# ================== GPIO SETUP ==================
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
SERVO_PIN = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# ================== YOLO MODEL ==================
model = YOLO("best.pt")

custom_names = {
    0: "lakshmikutty",
    1: "narayanankutty"
}

ALLOWED_CLASS_IDS = {0, 1}
CONF_THRESHOLD = 0.80
SERVER_INTERVAL = 10

SERVER_URL = "http://10.10.159.95:5000/api/events"
DEVICE_ID = "cam_1"

LATITUDE = 9.753
LONGITUDE = 76.65

# ================== RADAR SETTINGS ==================
SCAN_MIN = 40
SCAN_MAX = 140
SCAN_STEP = 5
DIST_THRESHOLD = 300   # cm
current_angle = SCAN_MIN
direction = 1

# ================== FUNCTIONS ==================

def set_servo_angle(angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo.ChangeDutyCycle(0)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = duration * 17150
    return round(distance, 2)

def sweep_and_detect():
    global current_angle, direction

    set_servo_angle(current_angle)
    distance = get_distance()

    print(f"Angle {current_angle}°  Distance: {distance} cm")

    if distance < DIST_THRESHOLD:
        print("🎯 TARGET LOCKED at angle:", current_angle)
        return True

    current_angle += direction * SCAN_STEP

    if current_angle >= SCAN_MAX or current_angle <= SCAN_MIN:
        direction *= -1

    return False

# ================== CAMERA + YOLO ==================

def run_detection():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not available")
        return

    start_time = time.time()
    MAX_CAMERA_RUNTIME = 20
    last_server_time = 0

    print("🐘 Detection started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        results = model(frame, imgsz=640, conf=CONF_THRESHOLD, iou=0.45, verbose=False)
        r = results[0]

        detected_now = None
        conf = 0.0

        if r.boxes is not None and len(r.boxes) > 0:
            confs = r.boxes.conf.cpu().numpy()
            clss = r.boxes.cls.cpu().numpy().astype(int)

            best_idx = confs.argmax()
            cls_id = clss[best_idx]
            conf = float(confs[best_idx])

            if cls_id in ALLOWED_CLASS_IDS:
                detected_now = custom_names[cls_id]

        annotated_frame = r.plot()
        cv2.imshow("Elephant Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        now = time.time()

        if detected_now and (now - last_server_time > SERVER_INTERVAL):
            payload = {
                "elephant_id": detected_now,
                "device_id": DEVICE_ID,
                "timestamp": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(),
                "lat": LATITUDE,
                "lon": LONGITUDE,
                "confidence": conf
            }

            try:
                res = requests.post(SERVER_URL, json=payload, timeout=2)
                if res.status_code == 201:
                    print("📡 Event sent to server")
                    last_server_time = now
            except Exception as e:
                print("⚠️ Server error:", e)

        # Stop camera after 20 sec
        if time.time() - start_time > MAX_CAMERA_RUNTIME:
            print("⏱ Camera session ended")
            break

    cap.release()
    cv2.destroyAllWindows()

# ================== MAIN LOOP ==================

print("\n🛰️ Elephant Watch Tower ACTIVE\n")

try:
    while True:

        # RADAR SWEEP MODE
        motion_found = sweep_and_detect()
        time.sleep(0.2)

        if not motion_found:
            continue

        # CAMERA MODE
        print("\n📷 Camera ON for 20 seconds\n")
        run_detection()

        print("\n🔄 Returning to radar scan...\n")
        time.sleep(2)

except KeyboardInterrupt:
    print("System stopped")
    GPIO.cleanup()
