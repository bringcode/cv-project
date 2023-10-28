import cv2
import numpy as np

# 두 꼭짓점 간의 거리를 계산하는 함수
def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# 두 점을 합치는 함수
def merge_points(points):
    if not points:
        return []

    merged_point = np.mean(points, axis=0, dtype=np.int32)
    return [merged_point]

# 비디오 캡처를 초기화합니다.
cap = cv2.VideoCapture('imgs/flagONLY.h264')  # 비디오 파일 경로 설정
# cap = cv2.VideoCapture('imgs/arrowONLY.h264')  # 비디오 파일 경로 설정

while True:
    # 프레임을 읽어옵니다.
    ret, frame = cap.read()
    if not ret:
        break

    # 노란색 물체를 감지합니다.
    lower_yellow = np.array([23, 43, 196])
    upper_yellow = np.array([41, 255, 255])
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = np.ones((3,3), 'uint8')

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
    
    # 노란색 물체의 컨투어를 찾습니다.
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    objects = []  # 물체의 정보를 저장할 리스트

    for contour in contours:
        # 근사정확도 지수(외곽선 길이에 비례하게 설정)
        epsilon = 0.06 * cv2.arcLength(contour, True)

        # 컨투어 근사화
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 꼭짓점 수 계산
        vertices = len(approx)
        
        # 꼭짓점 수가 3개 이상이고 10개 이하이며, 넓이가 1000 이상인 경우만 표시
        if 3 <= vertices and cv2.contourArea(contour) >= 500:
            # 컨투어를 그리기 위한 직사각형을 생성합니다.
            x, y, w, h = cv2.boundingRect(approx)
            
            # 물체 정보를 저장
            objects.append({
                'x': x,
                'y': y,
                'vertices': vertices,
                'contour': approx,
            })

    # 물체들을 y 좌표를 기준으로 내림차순 정렬
    objects.sort(key=lambda obj: obj['y'], reverse=True)

    # 물체 중에서 높은 물체만 "Flag"로 표시하고 그리기
    for obj in objects:
        if obj['vertices'] < 7:
            text = 'Flag'
            cv2.drawContours(frame, [obj['contour']], 0, (0, 255, 0), 2)
        else:
            text = 'Arrow'
            cv2.drawContours(frame, [obj['contour']], 0, (0, 0, 255), 2)
            
        cv2.putText(frame, text, (obj['x'], obj['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 각 객체의 꼭짓점 수를 텍스트로 표시
        cv2.putText(frame, f'Vertices: {obj["vertices"]}', (obj['x'], obj['y'] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 결과를 표시합니다.
    cv2.imshow('Video', frame)

    # 종료 키 (q)를 누르면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처를 해제하고 창을 닫습니다.
cap.release()
cv2.destroyAllWindows()