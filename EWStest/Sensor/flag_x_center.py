import numpy as np
import cv2
# flag_x_isMiddle: 깃발이 중앙에 있는지 판단 출력값은 'C', 'L', 'R'로 나뉘어 리턴.
# farthest_flag_center[0]: 깃발 박스의 중점 x좌표,   farthest_flag_center[1]: 깃발 박스의 중점 y좌표
class FlagxCenterMeasurer:
    def __init__(self, video_path=0, img_width=640, img_height=480):
        # self.cap = cv2.VideoCapture(video_path, cv2.CAP_V4L)
        #if not self.cap.isOpened():
            #raise ValueError(f"비디오 {video_path}를 열 수 없습니다.")
        self.img_width = img_width
        self.img_height = img_height
        self.green_boxes = []
        self.max_x = None
        self.min_x = None
        self.max_y = None
        self.min_y = None
        self.farthest_flag_boxes = []

    def getMaxMin(self, box):
        # 공에 박스 쳤을 때 왼쪽, 오른쪽 꼭짓점 좌표를 나타내는 변수(일단 최솟값은 최댓값으로 설정, 최댓값은 최솟값으로 설정)
        min_x, max_x = self.img_width, 0
        # 공에 박스 쳤을 때 아래, 위 꼭짓점 좌표(위와 같음)
        min_y, max_y = self.img_height, 0

        for x, y in box:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        return max_x, min_x, max_y, min_y

    def judgeMiddle(self, max_x, min_x):
        
        l_dist = min_x
        r_dist = self.img_width - max_x
        error_range = 40

        is_Middle = abs(r_dist - l_dist) < error_range

        if is_Middle:
            return 'C'
        else:
            if r_dist > l_dist:
                return 'L'
            else:
                return 'R'

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임 캡처에 실패했습니다.")
                break
                
            have_flag = False # 화면에 flag가 있으면 True, 없으면 False
            farthest_flag_center = [0, 0] # 화면에 flag가 있으면 True, 없으면 False
            
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            low_green = np.array([38, 100, 61])
            high_green = np.array([86, 255, 255])
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.green_boxes = [cv2.boundingRect(contour) for contour in contours]

            low_yellow = np.array([0, 16, 144])
            high_yellow = np.array([43, 184, 255])
            yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
            max_x, min_x = 0,0 # 깃발을 못 찾았을 때 오류나는 것을 방지하기 위해 바운딩 박스의 좌표를 0으로 초기화

            for green_box in self.green_boxes:
                x, y, w, h = green_box
                green_roi = frame[y:y+h, x:x+w]
                yellow_roi_mask = yellow_mask[y:y+h, x:x+w]
                yellow_contours, _ = cv2.findContours(yellow_roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                flag_centers = []

                for cnt in yellow_contours:
                    area = cv2.contourArea(cnt)
                    if area > 10:
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        max_x, min_x, max_y, min_y = self.getMaxMin(box)
                        cv2.drawContours(green_roi, [box], 0, (0, 255, 0), 2)
                        M = cv2.moments(cnt)
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            cv2.putText(frame, 'Flag', (x+cx, y+cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            flag_centers.append((cx, cy))

                if flag_centers:
                    farthest_flag_center = min(flag_centers, key=lambda center: center[1])
                    cv2.rectangle(green_roi, (farthest_flag_center[0] - 10, farthest_flag_center[1] - 10),
                                  (farthest_flag_center[0] + 10, farthest_flag_center[1] + 10), (0, 0, 255), 2)
                    cv2.putText(frame, 'Farthest Flag', (x + farthest_flag_center[0], y + farthest_flag_center[1]),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    self.farthest_flag_boxes.append((x + farthest_flag_center[0], y + farthest_flag_center[1], "FLAG"))
                    have_flag = True
                    
            break
        #     cv2.imshow('프레임', frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # cv2.destroyAllWindows()

        # if self.farthest_flag_boxes:
        #     max_x, min_x, max_y, min_y = self.max_x, self.min_x, self.max_y, self.min_y

        flag_x_isMiddle = self.judgeMiddle(max_x, min_x)
        return [flag_x_isMiddle, farthest_flag_center[0], farthest_flag_center[1], have_flag]


if __name__ == "__main__":
    video_path = 0  # 웹캠을 사용하려면 0을 사용
    shape_recognition = FlagxCenterMeasurer(video_path, img_width=640, img_height=480)
    print(shape_recognition.run())
