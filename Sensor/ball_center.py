# -*- coding: utf-8 -*-

import numpy as np
import cv2

#Define object specific variables  
dist = 0
focal = 450
pixels = 30
width = 4

img_width = 640
img_height = 480
middle = img_width // 2

#find the distance from then camera
def get_dist(rectange_params,image, name, isMiddle):
    #find no of pixels covered
    pixels = rectange_params[1][0]

    #calculate distance
    dist = (width*focal)/pixels
    
    #Write n the image
    if name == 'flag':
        image = cv2.putText(image, 'flag Distance from Camera in CM :', org, font,  
        1, color, 2, cv2.LINE_AA)

        image = cv2.putText(image, 'flag Middle : {}'.format(isMiddle), org, font,  
        1, color, 2, cv2.LINE_AA)
    elif name == 'ball':
        image = cv2.putText(image, 'ball Distance from Camera in CM :', org, font,  
        1, color, 2, cv2.LINE_AA)

        image = cv2.putText(image, 'flag Middle : {}'.format(isMiddle), org, font,  
        1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(dist), (110,50), font,  
    fontScale, color, 1, cv2.LINE_AA)

    return image, name

# box 좌표의 x축 최댓값과 최솟값을 return하는 함수
def getMaxMin(box):
    min_x, max_x = img_width, 0
    min_y, max_y = img_width, 0

    for x, y in box:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        elif y > max_y:
            max_y = y
    return max_x, min_x, max_y, min_y


# max_x, min_x를 입력받으면 해당 물체가 중간에 있는지 return하는 함수
def judgeMiddle(max_x, min_x):

    l_dist = min_x
    r_dist = img_width - max_x
    error_range = 80
    
    if abs(l_dist - r_dist) < error_range:
        return True
    else:
        return False

#Extract Frames 
cap = cv2.VideoCapture(0)


#basic constants for opencv Functs
kernel = np.ones((3,3),'uint8')
font = cv2.FONT_HERSHEY_SIMPLEX 
org = (0,20)  
fontScale = 0.6 
color = (0, 0, 255) 
thickness = 2


cv2.namedWindow('Object Dist Measure ', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure ', 700,600)


#loop to capture video frames
while True:
    ret, img = cap.read()
    # print(img.shape)
    
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #window version
    lower = np.array([170, 99, 100])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)
    lower1 = np.array([1, 99, 100])
    upper1 = np.array([5, 255, 255])
    mask += cv2.inRange(hsv_img, lower1, upper1)

    # lower_flag = np.array([35, 130, 150])
    # upper_flag = np.array([45, 255, 255])
    # mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)


    #Remove Extra garbage from image
    # d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)
    # f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel,iterations = 5)

    #mac version
    #predefined mask for color detection
    # lower = np.array([170, 100, 100])
    # upper = np.array([180, 255, 255])
    # mask = cv2.inRange(hsv_img, lower, upper)


    lower_flag = np.array([10, 150, 100])
    upper_flag = np.array([35, 255, 255])
    mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)


    # #Remove Extra garbage from image
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)
    f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel,iterations = 5)

    
    #find the histogram
    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    max_x, min_x, max_y, min_y = -1, img_width + 1, -1, img_width + 1
    ball_box = None
    
    for cnt in cont:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            ball_box = cv2.boxPoints(rect)
            ball_box = np.int0(ball_box)
            print('points :', ball_box)
            cv2.drawContours(img,[ball_box], -1,(255,0,0),3)

            max_x, min_x, max_y, min_y = getMaxMin(ball_box)
            isMiddle = judgeMiddle(max_x, min_x)
            
            img = get_dist(rect,img, 'ball', isMiddle)

    # 새로운거
    cont2,hei2 = cv2.findContours(f_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont2 = sorted(cont2, key = cv2.contourArea, reverse = True)[:1]

    f_max_x, f_min_x, f_max_y, f_min_y = -1, img_width + 1, -1, img_width + 1
    for cnt in cont2:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print('points :', box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)

            f_max_x, f_min_x, f_max_y, f_min_y = getMaxMin(box)
            isMiddle = judgeMiddle(f_max_x, f_min_x, )
            
            img = get_dist(rect,img, 'flag', isMiddle)
                
                
    if ball_box is not None and all(f_max_x > x > f_min_x and f_max_y > y > f_min_y for x, y in ball_box):
        cv2.circle(img, (100,200), 20, cv2.FILLED, cv2.LINE_AA)


    cv2.imshow('Object Dist Measure ', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()