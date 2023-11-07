import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []
        self.flags = []  # List to store recognized flags
        self.arrows = []  # List to store recognized arrows

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

        # For each green box, detect yellow shapes within it
        for green_box in self.green_boxes:
            x, y, w, h = green_box
            green_roi = frame[y:y+h, x:x+w]
            yellow_roi_mask = yellow_mask[y:y+h, x:x+w]
            yellow_contours, _ = cv2.findContours(yellow_roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            flag_detected = False  # Flag detection flag
            largest_shape_area = 0  # Area of the largest detected shape
            
            for cnt in yellow_contours:
                approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
                num_vertices = len(approx)
                area = cv2.contourArea(cnt)
                
                if num_vertices > 4:
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(green_roi, [box], 0, (0, 255, 0), 2)
                    M = cv2.moments(cnt)
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv2.putText(frame, f'SHAPE ({num_vertices})', (x+cx, y+cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        self.arrows.append((cx, cy, f'SHAPE ({num_vertices})'))
                        if area > largest_shape_area:
                            largest_shape_area = area
                            largest_shape = (cx, cy, f'SHAPE ({num_vertices})')
                else:
                    if not flag_detected:
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(green_roi, [box], 0, (0, 255, 0), 2)
                        M = cv2.moments(cnt)
                        if M['m00'] != 0:
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            cv2.putText(frame, 'FLAG', (x+cx, y+cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            self.flags.append((cx, cy, 'FLAG'))
                            flag_detected = True

            if flag_detected:
                self.flags = [largest_shape if f == largest_shape else f for f in self.flags]

        return frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab a frame")
                break

            frame = self.process_frame(frame)

            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
