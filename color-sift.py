import cv2 as cv
import numpy as np
import time
import sys

model_img = cv.imread('imgs/arrow_model.jpeg')

T = 0.7

cap = cv.VideoCapture('imgs/first.h264')

if not cap.isOpened():
	sys.exit('카메라 연결 실패')

while True:
    ret, img_color = cap.read()

    hue_yellow = 20
    distribution = 10

    lower_yellow = (hue_yellow-distribution, 100, 100)
    upper_yellow = (hue_yellow+distribution, 255, 255)

    img_color_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)
    model_img_hsv = cv.cvtColor(model_img, cv.COLOR_BGR2HSV)

    img_color_mask = cv.inRange(img_color_hsv, lower_yellow, upper_yellow)
    model_img_mask = cv.inRange(model_img_hsv, lower_yellow, upper_yellow)

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7,7))
    img_color_mask = cv.morphologyEx(img_color_mask, cv.MORPH_DILATE, kernel, iterations=3)
    model_img_mask = cv.morphologyEx(model_img_mask, cv.MORPH_DILATE, kernel, iterations=3)

    # smooth = np.hstack((img_color,
    #                 img_mask_color))
    
    # cv.imshow('Smooth', smooth)

    sift = cv.SIFT_create()
    kp1, des1 = sift.detectAndCompute(model_img_mask, None)
    kp2, des2 = sift.detectAndCompute(img_color_mask, None)
    # print('특징점 개수:', len(kp1), len(kp2))

    # start = time.time()
    flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_match = flann_matcher.knnMatch(des1, des2, 2)

    good_match = []
    for nearest1, nearest2 in knn_match:
        if (nearest1.distance/nearest2.distance)<T:
            good_match.append(nearest1)
        # print('매칭에 걸린 시간:', time.time()-start)

    img_match = np.empty((max(img_color.shape[0], img_color.shape[0]), img_color.shape[1]+ img_color.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(img_color, kp1, img_color, kp2, good_match, img_match, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv.imshow('Good Matches', img_match)

    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destroyAllWindows()