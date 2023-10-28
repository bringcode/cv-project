# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
import time


class Act(Enum):
    START = auto()  # 공통
    EXIT = auto()  # 공통

class SearchBunker:
    act: Act = Act.START
    robo: Robo = Robo()
    angle: int = 100

    def init_robo(self, robo: Robo):
        self.robo = robo
        
    @classmethod
    def is_okay_locat_ball(self):
        time.sleep(1)