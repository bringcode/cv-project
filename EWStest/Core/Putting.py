# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_LINE = auto()


    EXIT = auto()  # 공통


class Missionputting:
    act: Act = Act.START
    robo: Robo = Robo()
   

    def init_robo(self, robo: Robo):
        self.robo = robo

    @classmethod
    def is_okay_grab_milkbox(self):
        print("여기부터 시작")

        # if 오른쪽이면 왼쪾에서 칠 수 있게
        # elif 왼쪽이면 오른쪽에서 칠 수 있게
        # else 판단 불가 False