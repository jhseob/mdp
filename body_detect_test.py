import cv2
import numpy as np
import time
from picamera2 import Picamera2

# Load Haar Cascade for person detection
cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
body_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize global variables
flag = True
center = 0
body_true = 0
elapsed_time=0

def getFlagBody():
    global flag
    return flag

def setFlagBody_False():
    global flag
    flag = False

def getBodyTrue():
    global body_true
    return body_true

def getBodyCenter():
    global center
    return center

# Define the center of the frame
def get_frame_center(frame):
    height, width = frame.shape[:2]
    return (width // 2, height // 2)

# Determine if the body is in the center, left or right
def determine_position(frame, body_coords):
    frame_center_x, _ = get_frame_center(frame)
    x, w = body_coords[0], body_coords[2]
    body_center_x = x + w // 2

    if body_center_x < frame_center_x - (frame_center_x // 3):
        return 2  # Left
    elif body_center_x > frame_center_x + (frame_center_x // 3):
        return 3  # Right
    return 1  # Center

def body():
    global flag, center, body_true, elapsed_time
    fps = 30
    interval = 1 / fps
    last_time = time.time()

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (800, 600)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.start()

    while flag:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian Blur

        bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(50, 50))

        # Reset body_true for each frame
        body_true = 0
        
        for (x, y, w, h) in bodies:
            # Filter based on aspect ratio (height-to-width ratio)
            aspect_ratio = h / float(w)
            if 1.2 < aspect_ratio < 2.0:  # Adjust these values based on expected body shape
                body_true = 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                center = determine_position(frame, (x, y, w, h))

        cv2.imshow('Picamera2', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if getBodyTrue() == 1 and getBodyCenter() == 1:
            setFlagBody_False()
        else:
            if getBodyTrue() == 0:
                # 인식이 안 됨. 무작정 돌기
                motor_mode = 2
            elif getBodyTrue() == 1 and getBodyCenter() == 2:
                # 몸 인식 완료 , 왼쪽으로 돌기
                motor_mode = 2
            elif getBodyTrue() == 1 and getBodyCenter() == 3:
                # 몸 인식 완료, 오른쪽으로 돌기
                motor_mode = 3

        # Maintain desired fps
        elapsed_time = time.time() - last_time
        if elapsed_time < interval:
            time.sleep(interval - elapsed_time)
        last_time = time.time()

    # Cleanup
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()
