import cv2
import numpy as np

class HitPointer:
    def __init__(self, a, b, l, h):
        # 값을 받아와야 함
        self.a = a
        self.b = b
        self.l = np.radians(l)  # 각도 l을 라디안으로 변환
        self.h = h              # 로봇이 공으로부터 얼마나 떨어져서 타격할지 설정

    def calculate_c(self):
        # c = sqrt(a^2 + b^2 - 2ab*cos(l))
        return np.sqrt(self.a**2 + self.b**2 - 2*self.a*self.b*np.cos(self.l))

    def calculate_m(self, c):
        # cos(m) = (b^2 + c^2 - a^2) / (2bc)
        cos_m = (self.b**2 + c**2 - self.a**2) / (2*self.b*c)
        return np.arccos(cos_m)

    def calculate_x(self, m):
        # y = 90 - m (in degrees)
        y = 90 - np.degrees(m)
        # x = sqrt(b^2 + h^2 - 2bh*cos(y))
        y_rad = np.radians(y)  # 각도 y를 라디안으로 변환
        return np.sqrt(self.b**2 + self.h**2 - 2*self.b*self.h*np.cos(y_rad))

    def calculate_z(self, x):
        # cos(z) = (b^2 + x^2 - h^2) / (2bx)
        cos_z = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        return np.arccos(cos_z)

    def solve(self):
        c = self.calculate_c()
        m = self.calculate_m(c)
        x = self.calculate_x(m)
        z = self.calculate_z(x)
        z_deg = np.degrees(z)  # z를 도(degree) 단위로 변환

        # 결과 출력
        print(f"x: {x:.2f}, z: {z_deg:.2f} degrees")
        return x, z_deg

# 예제:
a = 5
b = 7
l = 45
h = 3

solver = HitPointer(a, b, l, h)
solver.solve()
