import cv2
import numpy as np

# 라즈베리 파이 카메라 초기화
cap = cv2.VideoCapture('arr.mp4')

# HSV 색상 범위 설정
lower_yellow = np.array([11, 34, 196])
upper_yellow = np.array([41, 255, 255])

while True:
    # 카메라에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

    # BGR 이미지를 HSV 이미지로 변환
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 노란색 마스크 생성
    yellow_mask = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)

    # 마스크에서 노이즈 제거 (모폴로지 연산)
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)
    yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)

    # 컨투어 찾기
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 노란색 픽셀이 포함된 박스 좌표 구하기
        x, y, w, h = cv2.boundingRect(contour)

        # 박스 중점 좌표 구하기
        center_x = x + w // 2
        center_y = y + h // 2

        # 중점 좌표의 색상 확인 (노란색 여부)
        center_color = hsv_frame[center_y, center_x]
        is_yellow = (center_color[0] >= lower_yellow[0] and center_color[0] <= upper_yellow[0] and
                     center_color[1] >= lower_yellow[1] and center_color[1] <= upper_yellow[1] and
                     center_color[2] >= lower_yellow[2] and center_color[2] <= upper_yellow[2])

        # 노란색 픽셀을 기준으로 화살표 또는 깃발로 판단
        if is_yellow:
            cv2.putText(frame, "Arrow", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Flag", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 화면에 표시
    cv2.imshow('Frame', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 카메라 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
