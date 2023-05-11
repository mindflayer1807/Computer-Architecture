import cv2
import RPi.GPIO as GPIO
import copy
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
                green_mask = cv2.inRange(hsv, (35, 89, 107), (45, 241, 213))
                _, countoursGreen, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                red_mask = cv2.inRange(hsv, (0, 118, 130), (5, 255, 255))
                _, countoursRed, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                group = green_mask + red_mask
                group = group >= 1
                group = group.astype('uint8') * 255
                result = cv2.bitwise_or(frame, frame, mask=group)
                if GPIO.input(BT2) == GPIO.LOW:
                    isDraw = True
                if isDraw:
                    draw(countoursRed, countoursGreen, result)
                cv2.imshow("Theshold", result)
                cv2.imshow("Camera", src)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    GPIO.cleanup()
                    cv2.destroyAllWindows()
                    break
def nothing(x):
    pass
def draw(countoursRed,countoursGreen, frame):
    for i in range(len(countoursRed)):
        if cv2.contourArea(countoursRed[i]) > 300:
            hull = cv2.convexHull(countoursRed[i])
            cv2.drawContours(frame, [hull], -1, (0, 0, 255))
    for i in range(len(countoursGreen)):
        if cv2.contourArea(countoursGreen[i]) > 300:
            hull = cv2.convexHull(countoursGreen[i])
            cv2.drawContours(frame, [hull], -1, (0, 255, 0))
try:
    main()
except KeyboardInterrupt:
    GPIO.cleanup()
    cv2.destroyAllWindows()