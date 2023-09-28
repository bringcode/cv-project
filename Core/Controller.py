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

    def location(self):
        time.sleep(1)
        self.ball = Sensor.findball.ball 
        self.dir = 90

        # 로봇이 왼쪽에서 시작한다고 생각하고 시작하는 부분
        self.robo._motion.set_head("DOWN", self.dir)
        
        # 고개 각도를 90도에서 50도로 변경하면서 공을 찾습니다.
        for _ in range(4):
            if self.ball:
                break
            self.dir -= 10
            self.robo._motion.set_head("DOWN", self.dir)

        # 로봇이 가운데로 생각하고 시작하는 부분
        self.dir = 50
        self.robo._motion.set_head("DOWN", self.dir)
        
        if not self.ball:
            # 오른쪽으로 시선 이동
            self.robo._motion.set_head("RIGHT", 10)
            if not self.ball:
                # 왼쪽으로 시선 이동
                self.robo._motion.set_head("LEFT", 20)

        if self.ball:
            print("공을 찾았습니다.")
        else:
            print("공을 찾지 못했습니다.")



    def walk_to_ball_and_flag(self):
        Robo._motion.basic()  # 초기 자세로 설정

        # 공 인식
        while True:
            if Sensor.dist_measure_draft.name == 'ball':
                break
            else:
                head_turn = 10   # 초기 회전
                Robo._motion.set_head("LEFT", head_turn)
                time.sleep(1)
                Robo._motion.set_head("RIGHT", head_turn)
                time.sleep(1)
                head_turn += 10   # 10도씩 더 회전하게끔..
        
        # 공 쪽까지 걸어가기
        while True:
            if Sensor.dist_measure_draft.dist <= 목표_거리:
                self.walk()
            else:
                break

        # 깃발, 홀컵 찾기
        while True:
            if Sensor.dist_measure_draft.name == "flag":
                break
            else:
                head_turn = 10   # 초기 회전
                Robo._motion.set_head("LEFT", head_turn)
                time.sleep(1)
                Robo._motion.set_head("RIGHT", head_turn)
                time.sleep(1)
                head_turn += 10   # 10도씩 더 회전하게끔..

        # 공이랑 일직선이 되게끔 각도 바꾸기
        while True:
            # 공이랑 깃발이 일직선이 아니면 계속 턴하면서 찾기
            if 'ball' == 'flag':   # 일직선이 되면 멈추고 공 차기
                break
            else:
                body_turn = 10
                Robo._motion.turn("LEFT", body_turn)
                time.sleep(1)
                Robo._motion.turn("RIGHT", body_turn)
                time.sleep(1)
                body_turn += 10

        # 공 치기
        
        Robo._motion.basic()  # 초기 자세로 설정
