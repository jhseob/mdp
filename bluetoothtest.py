import time
import serial

ser = serial.Serial(port='/dev/ttyAMA1', baudrate=9600, timeout=3)

def setWrite(code):
    ser.flush()
    time.sleep(0.1)
    ser.write(str(code).encode())

def read_serial_data():
    buffer = ""
    try:
        while True:
            # time.sleep(1)
            data = ser.read(1024).decode('UTF-8', errors='ignore')
            if data:
                buffer += data
                print(f"Received data: {data}")
                ser.flush()
            else:
                time.sleep(0.1)

            if len(buffer) > 1000:  
                process_data(buffer)
                buffer = ""  




    except Exception as e:
        print(f"Error: {e}")

    finally:
        ser.close()

def process_data(data):
    # ������ �����͸� ó���ϴ� ����
    print(f"Processing data: {data}")

read_serial_data()
