import math

class TargetPoint:
    def __init__(self, distRed, distYellow, degreeRedToYellow):
        self.distRed = distRed  # cm 단위
        self.distYellow = distYellow  # cm 단위
        self.degreeRedToYellow = degreeRedToYellow  # 도 단위

    def calculate_distances(self):
        # 도 단위 각도를 라디안으로 변환
        angleRedToYellowRad = math.radians(self.degreeRedToYellow)

        cosA = math.cos(angleRedToYellowRad)

        distRedToYellow = math.sqrt((self.distRed**2) + (self.distYellow**2) - 2 * self.distRed * self.distYellow * cosA)

        cosB = ((self.distYellow**2 + distRedToYellow**2 - self.distRed**2) / (2 * self.distYellow * distRedToYellow))

        # distMoveToFlag 및 distMoveToRed 계산을 수정
        distMoveToFlag = self.distYellow - (distRedToYellow / cosB)
        if distMoveToFlag < 0:
            distMoveToFlag = 0

        distMoveToRed = math.sqrt((self.distYellow**2) + (distRedToYellow**2) - 2 * self.distYellow * distRedToYellow * cosB) - 7  # TARGETPOINT 대신 7 사용

        return distMoveToFlag, distMoveToRed

if __name__ == "__main__":
    target = TargetPoint()

    # 거리 계산
    distMoveToFlag, distMoveToRed = target.calculate_distances()

    print(f"distMoveToFlag: {distMoveToFlag} cm")
    print(f"distMoveToRed: {distMoveToRed} cm")
