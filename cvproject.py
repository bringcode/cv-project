# import cv2 as cv
# import numpy as np

# img = cv.imread('imgs/강아지사진.jpeg')

# gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# canny1 = cv.Canny(gray,50,100)
# canny2 = cv.Canny(gray,100,200)
# canny3 = cv.Canny(gray,100,250)

# smooth = np.hstack((gray,
#                     canny1,
#                     canny2,
#                     canny3))

# cv.imshow('Smooth',smooth)

# cv.waitKey()
# cv.destroyAllWindows()

import cv2 as cv

img = cv.imread('imgs/arrow_line_prediction.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)

gray = cv.drawKeypoints(gray,kp,None,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.resize(gray, dsize=(0,0),fx=4, fy=4)
cv.imshow('sift', gray)

k = cv.waitKey()
cv.destroyAllWindows()