from Sensor.ball_x_center import BallxCenterMeasurer
from Core.Robo import Robo

# 공을 못 찾았을 때 반환하는 값
ball_x_angle = ["N", "N", "N"]

xcenterprocess = BallxCenterMeasurer(img_width=640, img_height=480)
ball_x_angle = xcenterprocess.process()

# 걸어가면서 틀어진 각도 맞추는 로직
while ball_x_angle[0] != "C":
	print("걸어가면서 틀어진 각도 맞추기")

while ball_x_angle[0] != "C":
    if ball_x_angle[0] == "L" or ball_x_angle[0] == "R":
        if ball_x_angle[0] == "L":
            self.robo._motion.set_head_small("LEFT", 1)
			time.sleep(0.1)
						
        if ball_x_angle[0] == "R":
            self.robo._motion.set_head_small("RIGHT", 1)
            time.sleep(0.1)

# 현재 머리 각도가 플러스면 오른쪽으로 턴해야 함
while self.robo._motion.x_head_angle > 0:
	self.robo._motion.x_head_angle = head_plus(60)
	self.robo._motion.x_head_angle = head_plus(45)
	self.robo._motion.x_head_angle = head_plus(20)
	self.robo._motion.x_head_angle = head_plus(10)
	self.robo._motion.x_head_angle = head_plus(5)
	self.robo._motion.x_head_angle = head_plus(3)
	self.robo._motion.x_head_angle = 0

# 현재 머리 각도가 마이너스면 왼쪽으로 턴해야 함
while self.robo._motion.x_head_angle < 0:
	self.robo._motion.x_head_angle = head_minus(60)
	self.robo._motion.x_head_angle = head_minus(45)
	self.robo._motion.x_head_angle = head_minus(20)
	self.robo._motion.x_head_angle = head_minus(10)
	self.robo._motion.x_head_angle = head_minus(5)
	self.robo._motion.x_head_angle = head_minus(3)
	self.robo._motion.x_head_angle = 0

# 오른쪽으로 턴
def head_plus(N):
	x_head_angle_n = self.robo._motion.x_head_angle // N
	if x_head_angle_n >= 1:
		for _ in range(x_head_angle_n):
			self.robo._mothon.turn("RIGHT", N)
			self.robo._motion.x_head_angle -= N
	elif x_head_angle_n == 0:
		return self.robo._motion.x_head_angle
	else:
		print("여기로 오면 안 되는뎁..")
	return self.robo._motion.x_head_angle

# 왼쪽으로 턴
def head_minus(N):
	x_head_angle_n = self.robo._motion.x_head_angle // N
	if x_head_angle_n >= 1:
		for _ in range(x_head_angle_n):
			self.robo._mothon.turn("LEFT", N)
			self.robo._motion.x_head_angle += N
	elif x_head_angle_n == 0:
		return self.robo._motion.x_head_angle
	else:
		print("여기로 오면 안 되는뎁..")
	return self.robo._motion.x_head_angle