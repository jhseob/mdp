import time
import serial
import shopping_mode as shopping

ser = serial.Serial(port='/dev/ttyAMA1',baudrate=9600,timeout=0.1)
mode = ' '
mode_flag = True
flag = 0
past_data = ser.read(1000)

# def serialInput(value):
#     global past_data
#     global ser
#     ser = value
#     past_data = ser.read(1000)

def setModeFlag():
    global mode_flag
    mode_flag = False

def getModeValue():
    return mode

def getFlag():
    return flag

def setWrite(code):
    ser.flush()
    time.sleep(0.1)
    ser.write(str(code).encode())

def bluetooth_code():
    global mode_ready
    global mode
    global mode_flag
    global past_data
    global flag

    try:
        while mode_flag:
            mode_ready = ser.readline()
            if mode_ready.decode('UTF-8', errors='ignore') != past_data.decode('UTF-8', errors='ignore') and flag!=1:
                mode = mode_ready.decode('UTF-8', errors='ignore')
                print(mode)
                flag = 1
            else:
                flag = 0
            past_data = mode_ready

            if shopping.sendBluetooth()!=" ":
                shopping.setFlag(flag)
                shopping.setBluetooth(mode)
                setWrite(shopping.sendBluetooth())


    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the serial port
        ser.close()