import serial
import time

# 시리얼 포트 초기화
ser = serial.Serial(port='/dev/ttyAMA0', baudrate=9600, timeout=1)

try:
    while True:
        # 시리얼 포트로 데이터 전송
        ser.write("Hwang".encode())

        # 시리얼 포트로부터 데이터 읽기
        mode_ready = ser.read(1024)
        print(mode_ready.decode())

        if mode_ready:
            try:
                mode = mode_ready.decode()
                print(f"받은 데이터: {mode}")
            except UnicodeDecodeError as e:
                print(f"데이터 디코딩 오류: {e}")

        time.sleep(1)  # 시리얼 포트가 과부하되지 않도록 1초 지연

except KeyboardInterrupt:
    print("사용자에 의해 프로그램이 중단되었습니다.")

finally:
    ser.close()  # 시리얼 포트를 제대로 닫기
    print("시리얼 포트가 닫혔습니다.")
