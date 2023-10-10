import numpy as np
import cv2


#Define object specific variables  
dist = 0
focal = 450
pixels = 30
width = 4

img_width = 1280
img_height = 720
middle = img_width // 2

#find the distance from then camera
def get_dist(rectange_params,image, name, isMiddle):
    #find no of pixels covered
    pixels = rectange_params[1][0]

    #calculate distance
    dist = (width*focal)/pixels
    
    #Wrtie n the image
    if name == 'flag':
        image = cv2.putText(image, 'flag Distance from Camera in CM :', org, font,  
        1, color, 2, cv2.LINE_AA)

        image = cv2.putText(image, 'flag Middle : {}'.format(isMiddle), org, font,  
        1, color, 2, cv2.LINE_AA)
    else:
        image = cv2.putText(image, 'ball Distance from Camera in CM :', org, font,  
        1, color, 2, cv2.LINE_AA)

        image = cv2.putText(image, 'flag Middle : {}'.format(isMiddle), (0,40), font,  
        1, color, 2, cv2.LINE_AA)

    image = cv2.putText(image, str(dist), (110,50), font,
    fontScale, color, 1, cv2.LINE_AA)

    return image

# box 좌표의 x축 최댓값과 최솟값을 return하는 함수
def getMaxMin(box):
    min_x, max_x = img_width, 0

    for x, y in box:
        if x < min_x:
            min_x = x
        elif x > max_x:
            max_x = x
    return max_x, min_x

# max_x, min_x를 입력받으면 해당 물체가 중간에 있는지 return하는 함수
def judgeMiddle(max_x, min_x):
    length = max_x - min_x
    error_range = length // (3/2)
    if max_x <= middle + error_range and min_x >= middle - error_range:
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


cv2.namedWindow('Object Dist Measure ',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Object Dist Measure ', 700,600)


#loop to capture video frames
while True:
    ret, img = cap.read()
    print(img.shape)

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


    #predefined mask for green colour detection
    lower = np.array([170, 100, 100])
    upper = np.array([180, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)


    lower_flag = np.array([10, 150, 100])
    upper_flag = np.array([20, 255, 255])
    mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)


    #Remove Extra garbage from image
    d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel,iterations = 5)
    f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel,iterations = 5)


    #find the histogram
    cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print('points :', box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)

            max_x, min_x = getMaxMin(box)
            isMiddle = judgeMiddle(max_x, min_x, )
            
            img = get_dist(rect,img, 'ball', isMiddle)

    # 새로운거
    cont2,hei2 = cv2.findContours(f_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cont2 = sorted(cont2, key = cv2.contourArea, reverse = True)[:1]

    for cnt in cont2:
        #check for contour area
        if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

            #Draw a rectange on the contour
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print('points :', box)
            cv2.drawContours(img,[box], -1,(255,0,0),3)

            max_x, min_x = getMaxMin(box)
            isMiddle = judgeMiddle(max_x, min_x, )
            
            img = get_dist(rect,img, 'flag', isMiddle)


    cv2.imshow('Object Dist Measure ', img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cv2.destroyAllWindows()