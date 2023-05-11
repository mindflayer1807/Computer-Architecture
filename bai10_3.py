import cv2
import RPi.GPIO as GPIO
import time
def main():
    BT4 = 19
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    global namewindow
    namewindow = "Camera User"
    capture = cv2.VideoCapture(0)
    print("Capture da ok")
    cap_stream = False
    while capture.isOpened():
        ret, frame = capture.read()
        if GPIO.input(BT4) == GPIO.LOW:
            print("press BT4")
            if not cap_stream:
                cap_stream = True
                time.sleep(0.5)
                continue
            if cap_stream:
                cap_stream = False
                cv2.destroyWindow(namewindow)
                time.sleep(0.5)
                continue
        if cap_stream:
            cv2.imshow(namewindow, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                GPIO.cleanup()
                cv2.destroyWindow(namewindow)
                break
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyWindow(namewindow)