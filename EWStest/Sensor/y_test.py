# 공이 가운데, 왼쪽, 오른쪽 중 어디에 있는지 판별하는 코드 (isMiddle)

# -*- coding: utf-8 -*-
import numpy as np
import cv2

class FlagxCenterMeasurer:

    def __init__(self, img_width=800, img_height=600, width=4, focal=450):
        self.dist = 0 
        self.focal = focal
        self.pixels = 30
        self.width = width

        self.img_width = img_width
        self.img_height = img_height
        self.img_width_middle = img_width // 2
        self.img_height_middle = img_height // 2

        self.kernel = np.ones((3, 3), 'uint8')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (0, 20)
        self.fontScale = 0.6
        self.color = (0, 0, 255)
        self.thickness = 2

    # 대희 형이 처음에 만든 면적으로 거리구하는 코드
    # def get_dist(self, rectangle_params, image, name, isMiddle):
    #     pixels = rectangle_params[1][0]
    #     dist = (self.width * self.focal) / pixels

    #     if name == 'flag':
    #         image = cv2.putText(image, 'flag is_Middle : {}'.format(isMiddle), self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
    #     else:
    #         image = cv2.putText(image, 'ball is_Middle : {}'.format(isMiddle), self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
    #     # image = cv2.putText(image, title, self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
    #     # image = cv2.putText(image, str(dist), (110, 50), self.font, self.fontScale, self.color, 1, cv2.LINE_AA)

    #     return image

    def getMaxMin(self, flag):
        # 공에 박스 쳤을 때 왼쪽, 오른쪽 꼭짓점 좌표를 나타내는 변수(일단 최솟값은 최댓값으로 설정, 최댓값은 최솟값으로 설정)
        min_x, max_x = self.img_width, 0
        # 공에 박스 쳤을 때 아래, 위 꼭짓점 좌표(위와 같음)
        min_y, max_y = self.img_height, 0

        for x, y in flag:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        return max_x, min_x, max_y, min_y

    # 가운데인지 판단하는 코드
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
                return 'L'
            else:
                return 'R'


    def process(self):
        your_area_threshold = 300  # 사용자 정의 임계값, 필요에 따라 값을 조정하세요

        cap = cv2.VideoCapture('YYY.h264')  # 비디오 파일 경로를 설정하세요

# 초록 영역 박스의 정보를 저장할 리스트
        green_boxes = []
        farthest_flag_box = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

    # 영상을 HSV 색 공간으로 변환
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 녹색 범위 정의
            low_green = np.array([57, 95, 61])
            high_green = np.array([89, 255, 255])

    # 녹색 범위에 해당하는 부분을 추출
            green_mask = cv2.inRange(hsv_frame, low_green, high_green)

    # 추출된 녹색 부분을 원본 프레임에 표시
            result_frame = cv2.bitwise_and(frame, frame, mask=green_mask)

    # 녹색 영역의 윤곽선 찾기
            contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 초록 영역 박스 정보 업데이트
            green_boxes = [cv2.boundingRect(contour) for contour in contours]

    # 노랑색 범위 정의
            low_yellow = np.array([0, 57, 187])
            high_yellow = np.array([45, 234, 255])

    # 노랑색 범위에 해당하는 부분을 추출
            yellow_mask = cv2.inRange(hsv_frame, low_yellow, high_yellow)
            shape_info=[]
            shape_info_list = []

            for green_box in green_boxes:
                x, y, w, h = green_box
                yellow_roi = yellow_mask[y:y + h, x:x + w]

        # 초록 상자 내부의 노랑색 영역 처리
                _, labels, stats, _ = cv2.connectedComponentsWithStats(yellow_roi, connectivity=8)

                for i in range(1, len(stats)):
                    x_blob, y_blob, w_blob, h_blob, area_blob = stats[i]

            # 영역값이 100픽셀 이하인 영역을 제거
                    if area_blob <= 100:
                        continue

                    cv2.rectangle(frame, (x + x_blob, y + y_blob), (x + x_blob + w_blob, y + y_blob + h_blob), (0, 255, 0), 2)

            # Convert the yellow region into a binary image for contour detection
                    yellow_binary = np.zeros_like(yellow_roi)
                    yellow_binary[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob] = yellow_roi[y_blob:y_blob + h_blob, x_blob:x_blob + w_blob]

            # Find contours in the binary image
                    yellow_contours, _ = cv2.findContours(yellow_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    for contour in yellow_contours:
                # Approximate the contour to find the vertices
                        epsilon = 0.04 * cv2.arcLength(contour, True)
                        approx = cv2.approxPolyDP(contour, epsilon, True)
                        num_vertices = len(approx)

                # Display the shape as ARROW or FLAG based on the number of vertices
                        shape_text = "ARROW" if 7 <= num_vertices <= 8 else "FLAG"

                # Calculate the center of the yellow region
                        center_x = x + x_blob + w_blob // 2
                        center_y = y + y_blob + h_blob // 2
                        center = (center_x, center_y)

                # Add shape information to the list
                        shape_info_list.append((center, shape_text))

    # 사용자 정의 조건
            custom_condition = True

            if custom_condition:
        # FLAG로 인식된 박스의 개수가 2개 이상인 경우
                flag_boxes = [box for box in shape_info_list if box[1] == "FLAG"]
                if len(flag_boxes) >= 2:
            # 카메라 화면의 중하단 중앙 좌표
                    camera_center = (frame.shape[1] // 2, frame.shape[0])

            # Find the farthest FLAG box among FLAG boxes
                    max_distance = 0

                    for box in flag_boxes:
                        box_center = box[0]
                        distance = ((box_center[0] - camera_center[0]) ** 2 + (box_center[1] - camera_center[1]) ** 2) ** 0.5

                        if distance > max_distance:
                            max_distance = distance
                            farthest_flag_box = box

            # Change the rest of the FLAG boxes to ARROW
                    for i, box in enumerate(shape_info_list):
                        if box[1] == "FLAG" and box != farthest_flag_box:
                            shape_info_list[i] = (box[0], "ARROW")
                
    # Display centers and shape information on the frame
            for shape_info in shape_info_list:
                center, shape_text = shape_info[0], shape_info[1]
                offset = 10  # Offset to move the text upward
                if shape_text == "FLAG":
                    point_x = shape_info[0]
                    cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] - offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    print(point_x)
                else:
                    cv2.putText(frame, f'Shape: {shape_text}', (center[0], center[1] + offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the original frame
            cv2.imshow('Green and Yellow Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

# Release the video capture and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
                    
        



if __name__ == "__main__":
    distance_measurer = FlagxCenterMeasurer() # img_width=1280, img_height=720
    print(distance_measurer.process())
