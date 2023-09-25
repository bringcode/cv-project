# 공, 깃발, 홀컵 인식
# 거리 계산 + 색 인식

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

#Define object specific variables  
dist = 0
focal = 450
pixels = 30
width = 4

#find the distance from then camera
def get_dist(rectange_params,image):
    #find no of pixels covered
    pixels = rectange_params[1][0]
    print(pixels)
    #calculate distance
    dist = (width*focal)/pixels
    
    #Wrtie n the image
    image = cv2.putText(image, 'Distance from Camera in CM :', org, font,  
       1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(dist), (110,50), font,  
       fontScale, color, 1, cv2.LINE_AA)

    return image
    
#basic constants for opencv Functs
kernel = np.ones((3,3),'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0,20)  
fontScale = 0.6 
color = (0, 0, 255) 
thickness = 2

cv2.namedWindow('Object Dist Measure ',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure ', 700,600)


#loop to capture video frames
while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


    #predefined mask for green colour detection
    lower = np.array([160, 100, 100])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
    


    #Remove Extra garbage from image
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)


    #find the histogram
    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont:
        #check for contour area
        if (cv2.contourArea(cnt)>70 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect) 
            box = np.int0(box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)
            
            img = get_dist(rect,img)

    cv2.imshow('Object Dist Measure ',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()
