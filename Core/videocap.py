# -*- coding: utf-8 -*-
import picamera
import time
import cv2

# 녹화 설정
camera = picamera.PiCamera()
camera.resolution = (1280, 720)  # 해상도 설정 (원하는 해상도로 변경 가능)
camera.framerate = 30            # 프레임 속도 설정 (원하는 속도로 변경 가능)

# 바탕화면에 저장할 파일 경로
output_file = "/home/pi/Desktop/녹화된파일.h264"

# 화면 미리보기 시작
camera.start_preview()

# 녹화 플래그 초기화
is_recording = False

try:
    while True:
        key = input("q를 눌러 녹화를 시작 또는 중지하세요: ")
        if key == "q":
            if not is_recording:
                print("녹화를 시작합니다.")
                # 녹화 시작
                camera.start_recording(output_file)
                is_recording = True
            else:
                print("녹화를 중지합니다.")
                # 녹화 중지
                camera.stop_recording()
                is_recording = False
            time.sleep(1)  # 다음 키 입력까지 대기
        
        # 녹화 중에 실시간 화면 보여주기
        if is_recording:
            frame = camera.capture_continuous(np.zeros((1280, 720, 3), dtype=np.uint8), format="bgr", use_video_port=True)
            frame = next(frame)
            cv2.imshow("실시간 녹화 화면", frame)
            cv2.waitKey(1)
except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 누르면 녹화를 중지하고 종료합니다.
    if is_recording:
        camera.stop_recording()
    camera.stop_preview()
    camera.close()
    cv2.destroyAllWindows()

