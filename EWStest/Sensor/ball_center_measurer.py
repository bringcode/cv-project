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
        self.middle = img_width // 2

        self.kernel = np.ones((3, 3), 'uint8')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (0, 20)
        self.fontScale = 0.6
        self.color = (0, 0, 255)
        self.thickness = 2

    def get_dist(self, rectangle_params, image, name, isMiddle):
        pixels = rectangle_params[1][0]
        dist = (self.width * self.focal) / pixels

        if name == 'flag':
            image = cv2.putText(image, 'flag is_Middle : {}'.format(isMiddle), self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
        else:
            image = cv2.putText(image, 'ball is_Middle : {}'.format(isMiddle), self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
        # image = cv2.putText(image, title, self.org, self.font, 1, self.color, 2, cv2.LINE_AA)
        # image = cv2.putText(image, str(dist), (110, 50), self.font, self.fontScale, self.color, 1, cv2.LINE_AA)

        return image

    def getMaxMin(self, box):
        # 공에 박스 쳤을 때 왼쪽, 오른쪽 꼭짓점 좌표
        min_x, max_x = self.img_width, 0
        # 공에 박스 쳤을 때 아래, 위 꼭짓점 좌표
        min_y, max_y = self.img_width, 0

        for x, y in box:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        return max_x, min_x, max_y, min_y

    def judgeMiddle(self, max_x, min_x):
        l_dist = min_x
        r_dist = self.img_width - max_x
        error_range = 80

        is_Middle = abs(r_dist - l_dist) < error_range

        if is_Middle == True:
            return 'middle'
        else:
            if r_dist > l_dist:
                return 'left'
            else:
                return 'right'


    def process(self):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow('Object Dist Measure ', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object Dist Measure ', 700, 600)

        while True:
            ret, img = cap.read()
            img = cv2.dilate(img, self.kernel, iterations=1)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            #window version
            lower = np.array([170, 99, 100])
            upper = np.array([180, 255, 255])
            mask = cv2.inRange(hsv_img, lower, upper)
            lower1 = np.array([1, 99, 100])
            upper1 = np.array([5, 255, 255])
            mask += cv2.inRange(hsv_img, lower1, upper1)

            # lower_flag = np.array([35, 130, 150])
            # upper_flag = np.array([45, 255, 255])
            # mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)

            #mac version
            # lower = np.array([170, 100, 100])
            # upper = np.array([180, 255, 255])
            # mask = cv2.inRange(hsv_img, lower, upper)


            lower_flag = np.array([10, 150, 100])
            upper_flag = np.array([35, 255, 255])
            mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)


            #모폴로지 연산
            d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations = 5)
            f_img = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, self.kernel, iterations = 5)

            
            cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

            max_x, min_x, max_y, min_y = -1, self.img_width + 1, -1, self.img_width + 1
            ball_box = None
            
            for cnt in cont:
                if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

                    rect = cv2.minAreaRect(cnt)
                    ball_box = cv2.boxPoints(rect)
                    ball_box = np.int0(ball_box)
                    # print('points :', ball_box)
                    cv2.drawContours(img,[ball_box], -1,(255,0,0),3)

                    max_x, min_x, max_y, min_y = self.getMaxMin(ball_box)
                    isMiddle = self.judgeMiddle(max_x, min_x)
                    img = self.get_dist(rect,img, 'ball', isMiddle)

            cont2,hei2 = cv2.findContours(f_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cont2 = sorted(cont2, key = cv2.contourArea, reverse = True)[:1]

            f_max_x, f_min_x, f_max_y, f_min_y = -1, self.img_width + 1, -1, self.img_width + 1
            for cnt in cont2:
                if (cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<306000):

                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    print('points :', box)
                    cv2.drawContours(img,[box], -1,(255,0,0),3)

                    f_max_x, f_min_x, f_max_y, f_min_y = self.getMaxMin(box)
                    isMiddle = self.judgeMiddle(f_max_x, f_min_x, )
                    
                    img = self.get_dist(rect,img, 'flag', isMiddle)
                        
                        
            if ball_box is not None and all(f_max_x > x > f_min_x and f_max_y > y > f_min_y for x, y in ball_box):
                    cv2.circle(img, (100,200), 20, cv2.FILLED, cv2.LINE_AA)


            cv2.imshow('Object Dist Measure ', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    distance_measurer = BallCenterMeasurer(img_width=1280, img_height=720)
    distance_measurer.process()