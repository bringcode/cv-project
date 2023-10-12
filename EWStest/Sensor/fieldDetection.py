import cv2
import numpy as np

class FieldDetection:

    def __init__(self, video_path, scale_percent=65):
        self.cap = cv2.VideoCapture(video_path)
        self.scale_percent = scale_percent

    def process_frame(self, frame):
        # 영상 resize
        width = int(frame.shape[1] * self.scale_percent / 100)
        height = int(frame.shape[0] * self.scale_percent / 100)
        dim = (width, height)
        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        
        hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
        
        # 경기장 색인식 범위 지정
        lower_green = np.array([40, 100, 40])
        upper_green = np.array([80, 255, 255])
        
        # 경기장 mask
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 제일 큰 컨투어가 경기장이라고 인식
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(resized_frame, [largest_contour], -1, (0, 255, 0), 2)

        return resized_frame

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)
            
            cv2.imshow("Processed Frame", processed_frame)

            if cv2.waitKey(30) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = FieldDetection("flagONLY.h264")
    detector.run()
