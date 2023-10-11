# 맵의 끝선을 검출

# -*- coding: utf-8 -*-
import cv2
import numpy as np

class OutlineDetection:

    def __init__(self, video_path, scale_percent=65):
        self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        self.scale_percent = scale_percent

    @staticmethod
    def detect_corners(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        dst = cv2.dilate(dst, None, iterations=6)
        image[dst > 0.01 * dst.max()] = [0, 0, 255]
        return image

    @staticmethod
    def detect_yellow_corners(image, hsv):
        yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([35, 240, 255]))
        yellow_part = cv2.bitwise_and(image, image, mask=yellow_mask)
        yellow_corners = OutlineDetection.detect_corners(yellow_part)
        image[yellow_corners[:, :, 2] == 255] = [0, 255, 0]
        return image

    def process_frame(self, frame):
        width = int(frame.shape[1] * self.scale_percent / 100)
        height = int(frame.shape[0] * self.scale_percent / 100)
        dim = (width, height)
        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

        hsv = cv2.cvtColor(cv2.GaussianBlur(resized_frame, (3, 3), 1), cv2.COLOR_BGR2HSV)
        kernel = np.ones((15, 15), np.uint8)
        masked_frame = cv2.morphologyEx(resized_frame, cv2.MORPH_CLOSE, kernel)
        masked_frame = cv2.GaussianBlur(masked_frame, (1, 1), 3)

        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    
        # Ball Detection
        mask_ball = cv2.inRange(hsv, np.array([0, 150, 120]), np.array([10, 255, 255]))
        mask_ball += cv2.inRange(hsv, np.array([170, 150, 120]), np.array([180, 255, 255]))

        contours_ball, _ = cv2.findContours(mask_ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours_ball) > 0:
            c = max(contours_ball, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 5:
                cv2.circle(resized_frame, (int(x), int(y)), int(radius), (0, 0, 255), 5)

        # Inline and Outline Detection
        # inline_mask = cv2.inRange(hsv, np.array([70, 105, 75]), np.array([120, 230, 200]))
        # yellow_mask = cv2.inRange(hsv, np.array([20, 50, 100]), np.array([35, 240, 255]))
        # inline_mask += yellow_mask
        outline_mask = cv2.inRange(hsv, np.array([40, 120, 45]), np.array([67, 250, 200]))
        
        # mask = inline_mask + outline_mask
        mask = outline_mask
        
        contours_outline, _ = cv2.findContours(outline_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for c in contours_outline:
            if cv2.contourArea(c) > 300:
                cv2.drawContours(resized_frame, [c], -1, (255, 0, 0), 2)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.putText(resized_frame, "outline", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return masked_frame, resized_frame

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            masked_frame, resized_frame = self.process_frame(frame)
            
            cv2.imshow("MaskedFrame", masked_frame)
            cv2.imshow("ResizedFrame", resized_frame)

            if cv2.waitKey(30) == 27:
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = OutlineDetection("first.h264")
    detector.run()