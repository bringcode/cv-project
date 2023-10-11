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
cap = cv2.VideoCapture('YYAR2.h264')  # 비디오 파일 경로 설정

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

    mask = cv2.morphologyEx(mask, cv2.MORPH_ERODE, kernel, iterations=1)
    
    # 노란색 물체의 컨투어를 찾습니다.
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    objects = []  # 물체의 정보를 저장할 리스트

    for contour in contours:
        # 컨투어를 근사화합니다.
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 꼭짓점 수 계산
        vertices = len(approx)
        
        # 꼭짓점 수가 3개 이상이고 10개 이하이며, 넓이가 1000 이상인 경우만 표시
        if 3 <= vertices <= 10 and cv2.contourArea(contour) >= 500:
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
            
        cv2.putText(frame, text, (obj['x'], obj['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 각 객체의 꼭짓점 수를 텍스트로 표시
        cv2.putText(frame, f'Vertices: {obj["vertices"]}', (obj['x'], obj['y'] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 물체의 꼭짓점을 비교하고 거리가 30 픽셀 이내인 점들을 하나로 합칩니다.
    for obj in objects:
        vertices = obj['contour'].reshape(-1, 2)
        merged_vertices = []  # 합쳐진 꼭짓점을 저장할 리스트
        merged = set()  # 이미 합쳐진 꼭짓점을 추적하기 위한 집합

        for i, vertex1 in enumerate(vertices):
            if i not in merged:
                # 이미 합쳐진 꼭짓점이 아닌 경우
                merged_point = [vertex1]  # 초기에 현재 꼭짓점 자체를 추가

                for j, vertex2 in enumerate(vertices):
                    if j not in merged and i != j:
                        distance = calculate_distance(vertex1, vertex2)
                        if distance <= 30:
                            # 거리가 30 픽셀 이내인 경우, 합칩니다.
                            merged_point.append(vertex2)
                            merged.add(j)  # 합쳐진 꼭짓점으로 표시

                # 합쳐진 꼭짓점을 계산하여 저장
                merged_vertices.extend(merge_points(merged_point))

        # 합쳐진 꼭짓점 수를 텍스트로 표시
        cv2.putText(frame, f'Merged Vertices: {len(merged_vertices)}', (obj['x'], obj['y'] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 서로 접해 있는 꼭짓점들 중 y값이 300 픽셀 이내로 접해 있는지 확인
        for i, vertex1 in enumerate(merged_vertices):
            for j, vertex2 in enumerate(merged_vertices):
                if i != j and abs(vertex1[1] - vertex2[1]) <= 300:
                    # y값이 300 픽셀 이내로 접해 있다면, 두 점을 동일한 점으로 간주
                    merged_vertices[i] = merge_points([vertex1, vertex2])[0]
                    merged_vertices[j] = merged_vertices[i]  # 두 점을 같은 점으로 설정

    # 결과를 표시합니다.
    cv2.imshow('Video', frame)

    # 종료 키 (q)를 누르면 루프를 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 비디오 캡처를 해제하고 창을 닫습니다.
cap.release()
cv2.destroyAllWindows()
