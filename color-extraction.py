import cv2 as cv
import sys
import numpy as np


cap = cv.VideoCapture('imgs/first.h264')

if not cap.isOpened():
	sys.exit('카메라 연결 실패')

hue_yellow = 55
distribution = 10

lower_yellow = (hue_yellow-distribution, 150, 100)
upper_yellow = (hue_yellow+distribution, 255, 255)

while True:
    ret, img_color = cap.read()
    img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
    

    img_mask = cv.inRange(img_hsv, lower_yellow, upper_yellow)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=3)
    img_mask_color = cv.cvtColor(img_mask, cv.COLOR_GRAY2BGR)

    smooth = np.hstack((img_color,
                    img_mask_color))
    
    cv.imshow('Smooth', smooth)

    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()