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

class Findball:
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

            
