# -*- coding: utf-8 -*-
import picamera
import time
import cv2
import numpy as np
from datetime import datetime

# 녹화 설정
camera = picamera.PiCamera()
camera.resolution = (800, 600)
camera.framerate = 30

# 화면 미리보기 시작
camera.start_preview()

# 녹화 플래그 초기화
is_recording = False

# 파일명 생성 함수
def get_current_time():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    return timestamp

try:
    while True:
        key = input("q를 눌러 녹화를 시작 또는 중지하세요: ")
        if key == "q":
            if not is_recording:
                timestamp = get_current_time()
                output_file = f"/home/pi/Desktop/record/{timestamp}_녹화된파일.h264"
                print(f"{timestamp}에 녹화를 시작합니다.")
                camera.start_recording(output_file)
                is_recording = True
            else:
                print("녹화를 중지합니다.")
                camera.stop_recording()
                is_recording = False
            time.sleep(1)
        
        if is_recording:
            # 실시간 화면 표시
            frame = np.empty((camera.resolution[1] * camera.resolution[0] * 3,), dtype=np.uint8)
            camera.capture(frame, 'bgr', use_video_port=True)
            frame = frame.reshape((camera.resolution[1], camera.resolution[0], 3))
            
            cv2.imshow("실시간 녹화 화면", frame)
            cv2.waitKey(1)

except KeyboardInterrupt:
    if is_recording:
        camera.stop_recording()
    camera.stop_preview()
    camera.close()
    cv2.destroyAllWindows()
