# -*- coding: utf-8 -*-
from Core.Controller import Controller

def main():
    while not Controller.go_robo():   #  반환 값이 False일 때까지 계속 루프를 실행
        continue


if __name__ == "__main__":
    main()