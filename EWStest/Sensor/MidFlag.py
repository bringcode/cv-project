import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []

    def process_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 녹색 범위 정의
        low_green = np.array([57, 78, 61])
        high_green = np.array([89, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        result_frame = cv2.bitwise_and(frame, frame, mask=green_mask)
        contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.green_boxes = [cv2.boundingRect(contour) for contour in contours]

        # 노랑색 범위 정의
        low_yellow = np.array([0, 16, 144])
        high_yellow = np.array([43, 184, 255])
        yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)

        farthest_flag_center = None  # 가장 먼 flag의 중점값을 저장하는 변수

        for green_box in self.green_boxes:
            x, y, w, h = green_box
            green_roi = frame[y:y+h, x:x+w]
            yellow_roi_mask = yellow_mask[y:y+h, x:x+w]
            yellow_contours, _ = cv2.findContours(yellow_roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # flag의 중점값을 저장하는 리스트
            flag_centers = []

            for cnt in yellow_contours:
                # 영역의 면적 계산
                area = cv2.contourArea(cnt)
                if area > 10:  # 일정 면적 이상의 영역만 처리
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(green_roi, [box], 0, (0, 255, 0), 2)
                    M = cv2.moments(cnt)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        cv2.putText(frame, 'Flag', (x+cx, y+cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                        # flag_centers 리스트에 중점값 추가
                        flag_centers.append((cx, cy))

            # flag_centers가 비어있지 않을 때만 실행
            if flag_centers:
                # flag_centers 리스트에서 중점값이 가장 높은 flag 선택
                farthest_flag_center_candidate = max(flag_centers, key=lambda center: center[1])

                # 최초로 찾은 flag 또는 더 멀리에 있는 flag 선택
                if farthest_flag_center is None or farthest_flag_center_candidate[1] > farthest_flag_center[1]:
                    farthest_flag_center = farthest_flag_center_candidate

        return frame, farthest_flag_center

    def run(self):
        farthest_flag_center = None

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab a frame")
                break

            frame, farthest_flag_center = self.process_frame(frame)

            # Display the original frame
            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        return farthest_flag_center

if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    farthest_flag_center = shape_recognition.run()
    if farthest_flag_center:
        print(f"Farthest Flag Center: {farthest_flag_center}")
