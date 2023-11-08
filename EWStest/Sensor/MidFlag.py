import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []
        self.farthest_flag_box = None  # 가장 높은 flag의 중점값을 저장할 변수

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

        # 가장 높은 flag의 Y 좌표 초기화
        max_flag_y = -1

        for green_box in self.green_boxes:
            x, y, w, h = green_box
            green_roi = frame[y:y+h, x:x+w]
            yellow_roi_mask = yellow_mask[y:y+h, x:x+w]
            yellow_contours, _ = cv2.findContours(yellow_roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in yellow_contours:
                M = cv2.moments(cnt)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    # 현재 flag의 중점값 중 Y 좌표가 가장 높은 flag를 찾음
                    if cy < max_flag_y or max_flag_y == -1:
                        max_flag_y = cy
                        self.farthest_flag_box = (x + cx, y + cy, "FLAG")
                        
                    if cy != max_flag_y:
                        # 현재 flag가 가장 높은 flag가 아닌 경우, 해당 flag에 대한 텍스트 제거
                        cv2.putText(frame, '', (x + cx, y + cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    else:
                        cv2.putText(frame, 'Flag', (x + cx, y + cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab a frame")
                break

            frame = self.process_frame(frame)

            # Display the original frame
            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        if self.farthest_flag_box is not None:
            print(f"Farthest Flag Center: {self.farthest_flag_box[0]}, {self.farthest_flag_box[1]}")

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
