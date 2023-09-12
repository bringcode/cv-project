import cv2
import numpy as np

# 비디오 파일을 초기화합니다.
cap = cv2.VideoCapture('0925_19_38.h264')

while True:
    # 비디오 파일로부터 프레임을 읽어옵니다.
    ret, frame = cap.read()

    if not ret:
        break

    # 흑백이미지로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 이진화 (Thresholding)를 적용하여 검은색 부분만 검출
    _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

    # 컨투어를 찾습니다.
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 컨투어의 면적을 계산합니다.
        area = cv2.contourArea(contour)
        if area > 1000:  # 화살표의 크기에 따라 이 값 조절
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
            # 화살표의 중심점을 찾습니다.
            M = cv2.moments(contour)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

    # 결과를 화면에 출력합니다.
    cv2.imshow("Result", frame)

    # 100ms 대기하고 ESC 키를 누르면 종료
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
