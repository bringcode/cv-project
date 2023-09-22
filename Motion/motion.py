import serial
import time
from threading import Thread, Lock

class Motion:
    # 초기화 함수
    def __init__(self, sleep_time=0):      # 명령 간 간격으로 사용할 시간(초) 설정
        self.serial_use = 1   # 시리얼 통신 사용 여부 (1:사용, 0:미사용)
        self.serial_port = None   # 시리얼 포트 객체
        self.Read_RX = 0   # 읽기 버퍼 (효율적으로 처리하기 위한 중간 저장 공간)
        self.receiving_exit = 1   # 수신 종료 여부
        self.threading_Time = 0.01   # 스레드 간 간격 설정 (초)
        self.sleep_time = sleep_time   
        self.lock = Lock()   # 스레드 간 동기화를 위한 Lock 객체
        self.distance = 0   # 거리 데이터
        BPS = 4800  # 4800,9600,14400, 19200,28800, 57600, 115200
            # BPS: 시리얼 통신 속도 (보드레이트)
        # ---------local Serial Port : ttyS0 --------
        # ---------USB Serial Port : ttyAMA0 --------
        self.serial_port = serial.Serial('/dev/ttyS0', BPS, timeout=0.01)   # 시리얼 포트 객체 생성
        self.serial_port.flush()  # serial cls
        self.serial_t = Thread(target=self.Receiving, args=(self.serial_port,))   # 시리얼 통신을 위한 스레드 객체 생성
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

    def TX_data_py2(self, one_byte):  # one_byte= 0~255
        # 1바이트 데이터를 시리얼 포트로 전송
        try:
            self.lock.acquire()
            self.serial_port.write(serial.to_bytes([one_byte]))  # python3
        finally:
            self.lock.release()
            time.sleep(0.02)

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
        # 시리얼 포트로부터 지속적으로 데이터 수신하는 스레드 함수
        self.receiving_exit = 1
        while True:
            if self.receiving_exit == 0:
                break
            time.sleep(self.threading_Time)
            time.sleep(0.08)

            while ser.inWaiting() > 0:
                time.sleep(0.5)
                result = ser.read(1)
                RX = ord(result)
                # -----  remocon 16 Code  Exit ------
                if RX == 16:
                    self.receiving_exit = 0
                    break
                elif RX == 200:
                    try:
                        self.lock.release()
                    except:
                        continue
                elif RX != 200:
                    self.distance = RX
