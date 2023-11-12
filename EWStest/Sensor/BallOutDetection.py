import cv2
import numpy as np

class BallOutDetection:
    
    def __init__(self, img_width=800, img_height=600, width=4, focal=450):
        self.dist = 0 
        self.focal = focal
        self.pixels = 30
        self.width = width

        self.img_width = img_width
        self.img_height = img_height
        self.img_width_middle = img_width // 2
        self.img_height_middle = img_height // 2

        self.kernel = np.ones((3, 3), 'uint8')
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (0, 20)
        self.fontScale = 0.6
        self.color = (0, 0, 255)
        self.thickness = 2
    
    def ball_detector(self, hsv, resized_frame):
        
        # robot version
        lower = np.array([137, 0, 0])
        upper = np.array([255, 255, 255])
        mask_ball = cv2.inRange(hsv, lower, upper)

        # 마스크에서 공을 찾음.
        contours_ball, _ = cv2.findContours(mask_ball, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours_ball:
            if cv2.contourArea(contour) > 100:  # 최소 면적 설정 (노이즈 제거)
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                if radius > 5:  # 반지름 설정
                    cv2.circle(resized_frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                    return (int(x), int(y)), int(radius)  # 공의 중심 좌표와 반지름 반환
        return None, 0  # 공이 감지되지 않았다면 None 반환

    def process_frame(self, frame):
        width = int(frame.shape[1])
        height = int(frame.shape[0])
        dim = (width, height)
        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        
        hsv = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2HSV)
        
        # 경기장 색인식 범위 지정
        lower_green = np.array([40, 70, 40])
        upper_green = np.array([140, 180, 255])
        
        # 경기장 mask
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        field_contour = None
        ball_out = False
        
        # 제일 큰 컨투어가 경기장이라고 인식
        if contours:
            field_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(resized_frame, [field_contour], -1, (0, 255, 0), 2)
        
        # 공의 위치를 감지한다.
        ball_position, radius = self.ball_detector(hsv, resized_frame)
        if ball_position and field_contour is not None:
            # 공이 경기장 경계 밖에 있는지 확인한다.
            if cv2.pointPolygonTest(field_contour, ball_position, False) < 0:
                ball_out = True
                print(ball_out)
                cv2.putText(resized_frame, "OUT", (ball_position[0] + 20, ball_position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            else:
                print("In")
        elif ball_position is None and field_contour is not None:
            print("Can't find ball")
        elif ball_position is not None and field_contour is None:
            print("Can't find field")

        return resized_frame, ball_out

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame, ball_out = self.process_frame(frame)
            
            if ball_out:
                print("The ball is out of the field!")
            
        #     cv2.imshow("Processed Frame", processed_frame)
            
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #                 cv2.destroyAllWindows()
        #                 break

        # self.cap.release()
        # cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = BallOutDetection()
    detector.run()
