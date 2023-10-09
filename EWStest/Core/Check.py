# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
#from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_FLAG = auto()
    FIND_BALL = auto()
    FIND_OUTLINE = auto()
    DETECT_DIRECTION = auto()
    EXIT = auto()  # 공통


class Check:
    act: Act = Act.START
    robo: Robo = Robo()
    

    def init_robo(self, robo: Robo):
        self.robo = robo

    @classmethod
    def is_okay_hole_in(self):
        print()