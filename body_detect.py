import cv2
import numpy as np
from picamera2 import Picamera2

def motor_output(value1,value2,value3):
    global motor1
    global motor2
    global motor3
    
    motor1 = value1
    motor2 = value2
    motor3 = value3

body_true = 0
body_center = 0
flag_body = True

picam2 = Picamera2()
picam2.preview_configuration.main.size=(1920,1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

# MobileNetSSD 모델 로드
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

# 클래스 이름 설정 (MobileNetSSD가 인식할 수 있는 클래스들)
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

def setFlagBody_False():
    global flag_body
    flag_body = False

def getFlagBody():
    global flag_body
    return flag_body

def setFlagBody_True():
    global flag_body
    flag_body = True

def getBodyTrue():
    global body_true
    return body_true

def getBodyCenter():
    global body_center
    return body_center


def body():
    global net
    global CLASSES
    global body_true
    global body_center
    global flag_body

    while flag_body:

        im = picam2.capture_array()

        # 이미지 크기 가져오기
        (h, w) = im.shape[:2]

        # blob 생성
        blob = cv2.dnn.blobFromImage(cv2.resize(im, (300, 300)), 0.007843, (300, 300), 127.5)

        # blob을 네트워크에 설정
        net.setInput(blob)

        # 객체 탐지 수행
        detections = net.forward()

        # 탐지된 객체들에 대해 루프 수행
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # 신뢰도 임계값 설정
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] != "person":
                    continue
                
                body_true = 1
                # 객체의 (x, y) 좌표 계산
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                w_value = endX-startX
                w_step = int(1920/w_value)
                if w_step%2==0 and w_step!=0:
                    w_distance = w_value/2+startX
                    if (1920/w_step*(w_step/2)-10)<=w_distance and (1920/w_step*(w_step/2)+5)>=w_distance:
                        body_center = 1
                    else:
                        if (1920/w_step*(w_step/2)-10)>w_distance:
                            body_center=3 #left
                        else:
                            body_center = 2 #right
                elif w_step!=0:
                    w_distance = startX
                    if (1920/w_step*(w_step/2)-10)<=w_distance and (1920/w_step*(w_step/2)+5)>=w_distance:
                        body_center = 1
                    else:
                        if (1920/w_step*(w_step/2)-10)>w_distance:
                            body_center=3 #left
                        else:
                            body_center = 2 #right

        if getBodyTrue() == 1 and getBodyCenter() == 1:
            motor1.off()
            motor2.off()
            motor3.off()
            setFlagBody_False()

        else:
            if getBodyTrue() == 0:
                # 인식이 안 됨. 무작정 돌기
                motor1.off()
                motor2.on()
                motor3.off()
            elif getBodyTrue() == 1 and getBodyCenter() == 2:
                # 몸 인식 완료 , 왼쪽으로 돌기
                motor1.off()
                motor2.on()
                motor3.off()
            elif getBodyTrue() == 1 and getBodyCenter() == 3:
                # 몸 인식 완료, 오른쪽으로 돌기
                motor1.on()
                motor2.on()
                motor3.off()

        # 결과 프레임 출력
        cv2.imshow("Frame", im)

        # 'q' 키를 눌러 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 캡처 객체 및 모든 창 닫기
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()