# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
#from Setting import cur
import time


class Act(Enum):
    START = auto()  # 공통
    FIND_BALL = auto() # 공 찾기
    FIND_OUTLIEN = auto() # 아웃라인 찾기
    FIND_FLAG = auto() # 깃발 찾기
    FIND_ARROW = auto() # 화살표 찾기
    EXIT = auto()  # 공통

class SearchFirst:
    act: Act = Act.START
    robo: Robo = Robo()
    angle: int = 100

    def init_robo(self, robo: Robo):
        self.robo = robo
        
    @classmethod # 공에 가까이 가서 치는 코드
    def is_okay_locat_ball(self):
        if self.ball == False:
            self.head_angle = 70
            # motion : 고개 각도 70도로 설정
            self.robo._motion.set_head("DOWN", 70)
            time.sleep(1)

            if self.ball == False:

                self.head_angle = 45
                # motion: 고개 각도 45도로 설정
                self.robo._motion.set_head("DOWN", 45)
                time.sleep(1)

                if self.ball == False:
                    self.head_angle = 30
                    # motion: 고개 각도 30도로 설정
                    self.robo._motion.set_head("DOWN",30)
                    time.sleep(1)

                else:
                    self.robo._motion.walk("FORWARD")
                    return True

            else:
                self.robo._motion.walk("FORWARD")
                time.sleep(1)

                if self.ball == False:
                    self.robo._motion.walk("FORWARD")
                    time.sleep(1)
                else:
                    self.robo._motion.walk("FORWARD")
                    return True


        else:
            return True      
        
        return False