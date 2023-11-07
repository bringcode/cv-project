import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path,cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.green_boxes = []  # List to store bounding boxes of green areas
        self.flags = []  # List to store recognized flags
        self.arrows = []  # List to store recognized arrows

    def process_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define green range
        low_green = np.array([50, 100, 100])
        high_green = np.array([70, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        # Find green contours
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.green_boxes = [cv2.boundingRect(contour) for contour in green_contours]

        # Define yellow range
        low_yellow = np.array([22, 93, 0])
        high_yellow = np.array([45, 255, 255])

        for green_box in self.green_boxes:
            x, y, w, h = green_box
            green_roi = frame[y:y+h, x:x+w]
            hsv_roi = hsv_frame[y:y+h, x:x+w]
            yellow_mask = cv2.inRange(hsv_roi, low_yellow, high_yellow)
            yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            min_y = float('inf')
            flag_contour = None
            for contour in yellow_contours:
                _, cy, _, _ = cv2.boundingRect(contour)
                if cy < min_y:
                    min_y = cy
                    flag_contour = contour

            for contour in yellow_contours:
                if contour is flag_contour:
                    self.flags.append(cv2.boundingRect(contour))
                    cv2.drawContours(green_roi, [contour], 0, (0, 0, 255), 2)
                    cv2.putText(frame, 'FLAG', (x, y + min_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.arrows.append(cv2.boundingRect(contour))
                    cv2.drawContours(green_roi, [contour], 0, (0, 255, 0), 2)
                    cx, cy, _, _ = cv2.boundingRect(contour)
                    cv2.putText(frame, 'ARROW', (x + cx, y + cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

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

if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = ShapeRecognition(video_path)
    shape_recognition.run()
