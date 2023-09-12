import cv2
import numpy as np

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture("detection_2.mp4")

# 영상 축소 비율
scale_percent = 65

while cap.isOpened():
    ret, frame = cap.read()

    # 프레임이 제대로 읽히지 않은 경우 루프 종료
    if not ret:
        break

    # 영상 크기 축소
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(
        cv2.GaussianBlur(resized_frame, (3, 3), 1),
        cv2.COLOR_BGR2HSV,
    )

    # ball detection start
    mask = cv2.inRange(hsv, np.array([0, 150, 120]), np.array([10, 255, 255]))
    mask += cv2.inRange(hsv, np.array([170, 150, 120]), np.array([180, 255, 255]))

    ball_frame = cv2.bitwise_and(hsv, hsv, mask=mask)
    ball_frame = cv2.cvtColor(ball_frame, cv2.COLOR_HSV2BGR)

    kernel = np.ones((20, 20), np.uint8)
    ball_frame = cv2.morphologyEx(ball_frame, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(
        cv2.cvtColor(ball_frame, cv2.COLOR_BGR2GRAY),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    cnts = cnts[0]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if radius > 5:
            cv2.circle(resized_frame, (int(x), int(y)), int(radius), (0, 0, 255), 5)
    # ball detection end

    # ground detection start
    mask = cv2.inRange(  # 초록(골프장 안쪽)
        hsv,
        # np.array([65, 90, 50]),
        np.array([68, 84, 50]),
        np.array([90, 255, 255]),
    )
    mask += cv2.inRange(  # 청록(골프장 바깥쪽)
        hsv,
        # np.array([90, 90, 0]),
        np.array([80, 65, 0]),
        np.array([110, 255, 255]),
    )
    mask += cv2.inRange(  # 노랑(깃발)
        hsv,
        # np.array([25, 70, 100]),
        np.array([20, 50, 100]),
        np.array([50, 255, 255]),
    )
    

    #검출할 부분만
    masked_frame = cv2.bitwise_and(hsv, hsv, mask=mask)
    masked_frame = cv2.cvtColor(masked_frame, cv2.COLOR_HSV2BGR)

    #객체의 작은 구멍을 메우는데 사용
    kernel = np.ones((15, 15), np.uint8)
    masked_frame = cv2.morphologyEx(masked_frame, cv2.MORPH_CLOSE, kernel)
    masked_frame = cv2.GaussianBlur(masked_frame, (1, 1), 3)

    gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)

    # Canny edge detection
    edges = cv2.Canny(gray, 50, 125)

    # Contour 찾기
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 윤곽선 그리기
    cv2.drawContours(resized_frame, contours, -1, (0, 255, 0), 2)
    # ground detection end

    # 결과 프레임 출력
    cv2.imshow("MaskedFrame", masked_frame)
    cv2.imshow("ResizedFrame", resized_frame)

    # 'esc' 키를 누르면 종료
    if cv2.waitKey(30) == 27:
        break

# 해제
cap.release()
cv2.destroyAllWindows()

