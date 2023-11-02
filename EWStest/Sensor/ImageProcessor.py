# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os
import time
import platform
# pip install imutils
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS

import warnings
warnings.simplefilter(
    action='ignore', category=FutureWarning)  # FutureWarning 제거

print('code: ImageProcessor.py - ## Debug')


if __name__ == "__main__":
    from EWStest.Sensor.ball_y_center import BallCenterMeasurer
    from outline import OutlineDetection

    

else:
    from EWStest.Sensor.ball_y_center import BallCenterMeasurer
    from outline import OutlineDetection
    

class ImageProccessor:
    def __init__(self, video: str = ""):
        print("init_imgprocessor")

        if video and os.path.exists(video):
            self._cam = FileVideoStream(path=video).start()
        else:
            print('# image processor #', platform.system())
            if platform.system() == "Linux":
                print('eee')
                self._cam = WebcamVideoStream(src=-1).start()
            else:
                self._cam = WebcamVideoStream(src=0).start()
            print('Acquire Camera ')

        self.fps = FPS()  # FPS
        print(self.fps)  # debuging: fps
        shape = (self.height, self.width, _) = self.get_img().shape
        print("Shape :: ", shape)  # debuging: image shape => height, width
        time.sleep(2)

    ########### 이미지 불러오기 ###########
    def get_img(self, show=False):
        img = self._cam.read()
        # 이미지를 받아오지 못하면 종료
        if img is None:
            exit()

        # 이미지를 받아오면 화면에 띄움
        if show:
            cv.imshow("imageProcessor-get_img", img)
            cv.waitKey(1)
        return img

    ########### 기본 공용 함수 ###########
    def blur(self, img, val):
        return cv.GaussianBlur(img, (val, val), 1)

    def light(self, img, val):  # 밝기
        arr = np.full(img.shape, (val, val, val), np.uint8)
        return cv.add(img, arr)

    def bright(self, img, alpha):  # 명도
        return np.clip((1+alpha)*img - 128*alpha, 0, 255).astype(np.uint8)

    def correction(self, img, val):
        img = self.blur(img, val)
        img = self.light(img, 0)
        img = self.bright(img, 0.0)
        return img

    def RGB2GRAY(self, img):
        return cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    def HSV2BGR(self, hsv):  # hsv 포맷 이미지를 파라미터로 받음
        return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    def hsv_mask(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)

        _, th_s = cv.threshold(s, 120, 255, cv.THRESH_BINARY)
        _, th_v = cv.threshold(v, 100, 255, cv.THRESH_BINARY_INV)

        th_mask = cv.bitwise_or(th_s, th_v)
        hsv = cv.bitwise_and(hsv, hsv, mask=th_mask)
        return hsv


    def get_s_mask(self, hsv, s_value):
        h, s, v = cv.split(hsv)
        ret_s, s_bin = cv.threshold(s, s_value, 255, cv.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        s_bin = self.mophorlogy(s_bin)
        return s_bin

    def get_v_mask(self, hsv, v_value):
        h, s, v = cv.split(hsv)
        ret_v, v_bin = cv.threshold(v, v_value, 255, cv.THRESH_BINARY)
        # morphology 연산으로 노이즈 제거
        v_bin = self.mophorlogy(v_bin)
        return v_bin

    def get_color_mask(self, hsv, const):
        lower_hue, upper_hue = np.array(const[0]), np.array(const[1])
        mask = cv.inRange(hsv, lower_hue, upper_hue)
        return mask

    #######################################

    ########### BALL CENTER DETECTION ###########
    # 공이 왼쪽에 있는지 가운데 있는지 오른쪾에 있는지 return 해줌

    def ball_location(self, show=False):
        img = self.get_img()

        
    