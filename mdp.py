from gpiozero import LED
import threading as th
import shopping_mode as clothes
# 길 안내 모드 모터 값 받아오기
import bluetooth_code as bluetooth
import time

#gpio motor
mode_return = LED(5)
bu = LED(6)
shop = LED(20)
motor1 = LED(13)
motor2 = LED(19)
motor3 = LED(26)


#attribute
flag_motor = True
size_go_flag = False
buzzer_mode = 0
motor_mode = 0
time_flag = False
shopping_flag = False

#all_mode
mode = ''

#size
# size=[]

# #clothes
# def size_go():
#     global shopping_flag
#     if shopping_flag==False:
#         clothes.shopping()
#         shopping_flag=True

# def size_getValue():
#     while size_go_flag:
#         global motor_mode
#         global size
#         motor_mode = clothes.getMotorMode()
#         if clothes.getSizeValueReturn()==1:
#             size = clothes.getSizeValue()
#             #print(size)

#mode_select
def mode_select():
    bluetooth.bluetooth_code()
    
# def setBuFalse():
#     bu.off()

# def mode_select_getValue():
#     global mode
#     while True:
#         mode = bluetooth.getModeValue()


blue_head = th.Thread(target=mode_select)
# blue_body = th.Thread(target=mode_select_getValue)

blue_head.start()
# blue_body.start()

#motor thread
# def motor_start():
#     global flag_motor
#     global motor_mode

#     while flag_motor:


#         if buzzer_mode:
#             buzzer.on()
#         else:
#             buzzer.off()

#         if motor_mode==1: #straight
#             motor1.on()
#             motor2.off()
#             motor3.off()
#         elif motor_mode==2: #right
            # motor1.off()
            # motor2.on()
            # motor3.off()
#         elif motor_mode==3: #left
#             motor2.on()
#             motor3.off()
#         elif motor_mode==4: #back
#             motor1.off()
#             motor2.off()
#             motor3.on()
#         else: #stop
#             motor1.off()
#             motor2.off()
#             motor3.            size.size_return()
# target=motor_start)
# motor.start()

start=1
flag = 0
setsetFlag = 1
mode_auto = 0

def setFalseAll():
    global setsetFlag

    if setsetFlag == 1:
        mode_return.off()
        bu.off()
        motor1.off()
        motor2.off()
        motor3.off()
        setsetFlag=0

try:
    while True:
        setFalseAll()
        if bluetooth.getModeValue()=='종료' and bluetooth.getFlag()==1:
            flag=1
            mode_return.off()
            motor1.off()
            motor2.off() 
            motor3.off()
            bu.off()
            bluetooth.setWrite("종료되었습니다")
        elif bluetooth.getModeValue()=='자동 모드' and bluetooth.getFlag()==1: # auto
            flag=2
            bluetooth.setWrite("자동 모드입니다 시작, 정지 중에 선택해주세요")
        elif bluetooth.getModeValue()=='수동 모드' and bluetooth.getFlag()==1: # user
            flag=3
            mode_return.off()
            bluetooth.setWrite("수동 모드입니다 가고자하는 경로에 물체가 있다면 신호가 울립니다.")
        elif bluetooth.getModeValue()=='쇼핑몰' and bluetooth.getFlag()==1: # shopping
            motor1.off()
            motor2.off()
            motor3.off()
            clothes.setBluetooth(" ")
            clothes.setBuMotor(bu, motor1,motor2,motor3)
            flag=4
            mode_return.on()
            shop.on()
            clothes.shopping()
            shop.off()
            mode_return.off()
            flag = 0
            bluetooth.setWrite("쇼핑몰이 나가졌습니다")
            # mode=bluetooth.switchModeValue('5') # mode value
        elif bluetooth.getModeValue()=='부저 작동':
            buzzer_mode = 1
        elif bluetooth.getModeValue()=='부저 멈춤':
            buzzer_mode = 0

        if flag==2:
            bu.off()
            if bluetooth.getModeValue()=='시작' and bluetooth.getFlag()==1:
                mode_return.on()
                mode_auto = 1
            elif bluetooth.getModeValue()=='정지' and bluetooth.getFlag()==1:
                mode_return.off()
                mode_auto = 0
            else:
                mode_auto = mode_auto

            if mode_auto==1:
                motor1.on()
                motor2.off()
                motor3.off()
            elif mode_auto==0:
                motor1.off()
                motor2.off()
                motor3.off()
            else:
                motor1.off()
                motor2.off()
                motor3.off()

except KeyboardInterrupt:
    pass

# motor.join()
blue_head.join()
# blue_body.join()
if flag==4:
    # size.join()
    print('쇼핑몰끝')

flag_motor=False
size_go_flag=False