import cv2 as cv

cap = cv.VideoCapture(0)

while True :
    
    ret,img_color = cap.read()  # 영상으로부터 프레임 얻어오기 > 두 개의 값을 반환하므로 두 변수 저장
    img_color=cv.resize(img_color, (400, 1000))

    blur = cv.GaussianBlur(img_color, (23, 23), 0)    # 블러 적용

    img_hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)  # BGR > HSV으로 변환

    hue_yellow = 0    # 빨간색의 hue값
    lower_yellow = (hue_yellow-5, 100, 100)  # 0을 기준으로 하위 레드값 (색상, 채도, 명도)
    upper_yellow = (hue_yellow+5, 255, 255)    # 0을 기준으로 상위 레드값
    img_mask = cv.inRange(img_hsv, lower_yellow, upper_yellow) # 마스크 이미지 생성

    kernel = cv.getStructuringElement( cv.MORPH_RECT, (5, 5) )  # 팽창 적용
    img_mask = cv.morphologyEx(img_mask, cv.MORPH_CLOSE, kernel, iterations=5) #팽창 3번 적용하기

    nlabels, lables, stats, centroids = cv.connectedComponentsWithStats(img_mask)

    max = -1
    max_index = -1

    for i in range(nlabels) :
        if i < 1 :
            continue

        area = stats[i, cv.CC_STAT_AREA]

        if area > max :
            max = area
            max_index = i

    if max_index != -1 :
        center_x = int(centroids[max_index, 0])
        center_y = int(centroids[max_index, 1])
        left = stats[max_index, cv.CC_STAT_LEFT]
        top = stats[max_index, cv.CC_STAT_TOP]
        width = stats[max_index, cv.CC_STAT_WIDTH]
        height = stats[max_index, cv.CC_STAT_HEIGHT]

        cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 5)
 

    cv.imshow('Red', img_mask)     # 빨간색의 위치 표시
    cv.imshow('Result', img_color)  # 내 웹캠 표시
    cv.imshow('Blur',blur)      #블러 화면 표시

    key = cv.waitKey(20)
    if key == 27 :
        break
