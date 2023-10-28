# -*- coding: utf-8 -*-
# Main code
from EWStest.Core.Controller import Controller

def main():
    while not Controller.go_robo():
        continue


if __name__ == "__main__":
    main() 