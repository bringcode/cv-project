# 공이 가운데, 왼쪽, 오른쪽 중 어디에 있는지 판별하는 코드 (isMiddle)

# -*- coding: utf-8 -*-
import numpy as np
import cv2

class BallxCenterMeasurer:

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

    # 가운데인지 판단하는 코드
    def judgeMiddle(self, max_x, min_x):
        l_dist = min_x  # l_dist: 공을 표시한 박스 가장 왼쪽으로부터 영상 가장 왼쪽 끝까지의 거리
        r_dist = self.img_width - max_x  # r_dist: 공을 표시한 박스 가장 오른쪽으로부터 영상 가장 오른쪽 끝까지의 거리
        
        error_range = 20 # 오차 허용 범위

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
        cap = cv2.VideoCapture(0, cv2.CAP_V4L) # 인자로 있었는데 몰루? -> cv2.CAP_V4L 요건 로봇에서만 넣어야 함
        # cv2.namedWindow('Object Dist Measure ', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Object Dist Measure ', 700, 600)

        for _ in range(50):
            ret, img = cap.read()
            if not ret:
                break
            img = cv2.dilate(img, self.kernel, iterations=1)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            #window version
            # lower = np.array([170, 99, 100])
            # upper = np.array([180, 255, 255])
            # mask = cv2.inRange(hsv_img, lower, upper)
            # lower1 = np.array([1, 99, 100])
            # upper1 = np.array([5, 255, 255])
            # mask += cv2.inRange(hsv_img, lower1, upper1)

            # lower_flag = np.array([35, 130, 150])
            # upper_flag = np.array([45, 255, 255])
            # mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)

            #mac version
            # lower = np.array([170, 100, 100])
            # upper = np.array([180, 255, 255])
            # mask = cv2.inRange(hsv_img, lower, upper)

            # # robot version
            # 공 색상값
            lower = np.array([137, 0, 0])
            upper = np.array([255, 255, 255])
            
            # lower2 = np.array([168, 0, 0])
            # upper2 = np.array([255, 255, 255])
            
            mask1 = cv2.inRange(hsv_img, lower, upper)

            mask = mask1

            #모폴로지 연산
            d_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations = 5)
            
            cont,hei = cv2.findContours(d_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cont = sorted(cont, key = cv2.contourArea, reverse = True)[:1]

            max_x, min_x, max_y, min_y = -1, self.img_width + 1, -1, self.img_width + 1
            ball_box = None
            print('ball_x_center.py: 돌아가고있어')
            ball_x_isMiddle = 'N'
            ball_x = 'N'
            ball_y = 'N'
            
            for cnt in cont:
                if (cv2.contourArea(cnt)>10 and cv2.contourArea(cnt)<306000): # cv2.contourArea(cnt)>100 and

                    rect = cv2.minAreaRect(cnt)
                    ball_box = cv2.boxPoints(rect)
                    ball_box = np.int0(ball_box)
                    # print('points :', ball_box)
                    cv2.drawContours(img,[ball_box], -1,(255,0,0),3)

                    max_x, min_x, max_y, min_y = self.getMaxMin(ball_box)
                    ball_x_isMiddle = self.judgeMiddle(max_x, min_x)
                    ball_x = round((max_x + min_x)/2, 2)
                    ball_y = round((max_y + min_y / 2), 2)


            # cv2.imshow('Object Dist Measure ', img)
            # print(ball_x_isMiddle)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            #     cv2.destroyAllWindows()

                        
            if ball_x_isMiddle != 'N':
                # 10번 찾았을 때, 공이 잡혔을 때 이것을 실행. 첫번째 인자에 R,L,C 중 하나가 들어오고, 두번쩨부터 각각 공의 x중심좌표, y중심좌표임.
                return [ball_x_isMiddle, ball_x, ball_y]
        return [ball_x_isMiddle, ball_x, ball_y] # 10번 찾았는데도 아무것도 안 잡혔을 때, ['N', 'N', 'N']을 return.
        # 만약 퍼팅 지점을 예측하기 위해 실행시켰는데 ['N', 'N', 'N']이 뜨면 고개를 움직이면서 공을 찾고, 공을 찾으면
        # 일단 공과 로봇의 거리를 구한다. 이후 로봇이 홀컵으로부터 고개를 왼쪽으로 돌렸는지 오른쪽으로 돌렸는지를 파악해 다시 홀컵쪽으로
        # 고개를 조금씩 돌려 홀컵과 공 사이의 각도를 알아낸다.(근데 y값 차이가 많이 나면 공의 중심 맞추고, 홀컵으로 고개를 돌렸을 때, 홀컵이 안잡힐 수 있음 주의!)



if __name__ == "__main__":
    distance_measurer = BallxCenterMeasurer(img_width=640, img_height=480) # img_width=1280, img_height=720
    print(distance_measurer.process())
