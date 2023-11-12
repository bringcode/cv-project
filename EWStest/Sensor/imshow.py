import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L)
while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임 캡처에 실패했습니다.")
        break

    cv2.imshow('dst', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
