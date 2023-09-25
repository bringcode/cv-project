# -*- coding: utf-8 -*-
# from Sensor.ImageProcessor import ImageProccessor
# from Sensor.DataPath import DataPath
from Motion.motion import Motion
from Setting import Setting

print('code: Robo.py - ## Debug')


class Robo:
    arrow: str = "RIGHT"
    dis_arrow: str = "LEFT"
    # black_room_list = list = []
    # alphabet_color: str
    # box_pos: int = 4
    feet_down = 'LEFT_DOWN'
    # _image_processor = ImageProccessor(video="")  # Image Processor

    def __init__(self, vpath=''):
        self._motion = Motion()  # Motion