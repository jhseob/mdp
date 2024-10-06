import boot.RKernel as kernel

flag = True
def setFlagDis():
    global flag
    flag = False

def setFlagDis_True():
    global flag
    flag = True

def setKernel():
    kernel.camera.stop()
    kernel.camera.close()
    kernel.cv.destroyAllWindows()

def closeCamera():
    pass
    print('카메라 꺼짐 시작')
    kernel.camera.stop()
    kernel.camera.close()
    kernel.cv.destroyAllWindows()
    print('카메라 꺼짐')

def dis():
    global flag
    if flag:
        frame = kernel.get_frame()
        kernel.raw_screen = frame
        kernel.set_tensor_input()
        kernel.render_tensor_and_etc()
    else:
        print('카메라 꺼짐 시작')
        
    # kernel.tick_screen()
            # if kernel.cv.waitKey(1) & 0xFF == kernel.key_engine.get_key("ROSOffKey").get("value"):

        # if time.time() - debug_start_time > 3:
        #     kernel.notification_engine.add_notification("hard_warning.png", "3 seconds passed.", ".")
        #     # kernel.notification_engine.add_notification("warning.png", "3 seconds passed1.")
        #     debug_start_time = time.time()

    
