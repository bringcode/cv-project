import numpy as np
import cv2

your_area_threshold = 300  # 사용자 정의 임계값, 필요에 따라 값을 조정

cap = cv2.VideoCapture('YYY.h264')  # 비디오 파일 경로를 설정하십시오.

# 초록 영역 박스의 정보를 저장할 리스트
green_boxes = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 영상을 HSV 색 공간으로 변환
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 녹색 범위 정의
    low_green = np.array([57, 95, 61])
    high_green = np.array([89, 255, 255])

    # 녹색 범위에 해당하는 부분을 추출
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)

    # 추출된 녹색 부분을 원본 프레임에 표시
    result_frame = cv2.bitwise_and(frame, frame, mask=green_mask)

    # 녹색 영역의 윤곽선 찾기
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 초록 영역 박스 정보 업데이트
    green_boxes = [cv2.boundingRect(contour) for contour in contours]

    # 노랑색 범위 정의
    low_yellow = np.array([0, 57, 187])
    high_yellow = np.array([45, 234, 255])

    # 노랑색 범위에 해당하는 부분을 추출
    yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

    # 초록 박스 내부에 있는 노랑 영역만 남기고 나머지 부분 제거
    for green_box in green_boxes:
        x, y, w, h = green_box
        yellow_roi = yellow_mask[y:y + h, x:x + w]

        # 초록 상자 내부의 노랑색 영역 처리
        _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_roi, connectivity=8)

        for i in range(1, len(stats)):
            x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]
            if area_blob > your_area_threshold:
                cv2.rectangle(frame, (x + x_blob, y + y_blob), (x + x_blob + w_blob, y + y_blob + h_blob), (0, 255, 0), 2)

                # Convert the yellow region into a binary image for contour detection
                yellow_binary = np.zeros_like(yellow_roi)
                yellow_binary[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob] = yellow_roi[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob]

                # Find contours in the binary image
                yellow_contours, _ = cv2.findContours(yellow_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in yellow_contours:
                    # Approximate the contour to find the vertices
                    epsilon = 0.04 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    num_vertices = len(approx)

                    # Display the shape as ARROW or FLAG based on the number of vertices
                    shape_text = "ARROW" if 6<= num_vertices <= 8 else "FLAG"
                    cv2.putText(frame, f'Shape: {shape_text}', (x + x_blob, y + y_blob - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 원본 영상을 표시
    cv2.imshow('Green and Yellow Frame', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
