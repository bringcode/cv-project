import numpy as np
import cv2

class FlagyCenterMeasurer:
    def __init__(self, video_path=0, img_width = 800, img_height = 600):
        #self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        #if not self.cap.isOpened():
        #    raise ValueError(f"Video at {video_path} cannot be opened")
        img_width = img_width
        img_height= img_height
        self.green_boxes = []
        self.image_width_middle = img_width // 2
        self.image_height_middle = img_height //2
        self.farthest_flag_boxes = []  # 모든 flag의 중점값을 저장하는 리스트
    
    def judgeMiddle(self, max_x, min_x):
        l_dist = min_x  # l_dist: 공을 표시한 박스 가장 왼쪽으로부터 영상 가장 왼쪽 끝까지의 거리
        r_dist = self.img_width - max_x  # r_dist: 공을 표시한 박스 가장 오른쪽으로부터 영상 가장 오른쪽 끝까지의 거리
        
        error_range = 30 # 오차 허용 범위

        # 박스가 영상의 왼쪽 오른쪽 끝 부분과 떨어진 거리가 오차 허용 범위(error_range) 이내일 때, True를 is_Middle에 저장
        is_Middle = abs(r_dist - l_dist) < error_range

        if is_Middle == True:
            return 'C'
        else:
            if r_dist > l_dist:
                return 'D'
            else:
                return 'U'
            
    def run(self):
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab a frame")
                break

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # 녹색 범위 정의
            low_green = np.array([57, 78, 61])
            high_green = np.array([89, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
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
                    farthest_flag_center = min(flag_centers, key=lambda center: center[1])
                    # 해당 flag의 박스 그리기
                    cv2.rectangle(green_roi, (farthest_flag_center[0] - 10, farthest_flag_center[1] - 10),
                                  (farthest_flag_center[0] + 10, farthest_flag_center[1] + 10), (0, 0, 255), 2)
                    cv2.putText(frame, 'Farthest Flag', (x + farthest_flag_center[0], y + farthest_flag_center[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    # farthest_flag_boxes 리스트에 중점값과 "FLAG" 추가
                    self.farthest_flag_boxes.append((x + farthest_flag_center[0], y + farthest_flag_center[1], "FLAG"))

            # Display the original frame
            #cv2.imshow('Frame', frame)

       

        if self.farthest_flag_boxes:
                for box in self.farthest_flag_boxes:
                    print(f"Farthest Flag Center: {box[0]}, {box[1]}")

                for box in self.farthest_flag_boxes:
                    max_x, min_x, max_y, min_y = box[0], box[1], box[2], box[3]
                    if self.max_x is None or max_x > self.max_x:
                        self.max_x = max_x
                    if self.min_x is None or min_x < self.min_x:
                        self.min_x = min_x
                    if self.max_y is None or max_y > self.max_y:
                        self.max_y = max_y
                    if self.min_y is None or min_y < self.min_y:
                        self.min_y = min_y

        #self.cap.release()
        #cv2.destroyAllWindows()
        flag_x_isMiddle = self.judgeMiddle(max_y, min_y)
        return [flag_x_isMiddle]
if __name__ == "__main__":
    video_path = 0  # Use 0 for webcam
    shape_recognition = FlagyCenterMeasurer(video_path)
    shape_recognition.run()
