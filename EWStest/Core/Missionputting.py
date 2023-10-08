# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_LINE = auto()

    ### danger ###
    # (예시)출
    SPEAK_DANGER = auto()
    DETECT_ALPHABET = auto()  # 방이름 감지
    DETECT_FIRST_MILKBOX_POS = auto()  # 장애물 초기 위치 찾기
    WALK_TO_MILKBOX = auto()  # 장애물 찾기
    OUT_OF_DANGER = auto()  # 위험지역 밖으로 장애물 옮기기
    REGRAB_MILKBOX = auto()  # 떨어진 장애물 다시 잡기 -> WALK_TO_MILKBOX로 충분할 것 같아서 일단 안씀
    SET_OUT_DIRECTION = auto()
    KICK_MILKBOX = auto()  # 자꾸 장애물을 떨어트릴 경우 이 방법 사용 (발로 차거나 치우기 동작 수행)
    BACK_TO_LINE = auto()
    EXIT = auto()  # 공통


class Missionputting:
    act: Act = Act.START
    robo: Robo = Robo()
    miss: int = 0
    limits: int = 5
    alphabet_color: str
    alphabet_name: str
    milkbox_pos: int
    head_angle: int = 70
    holding: bool
    first_milkbox_pos: int = cur.FIRST_MILKBOX_POS
    check_backline: int = 0
    out_direction: str # 위험지역 탈출 방향

    def init_robo(self, robo: Robo):
        self.robo = robo

    @classmethod
    def is_okay_grab_milkbox(self):
        print("여기부터 시작")