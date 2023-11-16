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
        
    def calculatezero_x(self):
        # c = sqrt(a^2 + b^2 - 2ab*cos(l))
        return np.sqrt(self.h**2 + (self.a-self.b)**2)
    def calculatezero_z(self):
        # c = sqrt(a^2 + b^2 - 2ab*cos(l))
        c = np.sqrt(self.h**2 + (self.a-self.b)**2)
        cos_z = ((self.a-self.b)**2 + c**2 - self.h**2) / (2*(self.a-self.b)*c)
        return  np.arccos(cos_z)
    
    # 타격지점이 삼각형 밖에 있을 때
    def calculate_out_x(self, m):
        y = 90 - np.degrees(m)
        # x = sqrt(b^2 + h^2 - 2bh*cos(y))
        y_rad = np.radians(y)
        return np.sqrt(self.b**2 + self.h**2 - 2*self.b*self.h*np.cos(y_rad))

    def calculate_out_z(self, x):
        # cos(p) = (b^2 + x^2 - h^2) / (2bx)
        cos_p = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        rad_z = self.l + np.arccos(cos_p)
        return rad_z
    
    def calculate_out_angle(self, x, m):
        y =  90 - np.degrees(m)
        y_rad = np.radians(y)
        cos_p = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        p_rad = np.arccos(cos_p)

        return y_rad+p_rad
  
      
    # 타격지점이 삼각형 안에 있을 때
    def calculate_in_x(self, m):
        y = np.degrees(m) - 90
        y_rad = np.radians(y)
        return np.sqrt(self.b**2 + self.h**2 - 2*self.b*self.h*np.cos(y_rad))
 
    def calculate_in_z(self, x):
        cos_p = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        rad_z = self.l - np.arccos(cos_p)
        
        return rad_z
      
    def calculate_in_angle(self, x, m):
        y = np.degrees(m) - 90
        y_rad = np.radians(y)
        cos_p = (self.b**2 + x**2 - self.h**2) / (2*self.b*x)
        rad_z = self.l - np.arccos(cos_p)
        p_rad = np.arccos(cos_p)
        print(y_rad, rad_z)
        return y_rad + p_rad
      
    def calculate_zero_angle(self):
        c = np.sqrt(self.h**2 + (self.a-self.b)**2)
        #여기서 NaN값 발생하는듯. cos값이 -1부터 1까지 인데 범위를 벗어난 값이 나오는 듯함.
        cos_z = (self.b**2 + c**2 - self.h**2) / (2*self.b*c)
        print("b : ", self.b)    #테스트
        print("c : ", c)    #테스트
        print("h : ", self.h)    #테스트
        print("cos_z : ", cos_z)    #테스트
        rad_z = np.arccos(cos_z)
        
        return  np.radians(90) + rad_z


    def solve(self):
        c = self.calculate_c()
        m = self.calculate_m(c)
        
        if np.degrees(m) <= 90: # 타격지점이 삼각형 밖에 위치
            if(self.l != 0):
                x = self.calculate_out_x(m)
                z = self.calculate_out_z(x)
                angle_triangle = int(np.degrees(self.calculate_out_angle(x,m)))
                judge_triangle = False
                c = int(c)
            else:
                c = int(self.a  - self.b)
                x=self.calculatezero_x()
                z=self.calculatezero_z()
                angle_triangle = int(np.degrees(self.calculate_zero_angle()))
                judge_triangle = False
        
        else:                   # 타격지점이 삼각형 안에 위치
            if(self.l != 0):
                x = self.calculate_in_x(m)
                z = self.calculate_in_z(x)
                angle_triangle = int(np.degrees(self.calculate_in_angle(x,m)))
                judge_triangle = True
                c = int(c)
            else:
                c = int(self.a  - self.b)
                x=self.calculatezero_x()
                z=self.calculatezero_z()
                angle_triangle = int(np.degrees(self.calculate_zero_angle()))
                judge_triangle = True                  
          
        z_deg = np.degrees(z)  # z를 도(degree) 단위로 변환
        

        # 결과 출력
        print(f"x: {x:.2f}, z: {z_deg:.2f} degrees")
        return [x, z_deg, angle_triangle, judge_triangle, c] 
        # x: 로봇의 첫 위치에서 목표지점까지 이동해야하는 직선 거리
        # z_deg: 로봇의 첫 위치에서 목표지점을 바라볼때 필요한 각도
        #angle triangle : 목표지점 이동 후 돌아야하는 각도(라디안 형태)     
        #judge_triangle : 타격지점이 삼각형 안 : True,  타격지점 삼각형 밖: False  (목표지점 이동후 왼쪽으로 돌지 오른쪽으로 돌지 판단에 필요)

# 예제 사용:

if __name__ == "__main__":
    solver = HitPointer(a, b, l, h)
    solver.solve()
