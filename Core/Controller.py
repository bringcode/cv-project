import Motion.motion
import Sensor.dict_measure_draft


class Controller:
    # 10cm 앞으로 이동
    def walk_10cm():
        minus_10cm = Sensor.dict_measure_draft.dist - 10   # 처음 거리에서 30cm 빼기
        if Sensor.dict_measure_draft.dist != minus_10cm:   # dist: 현재 인식되는 거리
            Motion.motion.walk_cm("FORWARD")

    # 30cm 앞으로 이동
    def walk_30cm():
        minus_30cm = Sensor.dict_measure_draft.dist - 30   # 처음 거리에서 30cm 빼기
        if Sensor.dict_measure_draft.dist != minus_30cm:   # dist: 현재 인식되는 거리
            Motion.motion.walk_cm("FORWARD")