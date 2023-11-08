import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []

    def find_highest_box(self, boxes):
        # 중점 y 좌표를 기준으로 가장 높은 위치의 박스를 찾습니다.
        if not boxes:
            return None

        highest_box = min(boxes, key=lambda box: box[1])
        return highest_box

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

        for green_box in self.green_boxes:
            x, y, w, h = green_box
            green_roi = frame[y:y+h, x:x+w]
            yellow_roi_mask = yellow_mask[y:y+h, x:x+w]
            yellow_contours, _ = cv2.findContours(yellow_roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
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

            # 가장 높은 위치의 박스를 찾습니다.
            target_box = self.find_highest_box(self.green_boxes)

            if target_box is not None:
                # 타겟 박스를 빨강색으로 표시
                x, y, w, h = target_box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, 'Target', (x + w // 2, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

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

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
