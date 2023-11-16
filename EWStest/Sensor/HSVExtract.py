import cv2
import numpy as np

class ColorTracker:
    def __init__(self):
        # 카메라를 캡처하기 위한 객체 생성. 0은 기본 카메라
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L)

        # 윈도우 생성
        cv2.namedWindow("Tracking")

        # 트래킹 바를 생성하는 함수 호출
        self.create_trackbars()

    def create_trackbars(self):
        # 각각의 HSV 색상 범위를 조정하기 위한 트래킹 바 생성
        # 'LH', 'LS', 'LV'는 하한(Hue, Saturation, Value)
        # 'UH', 'US', 'UV'는 상한
        cv2.createTrackbar("LH", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("LS", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("LV", "Tracking", 0, 255, self.nothing)
        cv2.createTrackbar("UH", "Tracking", 255, 255, self.nothing)
        cv2.createTrackbar("US", "Tracking", 255, 255, self.nothing)
        cv2.createTrackbar("UV", "Tracking", 255, 255, self.nothing)

    def nothing(self, x):
        # 트래킹 바 콜백 함수. 실제 동작은 없지만, 트래킹 바 생성에 필요함.
        pass

    def get_trackbar_values(self):
        # 하한 및 상한 값을 반환
        lh = cv2.getTrackbarPos("LH", "Tracking")
        ls = cv2.getTrackbarPos("LS", "Tracking")
        lv = cv2.getTrackbarPos("LV", "Tracking")
        uh = cv2.getTrackbarPos("UH", "Tracking")
        us = cv2.getTrackbarPos("US", "Tracking")
        uv = cv2.getTrackbarPos("UV", "Tracking")
        return np.array([lh, ls, lv]), np.array([uh, us, uv])

    def track(self):
        while True:
            _, frame = self.cap.read()

            # BGR에서 HSV 색상 공간으로 변환
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # 트래킹 바로부터 색상 범위를 얻어옴.
            l_b, u_b = self.get_trackbar_values()

            # 지정된 색상 범위에 있는 픽셀만을 강조하는 마스크 생성.
            mask = cv2.inRange(hsv, l_b, u_b)

            # 마스크를 적용하여 결과 이미지 생성.
            res = cv2.bitwise_and(frame, frame, mask=mask)

            cv2.imshow("Mask", mask)    # 마스크 표시
            cv2.imshow("Result", res)   # 최종 결과 표시

            # 'q' 키를 누르면 종료
            key = cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    tracker = ColorTracker()
    tracker.track()
