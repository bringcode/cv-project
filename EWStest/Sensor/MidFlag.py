import numpy as np
import cv2

class ShapeRecognition:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Video at {video_path} cannot be opened")
        self.flags = []  # List to store recognized flags
        self.arrows = []  # List to store recognized arrows

    def merge_contours(self, contours):
        # 병합된 컨투어들의 목록을 초기화
        merged_contours = []
        while contours:
            # 첫 컨투어를 병합 목록에 넣고 제거
            merge = [contours.pop(0)]
            # 병합 대상 컨투어의 경계 상자를 계산
            x, y, w, h = cv2.boundingRect(merge[0])
            # 나머지 컨투어들을 순회하면서 병합 여부 확인
            for contour in contours:
                ox, oy, ow, oh = cv2.boundingRect(contour)
                # 컨투어가 인접해 있는지 확인
                if (x < ox + ow and x + w > ox and y < oy + oh and y + h > oy):
                    merge.append(contour)
            # 병합할 컨투어들을 모두 제거
            for m in merge:
                if m in contours:
                    contours.remove(m)
            # 병합된 컨투어를 계산
            merged_contour = np.vstack(merge)
            merged_contours.append(merged_contour)
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
        # Initialize variables to identify the largest flag
        max_flag_area = 0
        largest_flag_contour = None
        # Check each yellow contour
        for contour in merged_yellow_contours:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            M = cv2.moments(contour)
            if M['m00'] != 0:
                area = cv2.contourArea(contour)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                # Identify if this is the largest flag
                if area > max_flag_area:
                    max_flag_area = area
                    largest_flag_contour = contour
                self.arrows.append((cx, cy))  # Assume it's an arrow for now
        # Draw the largest flag and update arrow list
        for contour in merged_yellow_contours:
            if contour is largest_flag_contour:
                self.flags.append(cv2.boundingRect(contour))  # Update to flag
                self.arrows.remove(cv2.boundingRect(contour))  # Remove from arrows
                cv2.drawContours(frame, [contour], 0, (0, 0, 255), 2)
                cv2.putText(frame, 'FLAG', cv2.boundingRect(contour)[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)
                cv2.putText(frame, 'ARROW', cv2.boundingRect(contour)[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
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
