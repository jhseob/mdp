import cv2
import cv2.data
from picamera2 import Picamera2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
face_true = 0
flag_face = True

def setFlagFace():
    global flag_face
    flag_face = False
    
def setFlagFace_True():
    global flag_face
    flag_face = True
    
def getFaceTrue():
    global face_true
    return face_true


def face():
    global flag_face
    global face_cascade
    global face_true

    picam2 = Picamera2()
    picam2.preview_configuration.main.size=(1920,1080)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.start_preview()
    picam2.start()

    while flag_face:

        im = picam2.capture_array()
        gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=6)

        for (x,y,w,h) in faces:
            face_true=1

        if getFaceTrue()==1:
            setFlagFace()

        # cv2.imshow("Frame", im)
            
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()

