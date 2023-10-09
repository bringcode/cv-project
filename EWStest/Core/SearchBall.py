# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_BALL = auto() # 공 찾기
    FIND_OUTLIEN = auto() # 아웃라인 찾기
    FIND_FLAG = auto() # 깃발 찾기
    FIND_ARROW = auto() # 화살표 찾기
    EXIT = auto()  # 공통

class SearchBall:
    act: Act = Act.START
    robo: Robo = Robo()
    head_angle: int = 70
    ball: bool

    

    def init_robo(self, robo: Robo):
        self.robo = robo

    @classmethod # 공 찾는 코드
    def is_okay_ball(self):
        if self.ball == False:

            # 치고나서 90도 돌고 찾기 시작하는 코드인데, 밑에 있는게 90도로 돌지 아직 모름.
            self.robo._motion.grab_turn(Robo.dis_arrow, 60)
            time.sleep(2.5)
            self.robo._motion.grab_turn(Robo.dis_arrow, 60)
            time.sleep(2.5)

            # 치고 나서 공에 가까이 가고
            # if 홀컵이 보이면 공이랑 홀컵이랑 일직선으로 스고
                # if 화살표가 보이면 화살표로
                # elif 아웃라인으로 판단해서 치고
            # else 찾아야 한다는 값을 내보내고

    @classmethod
    def find_turn(self):

        # 180도 돈다고 가정 하고 나중에 수정
        for i in range(3):
            self.robo._motion.turn("RIGHT", 60)
            time.sleep(2.5)

        # 고개 우측 90도 회전 후 왼쪽으로 천천히 각도 변경하면서 찾기
        self.robo._motion.head_angle("RIGHT", 90) # 로봇 머리 각도 우로 90도 회전
        time.sleep(1)

        real_turn = []
        self.count = 0

        while self.ball != True:
            self.robo._motion.head_angle("LEFT", 10) # 로봇 머리 각도 좌로 10도씩 회전
            count += 1

        self.angle = 10 * count


        angles = [60, 20, 10]  # 가능한 회전 각도 리스트 (큰 값부터 순서대로)
        index = 0

        if self.angle > 90:
            which_turn = 'LEFT'
        else:
            which_turn = 'RIGHT'

        self.angle = abs(90-self.angle)

        while self.angle > 0:
            if self.angle < angles[index]:
                index += 1
                continue
            else:    
                self.robo._motion.turn(which_turn, angles[index])
                self.angle -= angles[index]

        print("공을 찾고 공 방향으로 돌았습니다.")