import cv2
import mediapipe as mp
import numpy as np
from picamera2 import Picamera2

# MediaPipe 솔루션 초기화
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

size_true = 0
flag_size = True
size_value = [0, 0, 0, 0]

def setFlagSize():
    global flag_size
    flag_size = False

def setFlagSize_True():
    global flag_size
    flag_size = True
    
def getSizeTrue():
    global size_true
    return size_true

def getSizeValue():
    global size_value
    return size_value

def size():
    global mp_drawing
    global mp_pose
    global flag_size
    global size_true

    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1920, 1080)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.start()

    # MediaPipe Pose 객체 생성
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:

        while flag_size:
            # 이미지 캡처
            im = picam2.capture_array()

            # 이미지 크기 출력 (디버깅 용도)
            if im is None or im.size == 0:
                print("Captured image is empty.")
                continue

            # print(f"Captured image shape: {im.shape}")

            # BGR 이미지를 RGB 이미지로 변환
            image = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
            image.flags.writeable = False

            # Pose 추론 수행
            results = pose.process(image)

            # 다시 BGR 이미지로 변환
            image.flags.writeable = True

            # Pose 랜드마크가 있다면
            if results.pose_landmarks:
                # 랜드마크를 이미지에 그리기
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # 랜드마크 좌표 추출
                landmarks = results.pose_landmarks.landmark
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
                left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                left_heel = landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value]
                right_heel = landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value]

                # 좌표를 픽셀 값으로 변환
                h, w, _ = image.shape
                right_shoulder_coords = np.array([right_shoulder.x * w, right_shoulder.y * h])
                left_shoulder_coords = np.array([left_shoulder.x * w, left_shoulder.y * h])
                left_elbow_coords = np.array([left_elbow.x * w, left_elbow.y * h])
                left_wrist_coords = np.array([left_wrist.x * w, left_wrist.y * h])
                left_hip_coords = np.array([left_hip.x * w, left_hip.y * h])
                right_hip_coords = np.array([right_hip.x * w, right_hip.y * h])
                left_knee_coords = np.array([left_knee.x * w, left_knee.y * h])
                right_knee_coords = np.array([right_knee.x * w, right_knee.y * h])
                left_ankle_coords = np.array([left_ankle.x * w, left_ankle.y * h])
                right_ankle_coords = np.array([right_ankle.x * w, right_ankle.y * h])
                left_heel_coords = np.array([left_heel.x * w, left_heel.y * h])
                right_heel_coords = np.array([right_heel.x * w, right_heel.y * h])

                # 길이 계산
                shoulder_length = np.linalg.norm(right_shoulder_coords - left_shoulder_coords)
                
                leg_left_upper_length = np.linalg.norm(left_hip_coords - left_knee_coords)
                leg_right_upper_length = np.linalg.norm(right_hip_coords - right_knee_coords)
                
                leg_left_lower_short_length = np.linalg.norm(left_knee_coords - left_ankle_coords)
                leg_right_lower_short_length = np.linalg.norm(right_knee_coords - right_ankle_coords)

                leg_left_lower_wide_length = np.linalg.norm(left_knee_coords - left_heel_coords)
                leg_right_lower_wide_length = np.linalg.norm(right_knee_coords - right_heel_coords)

                left_leg_short_coords = leg_left_upper_length + leg_left_lower_short_length
                right_leg_short_coords = leg_right_upper_length + leg_right_lower_short_length

                left_leg_wide_coords = leg_left_upper_length + leg_left_lower_wide_length
                right_leg_wide_coords = leg_right_upper_length + leg_right_lower_wide_length

                leg_short_length = (left_leg_short_coords + right_leg_short_coords) / 2
                leg_wide_length = (left_leg_wide_coords + right_leg_wide_coords) / 2
                
                waist_length = np.linalg.norm(right_hip_coords - left_hip_coords)

                upper_arm_length = np.linalg.norm(left_shoulder_coords - left_elbow_coords)
                lower_arm_length = np.linalg.norm(left_elbow_coords - left_wrist_coords)
                arm_length = upper_arm_length + lower_arm_length

                size_value[0] = shoulder_length / 4.5
                size_value[1] = arm_length / 5
                size_value[2] = ((waist_length*1.3) / 4)*2.2
                size_value[3] = leg_short_length / 5

                if size_value[0]>60 or size_value[0]<20:
                    size_value[0] = None
                if size_value[1]>70 or size_value[1]<30:
                    size_value[1] = None
                if size_value[2]>100 or size_value[2]<60:
                    size_value[2] = None
                if size_value[3]>110 or size_value[3]<60:
                    size_value[3] = None

                # print('0', size_value[0])
                # print('1', size_value[1])
                # print('2', size_value[2])
                # print('3', size_value[3])

                if None not in size_value:
                    size_true = 1

                if getSizeTrue()==1:
                    setFlagSize()
                    return getSizeValue()

            # 이미지 표시
            # cv2.imshow("size", image)

            # 'q' 키를 누르면 종료
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

    # 캡처 객체 및 윈도우 해제
        picam2.stop()
        picam2.close()
        cv2.destroyAllWindows()
