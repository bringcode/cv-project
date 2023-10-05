import cv2

# 비디오 캡처 객체 초기화
cap = cv2.VideoCapture(0)  # 0은 라즈베리 파이의 내장 카메라를 가리킵니다.

# 비디오 녹화 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 녹화 코덱 설정 (XVID는 일반적인 비디오 코덱)
out = cv2.VideoWriter('녹화된파일.h264', fourcc, 20.0, (640, 480))  # 파일 이름 및 설정 변경 가능

while True:
    ret, frame = cap.read()  # 비디오 프레임 읽기
    if not ret:
        break

    out.write(frame)  # 프레임을 녹화 파일에 쓰기

    cv2.imshow('Recording', frame)  # 화면에 비디오 미리보기 표시
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 녹화 종료
cap.release()
out.release()
cv2.destroyAllWindows()
