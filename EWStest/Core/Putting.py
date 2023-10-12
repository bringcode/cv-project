# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
#from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_LINE = auto()


    EXIT = auto()  # 공통


class Putting:
    act: Act = Act.START
    robo: Robo = Robo()
   

    def init_robo(self, robo: Robo):
        self.robo = robo

    @classmethod
    def is_okay_grab_milkbox(self):
        pass

    # 우선순위를 홀컵, 화살표 순으로 설정
    # if 홀컵이 있다면 Controller의 check_ball_location에서 정보를 받아서 치기
    # elif 홀컵이 없고 화살표가 있으면, 화살표가 가르키는 쪽으로 치기 (여기서 구현)
    # else 홀컵이나 화살표가 다 없으면, 아웃라인을 기준으로 양쪽을 확인하고 치기