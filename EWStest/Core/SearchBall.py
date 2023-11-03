# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo

# from Setting import cur
import time
from Sensor.ball_y_center import BallyCenterMeasurer

# from Sensor.dist_measure import
import Motion.Motion


class Act(Enum):
    START = auto()  # 공통
    FIND_BALL = auto()  # 공 찾기
    FIND_OUTLIEN = auto()  # 아웃라인 찾기
    FIND_FLAG = auto()  # 깃발 찾기
    FIND_ARROW = auto()  # 화살표 찾기
    EXIT = auto()  # 공통


class SearchBall:
    act: Act = Act.START
    robo: Robo = Robo()
    head_angle: int = 70
    ball: bool

    def init_robo(self, robo: Robo):
        self.robo = robo

    # @classmethod # 공 찾는 코드
    # def is_okay_ball(self):   # 공이 이미 시야에 있다는 전제 하
    #     if 홀컵:
    #         # 1. (홀컵, 공) 홀컵이랑 공이 이미 일직선
    #         while 1:
    #             self.walk("FORWARD", 1, 0.1, True)
    #             if Sensor.dist_measure.distReal == 일정거리:   # 공이랑 일정 거리가 되면 자리에서 멈추고, 홀컵으로 목표 설정
    #                 self.find_hole()
    #                 break

    #         # 2. (홀컵, 공) 홀컵이랑 공이 일직선이 아니면 공이랑 일직선에 서서 공 쪽으로 가게끔
    #         while 1:
    #             if self.isMiddle == 'middle':  # 공이 가운데면
    #                 self.walk("FORWARD", 1, 0.1, True)  # 그쪽으로 걸어가기
    #                 if Sensor.dist_measure.distReal == 일정거리:   # 공이랑 일정 거리가 되면 자리에서 멈추고, 홀컵으로 목표 설정
    #                     self.find_hole()
    #                     break
    #             elif self.isMiddle == 'right':  # 공이 오른쪽에 있으면
    #                 Robo._motion.motion.set_head("RIGHT", 10)   # 공이 센터에 오게끔 오른쪽으로 10도씩 고개 돌리기 -> 공이 시야 가운데에 오면 그에 맞춰 몸 돌리기
    #             else:   # 공이 왼쪽에 있으면
    #                 Robo._motion.motion.set_head("LEFT", 10)   # 공이 센터에 오게끔 왼쪽으로 10도씩 고개 돌리기 -> 공이 시야 가운데에 오면 그에 맞춰 몸 돌리기

    #     # 3. (공) 홀컵이 안 보일 때
    #     elif 홀컵 == False:
    #         if self.arrow:
    #             # 화살표가 가리키는 쪽으로 치기
    #             pass
    #         elif self.contour:
    #             # 컨투어 라인 안으로 치기
    #             pass

    #     # 4. 공도 안 보일 때
    #     else:
    #         self.find_turn()

    # @classmethod   # 홀컵으로 목표 설정
    # def find_hole(self):
    #     while 1:
    #         if 어떤 기준을 만족하면..홀컵 찾기를 끝내지..:
    #             self.is_okay_ball()   # 1번으로 가서 공을 치게끔
    #             break
    #         elif 오른쪽에 홀컵 존재:   # 홀컵이 가운데보다 오른쪽에 있으면
    #             Robo._motion.motion.walk_side("LEFT")   # 왼쪽으로 옆이동
    #         else:   # 홀컵이 가운데보다 왼쪽에 있으면
    #             Robo._motion.motion.walk_side("RIGHT")   # 오른쪽으로 옆이동

    # @classmethod
    # def find_turn(self):

    #     # 180도 돈다고 가정 하고 나중에 수정
    #     for i in range(3):
    #         self.robo._motion.turn("RIGHT", 60)
    #         time.sleep(2.5)

    #     # 고개 우측 90도 회전 후 왼쪽으로 천천히 각도 변경하면서 찾기
    #     self.robo._motion.head_angle("RIGHT", 90) # 로봇 머리 각도 우로 90도 회전
    #     time.sleep(1)

    #     real_turn = []
    #     self.count = 0

    #     while self.ball != True:
    #         self.robo._motion.head_angle("LEFT", 10) # 로봇 머리 각도 좌로 10도씩 회전
    #         count += 1

    #     self.angle = 10 * count

    #     angles = [60, 20, 10]  # 가능한 회전 각도 리스트 (큰 값부터 순서대로)
    #     index = 0

    #     if self.angle > 90:
    #         which_turn = 'LEFT'
    #     else:
    #         which_turn = 'RIGHT'

    #     self.angle = abs(90-self.angle)

    #     while self.angle > 0:
    #         if self.angle < angles[index]:
    #             index += 1
    #             continue
    #         else:
    #             self.robo._motion.turn(which_turn, angles[index])
    #             self.angle -= angles[index]

    #     print("공을 찾고 공 방향으로 돌았습니다.")

    #     # ball_center_measurer.ball_isMiddle의 값을 얻기 위해 실행을 해줘야 함.
    #     distance_measurer = BallCenterMeasurer()
    #     distance_measurer.process()

    #     # 공이 정확하게 공이랑 일직선으로 되어 있는지 판단하는 부분 (일단 값을 10으로 넣긴 했는데 정확한 값을 찾아야 할 듯)
    #     if Sensor.ball_center_measurer.ball_isMiddle == "right": # 오른쪽
    #         self.robo._motion.turn("RIGHT", 10)

    #     elif Sensor.ball_center_measurer.ball_isMiddle == "middle": #가운데
    #         pass

    #     else: # 왼쪽
    #         self.robo._motion.turn("LEFT", 10)
