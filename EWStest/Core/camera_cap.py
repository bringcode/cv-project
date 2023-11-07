import cv2

cap = cv2.VideoCapture(0, cv2.CAP_V4L)
i = 1
while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()

    # 프레임을 화면에 표시
    cv2.imshow('Press S to take a picture', frame)

    # 'S' 키를 누를 때 사진 찍기
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # 파일로 사진 저장
        cv2.imwrite('captured_image{}.png'.format(i), frame)
        print("사진이 저장되었습니다.")
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료 시 리소스 해제
cap.release()
cv2.destroyAllWindows()
