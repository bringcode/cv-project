# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Core.Findballfirst import Findballfirst
from Core.Findball import Findball
from Core.Missionputting import Missionputting
from Core.Missionchecking import Missionchecking
from Setting import cur
import time

class Act(Enum):
    START = auto() # 시작
    SEARCH_FIRST = auto() # T샷 시작
    SEARCH_BALL = auto() # 공 찾기
    SEARCH_ARROW = auto() # 화살표 찾기
    SEARCH_FLAG = auto() # 깃발 찾기
    PUTTING = auto() # 공 퍼팅
    CHECK = auto() # 홀인 확인
    EXIT = auto() # 종료


# 상황 판단 하는 파트
class Controller:
    robo: Robo = Robo()
    act: Act = Act.START

    count_putting: int = 0 # 퍼팅 횟수
    check_holein: int = 0 # 홀인 판단 횟수
    area: str = "" # 현재 맵



    # Misson.py
    _first: Findballfirst = Findballfirst()
    _find: Findball = Findball()
    _check: Missionchecking = Missionchecking()
    _putt: Missionputting = Missionputting()

    # 처음 공이 어디에 있는지 확인하는 코드
    @classmethod
    def check_ball_first(self):
        time.sleep(1)
        
        # 이 부분에 첫 공을 찾는 부분을 넣어야하는게 맞는지?

    # 퍼팅 후 공이 나갔는지 확인하는 코드 (공을 발견하면 그 각도로 멈춤) (발견 못하면 나갔다고 판단)
    @classmethod
    def check_ball_out(self):
        time.sleep(1)

    # 퍼팅 후 공 위치가 위험한지 안 위험한지
    @classmethod
    def check_ball_location(self):
        time.sleep(1)

    # 홀인 했는지 안 했는지
    @classmethod
    def check_ball_in(self):
        time.sleep(1)


    
    