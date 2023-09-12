import cv2
import numpy as np

image = cv2.imread("arrow2.jpg")
height, width = image.shape[:2]
src = cv2.resize(image, (int(width * 0.2), int(height * 0.2)))
dst = src.copy()

hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([35, 240, 255]))

# 윤곽선 검출
contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
large_contours = [contour for contour in contours if cv2.contourArea(contour) > 1500]
cv2.drawContours(dst, large_contours, -1, (0, 255, 0), 3)

corners = cv2.goodFeaturesToTrack(yellow_mask, 100, 0.01, 5, blockSize=3, useHarrisDetector=True, k=0.12)

for i in corners:
    x, y = i[0]
    cv2.circle(dst, (int(x), int(y)), 3, (255, 0, 255), 2)

for i in corners:
    x, y = i[0]
    # 점이 large_contours 중 어느 윤곽선 내부에도 존재하지 않는 경우 건너뛰기
    if all(cv2.pointPolygonTest(contour, (x,y), False) < 0 for contour in large_contours):
        continue

    cv2.circle(dst, (int(x), int(y)), 3, (0, 0, 255), 2)


cv2.imshow("dst", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()