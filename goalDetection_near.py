import numpy as np
import cv2


#거리 구할 때 필요한 변수 값들 dist구하는데 사용됨
dist = 0
focal = 450
pixels = 30
width = 8


#거리 구하는코드(따로 변경 필요 x)
def get_dist(rectange_params,image, name):
    #find no of pixels covered
    pixels = rectange_params[1][0]
    print(pixels)
    #calculate distance
    dist =(int) ((width*focal)/pixels)
    


    image = cv2.putText(image, str(dist), (110,50), font,  
    fontScale, color, 1, cv2.LINE_AA)


    return image

#영상 불러오기 ()안 바꾸면  영상 바뀜
cap = cv2.VideoCapture('flagg.mp4')


#필터링 기술이나 거리 화면 폰트 관련 변수들
kernel = np.ones((5,5),'uint8')



#loop to capture video frames
while True:
    ret, img = cap.read()

    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# 색 영역값 파악
    lower = np.array([28, 180, 109])
    upper = np.array([255, 255, 255])
    mask = cv2.inRange(hsv_img, lower, upper)


    lower_flag = np.array([20, 68, 130])
    upper_flag = np.array([66, 255, 255])
    mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)


    #필터링 CLOSE , DILATE 사용 iteration도 로봇화면 보고 수정 필요
    d_img = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel,iterations = 3)
    f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_CLOSE, kernel,iterations = 11)


    #영역찾기 코드
   # 빨강 영역 구하기
    cont, hei = cv2.findContours(d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont = sorted(cont, key=cv2.contourArea, reverse=True)[:1]

    red_boxes = []  # List to store red box coordinates

    for cnt in cont:
        if 100 < cv2.contourArea(cnt) < 306000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            red_boxes.append(box)  # Store red box coordinates
            cv2.drawContours(img, [box], -1, (0, 0, 255), 3)

# 노랑영역 구하기
    cont2, hei2 = cv2.findContours(f_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cont2 = sorted(cont2, key=cv2.contourArea, reverse=True)[:1]

    yellow_boxes = []  # 노랑 영역좌표값 배열

    for cnt in cont2:
        if 100 < cv2.contourArea(cnt) < 306000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            yellow_boxes.append(box)  # Store yellow box coordinates
            cv2.drawContours(img, [box], -1, (0, 255, 255), 3)

# 노랑 영역속에 빨강영역이 포함되는지 확인하는 코드
    for red_box in red_boxes:
        for yellow_box in yellow_boxes:
            is_inside = True
            for point in red_box:
                x, y = point
                if x < yellow_box[0][0] and x > yellow_box[2][0] and y < yellow_box[0][1] and y > yellow_box[2][1]:
                    is_inside = False
                    break
            if is_inside:
                print('goal')
            else:
                print('no goal')

    resized_img_1 = cv2.resize(img, dsize=(800,500), interpolation=cv2.INTER_LINEAR)

    cv2.imshow('Object Dist Measure ', resized_img_1)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()