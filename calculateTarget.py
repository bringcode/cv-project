import math

TARGETPOINT = 7
distMoveToFlag = 0
distMoveToRed = 0
distRed = 24  # cm 단위, 받아야 할 값
distYellow = 180  # cm 단위, 받아야 할 값
degreeRedToYellow = 90  # 공과 목표물 간 각도 측정해서 받아야 할 값

# 도 단위 각도를 라디안으로 변환
angleRedToYellowRad = math.radians(degreeRedToYellow)

cosA = math.cos(angleRedToYellowRad)

distRedToYellow = math.sqrt((distRed**2) + (distYellow**2) - 2 * distRed * distYellow * cosA)

cosB = ((distYellow**2 + distRedToYellow**2 - distRed**2) / (2 * distYellow * distRedToYellow))

# distMoveToFlag 및 distMoveToRed 계산을 수정
distMoveToFlag = distYellow - (distRedToYellow / cosB)
if distMoveToFlag<0:
    distMoveToFlag = 0

distMoveToRed = math.sqrt((distYellow**2) + (distRedToYellow**2) - 2 * distYellow * distRedToYellow * cosB)- TARGETPOINT

print(distMoveToFlag, distMoveToRed)

#작동 원리:    distMoveToFlag의 거리만큼 깃발 방향을 중심으로 움직임-> 몸을 돌려서 공을 중심으로 distMoveToRed만큼 움직임

