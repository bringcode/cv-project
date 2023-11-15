# -*- coding: utf-8 -*-
import serial
import time
from threading import Thread, Lock


class Motion:
    # 초기화 함수
    def __init__(self, sleep_time=0):  # 명령 간 간격으로 사용할 시간(초) 설정
        self.x_head_angle = 0
        self.y_head_angle = 90
        self.serial_use = 1  # 시리얼 통신 사용 여부 (1:사용, 0:미사용)
        self.serial_port = None  # 시리얼 포트 객체
        self.Read_RX = 0  # 읽기 버퍼 (효율적으로 처리하기 위한 중간 저장 공간)
        self.receiving_exit = 1  # 수신 종료 여부
        self.threading_Time = 0.01  # 스레드 간 간격 설정 (초)
        self.sleep_time = sleep_time
        self.lock = False  # 스레드 간 동기화를 위한 Lock 객체
        self.distance = 0  # 거리 데이터
        BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
        # BPS: 시리얼 통신 속도 (보드레이트)
        # ---------local Serial Port : ttyS0 --------
        # ---------USB Serial Port : ttyAMA0 --------
        self.serial_port = serial.Serial("/dev/ttyS0", BPS, timeout=1)  # 시리얼 포트 객체 생성
        self.serial_port.flush()  # serial cls
        self.serial_t = Thread(
            target=self.Receiving, args=(self.serial_port,)
        )  # 시리얼 통신을 위한 스레드 객체 생성
        self.serial_t.daemon = True
        self.serial_t.start()
        time.sleep(0.1)

    # DELAY DECORATOR
    def sleep(self, func):
        # 함수 실행 후 sleep_time만큼 대기하는 데코레이터
        def decorated():
            func()
            time.sleep(self.sleep_time)

        return decorated

    def TX_data_py3(self, one_byte):  # one_byte= 0~255
        # 1바이트 데이터를 시리얼 포트로 전송
        self.lock = True
        self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        time.sleep(0.1)

    # def TX_data_py3(self, one_byte):
    #     self.lock = True
    #     self.serial_port.write(serial.to_bytes([one_byte]))
    #     time.sleep(0.1)

    def RX_data(self):
        # 시리얼 포트로부터 데이터 수신
        time.sleep(0.02)
        if self.serial_port.inWaiting() > 0:
            result = self.serial_port.read(1)
            RX = ord(result)
            return RX
        else:
            return 0

    def Receiving(self, ser):
        # time.sleep(0.1)
        self.receiving_exit = 1
        while True:
            if self.receiving_exit == 0:
                break
            time.sleep(self.threading_Time)
            # time.sleep(0.1)
            while ser.inWaiting() > 0:
                time.sleep(0.1)
                result = ser.read(1)
                aa = len(result)
                if aa > 0:
                    RX = ord(result)

                    # -----  remocon 16 Code  Exit ------
                    if RX == 38:
                        self.lock = False
                    else:
                        self.distance = RX
                    if RX == 16:
                        self.receiving_exit = 0
                        break
            if self.receiving_exit == 0:
                break

    ############################################################
    # 현재 로봇 머리 각도
    # def current_head_angle(self):
    #     self.x_head_angle = 0
    #     self.y_head_angle = 0

    ############################################################
    # 기본자세 (100) -> 로봇을 기본 자세로 설정
    def basic(self):
        self.TX_data_py3(100)

    # 걷기 (101~120)
    def walk(self, dir, loop=1, sleep=0.1, short=False):
        """
        dir: {FORWARD, BACKWARD} - 로봇 이동 방향
        loop: 반복 횟수
        sleep: 각 동작 간 간격 (초)
        short: 짧은 걸음 여부
        """

        """ parameter :
        dir : {FORWARD, BACKWARD}
        """
        dir_list = {"FORWARD": 101, "BACKWARD": 111}  # motion.bas 수정 해야할 듯?
        if short:
            dir_list[dir] += 1

        for _ in range(loop):
            self.TX_data_py3(dir_list[dir])
            time.sleep(sleep) # 주석하면 큰일날듯


    # 머리 각도 (121~140)
    def set_head(self, dir, angle=0):
        """
        dir: {DOWN, LEFT, RIGHT, UPDOWN_CENTER, LEFTRIGHT_CENTER} - 머리 방향
        angle: 머리 각도
        """

        """ parameter :
        dir : {DOWN, LEFT, RIGHT, UPDOWN_CENTER, LEFTRIGHT_CENTER}
        angle: {DOWN:{20,30,40,45,60,70,80,90,100,110},
        LEFT:{30,45,60,90},
        RIGHT:{30,45,60,90}
        """
        if dir == "DOWN":
            self.y_head_angle = angle
            print("down_angle: ", angle)
            print("y_head_angle: ", self.y_head_angle)
            print("===========================")
        elif dir == "LEFT" or dir == "RIGHT":
            self.x_head_angle = angle
            print("left_right_angle: ", angle)
            print("x_head_angle: ", self.x_head_angle)
            print("===========================")

        center_list = {"UPDOWN_CENTER": 140, "LEFTRIGHT_CENTER": 135}
        dir_list = {
            "DOWN": {
                20: 121,
                30: 122,
                40: 189,
                42: 194,
                45: 123,
                50: 188,
                55: 124,
                60: 125,
                73: 193,
                75: 126,
                80: 127,
                85: 192,
                90: 128,
                92: 191,
                95: 190,
                100: 129,
                110: 130,
            },
            "LEFT": {30: 134, 45: 133, 54: 173, 60: 132, 90: 131},
            "RIGHT": {30: 136, 45: 137, 54: 172, 60: 138, 90: 139},
        }

        if dir in center_list:
            self.TX_data_py3(center_list[dir])
        else:
            self.TX_data_py3(dir_list[dir][angle])

        # time.sleep(0.3)

    # 돌기 (141~160) + (178~181)
    def turn(self, dir, angle, loop=1, sleep=0.5):
        """
        dir: {LEFT, RIGHT} - 회전 방향
        angle: 회전 각도
        loop: 반복 횟수
        sleep: 각 동작 간 간격 (초)
        arm: 팔을 들고 회전 여부
        """

        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {
            "LEFT": {3:181, 5:179, 10: 141, 20: 142, 45: 143, 60: 144},
            "RIGHT": {3:180, 5:178, 10: 145, 20: 146, 45: 147, 60: 148},
        }
        for _ in range(loop):
            self.TX_data_py3(dir_list[dir][angle])
            time.sleep(sleep) # 이 타임 슬립 지우면 절대 안 돼

    # 옆으로 이동 (161~169)
    def walk_side(self, dir):
        """
        dir: {LEFT, RIGHT} - 이동 방향
        """

        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {"LEFT": 161, "RIGHT": 169}
        self.TX_data_py3(dir_list[dir])

    # 공 치기 (170~171)
    def hit_the_ball(self, dir, short=False):
        """
        dir: {LEFT, RIGHT} - 치는 방향
        """

        dir_list = {"LEFT": 2, "RIGHT": 5}
        

        if short:
            dir_list[dir] += 16 # 짧게 치는게 왼쪽 187, 오른쪽 186임.

        if dir == "LEFT":
            print("왼쪽에서 치겠습니다.")
            self.TX_data_py3(dir_list[dir])
        elif dir == "RIGHT":
            print("오른쪽에서 치겠습니다.")
            self.TX_data_py3(dir_list[dir])
        time.sleep(8)

    # 1도씩 set_head하기 (174~177) + (182+185)
    def set_head_small(self, dir, angle=0):
        """
        dir: {UP, DOWN, LEFT, RIGHT} - 머리 방향
        angle: 머리 각도
        """

        """ parameter :
        dir : {UP, DOWN, LEFT, RIGHT}
        angle: {
        UP: {1,3},
        DOWN:{1,3},
        LEFT:{1,3},
        RIGHT:{1,3}
        }
        """
        if dir == "UP":
            self.y_head_angle += angle
            print("2_up_angle: ", angle)
            print("y_head_angle: ", self.y_head_angle)
            print("===========================")
        elif dir == "DOWN":
            self.y_head_angle -= angle
            print("2_down_angle: ", angle)
            print("y_head_angle: ", self.y_head_angle)
            print("===========================")
        elif dir == "LEFT":
            self.x_head_angle -= angle
            print("2_left_angle: ", angle)
            print("x_head_angle: ", self.x_head_angle)
            print("===========================")
        elif dir == "RIGHT":
            self.x_head_angle += angle
            print("2_right_angle: ", angle)
            print("x_head_angle: ", self.x_head_angle)
            print("===========================")

        dir_list = {
            "UP": {1: 175, 3:183},
            "DOWN": {1: 174, 3:182},
            "LEFT": {1: 176, 3:184},
            "RIGHT": {1: 177, 3:185},
        }

        self.TX_data_py3(dir_list[dir][angle])
        # time.sleep(0.3)

  
    # 세레머니하기 (8)
    def ceremony(self, goal):
        ceremony = {"goal": 8}
        self.TX_data_py3(ceremony[goal])

    ############################################################


if __name__ == "__main__":
    motion = Motion()
    motion.set_head("LEFTRIGHT_CENTER")
