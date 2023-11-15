# 공이 X축 기준으로 가운데 있을 때 true, 아니면 false

# -*- coding: utf-8 -*-
import numpy as np
import cv2


class BallCenterMeasurer:
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

        error_range = self.img_height // 8  # 오차 허용 범위

        # 박스가 영상의 왼쪽 오른쪽 끝 부분과 떨어진 거리가 오차 허용 범위(error_range) 이내일 때, True를 is_Middle에 저장
        is_Middle = abs(up_dist - down_dist) < error_range
        return is_Middle

    def process(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)  # 인자로 있었는데 몰루? -> cv2.CAP_V4L
        # cv2.namedWindow('Object Dist Measure ', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Object Dist Measure ', 700, 600)

        while True:
            ret, img = cap.read()
            if not ret:
                print("영상정보를 가져올 수 없습니다.")
                break
            img = cv2.dilate(img, self.kernel, iterations=1)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # robot version
            lower = np.array([137, 0, 0])
            upper = np.array([255, 255, 255])
            lower1 = np.array([0, 66, 87])
            upper1 = np.array([14, 255, 255])
            # lower2 = np.array([168, 0, 0])
            # upper2 = np.array([255, 255, 255])
            
            mask1 = cv2.inRange(hsv_img, lower, upper)
            mask2 = cv2.inRange(hsv_img, lower1, upper1)
            # mask3 = cv2.inRange(hsv_img, lower2, upper2)

            mask = mask1+mask2

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

            for cnt in cont:
                if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 306000:
                    rect = cv2.minAreaRect(cnt)
                    ball_box = cv2.boxPoints(rect)
                    ball_box = np.int0(ball_box)
                    # print('points :', ball_box)
                    cv2.drawContours(img, [ball_box], -1, (255, 0, 0), 3)

                    max_x, min_x, max_y, min_y = self.getMaxMin(ball_box)
                    ball_y_isMiddle = self.judgeMiddle(max_y, min_y)
                    return (
                        ball_y_isMiddle  # imshow 하려함 => 위에 있는 주석을 활성화하고, return은 주석처리
                    )
            return False

            # imshow
            font = cv2.FONT_HERSHEY_SIMPLEX
            org = (0, 20)
            fontScale = 0.6
            color = (0, 0, 255)
            thickness = 2

            image = cv2.putText(
                img,
                "flag Middle : {}".format(ball_y_isMiddle),
                org,
                font,
                1,
                color,
                2,
                cv2.LINE_AA,
            )

        #     cv2.imshow("Object Dist Measure ", img)


        #     if cv2.waitKey(1) & 0xFF == ord("q"):
        #         break

        # cv2.destroyAllWindows()




if __name__ == "__main__":
    distance_measurer = BallCenterMeasurer()
    print(distance_measurer.process())
