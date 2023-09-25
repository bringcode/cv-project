# -*- coding: utf-8 -*-
import Motion.motion
import Sensor.dist_measure_draft
import time


class Controller:
    # 10cm 앞으로 이동
    def walk_10cm():
        minus_10cm = Sensor.dist_measure_draft.dist - 10   # 처음 거리에서 10cm 빼기
        # time으로 몇초 이동하는지 확인하기

        if Sensor.dist_measure_draft.dist != minus_10cm:   # dist: 현재 인식되는 거리
            Motion.motion.walk_cm("FORWARD")

    # 30cm 앞으로 이동
    def walk_30cm():
        minus_30cm = Sensor.dist_measure_draft.dist - 30   # 처음 거리에서 30cm 빼기
        # time으로 몇초 이동하는지 확인하기
        
        if Sensor.dist_measure_draft.dist != minus_30cm:   # dist: 현재 인식되는 거리
            Motion.motion.walk_cm("FORWARD")