# 공이 가운데, 위, 아래 중 어디에 있는지 판별하는 코드 (isMiddle)

# -*- coding: utf-8 -*-
import numpy as np
import cv2


class BallyCenterMeasurer:
    def __init__(self, img_width=640, img_height=480, width=4, focal=450):
        self.dist = 0
        self.focal = focal
        self.pixels = 30
        self.width = width

        self.img_width = img_width
        self.img_height = img_height
        self.img_width_middle = img_width // 2
        self.img_height_middle = img_height // 2

        self.kernel = np.ones((3, 3), "uint8")
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

    def getMaxMin(self, box):
        # 공에 박스 쳤을 때 왼쪽, 오른쪽 꼭짓점 좌표를 나타내는 변수(일단 최솟값은 최댓값으로 설정, 최댓값은 최솟값으로 설정)
        min_x, max_x = self.img_height, 0
        # 공에 박스 쳤을 때 아래, 위 꼭짓점 좌표(위와 같음)
        min_y, max_y = self.img_height, 0

        for x, y in box:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        return max_x, min_x, max_y, min_y

    # 가운데인지 판단하는 코드
    def judgeMiddle(self, max_y, min_y):
        up_dist = min_y  # l_dist: 공을 표시한 박스 가장 왼쪽으로부터 영상 가장 왼쪽 끝까지의 거리
        down_dist = (
            self.img_height - max_y
        )  # r_dist: 공을 표시한 박스 가장 오른쪽으로부터 영상 가장 오른쪽 끝까지의 거리

        error_range = 30  # 오차 허용 범위

        # 박스가 영상의 왼쪽 오른쪽 끝 부분과 떨어진 거리가 오차 허용 범위(error_range) 이내일 때, True를 is_Middle에 저장
        is_Middle = abs(up_dist - down_dist) < error_range
        print("ball_y_center.py: pass")

        if is_Middle == True:
            return "C"
        else:
            if up_dist > down_dist:
                return "D"
            else:
                return "U"

    def process(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)  # 인자로 있었는데 몰루? -> cv2.CAP_V4L
        # cv2.namedWindow('Object Dist Measure ', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Object Dist Measure ', 700, 600)

        for _ in range(10):
            ret, img = cap.read()
            if not ret:
                print("영상정보를 가져올 수 없습니다.")
                break
            img = cv2.dilate(img, self.kernel, iterations=1)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # window version
            # lower = np.array([170, 99, 100])
            # upper = np.array([180, 255, 255])
            # mask = cv2.inRange(hsv_img, lower, upper)
            # lower1 = np.array([1, 99, 100])
            # upper1 = np.array([5, 255, 255])
            # mask += cv2.inRange(hsv_img, lower1, upper1)

            # lower_flag = np.array([35, 130, 150])
            # upper_flag = np.array([45, 255, 255])
            # mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)

            # mac version
            # lower = np.array([170, 100, 100])
            # upper = np.array([180, 255, 255])

            # robot version
            lower = np.array([137, 0, 0])
            upper = np.array([255, 255, 255])
            mask = cv2.inRange(hsv_img, lower, upper)

            # lower_flag = np.array([10, 150, 100])
            # upper_flag = np.array([35, 255, 255])
            # mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)

            # 모폴로지 연산
            d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations=5)

            cont, hei = cv2.findContours(
                d_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            cont = sorted(cont, key=cv2.contourArea, reverse=True)[:1]

            max_x, min_x, max_y, min_y = -1, self.img_width + 1, -1, self.img_width + 1
            ball_box = None
            ball_y_isMiddle = 'N'

            for cnt in cont:
                if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 306000:
                    rect = cv2.minAreaRect(cnt)
                    ball_box = cv2.boxPoints(rect)
                    ball_box = np.int0(ball_box)
                    # print('points :', ball_box)
                    cv2.drawContours(img, [ball_box], -1, (255, 0, 0), 3)

                    max_x, min_x, max_y, min_y = self.getMaxMin(ball_box)
                    ball_y_isMiddle = self.judgeMiddle(max_y, min_y)
                    print(ball_y_isMiddle)

                    #cv2.imshow('Object Dist Measure ', img)
                    #if cv2.waitKey(1) & 0xFF == ord('q'):
                         #break

                    #cv2.destroyAllWindows()

                    return [ball_y_isMiddle]
            
            if ball_y_isMiddle != 'N':
                return [ball_y_isMiddle] # 공이 잡힌 경우, R, L, C 중 하나를 return.
        return [ball_y_isMiddle] # 10번 찾아봤는데 공이 검출되지 않는다면, ['N']이 return.



if __name__ == "__main__":
    distance_measurer = BallyCenterMeasurer()
    print(distance_measurer.process())
