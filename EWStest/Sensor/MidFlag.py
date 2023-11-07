import numpy as np
import cv2

class ShapeInfo:
    def __init__(self, center, shape):
        self.center = center
        self.shape = shape

class MidFlag:
    def __init__(self, video_path, area_threshold):
        self.video_path = video_path
        self.area_threshold = area_threshold
        self.farthest_flag_center = None

    def process(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)

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

            # 녹색 영역의 윤곽선 찾기
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 초록 영역 박스 정보 업데이트
            green_boxes = [cv2.boundingRect(contour) for contour in contours]

            # 노랑색 범위 정의
            low_yellow = np.array([0, 57, 187])
            high_yellow = np.array([45, 234, 255])

            # 노랑색 범위에 해당하는 부분을 추출
            yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

            shape_info_list = []

            for green_box in green_boxes:
                x, y, w, h = green_box
                yellow_roi = yellow_mask[y:y + h, x:x + w]

                # 초록 상자 내부의 노랑색 영역 처리
                _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_roi, connectivity=8)

                for i in range(1, len(stats)):
                    x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]
                    if area_blob > self.area_threshold:
                        cv2.rectangle(frame, (x + x_blob, y + y_blob), (x + x_blob + w_blob, y + y_blob + h_blob), (0, 255, 0), 2)

                        yellow_binary = np.zeros_like(yellow_roi)
                        yellow_binary[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob] = yellow_roi[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob]

                        yellow_contours, _ = cv2.findContours(yellow_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        for contour in yellow_contours:
                            epsilon = 0.04 * cv2.arcLength(contour, True)
                            approx = cv2.approxPolyDP(contour, epsilon, True)
                            num_vertices = len(approx)
                            shape_text = "ARROW" if 7 <= num_vertices <= 8 else "FLAG"

                            center_x = x + x_blob + w_blob // 2
                            center_y = y + y_blob + h_blob // 2
                            center = (center_x, center_y)

                            shape_info = ShapeInfo(center, shape_text)
                            shape_info_list.append(shape_info)

            custom_condition = True

            if custom_condition:
                flag_boxes = [box for box in shape_info_list if box.shape == "FLAG"]
                if len(flag_boxes) >= 2:
                    camera_center = (frame.shape[1] // 2, frame.shape[0])
                    max_distance = 0

                    for box in flag_boxes:
                        box_center = box.center
                        distance = ((box_center[0] - camera_center[0]) ** 2 + (box_center[1] - camera_center[1]) ** 2) ** 0.5

                        if distance > max_distance:
                            max_distance = distance
                            self.farthest_flag_center = box.center

                    for box in flag_boxes:
                        if box.center != self.farthest_flag_center:
                            box.shape = "ARROW"

            for shape_info in shape_info_list:
                center, shape_text = shape_info.center, shape_info.shape
                cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Green and Yellow Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return self.farthest_flag_center

if __name__ == "__main__":
    processor = MidFlag(0, 300)  # 비디오 파일 경로를 지정
    farthest_flag_center = processor.process()
    print(f"Farthest FLAG Center: {farthest_flag_center}")
