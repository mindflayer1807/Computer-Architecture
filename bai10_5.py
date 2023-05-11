import cv2
import RPi.GPIO as GPIO
import copy
import numpy as np
def main():
    BT1 = 21
    BT2 = 26
    cap = cv2.VideoCapture(0)
    print("Cap ok")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BT2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    isDraw = False
    while True:
        if GPIO.input(BT1) == GPIO.LOW:
            print("press BT1")
            while True:
                ret, src = cap.read()
                frame = copy.copy(src)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, (0, 118, 130), (5, 255, 255))
                _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                result = cv2.bitwise_or(frame, frame, mask=mask)
                if GPIO.input(BT2) == GPIO.LOW:
                    isDraw = True
                if isDraw:
                    draw(contours, result)
                cv2.imshow("Camera", src)
                cv2.imshow("Theshold", result)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    GPIO.cleanup()
                    cv2.destroyAllWindows()
                    break
def nothing(x):
    pass
def draw(contours, frame):
    if contours is None:
        print("No have contours. Please try to agian")
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 300:
            hull = cv2.convexHull(contours[i])
            cv2.drawContours(frame, [hull], -1, (0, 0, 255))
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()
