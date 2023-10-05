# -*- coding: utf-8 -*-
from Core.Robo import Robo
import Sensor.dist_measure_draft
import time


class Controller:
    #####################################
    # 10cm 앞으로 이동
    def walk_10cm():
        minus_10cm = Sensor.dist_measure_draft.dist - 10   # 처음 거리에서 10cm 빼기
        # time으로 몇초 이동하는지 확인하기

        if Sensor.dist_measure_draft.dist != minus_10cm:   # dist: 현재 인식되는 거리
            Robo._motion.walk_cm("FORWARD")



    #####################################
    # 30cm 앞으로 이동
    def walk_30cm():
        minus_30cm = Sensor.dist_measure_draft.dist - 30   # 처음 거리에서 30cm 빼기
        # time으로 몇초 이동하는지 확인하기
        
        if Sensor.dist_measure_draft.dist != minus_30cm:   # dist: 현재 인식되는 거리
            Robo._motion.motion.walk_cm("FORWARD")



    #####################################
    # 공 찾는 코드..?
    def location(self):
        time.sleep(1)
        self.ball = Sensor.findball.ball 
        self.dir = 90

        # 로봇이 왼쪽에서 시작한다고 생각하고 시작하는 부분
        self.robo._motion.set_head("DOWN", self.dir)
        
        # 고개 각도를 90도에서 50도로 변경하면서 공을 찾습니다.
        for _ in range(4):
            if self.ball:
                break
            self.dir -= 10
            self.robo._motion.set_head("DOWN", self.dir)

        # 로봇이 가운데로 생각하고 시작하는 부분
        self.dir = 50
        self.robo._motion.set_head("DOWN", self.dir)
        
        if not self.ball:
            # 오른쪽으로 시선 이동
            self.robo._motion.set_head("RIGHT", 10)
            if not self.ball:
                # 왼쪽으로 시선 이동
                self.robo._motion.set_head("LEFT", 20)

        if self.ball:
            print("공을 찾았습니다.")
        else:
            print("공을 찾지 못했습니다.")



    #####################################
    # 공을 치는 코드
    def is_hole(self):
        time.sleep(1)
        self.hole = Sensor.findhole
        self.danger = Sensor.outline-contour 
        # right: 오른쪽 (오른쪽 아웃라인이 보이는 경우) 
        # left: 왼쪽 (왼쪽 아웃라인이 보이는 경우)
        # center: 가운데(왼쪽 오른쪽 다 보이는 경우 or 왼쪽 오른쪽 아웃라인이 안 보이는 경우 )


        # 조건
        if self.hole == True:
            print("hole이 보입니다.")
            
            if self.danger == Right:
                print("위험 지역이 오른쪽에 있습니다.")


            elif self.danger == left:
                print("위험 지역이 오른쪽에 있습니다.")
            
            elif self.danger == center:
                print("위험 지역이 가운데 있습니다.")

            else:
                print("위험 지역이 보이지 않습니다.")            


        else:
            print("hole이 보이지 않습니다.")

            if self.danger == Right:
                print("위험 지역이 오른쪽에 있습니다.")

            elif self.danger == left:
                print("위험 지역이 오른쪽에 있습니다.")
            
            elif self.danger == center:
                print("위험 지역이 가운데 있습니다.")

            else:
                print("위험 지역이 보이지 않습니다.")



    #####################################
    # 홀인 했는지 확인하는 코드
    def check_holein(self):
        time.sleep(1)
        self.hole = Sensor.findhole.holedist
        self.ball = Sensor.findball.ball


    # hole까지 걷기
        #while holedist > [특정값]:
    #       self.robo._motion.walk()

        #if ball위치 == 홀위치:
            #print("홀인했습니다.")



    #####################################
    # 넘어지고 실행하는 거 이어지게 하는 코드 -> 가장 위에 두고 while문 안에 코드들 넣기
    # 넘어짐 감지하기
    # 함수들마다 변수 bool를 넣어 true인 코드만(실행 중) 다시 실행하도록
    def_bool = [함수1(), 함수2(), 함수3()]
    def detect_fall():
        if 넘어짐감지:  # 아마 적외선으로..?
            for i in range(len(def_bool)):
                if i == true:
                    def_bool[i]()  # 해당 함수 실행
        else:
            print("로봇이 안전하여 실행을 계속합니다.")
            return True
        
    # 실행할 함수
    def robot_task():
        while detect_fall():
            # 함수들 넣기




    #####################################
    # 컨투어 활용해서 위험 지역 정해서 못 가게 하는 코드
    # 걷다가 위험지역이 보이면 일단 멈추고, 고개 가장 아래로
    # 고개 가장 아래로 했는데도 위험지역이 보이면 거기서 다른 거 수행, 안 보이면 조금 움직이고 다시 고개 아래로
    def contour_danger(self):
        if 위험지역보임:  # 10은 로봇 시야로 보면서 조절
            while 가장아래가아니면:
                self.robo._motion.set_head("DOWN", self.dir)
            if 위험지역보임:
                다른거수행
            else:
                # 정밀하게 움직이는 코드 짜기(한 1cm..)

    


    #####################################
    # 공에 가까이 가는 코드
    def walk_to_ball_and_flag(self):
        Robo._motion.basic()  # 초기 자세로 설정

        # 공 인식
        while True:
            if Sensor.dist_measure_draft.name == 'ball':
                break
            else:   # 공이 안 보이면 찾게끔
                head_turn = 10
                Robo._motion.set_head("LEFT", head_turn)
                time.sleep(1)
                Robo._motion.set_head("RIGHT", head_turn)
                time.sleep(1)
                head_turn += 10   # 10도씩 더 회전하여 찾을 수 있게
        
        # 공 쪽까지 걸어가기
        while True:
            if Sensor.dist_measure_draft.dist <= 공과의_목표_거리:
                self.walk()
            else:
                break

        # 깃발, 홀컵 찾기
        # while True:
        #     if Sensor.dist_measure_draft.name == "flag":
        #         break
        #     else:
        #         head_turn = 10   # 초기 회전
        #         Robo._motion.set_head("LEFT", head_turn)
        #         time.sleep(1)
        #         Robo._motion.set_head("RIGHT", head_turn)
        #         time.sleep(1)
        #         head_turn += 10   # 10도씩 더 회전하게끔..

        # 공이랑 일직선이 되게끔 각도 바꾸기
        # while True:
        #     # 공이랑 깃발이 일직선이 아니면 계속 턴하면서 찾기
        #     if 'ball' == 'flag':   # 일직선이 되면 멈추고 공 차기
        #         break
        #     else:
        #         body_turn = 10
        #         Robo._motion.turn("LEFT", body_turn)
        #         time.sleep(1)
        #         Robo._motion.turn("RIGHT", body_turn)
        #         time.sleep(1)
        #         body_turn += 10

        
    Robo._motion.basic()  # 초기 자세로 설정

# 목표를 2개 변수로 정해서 무조건 하나는 공, 하나는 홀컵을 넣기
# 그 목표에 따라 코드 짜면 될 듯..? 