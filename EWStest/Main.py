# -*- coding: utf-8 -*-
# Main code
from Core.Controller import Controller
from Motion.Motion import Motion
import time


def main():
    while not Controller.go_robo():
        continue


if __name__ == "__main__":
    Motion = Motion()
    # Motion.TX_data_py3(143)
    # time.sleep(0.5)
    # Motion.TX_data_py3(143)
    #time.sleep(2)
    #print("head right")
    #Motion.TX_data_py3(177)  # 1도우향
    #time.sleep(2)
    #Motion.TX_data_py3(177)
    # print("head right")
    # Motion.TX_data_py3(177)
    # time.sleep(3)
    # print("head right")
    # Motion.TX_data_py3(177)
    main() # 그냥 모션만 테스트할거면 여기 주석 처리