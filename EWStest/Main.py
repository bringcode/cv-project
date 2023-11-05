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
    Motion.TX_data_py3(161)
    # print("head down")
    # time.sleep(3)
    main() 
    