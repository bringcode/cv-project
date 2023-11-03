# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Core.SearchFirst import SearchFirst
from Core.SearchBall import SearchBall
from Core.Putting import Putting
from Core.Check import Check
from Sensor.search_ball import FindBall
from Sensor.ball_y_center import BallyCenterMeasurer
from Sensor.ball_x_center import BallxCenterMeasurer

# from Setting import cur
import time


class Act(Enum):
    START = auto()  # 시작 - 아무도 동작도 안 함
    SEARCH_FIRST = auto()  # T샷 시작
    SEARCH_BALL = auto()  # 공 찾기
    SEARCH_FLAG = auto()  # 깃발 찾기
    SEARCH_ARROW = auto()  # 화살표 찾기
    SEARCH_BUNKER = auto()  # 벙커 찾기
    PUTTING = auto()  # 공 퍼팅
    CHECK = auto()  # 홀인 확인
    EXIT = auto()  # 종료


# 상황 판단 하는 파트
class Controller:
    robo: Robo = Robo()
    act: Act = Act.START

    count_putting: int = 0  # 퍼팅 횟수
    check_holein: int = 0  # 홀인 판단 횟수
    area: str = ""  # 현재 맵
    ball: bool

    # Misson.py
    _first: SearchFirst = SearchFirst()
    _find: SearchBall = SearchBall()
    _check: Check = Check()
    _putt: Putting = Putting()

    # 처음 공이 어디에 있는지 확인하는 코드
    @classmethod
    def check_ball_first(self):
        act = self.act
        time.sleep(3)
        dir = 100

        ballFunction = FindBall()  # Search_ball 함수
        is_ball_find = ballFunction.process()  # process 가져옴 True / False로 반환됨.

        for i in range(3):
            if is_ball_find == False:
                dir -= 10
                self.robo._motion.set_head("DOWN", dir)
                is_ball_find = ballFunction.process()
                time.sleep(3)
            elif is_ball_find == True:
                print("공을 찾았습니다.")
                break
            else:
                print("왼쪽 위치에 있지 않거나, 문제가 있을 수 있습니다.")
                print("로봇이 가운데 위치한다고 생각하고 시작하겠습니다.")

        if is_ball_find != True:
            self.robo._motion.set_head("RIGHT", 45)
            time.sleep(2)
            is_ball_find = ballFunction.process()
            if is_ball_find == True:
                print("Center: 공을 오른쪽에서 찾았습니다.")
            elif is_ball_find == False:
                print("가운데 오른쪽 X")
                self.robo._motion.set_head("LEFT", 45)
                time.sleep(2)
                is_ball_find = ballFunction.process()
                if is_ball_find == True:
                    print("Center: 공을 왼쪽에서 찾았습니다.")
                elif is_ball_find == False:
                    self.robo._motion.set_head("LEFTRIGHT_CENTER")
                    is_ball_find = ballFunction.process()
                    time.sleep(2)
                    if is_ball_find == True:
                        print("Center: 공을 가운데에서 찾았습니다.")
                    elif is_ball_find == False:
                        print("공을 처음 시작할 때 어디서도 찾지 못했습니다.")
                    else:
                        print("True False가 반환되지 않았습니다.")

        # 로봇이 왼쪽에서 시작한다고 생각하고 시작하는 부분

        # 고개 각도를 90도에서 50도로 변경하면서 공을 찾습니다.
        # for _ in range(3):
        #     print(self.ball)
        #     if self.ball == True:
        #         print("공을 찾았습니다.")
        #         break
        #     dir -= 10
        #     self.robo._motion.set_head("DOWN", dir)
        #     time.sleep(3)

        # 로봇이 가운데로 생각하고 시작하는 부분
        # dir = 50
        # self.robo._motion.set_head("DOWN", dir)

        # if not self.ball == True:
        #     time.sleep(3)
        #     # 오른쪽으로 시선 이동
        #     self.robo._motion.set_head("RIGHT", 45)
        #     time.sleep(3)
        #     if not self.ball == True:
        #         # 왼쪽으로 시선 이동
        #         self.robo._motion.set_head("LEFT", 45)
        #         time.sleep(3)

        # if self.ball == True:
        #     print("공을 찾았습니다.")
        # else:
        #     print("공을 찾지 못했습니다.")
        # 처음에는 공이 안 보임
        # 로봇이 왼쪽에 있다고 생각
        # 10도 내리면 왼쪽 기준으로 가장 먼 쪽을 봄
        # 다시 10도 내리면 가운데
        # 다시 10도 내리면 왼쪽

        # 이때 로봇이 공을 인식 못하면 로봇이 가운데 있다고 생각
        # 이제 10도를 더 내려서 가운데 확인
        # 오른쪽 확인
        # 왼쪽 확인

        # 이 부분에 첫 공을 찾는 부분을 넣어야하는게 맞는지?

    @classmethod
    def ball_feature_ball(self):
        print("Debug in ball_feature_ball")
        time.sleep(1)
        ball_feature = ["None", "None", "None"]  # [공의 가운데 여부, 공의 x중심좌표, 공의 y중심좌표]
        print("pass jun", ball_feature[0])
        # ball_ball_feature_measure 에서 return 값: L / C / R
        while ball_feature[0] != "C":
            cmeasurer = BallxCenterMeasurer()
            ball_feature = cmeasurer.process()
            print(ball_feature[0])

            if ball_feature[0] == "L":
                time.sleep(0.5)
                print("공이 왼쪽에 있습니다.")
                self.robo._motion.walk_side("LEFT")
                time.sleep(2)

            elif ball_feature[0] == "C":
                time.sleep(0.5)
                print("공이 가운데 있습니다.")
                break

            elif ball_feature[0] == "R":
                time.sleep(0.5)
                print("공이 오른쪽에 있습니다.")
                self.robo._motion.walk_side("RIGHT")
                time.sleep(2)
            else:
                time.sleep(0.5)
                print("원하는 값이 반환되지 않았습니다.")

    # 퍼팅 후 공이 나갔는지 확인하는 코드 (공을 발견하면 그 각도로 멈춤)
    @classmethod
    def check_ball_out(self):
        # 위험 지역에 공이 있으면 공이 나간 걸로 판단 -> 위험 지역을 판별할 cv 생각해야 함

        time.sleep(1)

    # 퍼팅 후 공 위치가 위험한지 안 위험한지
    @classmethod
    def check_ball_location(self):
        time.sleep(1)

        # 고려해야 할 점: 아웃라인을 넘어서 로봇이 서지 않게 해야 함.

        # 홀컵이 있을 때
        # if 홀컵의 오른쪽이면 공의 왼쪽에서 칠 수 있게 -> 홀컵을 인식하고, 홀컵 기준 오른쪽에서 왼쪽 방향으로 치기
        # elif 홀컵의 왼쪽이면 공의 오른쪽에서 칠 수 있게 -> 홀컵을 인식하고, 홀컵 기준 왼쪽에서 오른쪽 방향으로 치기
        # elif 홀선과 일직선이면 홀컵 쪽으로 치기
        # else 판단 불가 False

    # 홀인 했는지 안 했는지
    @classmethod
    def check_ball_in(self):
        time.sleep(1)

    @classmethod
    def go_robo(self):
        act = self.act
        robo: Robo = Robo()

        self.robo._motion.set_head("DOWN", 45)
        time.sleep(1)
        self.ball_feature_ball()
        time.sleep(2)

        self.act = act.START

        if act == act.START:
            print("ACT: ", act)  # Debug
            # print("current area: ", cur.AREA, "(Setting.py Hard Coding for Debuging)")
            # time.sleep(0.5)
            self.act = act.SEARCH_FIRST

        elif act == act.SEARCH_FIRST:
            print("ACT: ", act)  # Debug
            time.sleep(0.5)

            self.check_ball_first()
            self.act = act.SEARCH_BALL

        elif act == act.SEARCH_BALL:
            print("Act:", act)  # Debug
            time.sleep(0.5)

            self.ball_feature_ball()
            self.act = act.SEARCH_FLAG

        elif act == act.SEARCH_FLAG:
            print("Act:", act)  # Debug

            self.act = act.SEARCH_ARROW

        elif act == act.SEARCH_ARROW:
            print("Act:", act)  # Debug

            self.act = act.SEARCH_BUNKER

        elif act == act.SEARCH_BUNKER:
            print("Act:", act)  # Debug

            self.act = act.PUTTING

        elif act == act.PUTTING:
            print("Act:", act)  # Debug

            self.act = act.CHECK

        elif act == act.CHECK:
            print("Act:", act)  # Debug

            self.act = act.EXIT

        elif act == act.EXIT:
            print("Act:", act)  # Debug

        else:
            print("이쪽으로 빠지면 문제가 있는거임.")

        return False
