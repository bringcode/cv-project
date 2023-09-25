# -*- coding: utf-8 -*-
from Core.Robo import Robo
import Sensor.dist_measure_draft
import time


class Controller:
    # 10cm 앞으로 이동
    def walk_10cm():
        minus_10cm = Sensor.dist_measure_draft.dist - 10   # 처음 거리에서 10cm 빼기
        # time으로 몇초 이동하는지 확인하기

        if Sensor.dist_measure_draft.dist != minus_10cm:   # dist: 현재 인식되는 거리
            Robo._motion.walk_cm("FORWARD")

    # 30cm 앞으로 이동
    def walk_30cm():
        minus_30cm = Sensor.dist_measure_draft.dist - 30   # 처음 거리에서 30cm 빼기
        # time으로 몇초 이동하는지 확인하기
        
        if Sensor.dist_measure_draft.dist != minus_30cm:   # dist: 현재 인식되는 거리
            Robo._motion.motion.walk_cm("FORWARD")

    def walk_to_ball_and_flag(self):
        Robo._motion.basic()  # 초기 자세로 설정

        # 공 인식
        while True:
            if Sensor.dist_measure_draft.name == "ball":
                break
            else:
                Robo._motion.set_head("LEFT")  # 혹은 "RIGHT"
        
        # 공 쪽까지 걸어가기
        while True:
            if Sensor.dist_measure_draft.dist > 목표_거리:
                self.walk_10cm()  # 혹은 walk_30cm()
            else:
                break

        # 깃발, 홀컵 찾기
        while True:
            if Sensor.dist_measure_draft.name == "flag":
                break
            else:
                Robo._motion.set_head("LEFT")

        # 공이랑 일직선이 되게끔 각도 바꾸기
        while True:
            # 만약 머리 각도를 바꾸다가 공이랑 깃발이 일직선에 있을 경우 멈추기..
            if Robo._motion.set_head():
                if 'ball' != 'flag':
                    Robo._motion.turn("LEFT", 회전각도)
            else:
                break

        # 공 치기
        
        Robo._motion.basic()  # 초기 자세로 설정
