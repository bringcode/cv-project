# -*- coding: utf-8 -*-
# from Sensor.ImageProcessor import ImageProccessor
from Motion.Motion import Motion
from Setting import Setting
from Sensor.ball_y_center import BallyCenterMeasurer


print("code: Robo.py - ## Debug")


class Robo:
    arrow: str = "RIGHT"
    dis_arrow: str = "LEFT"
    black_room_list = list = []
    alphabet_color: str
    box_pos: int = 4
    feet_down = "LEFT_DOWN"
    # _image_processor = ImageProccessor(video="")  # Image Processor

    def __init__(self, vpath=""):
        # self._image_processor = ImageProccessor(video=vpath) # Image Processor
        self._motion = Motion()  # Motion
