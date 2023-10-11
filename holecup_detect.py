import cv2
import os,re,sys
import numpy as np

def is_ellipse_like(contour, frame, threshold=0.08):
    if len(contour) < 5:
        return False

    ellipse = cv2.fitEllipse(contour)
    # ellipse : ((중심 좌표), (minor_axis_length, major_axis_length), 타원의 회전 각도))

    # 타원의 주축과 소축 길이
    minor_axis, major_axis = ellipse[1]
    if major_axis == 0 or minor_axis == 0:
        return False

    # #주축이 가로축 일 때만
    # if (0 <= ellipse[2] < 45) or (135 <= ellipse[2] < 180):
    #     # 주축과 소축의 비율
    #     ratio = float(major_axis) / float(minor_axis)
    #     if 0.85 < ratio < 2.2:
    #         return False
    # else:
    #     return False
    
    #주축이 가로축 일 때만
    ratio = float(major_axis) / float(minor_axis)
    if 0.85 < ratio < 2.2:
        return False
    
    # frame.shape == (480, 640, 3)
    ellipse_contour_img = cv2.ellipse(np.zeros(frame.shape[:2], dtype=np.uint8), ellipse, 255, 2)
    ellipse_contours, _ = cv2.findContours(ellipse_contour_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # ellipse_contours : 검출된 윤곽선들의 목록, 각 윤곽선은 점들의 배열로 표현
    
    if not ellipse_contours:
        return False

    ellipse_contour = max(ellipse_contours, key=cv2.contourArea)

    # 타원 컨투어 그리기 (디버깅 용도) - 파란색
    cv2.drawContours(frame, [ellipse_contour], -1, (255,0,0), 2) 
    
    # 원본 컨투어와 타원 컨투어의 유사도 비교
    diff = cv2.matchShapes(contour, ellipse_contour, cv2.CONTOURS_MATCH_I1, 0.0)
    return diff < threshold


def process_frame(frame):
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_flag = np.array([5, 100, 50])
    upper_flag = np.array([37, 255, 255])
    mask_flag = cv2.inRange(hsv_img, lower_flag, upper_flag)
    
    # 모폴로지 연산
    kernel = np.ones((5,5),np.uint8)

    mask_flag = cv2.morphologyEx(mask_flag, cv2.MORPH_OPEN, kernel)
    mask_flag = cv2.morphologyEx(mask_flag, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_flag, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected = False
    
    #check##########################################
    cv2.imshow('HSV Mask', mask_flag)
    
    debug_frame = frame.copy()
    cv2.drawContours(debug_frame, contours, -1, (0,255,0), 2)
    cv2.imshow('Contours', debug_frame)
    # print("Number of contours:", len(contours))

    for con in contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        if is_ellipse_like(largest_contour, frame):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "HOLE CUP", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            detected = True
        else:
            detected = False

    if not detected:
        cv2.putText(frame, "NO HOLE CUP DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    return frame


def main(video_name='./imgs/YYY.h264'):
    video_path = os.path.join(os.getcwd(), video_name)
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        processed_frame = process_frame(frame)
        cv2.imshow('Processed Video', processed_frame)
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()