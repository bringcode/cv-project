import cv2
import numpy as np

class ColorTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        cv2.namedWindow("Tracking")
        self.create_trackbars()

    def create_trackbars(self):
        # 트래킹 바 생성
        # 'LH', 'LS', 'LV'는 하한(Hue, Saturation, Value)
        # 'UH', 'US', 'UV'는 상한
        cv2.createTrackbar("LH", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("LS", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("LV", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("UH", "Tracking", 255, 255, self.nothing)
        cv2.createTrackbar("US", "Tracking", 255, 255, self.nothing)
        cv2.createTrackbar("UV", "Tracking", 255, 255, self.nothing)

    def nothing(self, x):
        # 트래킹 바 콜백 함수 (동작 없음)
        pass

    def mouse_callback(self, event, x, y, flags, param):
        # 마우스 이벤트 콜백 함수. 마우스 위치에 따라 HSV 값을 화면에 출력
        if event == cv2.EVENT_MOUSEMOVE:
            self.hsv_value = self.hsv[y, x]
            self.mouse_x, self.mouse_y = x, y

    def track(self):
        self.hsv_value = (0, 0, 0)
        self.mouse_x, self.mouse_y = 0, 0

        while True:
            _, frame = self.cap.read()
            self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            l_b, u_b = self.get_trackbar_values()
            mask = cv2.inRange(self.hsv, l_b, u_b)
            res = cv2.bitwise_and(frame, frame, mask=mask)

            # 마우스 위치 아래에 HSV 값을 표시
            text = f"HSV: {self.hsv_value}"
            cv2.putText(res, text, (self.mouse_x, self.mouse_y + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            cv2.imshow("Mask", mask)
            cv2.imshow("Result", res)
            # 'Result' 윈도우에 마우스 콜백 설정
            cv2.setMouseCallback("Result", self.mouse_callback)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_trackbar_values(self):
        # 트래킹 바의 현재 값들을 반환
        lh = cv2.getTrackbarPos("LH", "Tracking")
        ls = cv2.getTrackbarPos("LS", "Tracking")
        lv = cv2.getTrackbarPos("LV", "Tracking")
        uh = cv2.getTrackbarPos("UH", "Tracking")
        us = cv2.getTrackbarPos("US", "Tracking")
        uv = cv2.getTrackbarPos("UV", "Tracking")
        return np.array([lh, ls, lv]), np.array([uh, us, uv])

if __name__ == "__main__":
    tracker = ColorTracker()
    tracker.track()
