# -*- coding: utf-8 -*-
# Main code
from Core.Controller import Controller
import time

def main():
    while not Controller.go_robo():
        continue


if __name__ == "__main__":
    time.slepp(1)
    main() 