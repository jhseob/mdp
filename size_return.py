import body_detect as body      #ok - body_detect
import threading as th
import cv2
import time
import bluetooth_code as blue

fffFlag = True

def setBu(bu):
    global buzer
    buzer = bu
def setMotor(m1,m2,m3):
    global motor1, motor2,motor3
    motor1 = m1
    motor2 = m2
    motor3 = m3

cnt = 30000

body_flag=True
face_flag=False
dis_flag=False
size_flag=False
size_all_flag=True

body_stop = 0
face_stop = 1
dis_stop = 1
size_stop = 1

dis_value = 0
size_value_return =0
size_value = []

mode=1

def getBodyFlag():
    global body_flag
    return body_flag

def setSizeFlag_False():
    global body_flag
    global face_flag
    global size_flag
    global size_all_flag

    global body_stop
    global face_stop
    global size_stop
    global dis_flag
    global dis_stop
    global size_all_flag

    body_stop = 1
    face_stop = 1
    dis_stop = 1
    size_stop = 1

    body_flag=False
    face_flag=False
    dis_flag=False
    size_flag=False

    size_all_flag=False

    body.setFlagBody_False()
    dis.setFlagDis()
    face.setFlagFace()
    size.setFlagSize()

def setSizeFlag_True():
    global body_flag
    global face_flag
    global size_flag
    global size_all_flag
    global body_stop
    global face_stop
    global size_stop
    global mode
    global dis_flag
    global dis_stop
    global size_value_return
    global cnt
    
    cnt = 0

    size_value_return = 0

    body_stop = 0
    face_stop = 1
    dis_stop = 1
    size_stop = 1
    mode=1

    body_flag=True
    face_flag=False
    dis_flag=False
    size_flag=False

    size_all_flag=True

def getSizeValue():
    global size_value
    return size_value

def getSizeValueReturn():
    global size_value_return
    return size_value_return

# face_detect_code_start
def face_func1():
    face.face()

# face_detect_true/false
def face_func2():
    global face_flag
    global face_stop
    global mode

    while face_flag:
        # print(face.getFaceTrue())
        if face.getFaceTrue()==1:
            motor1.off()
            motor2.off()
            motor3.off()
            face_stop=1
            face.setFlagFace()
        else:
            mode=3

# size_detect_code_start
def size_func1():
    size.size()

# size_detect_value
def size_func2():
    global size_value
    global size_flag
    global size_stop
    global mode

    while size_flag:
        if size.getSizeTrue()==1:
            size_value = size.getSizeValue()
            size_stop=1
            size.setFlagSize()
        else:
            mode=4


def size_return():
    global body_flag
    global face_flag
    global dis_flag
    global size_flag
    global size_all_flag
    global body_stop
    global mode
    global dis
    # global body_start

    # body_th = th.Thread(target=body_func1)
    # body_th.start()
    if body_flag:
        body.motor_output(motor1,motor2,motor3)
        body.body()
        mode = 1
        body_stop = 1
        time.sleep(0.2)

    import ROS as dis
    
    dis.setFlagDis_True()

    dis_flag=True
    while dis_flag:
        dis.dis()

        outputs = dis.kernel.tensor_engine.tensor_output

        if outputs!=None:
            # print(outputs)
            # outputs = outputs[1]
            # (boxes, classes, scores, distances)
            # for output in outputs:
            boxes, classes, scores, distance = outputs
            for i in range(len(classes)):
                dis_value = distance[i]
                break

            if dis_value!=None and dis_value>=0:

                dis_value = float(dis_value)

                print(dis_value)

                if dis_value>=200 and dis_value<=204:
                    motor1.off()
                    motor2.off()
                    motor3.off()
                    dis.setFlagDis()
                    dis.closeCamera()
                    time.sleep(0.2)
                    dis_stop=1 
                    dis_flag=False
                    # dis.setKernel()
                else:
                    if dis_value>200:
                        # print('front')
                        #straight
                        motor1.on()
                        motor2.off()
                        motor3.off()
                    elif dis_value<204:
                        # print('back')
                        #back
                        motor1.off()
                        motor2.off()
                        motor3.on()
                    mode=2

            else:
                continue

    def body_detect_mode():
        global mode
        global body_flag
        global dis_flag
        global dis_stop
        # global dis_th
        global dis

        if body_stop==1:
            motor1.off()
            motor2.off()
            motor3.off()
            #motor_stop

            #body_detect_stop
            body_flag=False
            # body_start.join()

            # if cv2.getWindowProperty("ROS",cv2.WND_PROP_VISIBLE)>=0:
            #     cv2.destroyWindow("ROS")
            # picam2 = Picamera2
            # picam2.stop()
            # picam2.close()

            #face_detect_start
            dis_stop=0

            #dis_detect_mode_on
            mode=2
        else:
            #motor right
            motor1.off()
            motor2.on()
            motor3.off()

    def distance_mode():
        global mode
        global dis_flag
        global face_flag
        global face_stop
        global face_th
        global face_start
        global face

        # dis_th = th.Thread(target=dis_func1)
        # dis_th.start()

        if dis_stop==1:
            #motor_stop
            motor1.off()
            motor2.off()
            motor3.off()

            #distance_stop
            # dis_th.join()
            #face_detect_start
            face_stop=0
            face_flag=True
        
            print('face 시작')

            import face_detect as face
            print('face import')

            face_th = th.Thread(target=face_func1)
            face_th.start()
            face_start = th.Thread(target=face_func2)
            face_start.start()

            #face_detect_mode_on
            mode=3

    def face_detect_mode():
        global mode
        global face_flag
        global size_flag
        global size_stop
        global size_th
        global size_start
        global size
        global cnt
        global fffFlag

        if face_stop==1:
            #motor_stop
            buzer.off()
            motor1.off()
            motor2.off()
            motor3.off()

            #face_detect_stop
            face_flag=False
            face_th.join()
            face_start.join()

            #distance_start
            size_stop=0
            size_flag=True

            import size

            size.setFlagSize_True()

            size_th = th.Thread(target=size_func1)
            size_th.start()
            size_start = th.Thread(target=size_func2)
            size_start.start()

            mode=4
        else:
            motor1.off()
            motor2.off()
            motor3.off()
            buzer.on()
            if fffFlag==True:
                blue.setWrite("몸의 정면을 부저 소리가 울리는 곳으로 위치해주세요")
                fffFlag=False


    def size_detect_mode():
        global size_flag
        global mode
        global size_value_return
        global size_all_flag

        if size_stop==1:
            #size_detect_stop
            motor1.off()
            motor2.off()
            motor3.off()
            size_flag=False
            size_th.join()
            size_start.join()

            size_value_return = 1

            size_all_flag = False
            

    try:
        # cv2.destroyAllWindows()
        while size_all_flag:
            if mode==1:
                body_detect_mode()
            elif mode==2:
                distance_mode()
            elif mode==3:
                face_detect_mode()
            elif mode==4:
                size_detect_mode()
                
        motor1.off()
        motor2.off()
        motor3.off()
            
        
    except KeyboardInterrupt:
        pass

    body_flag=False
    face_flag=False
    dis_flag=False
    size_flag=False
    size_all_flag=False

    if body_stop==0:
        # body_th.join()
        pass
        # body_start.join()
    elif face_stop==0:
        # dis_th.join()
        face_th.join()
        face_start.join()
    elif dis_stop==0:
        # body_start.join()
        # dis_th.join()
        pass
    elif size_stop==0:
        face_th.join()
        face_start.join()
        size_th.join()
        size_start.join()

    cv2.destroyAllWindows()