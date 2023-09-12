import cv2
import numpy as np

def find_arrow_center(contour):
    M = cv2.moments(contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def distance(pt1, pt2):
    return np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

image = cv2.imread("arrow3.jpg")
height, width = image.shape[:2]
image = cv2.resize(image, (int(width * 0.2), int(height * 0.2)))

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([35, 240, 255]))

contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    if cv2.contourArea(contour) > 1500: 
        arrow_contour = contour

epsilon = 0.01 * cv2.arcLength(arrow_contour, True)
approx_contour = cv2.approxPolyDP(arrow_contour, epsilon, True)

# 화살표 중심 찾기
center = find_arrow_center(approx_contour)

# 꼭짓점들 중에서 중심과 가장 먼 꼭짓점 찾기
max_distance = 0
farthest_point = None
for point in approx_contour:
    dist = distance(center, tuple(point[0]))
    if dist > max_distance:
        max_distance = dist
        farthest_point = tuple(point[0])

# 결과 이미지에 중심점, 꼭지점, 그리고 중심에서 가장 먼 꼭짓점 그리기
cv2.drawContours(image, [approx_contour], 0, (255, 255, 0), 2)  # 단순화된 윤곽선 그리기
cv2.circle(image, center, 5, (0, 0, 255), -1)  # 중심점을 빨간색으로 표시
for point in approx_contour:
    cv2.circle(image, tuple(point[0]), 5, (0, 255, 0), -1)  # 각 꼭짓점을 초록색으로 표시

cv2.circle(image, farthest_point, 7, (255, 0, 0), -1)  # 중심에서 가장 먼 꼭짓점을 파란색으로 표시

cv2.imshow("Arrow Farthest Corner", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
