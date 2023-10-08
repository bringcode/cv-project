# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
import Core.Findballfirst import Findballfirst
import Core.Findball import Findball
import Core.Missionputting import Missionputting
import Core.Missionchecking import Missionchecking
from Setting import cur
import time

class Act(Enum):
    START = auto()
    SEARCH_FIRST = auto()
    SEARCH_ARROW = auto()
    SEARCH_FLAG = auto()
    EXIT = auto()


class Controller:

    robo: Robo = Robo()
    act: Act = Act.START
    count_putting: int = 0
    check_holein: int = 0
    area: str = "" # 현재 맵



    # Misson.py
    _first: Findballfirst = Findballfirst()
    _find: Findball = Findball()
    _check: Missionchecking = Missionchecking()
    _putt: Missionputting = Missionputting()




    
    