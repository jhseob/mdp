from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size=(1920,1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

while True:
    user = input()
    if user=='1':
        picam2.stop()
        picam2.close()
    elif user=='2':
        picam2._open_camera()
        picam2.start()
