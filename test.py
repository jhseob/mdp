from gpiozero import LED

motor1 = LED(13)
motor2 = LED(19)
motor3 = LED(26)
mode_return = LED(5)


bu = LED(6)

while True:
    gogogo = int(input())
    if gogogo ==1:
        motor1.on()
        motor2.off()
        print(gogogo)
    elif gogogo ==2:
        motor1.off()
        motor2.on()
        motor3.off()
        print(gogogo)
    elif gogogo==3:
        motor1.on()
        motor2.on()
        motor3.off()
        print(gogogo)
    elif gogogo==4:
        motor1.off()
        motor2.off()
        motor3.on()
        print(gogogo)
    elif gogogo==5:
        motor1.off()
        motor2.off()
        motor3.off()
        print(gogogo)
    elif gogogo==6:
        bu.on()
        motor1.off()
        motor2.off()
        motor3.off()
    elif gogogo==7:
        bu.off()
        motor1.off()
        motor2.off()
        motor3.off()
    elif gogogo==8:
        mode_return.on()
    else:
        mode_return.off()