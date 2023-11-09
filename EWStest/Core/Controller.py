# -*- coding: utf-8 -*-
from enum import Enum, auto
from Core.Robo import Robo
from Sensor.search_ball import FindBall # 
from Sensor.ball_y_center import BallyCenterMeasurer #
from Sensor.ball_x_center import BallxCenterMeasurer #
from Sensor.tan_dist_measure import DistMeasurer #
from Sensor.t_put_judge import BallCenterMeasurer #
from Sensor.t_put_x_judge import Tputting_x_BallCenterMeasurer #
from Sensor.flag_x_center import FlagxCenterMeasurer #
from Sensor.flag_y_center import FlagyCenterMeasurer #

# from Setting import cur
import time


class Act(Enum):
    START = auto()  # 시작 - 아무도 동작도 안 함
    SEARCH_FIRST = auto()  # T샷 시작
    SEARCH_BALL = auto()  # 공 찾기
    SEARCH_FLAG = auto()  # 깃발 찾기
    SEARCH_PUTTING_LOCATION = auto()  # 치는 위치 찾기
    CHECK = auto()  # 홀인 확인
    EXIT = auto()  # 종료


# 상황 판단 하는 파트
class Controller:
    robo: Robo = Robo()
    act: Act = Act.START # 순서도 시작

    count_putting: int = 0  # 퍼팅 횟수
    check_holein: int = 0  # 홀인 판단 횟수
    area: str = ""  # 현재 맵
    ball: bool # 공 T/F 

    # T샷할 때 사용하는 위치 파악하는 변수 위치가 파악되면 그 위치의 변수가 1이 된다.
    L_right: int = 0  # 로봇: L / 공: right
    L_center: int = 0  # 로봇: L / 공: center
    L_left: int = 0  # 로봇: L / 공: left
    C_right: int = 0  # 로봇: C / 공: right
    C_center: int = 0 # 로봇: C / 공: center
    C_left: int = 0 # 로봇: C / 공: left

    canPutting: float = 0.0 # 칠 수 있는 거리있는지 판단 변수 (길이)

    # 처음 공이 어디에 있는지 확인하는 코드
    @classmethod
    def check_ball_first(self):
        L_right = self.L_right # 로봇: L / 공: right
        L_center = self.L_center # 로봇: L / 공: center
        L_left = self.L_left # 로봇: L / 공: left
        C_right = self.C_right # 로봇: C / 공: right
        C_center = self.C_center # 로봇: C / 공: center
        C_left = self.C_left # 로봇: C / 공: left
        
        #  .process():  공에 유무를 반환함 T/F
        dir_list = [45, 60, 80, 90] # 임의로 지정한 로봇 머리 값
        dir = 3 # dir_list 에서 90을 고를 수 있도록 설정하는 값
        cnt = 0 # 로봇이 어디에서 찾았는지 구분하는 변수

        time.sleep(1) # 함수를 실행할 때 오류가 안 나도록 하는 time.sleep



        for i in range(3): # 왼쪽 경우의 숫 3개
            self.robo._motion.set_head("DOWN", dir_list[dir]) # 왼쪽에 있을 떄 사용하는 로봇 각도 값 모션
            dir -= 1 # 각도 임의값 변경
            time.sleep(0.1) 
            Tput_center_isFind_Big = BallCenterMeasurer().process() 
            print("Ball find and center T/F: ",Tput_center_isFind_Big)  #공 T/F값 출력

            if Tput_center_isFind_Big == False: # 발견되지 않았을 때
                cnt += 1

            elif Tput_center_isFind_Big == True: # 발견됐을 때
                print("공을 찾았습니다.")
                if cnt == 0:
                    self.L_right = 1
                elif cnt == 1:
                    self.L_center = 1
                elif cnt == 2:
                    self.L_left = 1
                break

            else: # 이 부분은 삭제 해도 될 것 같긴함.

                print("왼쪽 위치에 있지 않거나, 문제가 있을 수 있습니다.")
                print("로봇이 가운데 위치한다고 생각하고 시작하겠습니다.")
                cnt += 1

        cnt += 1
        dir = 0
        self.robo._motion.set_head("DOWN", dir_list[dir])

        if Tput_center_isFind_Big == False:
            print("가운데에 있다고 생각하겠습니다.")
            Tput_center_isFind_Big = BallCenterMeasurer().process()
            print("Ball find and center T/F: ",Tput_center_isFind_Big) 

            # 이 부분이 필요없을 것 같음.
            # Tput_center_isFind_Small = Tputting_x_BallCenterMeasurer(img_width=640, img_height=480).process() 
            # print("Tput_x_center: ",Tput_center_isFind_Small) 
            # time.sleep(0.1) 

            if Tput_center_isFind_Big == True: # fix
                print("Center: 공을 가운데에서 찾았습니다.")

                if cnt == 3:
                    self.C_center = 1

            else:
                print("가운데 가운데 X")
                self.robo._motion.set_head("LEFT", 54)
                time.sleep(0.1)
                Tput_center_isFind_Big = BallCenterMeasurer().process()
                time.sleep(0.1)
                Tput_center_isFind_Small = Tputting_x_BallCenterMeasurer(img_width=640, img_height=480).process()
                time.sleep(0.1)
                cnt += 1

                print("Tput_isFind: ", Tput_center_isFind_Big)
                print("Tput_center: ", Tput_center_isFind_Small)
                if Tput_center_isFind_Small == True:
                    print("Center: 공을 왼쪽에서 찾았습니다.")
                    if cnt == 4:
                        self.C_left = 1

                else:
                    print("가운데 왼쪽 X")
                    self.robo._motion.set_head("RIGHT", 54)
                    time.sleep(0.1)
                    Tput_center_isFind_Big = BallCenterMeasurer().process()
                    time.sleep(0.1)
                    Tput_center_isFind_Small = Tputting_x_BallCenterMeasurer(img_width=640, img_height=480).process()
                    time.sleep(0.1)
                    cnt += 1

                    print("Tput_isFind: ", Tput_center_isFind_Big)
                    print("Tput_center: ", Tput_center_isFind_Small)
                    if Tput_center_isFind_Small == True:
                        print("Center: 공을 오른쪽에서 찾았습니다.")
                        if cnt == 5:
                            self.C_right = 1

                    else:
                        print("공을 처음 시작할 때 어디서도 찾지 못했습니다.")


    # 공이 가운데 있는지 확인해서 로봇 왼쪽 오른쪽 모션
    @classmethod
    def ball_feature_ball(self):
        print("Debug in ball_feature_ball")
        ball_is_x_center = ["N", "N", "N"] # fix
        # [공의 가운데 여부, 공의 x중심좌표, 공의 y중심좌표]
        
        # ball_ball_feature_measure 에서 return 값: L / C / R
        while ball_is_x_center[0] != "C":
            ball_is_x_center = BallxCenterMeasurer().process()
            print("카메라 기준(공): ",ball_is_x_center[0]) # 카메라 기준(공): L or C or R

            if ball_is_x_center[0] == "L":
                print("공이 왼쪽에 있습니다.")
                self.robo._motion.walk_side("LEFT")
                time.sleep(0.5)

            elif ball_is_x_center[0] == "C":
                print("공이 가운데 있습니다.")
                break

            elif ball_is_x_center[0] == "R":
                print("공이 오른쪽에 있습니다.")
                self.robo._motion.walk_side("RIGHT")
                time.sleep(0.5)
            else:
                print("원하는 값이 반환되지 않았습니다.")


    # 퍼팅 후 공 위치 찾기 -
    @classmethod
    def check_ball_location(self):
        print("Debug check_ball_location in Controller")
        time.sleep(0.1)

        # 구간을 나눠서 찾는다고 생각
        short_left_location = 0 # 짧은 거리 왼쪽
        short_right_location = 0 # 짧은 거리 오른쪽
        short_forward_location = 0 # 짧은 거리 정면
        long_forward_location = 0 # 긴 거리 정면
        long_left_location = 0 # 긴 거리 왼쪽
        long_right_location = 0 # 긴 거리 오른쪽

        exist_ball = FindBall().process() # 공 찾은 값 True/False
        print("공을 찾았습니다 (T/F): ",exist_ball)

        if exist_ball == True: 
            print("공이 화면에 보입니다.")
            print("공이 안 쳐진듯..")

        elif exist_ball == False:
            print("공을 찾지 못했습니다.")
            short_forward_location = 1
            if short_forward_location == 1:
                self.robo._motion.turn("LEFT", 45)
                time.sleep(0.8)
                self.robo._motion.turn("LEFT", 45)
                time.sleep(0.8)
                self.robo._motion.set_head("DOWN", 45)
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 short_forward_location에서 찾았습니다.")

                else:
                    short_left_location = 1

            if short_left_location == 1:
                print("짧은 왼쪽에 있다고 생각")

                self.robo._motion.set_head("LEFT", 45)
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 short_left_location에서 찾았습니다.")

                else:
                    short_right_location = 1

            if short_right_location == 1:
                print("짧은 오른쪽에 있다고 생각")

                self.robo._motion.set_head("RIGHT", 45)
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 short_right_location에서 찾았습니다.")

                else:
                    long_right_location = 1

            if long_right_location == 1:
                print("긴 오른쪽에 있다고 생각")

                self.robo._motion.set_head("DOWN", 80)
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 long_right_location에서 찾았습니다.")

                else:
                    long_forward_location = 1

            if long_forward_location == 1:
                print("긴 가운데에 있다고 생각")

                self.robo._motion.set_head("LEFTRIGHT_CENTER")
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 long_forward_location에서 찾았습니다.")

                else:
                    long_left_location = 1

            if long_left_location == 1:
                print("긴 왼쪽에 있다고 생각")

                self.robo._motion.set_head("LEFT", 45)
                time.sleep(0.1)

                exist_ball = FindBall().process()
                print(exist_ball)

                if exist_ball == True:
                    print("공을 long_left_location에서 찾았습니다.")

                else:
                    print("어라 어딨지..?")

        else:
            print("원하는 값이 반환되지 않았습니다.")

    # 공 1도씩 조정하면서 각도 확인
    @classmethod
    def check_ball_distance(self):
        print("Debug in check_ball_distance")

        correctAngle = 0  # 공이 센터에 왔을 때 1로 변경

        # 공을 못 찾았을 때 반환하는 값
        ball_x_angle = ["N", "N", "N"]
        ball_y_angle = ["N"]

        while correctAngle != 1:
            ballxcenter = BallxCenterMeasurer(img_width=640, img_height=480)
            ball_x_angle = ballxcenter.process()
            time.sleep(0.2)
            print("ball_x_angle: ", end="")
            print(ball_x_angle[0])

            if ball_x_angle[0] == "C":
                # x축 기준으로 센터라면, y축 기준으로 어디에 있는지 판별
                ballycenter = BallyCenterMeasurer(img_width=640, img_height=480)
                ball_y_angle = ballycenter.process()
                time.sleep(0.2)
                if ball_y_angle[0] == "C":
                    print("ball_x_angle: ", ball_x_angle[0])
                    print("ball_y_angle: ", ball_y_angle[0])
                    print("중앙에 왔습니다.")
                    correctAngle = 1
                    break

                elif ball_y_angle[0] == "D" or ball_y_angle[0] == "U":
                    # 아래로 1도씩 움직이기
                    while ball_y_angle[0] != "C":
                        ballycenter = BallyCenterMeasurer(img_width=640, img_height=480)
                        ball_y_angle = ballycenter.process()
                        time.sleep(0.2)
                        print("ball_y: ", ball_y_angle[0])

                        if ball_y_angle[0] == "U":
                            self.robo._motion.set_head_small("UP", 1)
                            time.sleep(0.1)

                        if ball_y_angle[0] == "D":
                            self.robo._motion.set_head_small("DOWN", 1)
                            time.sleep(0.1)

                    correctAngle = 1
                    print("중앙에 왔습니다.")
                    break

                else:
                    print("check_ball_distance 함수에서 원하는 Y angle이 안 들어옴.")

            elif ball_x_angle[0] == "L" or ball_x_angle[0] == "R":
                # 왼쪽으로 1도씩 움직이기
                while ball_x_angle[0] != "C":
                    ballxcenter = BallxCenterMeasurer(img_width=640, img_height=480)
                    ball_x_angle = ballxcenter.process()
                    time.sleep(0.2)
                    print("ball_x: ", ball_x_angle[0])

                    if ball_x_angle[0] == "L":
                        self.robo._motion.set_head_small("LEFT", 1)
                        time.sleep(0.1)
                    if ball_x_angle[0] == "R":
                        self.robo._motion.set_head_small("RIGHT", 1)
                        time.sleep(0.1)

            else:
                print("check_ball_distance 함수에서 원하는 X angle이 안 들어옴.")

    # 깃발 1도씩 조정하면서 각도 확인
    @classmethod
    def check_flag_distance(self):
        print("Debug in check_flag_distance")

        flagxcenter = FlagxCenterMeasurer(img_width=640, img_height=480)
        flagycneter = FlagyCenterMeasurer(img_width=640, img_height=480)

        correctAngle = 0  # 공이 센터에 왔을 때 1로 변경

        # 깃발을 못 찾았을 때 반환하는 값

        while correctAngle != 1:
            flag_x_angle = flagxcenter.run()
            time.sleep(0.2)
            print("flag_x_angle: ", end="")
            print(flag_x_angle[0])
            print(flag_x_angle[0] == "C")

            if flag_x_angle[0] == "C":
                print("통과했어요")
                flag_y_angle = flagycneter.run()
                print(flag_y_angle[0])
                time.sleep(0.2)

                if flag_y_angle[0] == "C":
                    print("flag_x_angle: ", flag_x_angle[0])
                    print("flag_y_angle: ", flag_y_angle[0])
                    print("중앙에 있습니다.")
                    correctAngle = 1
                    break

                elif flag_y_angle[0] == "D" or flag_y_angle[0] == "U":
                    while flag_y_angle[0] != "C":
                        flag_y_angle = flagycneter.run()
                        time.sleep(0.2)
                        print("flag_y: ", flag_y_angle[0])

                        if flag_y_angle[0] == "U":
                            self.robo._motion.set_head_small("UP", 1)
                            time.sleep(0.1)

                        if flag_y_angle[0] == "D":
                            self.robo._motion.set_head_small("DOWN", 1)
                            time.sleep(0.1)

                    correctAngle = 1
                    print("중앙에 왔습니다.")
                    break

                else:
                    print("check_flag_distance 함수에서 원하는 Y angle이 안 들어왔습니다.")

            elif flag_x_angle[0] == "L" or flag_x_angle[0] == "R":
                print("flag_x_angle: R or L이 들어왔습니다.")
                print(flag_x_angle[0])

                while flag_x_angle[0] != "C":
                    print("while문이 실행되었습니다.")
                    flag_x_angle = flagxcenter.run()
                    time.sleep(0.2)
                    print("flag_x: ", flag_x_angle[0])

                    if flag_x_angle[0] == "L":
                        self.robo._motion.set_head_small("LEFT", 1)
                        time.sleep(0.1)
                    if flag_x_angle[0] == "R":
                        self.robo._motion.set_head_small("RIGHT", 1)
                        time.sleep(0.1)
            else:
                print("flag_ball_distance 함수에서 원하는 X angle이 안 들어옴.")

    # 걸어갈 때, 틀어질 경우를 대비해서 다시 위치 잡는 함수
    @classmethod
    def correct_position(self):
        # 공을 못 찾았을 때 반환하는 값
        ball_x_angle = ["N", "N", "N"]

        xTput_x_center = BallxCenterMeasurer(img_width=640, img_height=480)
        ball_x_angle = xTput_x_center.process()

        # 걸어가면서 틀어진 각도 맞추는 로직
        while ball_x_angle[0] != "C":
            print("걸어가면서 틀어진 각도 맞추기")

        while ball_x_angle[0] != "C":
            if ball_x_angle[0] == "L" or ball_x_angle[0] == "R":
                if ball_x_angle[0] == "L":
                    self.robo._motion.set_head_small("LEFT", 1)
                    time.sleep(0.1)

                if ball_x_angle[0] == "R":
                    self.robo._motion.set_head_small("RIGHT", 1)
                    time.sleep(0.1)

        # 현재 머리 각도가 플러스면 오른쪽으로 턴해야 함
        while self.robo._motion.x_head_angle > 0:
            self.robo._motion.x_head_angle = head_plus(60)
            self.robo._motion.x_head_angle = head_plus(45)
            self.robo._motion.x_head_angle = head_plus(20)
            self.robo._motion.x_head_angle = head_plus(10)
            self.robo._motion.x_head_angle = head_plus(5)
            self.robo._motion.x_head_angle = head_plus(3)
            self.robo._motion.x_head_angle = 0

        # 현재 머리 각도가 마이너스면 왼쪽으로 턴해야 함
        while self.robo._motion.x_head_angle < 0:
            self.robo._motion.x_head_angle = head_minus(60)
            self.robo._motion.x_head_angle = head_minus(45)
            self.robo._motion.x_head_angle = head_minus(20)
            self.robo._motion.x_head_angle = head_minus(10)
            self.robo._motion.x_head_angle = head_minus(5)
            self.robo._motion.x_head_angle = head_minus(3)
            self.robo._motion.x_head_angle = 0

        # 오른쪽으로 턴
        def head_plus(self, N):
            x_head_angle_n = self.robo._motion.x_head_angle // N
            if x_head_angle_n >= 1:
                for _ in range(x_head_angle_n):
                    self.robo._mothon.turn("RIGHT", N)
                    self.robo._motion.x_head_angle -= N
            elif x_head_angle_n == 0:
                return self.robo._motion.x_head_angle
            else:
                print("여기로 오면 안 되는뎁..")
            return self.robo._motion.x_head_angle

        # 왼쪽으로 턴
        def head_minus(self, N):
            x_head_angle_n = self.robo._motion.x_head_angle // -N
            if x_head_angle_n >= 1:
                for _ in range(x_head_angle_n):
                    self.robo._mothon.turn("LEFT", N)
                    self.robo._motion.x_head_angle += N
            elif x_head_angle_n == 0:
                return self.robo._motion.x_head_angle
            else:
                print("여기로 오면 안 되는뎁..")
            return self.robo._motion.x_head_angle

    @classmethod
    def go_robo(self):
        act = self.act
        robo: Robo = Robo()
        L_right = self.L_right
        L_center = self.L_center
        L_left = self.L_left
        C_right = self.C_right
        C_center = self.C_center
        C_left = self.C_left

        canPutting = self.canPutting

        # self.robo._motion.set_head("DOWN", 90)  # test
        # time.sleep(0.5)  # test

        # self.robo._motion.hit_the_ball("RIGHT")
        # time.sleep(5)
        # self.robo._motion.hit_the_ball("LEFT")
        self.check_flag_distance()  # test
        time.sleep(0.2)
        angle = abs(self.robo._motion.y_head_angle - 20)  # test
        dist_flag = DistMeasurer()  # test
        print(dist_flag.display_distance(angle))  # test
        time.sleep(0.2)  # test

        # self.robo._motion.set_head("DOWN",30) # test
        # time.sleep(0.2) # test
        self.check_ball_distance()  # test

        angle = abs(self.robo._motion.y_head_angle - 20)  # test
        dist_ball = DistMeasurer()  # test
        print(dist_ball.display_distance(angle))  # test

        print("11111")  # test
        time.sleep(10)  # test

        if act == act.START:
            print("ACT: ", act)  # Debug
            self.act = act.SEARCH_FIRST

        elif act == act.SEARCH_FIRST:
            print("ACT: ", act)  # Debug
            time.sleep(0.5)

            self.check_ball_first()

            if self.L_right == 1:
                self.robo._motion.walk("FORWARD", 10, 1.0)
                time.sleep(0.1)

                self.ball_feature_ball()
                time.sleep(0.1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")
                    self.robo._motion.hit_the_ball("RIGHT")
                    time.sleep(0.1)

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 L_right 오류")

            elif self.L_center == 1:
                self.robo._motion.walk("FORWARD", 5, 1.0)
                time.sleep(0.1)

                self.ball_feature_ball()
                time.sleep(0.1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)
                time.sleep(0.1)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 L_center 오류")

                self.robo._motion.hit_the_ball("RIGHT")
                time.sleep(3)

            elif self.L_left == 1:
                self.robo._motion.walk("FORWARD", 1)
                time.sleep(0.1)

                self.ball_feature_ball()
                time.sleep(0.1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)
                time.sleep(0.1)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")
                    self.robo._motion.hit_the_ball("RIGHT")
                    time.sleep(3)

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 L_left 오류")

            elif self.C_center == 1:
                print("이 부분 추가해야함")
                time.sleep(0.1)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)
                self.robo._motion.walk_side("LEFT")
                time.sleep(0.5)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)

                self.ball_feature_ball()
                time.sleep(1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)
                time.sleep(1)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")
                    self.robo._motion.hit_the_ball("RIGHT")
                    time.sleep(3)

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 C_center 오류")

            elif self.C_right == 1:
                self.robo._motion.walk_side("RIGHT")
                time.sleep(0.5)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)
                self.robo._motion.walk_side("LEFT")
                time.sleep(0.5)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)

                self.ball_feature_ball()
                time.sleep(1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)
                time.sleep(1)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")
                    print("퍼팅하는거 모션에 넣어줘야 함.")

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 C_right 오류")

            elif self.C_left == 1:
                self.robo._motion.walk_side("LEFT")
                time.sleep(0.5)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)
                self.robo._motion.walk_side("LEFT")
                time.sleep(0.5)
                self.robo._motion.turn("RIGHT", 45)
                time.sleep(0.8)

                self.ball_feature_ball()
                time.sleep(1)

                dist_Process = DistMeasurer()
                angle = 0
                dist = dist_Process.display_distance(angle)
                time.sleep(0.1)

                if dist > (self.canPutting - 1) and dist < (self.canPutting + 1):
                    print("퍼팅 하겠습니다.")
                    print("퍼팅하는거 모션에 넣어줘야 함.")

                elif dist < (self.canPutting - 1):
                    self.robo._motion.walk("FORWARD", 1)

                elif dist < (self.canPutting + 1):
                    self.robo._motion.walk("BACKWARD", 1)

                else:
                    print("T샷 C_left 오류")

            else:
                print("원하는 값이 안 옴")
                time.sleep(1)

            self.act = act.SEARCH_BALL

        elif act == act.SEARCH_BALL:
            print("Act:", act)  # Debug
            time.sleep(0.1)
            angle = abs(self.robo._motion.y_head_angle - 20)
            dist_ball = DistMeasurer(angle)  # 볼 거리 구한 값 저장
            print(dist_ball)

            # self.ball_feature_ball()
            self.act = act.SEARCH_FLAG

        elif act == act.SEARCH_FLAG:
            print("Act:", act)  # Debug

            self.act = act.SEARCH_PUTTING_LOCATION

        elif act == act.SEARCH_PUTTING_LOCATION:  # 치는 위치 확인
            print("Act:", act)  # Debug

            self.act = act.CHECK

        elif act == act.CHECK:  # 홀인했는지 확인
            print("Act:", act)  # Debug

            self.act = act.EXIT

        elif act == act.EXIT:
            print("Act:", act)  # Debug
            self.robo._motion.turn("LEFT", 60)
            time.sleep(1)

        else:
            print("이쪽으로 빠지면 문제가 있는거임.")

        return False
