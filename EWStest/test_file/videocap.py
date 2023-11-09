import picamera
import time
from datetime import datetime

# 녹화 설정
camera = picamera.PiCamera()
camera.resolution = (800, 600)  # 해상도 설정 (원하는 해상도로 변경 가능)
camera.framerate = 10            # 프레임 속도 설정 (원하는 속도로 변경 가능)

# 화면 미리보기 시작
camera.start_preview(fullscreen=False, window=(100, 100, 640, 480))
camera.preview_alpha = 0  # 미리보기 화면을 투명하게 설정하여 화면 표시

# 녹화 플래그 초기화
is_recording = False

def get_current_time():
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # 년월일_시분초 형식의 시간 정보 생성
    return timestamp

try:
    while True:
        key = input("q를 눌러 녹화를 시작 또는 중지하세요: ")
        if key == "q":
            if not is_recording:
                timestamp = get_current_time()  # 현재 시간 정보 가져오기
                output_file = f"/home/pi/Desktop/record/{timestamp}_녹화된파일.h264"  # 파일명에 시간 추가
                print(f"{timestamp}에 녹화를 시작합니다.")
                time.sleep(2)  # 미리보기를 위한 딜레이 추가
                # 녹화 시작
                camera.start_recording(output_file)
                is_recording = True
            else:
                print("녹화를 중지합니다.")
                # 녹화 중지
                camera.stop_recording()
                is_recording = False
            time.sleep(1)  # 다음 키 입력까지 대기

except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 누르면 녹화를 중지하고 종료합니다.
    if is_recording:
        camera.stop_recording()
    camera.stop_preview()
    camera.close()
