from gpiozero import Button

user_use_detect = 0

def getButton():
    return user_use_detect

def button_detect():
    sw = Button(1)

    def on_button_pressed():
        global user_use_detect
        user_use_detect = 1

    sw.when_pressed = on_button_pressed