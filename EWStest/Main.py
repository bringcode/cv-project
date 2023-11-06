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
    # Motion.TX_data_py3(123)
    print("head left")
    time.sleep(3)
    Motion.TX_data_py3(176)  # 1도좌향
    time.sleep(1)
    Motion.TX_data_py3(176)
    time.sleep(1)
    Motion.TX_data_py3(176)
    main()
