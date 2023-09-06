import cv2 as cv
import sys
import numpy as np


hue_yellow = 10
distribution = 10
isContinueVideo = True

# q를 누르면 동영상이 꺼지고, n을 누르면 hue_yellow값에 10을 더한다.
while hue_yellow <= 240 and isContinueVideo:
    cap = cv.VideoCapture('imgs/first.h264')
    
    while True:
        if not cap.isOpened():
            sys.exit('카메라 연결 실패')

        ret, img_color = cap.read()
        lower_yellow = (hue_yellow-distribution, 150, 100)
        upper_yellow = (hue_yellow+distribution, 255, 255)

        img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
        img_mask = cv.inRange(img_hsv, lower_yellow, upper_yellow)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5,5))
        img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations=3)
        img_mask_color = cv.cvtColor(img_mask, cv.COLOR_GRAY2BGR)

        cv.putText(img_mask_color, "hue: "+str(hue_yellow) , (10,10), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        smooth = np.hstack((img_color,
                        img_mask_color))
        
        cv.imshow('Smooth', smooth)

        key = cv.waitKey(1)
        if key == ord('n'):
            hue_yellow += 10
            break
        elif key == ord('q'):
            isContinueVideo = False
            break

cap.release()
cv.destroyAllWindows()