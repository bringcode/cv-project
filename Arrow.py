import cv2
import numpy as np

# 이미지를 읽어옵니다.
image = cv2.imread('ews/img/arrow_right.jpeg')

# 이미지를 HSV 색 공간으로 변환합니다.
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 노란색 범위를 정의합니다. (노란색은 H(색상) 값으로 표현 가능)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# 노란색 범위 내의 픽셀을 마스크로 선택합니다.
yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# 노란색 화살표를 찾습니다.
contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 방향을 저장할 변수를 초기화합니다.
direction_counts = {"Straight": 0, "Right": 0, "Left": 0}

for contour in contours:
    # 화살표의 둘레 길이를 계산합니다.
    perimeter = cv2.arcLength(contour, True)

    # 화살표 근사치를 찾습니다.
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # 화살표의 중심 좌표를 계산합니다.
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0


    # 화살표의 방향을 계산합니다.
    if len(approx) == 3:  # 삼각형이면 직선
        direction = "Straight"
    else:
        # 중심에서 꼭짓점까지의 각도를 계산합니다.
        angle = np.arctan2(approx[0][0][1] - cY, approx[0][0][0] - cX) * 180 / np.pi

        if -45 < angle < 45:  # 각도가 -45도에서 45도 사이면 오른쪽
            direction = "Right"
        elif 135 < angle or angle < -135:  # 각도가 135도에서 -135도 사이면 왼쪽
            direction = "Left"
        else:
            direction = "Straight"

     # 각 방향의 카운트를 증가시킵니다.
    direction_counts[direction] += 1

    # 화살표 주변에 직사각형을 그려서 표시합니다.
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, direction, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

most_common_direction = max(direction_counts, key=direction_counts.get)

# 결과 이미지를 표시합니다.
cv2.imshow("Arrow Direction Detection", image)

#결과 방향을 터미널 창에 출력합니다.
print("가장 많은 방향:", most_common_direction)

cv2.waitKey(0)
cv2.destroyAllWindows()


