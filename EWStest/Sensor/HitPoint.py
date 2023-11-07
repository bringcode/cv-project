import cv2
import numpy as np

class HitPointer:
    
    def __init__(self, a, b, l, h):
        # 값을 받아와야 함
        self.a = a              # 로봇과 깃발 거리
        self.b = b              # 로봇과 공 거리
        self.l = np.radians(l)  # 각도 l을 라디안으로 변환
        self.h = h              # 로봇이 공으로부터 얼마나 떨어져서 타격할지 설정

    def calculate_c(self):
        # c = sqrt(a^2 + b^2 - 2ab*cos(l))
        return np.sqrt(self.a**2 + self.b**2 - 2*self.a*self.b*np.cos(self.l))

    def calculate_m(self, c):
        # cos(m) = (b^2 + c^2 - a^2) / (2bc)
        cos_m = (self.b**2 + c**2 - self.a**2) / (2*self.b*c)
        return np.arccos(cos_m)

    # 타격지점이 삼각형 밖에 있을 때
    def calculate_out_x(self, m):
        y = 90 - np.degrees(m)
        # x = sqrt(b^2 + h^2 - 2bh*cos(y))
        y_rad = np.radians(y)
        return np.sqrt(self.b**2 + self.h**2 - 2*self.b*self.h*np.cos(y_rad))

    def calculate_out_z(self, x):
        # cos(z) = (b^2 + x^2 - h^2) / (2bx)
        cos_z = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        return np.arccos(cos_z)
      
    # 타격지점이 삼각형 안에 있을 때
    def calculate_in_x(self, m):
        y = np.degrees(m) - 90
        y_rad = np.radians(y)
        return np.sqrt(self.b**2 + self.h**2 - 2*self.b*self.h*np.cos(y_rad))

    def calculate_in_z(self, x):
        cos_p = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        rad_z = self.l - np.arccos(cos_p)
        return rad_z

    def solve(self):
        c = self.calculate_c()
        m = self.calculate_m(c)
        
        if np.degrees(m) <= 90: # 타격지점이 삼각형 밖에 위치
          x = self.calculate_out_x(m)
          z = self.calculate_out_z(x)
        else:                   # 타격지점이 삼각형 안에 위치
          x = self.calculate_in_x(m)
          z = self.calculate_in_z(x)
          
        z_deg = np.degrees(z)  # z를 도(degree) 단위로 변환

        # 결과 출력
        print(f"x: {x:.2f}, z: {z_deg:.2f} degrees")
        return x, z_deg

# 예제 사용:
a = 5
b = 7
l = 45
h = 3

solver = HitPointer(a, b, l, h)
solver.solve()
