import cv2, sys
import numpy as np
import platform

def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), thickness= 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), lineType=cv2.LINE_AA)

#def clock():
    #return cv2.getTickCount() / cv2.getTickFrequency()

W_View_size = 320
H_View_size = int(W_View_size / 1.333)

FPS = 90

cap = cv2.VideoCapture(0)

cap.set(3, W_View_size)
cap.set(4, H_View_size)
cap.set(5, FPS)

#old_time = clock()
#View_select = 1

def empty(a):
    pass

def resize_final_img(x,y,*argv):
    images  = cv2.resize(argv[0], (x, y))
    for i in argv[1:]:
        resize = cv2.resize(i, (x, y))
        images = np.concatenate((images,resize),axis = 1)
    return images

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 300, 300)
cv2.createTrackbar("HUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("HUE Max", "HSV", 255, 255, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)


while True:
    ret, img = cap.read()
    if not ret:
        break


    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_img, lower, upper)
    kernel = np.ones((3,3),'uint8')

    
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)

    final_img = resize_final_img(300,300, mask, d_img)
    
    # final_img = np.concatenate((mask,d_img,e_img),axis =1)
    cv2.imshow('F',final_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break