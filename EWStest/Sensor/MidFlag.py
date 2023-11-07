import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.flags = []  # List to store recognized flags
        self.arrows = []  # List to store recognized arrows

    def merge_contours(self, contours, threshold=10):
        if not contours:
            return []

        # 병합된 컨투어들의 목록을 초기화
        merged_contours = [contours[0]]
        for current_contour in contours[1:]:
            x, y, w, h = cv2.boundingRect(current_contour)
            # 현재 컨투어를 기존에 병합된 컨투어들과 비교
            for i in range(len(merged_contours)):
                merged_x, merged_y, merged_w, merged_h = cv2.boundingRect(merged_contours[i])
                # If current contour is close enough to merged one, merge them
                if (abs(merged_x - x) <= threshold and
                    abs(merged_y - y) <= threshold and
                    abs(merged_w - w) <= threshold and
                    abs(merged_h - h) <= threshold):
                    merged_contours[i] = np.vstack((merged_contours[i], current_contour))
                    break
            else:
                # If current contour didn't match any merged contour, add as new
                merged_contours.append(current_contour)

        return merged_contours

    def process_frame(self, frame):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Define color ranges
        low_yellow = np.array([22, 93, 0])
        high_yellow = np.array([45, 255, 255])
        yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
        # Find and merge yellow contours
        yellow_contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        merged_yellow_contours = self.merge_contours(yellow_contours)
        # Initialize variables to identify the highest flag
        min_flag_y = float('inf')
        highest_flag_contour = None
        # Check each yellow contour
        for contour in merged_yellow_contours:
            x, y, w, h = cv2.boundingRect(contour)
            if y < min_flag_y:
                min_flag_y = y
                highest_flag_contour = contour
        # Draw the highest flag and update arrow list
        for contour in merged_yellow_contours:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            M = cv2.moments(contour)
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x, y, w, h = cv2.boundingRect(contour)
                if contour is highest_flag_contour:
                    self.flags.append((x, y, w, h))  # Update to flag
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                    cv2.putText(frame, 'FLAG', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                else:
                    self.arrows.append((x, y, w, h))  # Assume it's an arrow
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                    cv2.putText(frame, 'ARROW', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
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
