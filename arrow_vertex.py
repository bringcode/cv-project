import cv2
import numpy as np

image = cv2.imread("arrow3.jpg", cv2.COLOR_BGR2GRAY)
# 이미지의 크기를 절반으로 조절
height, width = image.shape[:2]
image = cv2.resize(image, (int(width * 0.2), int(height * 0.2)))

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([35, 240, 255]))

# 윤곽선 검출
contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 윤곽선 그리기
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

for contour in contours:
    if cv2.contourArea(contour) > 1500: 
        arrow_contour = contour
        
curvatures = []
        
# 곡률 값의 임계값 설정
# threshold_curvature = 0.13
threshold_curvature = 0.13

k = 7  # 이웃 점들의 수
for i in range(len(arrow_contour)):
    pt1 = arrow_contour[i - k]
    pt2 = arrow_contour[i]
    pt3 = arrow_contour[(i + k) % len(arrow_contour)]
    
    cv2.circle(image, tuple(pt1[0]), 3, (255, 0, 0), -1)
    cv2.circle(image, tuple(pt2[0]), 3, (255, 0, 0), -1)
    cv2.circle(image, tuple(pt3[0]), 3, (255, 0, 0), -1)
    
    triangle_area = abs(pt1[0][0] * (pt2[0][1] - pt3[0][1]) + pt2[0][0] * (pt3[0][1] - pt1[0][1]) + pt3[0][0] * (pt1[0][1] - pt2[0][1])) / 2.0
    a = np.linalg.norm(pt1 - pt2)
    b = np.linalg.norm(pt2 - pt3)
    c = np.linalg.norm(pt3 - pt1)
    curvature = (4 * triangle_area) / (a * b * c)
    if curvature > threshold_curvature:
      curvatures.append(curvature)

for i, curvature in enumerate(curvatures):
    if curvature > threshold_curvature:
        cv2.circle(image, tuple(arrow_contour[i][0]), 5, (255, 0, 0), -1)  # 파란색으로 점 그리기
    
# 최대 곡률을 가진 점 찾기
tip_point = tuple(arrow_contour[np.argmax(curvatures)][0])


cv2.circle(image, tip_point, 5, (0, 0, 255), -1)
cv2.imshow("Arrow Tip Point", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
