import body_detect as body      #ok - body_detect
import threading as th
import cv2
import time

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

motor_mode=0
buzzer_mode=0
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
    global motor_mode
    global size_all_flag

    motor_mode =0
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
    global motor_mode
    global buzzer_mode
    global body_stop
    global face_stop
    global size_stop
    global mode
    global dis_flag
    global dis_stop
    global size_value_return

    size_value_return = 0

    motor_mode = 0
    buzzer_mode = 0
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

def getMotorMode():
    global motor_mode
    return motor_mode

def getSizeValueReturn():
    global size_value_return
    return size_value_return

def body_func1():
    global body_flag
    global mode
    global body_stop
    global dis_stop
    if body_flag:
        mode = 1
        body.body()
        body_stop = 1
        time.sleep(0.2)

# body_detect_true/false
# def body_func2():
    # global body_stop
    # global body_flag
    # global motor_mode
    # global mode

    # while body_flag:
    #     if body.getBodyTrue()==1 and body.getBodyCenter()==1:
    #         # 몸 인식, 가운데 위치
    #         body_stop=1
    #         body.setFlagBody_False()
            
    #     else:
    #         if body.getBodyTrue()==0:
    #             # 인식이 안 됨. 무작정 돌기
    #             motor_mode=2
    #         elif body.getBodyTrue()==1 and body.getBodyCenter()==2:
    #             # 몸 인식 완료 , 왼쪽으로 돌기
    #             motor_mode=2
    #         elif body.getBodyTrue()==1 and body.getBodyCenter()==3:
    #             # 몸 인식 완료, 오른쪽으로 돌기
    #             motor_mode=3
    #         mode=1

# def dis_func1():
#     # dis.dis()
#     pass

# dis_detect_true/false
def dis_func2():
    global dis_stop
    global dis_flag
    global mode
    global motor_mode
    global dis_flag

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

                if dis_value>=199 and dis_value<=202:
                    dis_stop=1
                    dis.setFlagDis()
                    # dis.setKernel()
                else:
                    mode=2

            else:
                continue

# face_detect_true/false
def face_func2():
    global face_flag
    global face_stop
    global mode

    mode = 3
    face.face()
    face_stop=1
    time.sleep(0.2)


# size_detect_value
def size_func2():
    global size_value
    global size_flag
    global size_stop
    global mode

    mode=4
    size_value = size.size()
    size_stop=1
    time.sleep(0.2)


def size_return():
    global body_flag
    global face_flag
    global dis_flag
    global size_flag
    global size_all_flag
    global body_th
    global body_stop
    # global body_start

    body_th = th.Thread(target=body_func1)
    body_th.start()
    # body_start = th.Thread(target=body_func2)
    # body_start.start()    

    def body_detect_mode():
        global motor_mode
        global mode
        global body_flag
        global dis_flag
        global dis_stop
        # global dis_th
        global dis_start
        global dis

        if body_stop==1:
            #motor_stop
            motor_mode=0

            #body_detect_stop
            body_flag=False
            body_th.join()
            # body_start.join()

            # if cv2.getWindowProperty("ROS",cv2.WND_PROP_VISIBLE)>=0:
            #     cv2.destroyWindow("ROS")
            # picam2 = Picamera2
            # picam2.stop()
            # picam2.close()

            #face_detect_start
            dis_stop=0

            import ROS as dis

            dis.setFlagDis_True()

            # dis_th = th.Thread(target=dis_func1)
            # dis_th.start()
            dis_start = th.Thread(target=dis_func2)
            dis_start.start()

            #dis_detect_mode_on
            mode=2
        else:
            #motor right
            motor_mode=2

    def distance_mode():
        global motor_mode
        global mode
        global dis_flag
        global dis_start
        global face_flag
        global face_stop
        global face_start
        global face

        if dis_stop==1:
            #motor_stop
            motor_mode=0

            #distance_stop
            dis_flag=False
            # dis_th.join()
            dis_start.join()

            #face_detect_start
            face_stop=0
            face_flag=True

            import face_detect as face

            face_start = th.Thread(target=face_func2)
            face_start.start()

            #face_detect_mode_on
            mode=3
            motor_mode=0
        else:
            if dis_value>200:
                #straight
                motor_mode=1
            elif dis_value<200:
                #back
                motor_mode=4

    def face_detect_mode():
        global motor_mode
        global mode
        global face_flag
        global size_flag
        global size_stop
        global size_start
        global size

        if face_stop==1:
            #motor_stop
            motor_mode=0

            #face_detect_stop
            face_flag=False
            face_start.join()

            #distance_start
            size_stop=0
            size_flag=True

            import size

            size.setFlagSize_True()

            size_start = th.Thread(target=size_func2)
            size_start.start()

            #distance_mode_on
            mode=4
        else:
            motor_mode=2 #again code write

    def size_detect_mode():
        global size_flag
        global mode
        global size_value_return
        global size_all_flag

        if size_stop==1:
            #size_detect_stop
            size_flag=False
            size_start.join()

            size_value_return = 1

            print(size_value)

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
            
        
    except KeyboardInterrupt:
        pass

    body_flag=False
    face_flag=False
    dis_flag=False
    size_flag=False
    size_all_flag=False

    if body_stop==0:
        body_th.join()
        # body_start.join()
    elif face_stop==0:
        # dis_th.join()
        dis_start.join()
        face_start.join()
    elif dis_stop==0:
        body_th.join()
        # body_start.join()
        # dis_th.join()
        dis_start.join()
    elif size_stop==0:
        face_start.join()
        size_start.join()

    cv2.destroyAllWindows()