import math

class DistMeasurer:
    def __init__(self, height=33.4):
        self.height = height

    def calculate_distance(self, angle):
        # tan(angle-10) 계산
        d = self.height * math.tan(math.radians(angle))
        return round(d, 2)

    def display_distance(self, angle):
        d = self.calculate_distance(angle)
        # print(f"Distance d = {d} cm")
        return d

if __name__ == "__main__":
    dist = DistMeasurer()
    angle = 30
    print(dist.display_distance(angle))