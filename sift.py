import cv2 as cv
import numpy as np
import time
import sys

img1 = cv.imread('imgs/arrow_model.jpeg')
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
T = 0.6

cap = cv.VideoCapture('imgs/first.h264')

if not cap.isOpened():
	sys.exit('카메라 연결 실패')

while True:
    ret, img_color = cap.read()

    gray2 = cv.cvtColor(img_color, cv.COLOR_RGB2GRAY)

    sift = cv.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)
    # print('특징점 개수:', len(kp1), len(kp2))

    # start = time.time()
    flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
    knn_match = flann_matcher.knnMatch(des1, des2, 2)

    good_match = []
    for nearest1, nearest2 in knn_match:
        if (nearest1.distance/nearest2.distance)<T:
            good_match.append(nearest1)
        # print('매칭에 걸린 시간:', time.time()-start)

    img_match = np.empty((max(img1.shape[0], img_color.shape[0]), img1.shape[1]+ img_color.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(img1, kp1, img_color, kp2, good_match, img_match, flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv.imshow('Result', img_color)
    cv.imshow('Good Matches', img_match)


    key = cv.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv.destoyAllWindows()